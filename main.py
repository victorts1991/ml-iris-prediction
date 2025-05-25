from fastapi import FastAPI
from core.config import settings
from api.v1.endpoints import auth, predictions
import logging
from db.database import create_db_tables

# Configuração de Logging (mantida aqui ou centralizada em config)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_modelo")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para prever a espécie de flor Iris e registrar as predições.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    create_db_tables()
    logger.info("Tabelas do banco de dados criadas/verificadas na inicialização.")

# Incluir os routers
app.include_router(auth.router, tags=["Autenticação"])
app.include_router(predictions.router, tags=["Predições"])

# Rota de saúde (mantida no main para simplicidade)
@app.get("/health", summary="Verifica a saúde da API")
async def health():
    return {"status": "OK"}

# Rodar a aplicação (apenas para o caso de executar como script, embora uvicorn seja o recomendado)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)