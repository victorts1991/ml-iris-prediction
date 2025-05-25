import datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from core.config import settings

# Configuração do Banco de Dados
DB_URL = settings.DATABASE_URL
engine = create_engine(DB_URL, echo=False) # echo=True para ver as queries SQL no log
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modelo de Banco de Dados
class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sepal_length = Column(Float, nullable=False)
    sepal_width = Column(Float, nullable=False)
    petal_length = Column(Float, nullable=False)
    petal_width = Column(Float, nullable=False)
    predicted_class = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Função para criar as tabelas (chame isso uma vez na inicialização da aplicação, ou em um script separado)
def create_db_tables():
    Base.metadata.create_all(engine)

# Chame a função para garantir que as tabelas sejam criadas ao importar este módulo
# Em um ambiente de produção, você pode querer controlar isso de forma mais explícita
create_db_tables()