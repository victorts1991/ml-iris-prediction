import pytest
import os
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression # Importe o tipo do modelo esperado

# Importa o caminho do modelo do model_loader para consistência
from ml.model_loader import MODEL_PATH

# Fixture para carregar o modelo existente e dados de teste (se necessário)
@pytest.fixture(scope="module")
def loaded_production_model_and_test_data():
    """
    Carrega o modelo de produção existente e prepara dados de teste para validação.
    """
    if not os.path.exists(MODEL_PATH):
        pytest.fail(f"Modelo de produção não encontrado em {MODEL_PATH}. Não é possível executar os testes do modelo.")
    
    # Carrega o modelo existente
    model = joblib.load(MODEL_PATH)
    
    # Prepara dados de teste para validar o modelo
    # IMPORTANTE: Use dados que o modelo deve prever corretamente
    # Para o Iris, load_iris() e split é uma boa forma de ter dados conhecidos.
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    
    iris = load_iris()
    X, y = iris.data, iris.target
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    yield model, X_test, y_test


def test_model_loading_and_instance(loaded_production_model_and_test_data):
    """
    Verifica se o modelo foi carregado corretamente e se é uma instância do tipo esperado.
    """
    loaded_model, _, _ = loaded_production_model_and_test_data
    assert loaded_model is not None
    assert isinstance(loaded_model, LogisticRegression) # Adapte o tipo do modelo se for diferente


def test_model_prediction_output(loaded_production_model_and_test_data):
    """
    Testa se o modelo faz predições e o formato da saída.
    """
    loaded_model, X_test, _ = loaded_production_model_and_test_data
    
    # Pega uma amostra do conjunto de teste para predição
    sample_input = X_test[0:1] 
    
    prediction = loaded_model.predict(sample_input)
    assert isinstance(prediction, np.ndarray)
    assert len(prediction) == 1
    assert prediction[0] in [0, 1, 2] # Classes da Iris


def test_model_accuracy_on_known_test_set(loaded_production_model_and_test_data):
    """
    Testa a acurácia do modelo no conjunto de teste conhecido (o que foi usado no Jupyter).
    """
    loaded_model, X_test, y_test = loaded_production_model_and_test_data
    
    score = loaded_model.score(X_test, y_test)
    
    # Se a acurácia esperada for 1.0 (ou outro valor fixo e conhecido)
    assert score == 1.0 
    # Ou se puder ter pequena variação: assert score >= 0.99