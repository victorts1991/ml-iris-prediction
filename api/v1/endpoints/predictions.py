import numpy as np
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from api.v1.models.iris import IrisFeatures, PredictionResponse, PredictionRecord
from core.dependencies import get_db
from core.security import verify_token
from db.crud import create_prediction, get_predictions_from_db
from ml.model_loader import loaded_model # Importa o modelo carregado
from core.config import predictions_cache # Importa o cache

logger = logging.getLogger("api_modelo")

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse, summary="Realiza a predição de espécie de Iris")
async def predict_iris(
    features: IrisFeatures,
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_token)
):
    """
    Endpoint protegido por token para obter predição de espécie de Iris.
    """
    if loaded_model is None: # Usa 'loaded_model' aqui
        raise HTTPException(status_code=500, detail="Modelo de ML não carregado.")

    sepal_length = features.sepal_length
    sepal_width = features.sepal_width
    petal_length = features.petal_length
    petal_width = features.petal_width

    # Verificar se já está no cache
    features_tuple = (sepal_length, sepal_width, petal_length, petal_width)
    if features_tuple in predictions_cache:
        logger.info("Cache hit para %s", features_tuple)
        predicted_class = predictions_cache[features_tuple]
    else:
        # Rodar o modelo
        input_data = np.array([features_tuple])
        prediction = loaded_model.predict(input_data) # Usa 'loaded_model' aqui
        predicted_class = int(prediction[0])
        # Armazenar no cache
        predictions_cache[features_tuple] = predicted_class
        logger.info("Cache updated para %s", features_tuple)

    # Armazenar no banco de dados a predição
    new_pred = create_prediction(db, features, predicted_class) # Chama a função CRUD
    return PredictionResponse(prediction=new_pred.predicted_class)


@router.get("/predictions", response_model=List[PredictionRecord], summary="Lista as predições armazenadas no banco")
async def list_predictions_endpoint(
    limit: int = 10, offset: int = 0,
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_token)
):
    """
    Lista as predições armazenadas no banco.
    Parâmetros opcionais (via query string):
      - limit (int): quantos registros retornar, padrão 10
      - offset (int): a partir de qual registro começar, padrão 0
    """
    preds = get_predictions_from_db(db, limit, offset) # Chama a função CRUD
    return preds