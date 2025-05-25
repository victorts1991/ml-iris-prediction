from sqlalchemy.orm import Session
from db.database import Prediction
from api.v1.models.iris import IrisFeatures # Importa o modelo Pydantic para tipagem
import logging

logger = logging.getLogger("api_modelo")

def create_prediction(db: Session, features: IrisFeatures, predicted_class: int):
    new_pred = Prediction(
        sepal_length=features.sepal_length,
        sepal_width=features.sepal_width,
        petal_length=features.petal_length,
        petal_width=features.petal_width,
        predicted_class=predicted_class
    )
    db.add(new_pred)
    db.commit()
    db.refresh(new_pred) # Atualiza o objeto com o ID e created_at do banco
    logger.info("Predição salva no DB com ID: %s", new_pred.id)
    return new_pred

def get_predictions_from_db(db: Session, limit: int = 10, offset: int = 0):
    return db.query(Prediction).order_by(Prediction.id.desc()).limit(limit).offset(offset).all()
