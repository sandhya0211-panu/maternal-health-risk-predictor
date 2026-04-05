import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from pydantic import BaseModel
from src.predict import predict

app = FastAPI()


class InputData(BaseModel):
    Age: float
    SystolicBP: float
    DiastolicBP: float
    BS: float
    BodyTemp: float
    HeartRate: float


@app.get("/")
def home():
    return {"message": "API Running"}


@app.post("/predict")
def get_prediction(data: InputData):
    input_data = [
        data.Age,
        data.SystolicBP,
        data.DiastolicBP,
        data.BS,
        data.BodyTemp,
        data.HeartRate
    ]

    result, reasons, suggestions = predict(input_data)

    risk_map = {
        0: "Low Risk",
        1: "Mid Risk",
        2: "High Risk"
    }

    return {
         "RiskLevel": risk_map.get(result),
         "Reasons": reasons,
         "Suggestions": suggestions,
         "Disclaimer": "This prediction is based on a machine learning model and is not a medical diagnosis. Please consult a qualified healthcare professional for proper medical advice."
} 