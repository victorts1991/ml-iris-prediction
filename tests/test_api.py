# iris_prediction_api/tests/test_api.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, ANY
import datetime
from typing import List

from api.v1.models.auth import Token, UserLogin
from api.v1.models.iris import IrisFeatures, PredictionResponse, PredictionRecord

# As fixtures 'client' e 'auth_token' vêm do conftest.py

def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_login_success(client: TestClient):
    response = client.post("/login", json={"username": "admin", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials(client: TestClient):
    response = client.post("/login", json={"username": "admin", "password": "wrong_password"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas"

def test_predict_unauthenticated(client: TestClient):
    response = client.post("/predict", json={"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2})
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_predict_invalid_input(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/predict", json={"sepal_length": "invalid", "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}, headers=headers)
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"][0]["loc"] == ["body", "sepal_length"]

# Mocka o modelo de ML e a função de criação de predição no DB
@patch('api.v1.endpoints.predictions.loaded_model')
@patch('api.v1.endpoints.predictions.create_prediction')
def test_predict_success(mock_create_prediction: MagicMock, mock_model: MagicMock, client: TestClient, auth_token: str):
    mock_model.predict.return_value = [0] 

    mock_prediction_obj = MagicMock(spec=PredictionRecord) 
    mock_prediction_obj.id = 1
    mock_prediction_obj.sepal_length = 5.1
    mock_prediction_obj.sepal_width = 3.5
    mock_prediction_obj.petal_length = 1.4
    mock_prediction_obj.petal_width = 0.2
    mock_prediction_obj.predicted_class = 0
    mock_prediction_obj.created_at = datetime.datetime.now()
    mock_create_prediction.return_value = mock_prediction_obj

    headers = {"Authorization": f"Bearer {auth_token}"}
    features = {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}
    response = client.post("/predict", json=features, headers=headers)
    
    assert response.status_code == 200
    assert response.json()["prediction"] == 0
    mock_model.predict.assert_called_once()
    mock_create_prediction.assert_called_once_with(
        ANY, # Usando ANY para a sessão do DB - ESTÁ CORRETO AQUI
        IrisFeatures(**features),
        0 
    )


def test_list_predictions_unauthenticated(client: TestClient):
    response = client.get("/predictions")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


@patch('api.v1.endpoints.predictions.get_predictions_from_db')
def test_list_predictions_success(mock_get_predictions: MagicMock, client: TestClient, auth_token: str):
    mock_get_predictions.return_value = [
        MagicMock(spec=PredictionRecord, id=i+1, sepal_length=5.0+i*0.1, sepal_width=3.0, petal_length=1.0, petal_width=0.1, predicted_class=0, created_at=datetime.datetime.now())
        for i in range(10)
    ]

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/predictions", headers=headers)
    
    assert response.status_code == 200
    predictions = response.json()
    
    assert isinstance(predictions, list)
    assert len(predictions) == 10 
    
    # CORREÇÃO: Remover a asserção sobre o primeiro argumento 'db' (ANY)
    # pois o 'assert_called_once_with' pode ser muito estrito com objetos complexos
    # Focar nos argumentos que realmente importam.
    # A chamada `mock_get_predictions.assert_called_once()` já verifica que foi chamado.
    mock_get_predictions.assert_called_once() # Garante que a função foi chamada
    assert mock_get_predictions.call_args.args[1] == 10 # Argumento 'limit'
    assert mock_get_predictions.call_args.args[2] == 0 # Argumento 'offset'
    
    # Se quiser verificar a chamada com parâmetros exatos, use assert_called_once_with
    # E para o primeiro argumento que é a sessão (um objeto complexo), use um mock mais robusto
    # Ex: mock_get_predictions.assert_called_once_with(ANY, limit=10, offset=0)
    # Mas como já deu erro com ANY, vamos testar de forma mais granular.


@patch('api.v1.endpoints.predictions.loaded_model')
@patch('api.v1.endpoints.predictions.create_prediction')
@patch('api.v1.endpoints.predictions.get_predictions_from_db')
def test_predictions_flow_and_list(mock_get_predictions: MagicMock, mock_create_prediction: MagicMock, mock_model: MagicMock, client: TestClient, auth_token: str):
    mock_model.predict.return_value = [1] 
    
    mock_pred_obj_1 = MagicMock(spec=PredictionRecord, id=1, sepal_length=6.0, sepal_width=3.0, petal_length=4.0, petal_width=1.5, predicted_class=1, created_at=datetime.datetime.now())
    mock_pred_obj_2 = MagicMock(spec=PredictionRecord, id=2, sepal_length=7.0, sepal_width=3.2, petal_length=5.5, petal_width=2.0, predicted_class=1, created_at=datetime.datetime.now())
    mock_create_prediction.side_effect = [mock_pred_obj_1, mock_pred_obj_2]

    mock_data_for_default_limit = [
        MagicMock(spec=PredictionRecord, id=i, sepal_length=float(i), sepal_width=3.0, petal_length=1.0, petal_width=0.1, predicted_class=0, created_at=datetime.datetime.now())
        for i in range(10, 0, -1)
    ] 
    mock_get_predictions.return_value = mock_data_for_default_limit

    headers = {"Authorization": f"Bearer {auth_token}"}
    features1 = {"sepal_length": 6.0, "sepal_width": 3.0, "petal_length": 4.0, "petal_width": 1.5}
    features2 = {"sepal_length": 7.0, "sepal_width": 3.2, "petal_length": 5.5, "petal_width": 2.0}

    response1 = client.post("/predict", json=features1, headers=headers)
    assert response1.status_code == 200
    response2 = client.post("/predict", json=features2, headers=headers)
    assert response2.status_code == 200

    response_list = client.get("/predictions", headers=headers)
    assert response_list.status_code == 200
    predictions = response_list.json()
    
    assert len(predictions) == 10 
    assert predictions[0]["id"] == 10
    assert predictions[1]["id"] == 9
    
    assert mock_create_prediction.call_count == 2 # OK, continua como está
    # CORREÇÃO: Remover a asserção sobre o argumento 'db' (ANY)
    mock_get_predictions.assert_called_once() # Garante que a função foi chamada
    assert mock_get_predictions.call_args.args[1] == 10 # Argumento 'limit'
    assert mock_get_predictions.call_args.args[2] == 0 # Argumento 'offset'


@patch('api.v1.endpoints.predictions.loaded_model')
@patch('api.v1.endpoints.predictions.create_prediction')
@patch('api.v1.endpoints.predictions.get_predictions_from_db')
def test_predictions_limit_offset(mock_get_predictions: MagicMock, mock_create_prediction: MagicMock, mock_model: MagicMock, client: TestClient, auth_token: str):
    mock_model.predict.return_value = [0] 
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    mock_records_in_creation_order = []
    for i in range(1, 6): # IDs de 1 a 5
        mock_records_in_creation_order.append(
            MagicMock(spec=PredictionRecord,
                      id=i, 
                      sepal_length=round(5.0 + i*0.1, 1), 
                      sepal_width=3.0,
                      petal_length=1.0,
                      petal_width=0.1,
                      predicted_class=0,
                      created_at=datetime.datetime.now()
            )
        )
    
    ordered_for_api_response_desc = list(reversed(mock_records_in_creation_order))

    mock_get_predictions.side_effect = [
        # Primeira chamada: ?limit=2 (limit=2, offset=0)
        ordered_for_api_response_desc[0:2], 
        
        # Segunda chamada: ?limit=2&offset=1
        ordered_for_api_response_desc[1:3]  
    ]

    # Testar limit=2, offset=0 (primeira chamada)
    response = client.get("/predictions?limit=2", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["sepal_length"] == pytest.approx(5.5)
    assert response.json()[1]["sepal_length"] == pytest.approx(5.4)
    
    # Testar offset (segunda chamada)
    response = client.get("/predictions?limit=2&offset=1", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["sepal_length"] == pytest.approx(5.4)
    assert response.json()[1]["sepal_length"] == pytest.approx(5.3)
    
    assert mock_get_predictions.call_count == 2 # OK, continua como está
    # Remover a asserção sobre o argumento 'db' (ANY) para cada chamada
    # Verificar a chamada com parâmetros exatos
    assert mock_get_predictions.call_args_list[0].args[1] == 2 # Primeira chamada: limit=2
    assert mock_get_predictions.call_args_list[0].args[2] == 0 # Primeira chamada: offset=0
    assert mock_get_predictions.call_args_list[1].args[1] == 2 # Segunda chamada: limit=2
    assert mock_get_predictions.call_args_list[1].args[2] == 1 # Segunda chamada: offset=1