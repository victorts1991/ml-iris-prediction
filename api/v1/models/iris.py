from pydantic import BaseModel, Field
import datetime

class IrisFeatures(BaseModel):
    sepal_length: float = Field(..., example=5.1)
    sepal_width: float = Field(..., example=3.5)
    petal_length: float = Field(..., example=1.4)
    petal_width: float = Field(..., example=0.2)

class PredictionResponse(BaseModel):
    prediction: int = Field(..., example=0)

class PredictionRecord(BaseModel):
    id: int
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    predicted_class: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True # Updated from orm_mode=True for Pydantic v2