# iris_prediction_api/ml/model_loader.py

import joblib
import logging
import os

logger = logging.getLogger("api_modelo")

# Caminho do modelo (espera-se que esteja dentro da pasta 'ml' na raiz do projeto)
MODEL_PATH = "ml/modelo_iris.pkl"

loaded_model = None # Inicializa como None

try:
    if os.path.exists(MODEL_PATH):
        loaded_model = joblib.load(MODEL_PATH)
        logger.info("Modelo de ML '%s' carregado com sucesso.", MODEL_PATH)
    else:
        # Esta mensagem será logada se o arquivo não for encontrado no caminho especificado
        logger.error("Arquivo do modelo de ML '%s' não encontrado. As predições não funcionarão.", MODEL_PATH)
except Exception as e:
    # Esta captura é genérica e pode mascarar erros de carregamento (compatibilidade de versão, corrupção)
    logger.error("Erro ao carregar o modelo de ML '%s': %s", MODEL_PATH, e)