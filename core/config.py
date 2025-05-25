import os
import logging

# Configurações JWT
JWT_SECRET = os.getenv("JWT_SECRET", "MEUSEGREDOAQUI")
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600

# Configuração do Banco de Dados SQLite
DB_URL = os.getenv("DATABASE_URL", "sqlite:///predictions.db")

# Credenciais de teste para login (em um ambiente real, viriam de env ou vault)
TEST_USERNAME = os.getenv("TEST_USERNAME", "admin")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "secret")

# Nome do Projeto (para o FastAPI title)
PROJECT_NAME = "API de Predição Iris"

# Cache de predições (mantido globalmente como no original)
predictions_cache = {}

# Configuração de Logging (pode ser mais elaborada aqui)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_modelo")

# Você pode usar uma classe Pydantic Settings aqui para mais robustez,
# mas para manter o mais próximo possível da lógica original, variáveis simples estão ok.
class Settings:
    JWT_SECRET: str = os.getenv("JWT_SECRET", "MEUSEGREDOAQUI")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXP_DELTA_SECONDS: int = 3600
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///predictions.db")
    TEST_USERNAME: str = os.getenv("TEST_USERNAME", "admin")
    TEST_PASSWORD: str = os.getenv("TEST_PASSWORD", "secret")
    PROJECT_NAME: str = "API de Predição Iris"
    # Adicionando o cache aqui para que seja importável de um lugar central
    predictions_cache: dict = {}

settings = Settings()