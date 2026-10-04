from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI

from app.schemas import EnergyInput

app = FastAPI(
    title="EcoPredict AI",
    description="Cloud-ready household energy consumption prediction API",
    version="1.0.0",
)

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "energy_model.pkl"

model_data = joblib.load(MODEL_PATH)
model = model_data["model"]
FEATURES = model_data["features"]


@app.get("/")
def root():
    return {
        "service": "EcoPredict AI",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "EcoPredict AI"}


@app.post("/predict")
def predict_energy(data: EnergyInput):
    input_data = pd.DataFrame([data.model_dump()])
    input_data = input_data[FEATURES]

    prediction = float(model.predict(input_data)[0])

    if prediction < 50:
        category = "Low"
        recommendation = "Predicted consumption is relatively low. Maintain efficient usage."
    elif prediction < 150:
        category = "Moderate"
        recommendation = "Predicted consumption is elevated. Consider reducing unnecessary loads."
    else:
        category = "High"
        recommendation = "Predicted consumption is high. Review appliance and lighting usage."

    return {
        "predicted_energy_wh": round(prediction, 2),
        "consumption_category": category,
        "recommendations": [recommendation],
    }
