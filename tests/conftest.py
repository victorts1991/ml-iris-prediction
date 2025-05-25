import pytest
from fastapi.testclient import TestClient

# Importa a instância 'app' do seu main.py
from main import app
# Note: Removida a importação de SessionLocal, Base, Prediction, e create_engine
# Não precisamos mais deles aqui, pois o DB será mockado para testes de API.

@pytest.fixture(name="client")
def client_fixture():
    """
    Cria um cliente de teste para a aplicação FastAPI.
    Não sobrescreve dependências de DB neste conftest,
    pois os testes de API deverão mockar o DB diretamente.
    """
    with TestClient(app) as c:
        yield c

@pytest.fixture(name="auth_token")
def auth_token_fixture(client: TestClient):
    """
    Fixture para obter um token de autenticação de teste.
    """
    # As credenciais TEST_USERNAME e TEST_PASSWORD são importadas indiretamente
    # via `main.py` -> `api.v1.endpoints.auth` -> `core.config.settings`
    response = client.post("/login", json={"username": "admin", "password": "secret"})
    assert response.status_code == 200
    return response.json()["access_token"]