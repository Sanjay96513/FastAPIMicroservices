from fastapi import FastAPI
import joblib
import numpy as np
from pydantic import BaseModel
from typing import List

from shared_lib.database import init_db

# --- ML Model Loading ---
# This is a placeholder for the actual model object
model = None
MODEL_PATH = "app/models/isolation_forest.joblib"

class TransactionFeatures(BaseModel):
    """Pydantic model for the input data for risk analysis."""
    amount: float
    # In a real-world scenario, you'd have more features like:
    # time_of_day, day_of_week, user's avg_transaction_value, etc.
    # For this example, we'll just use the amount.
    features: List[float] # This will represent a vector of features for the model

app = FastAPI(
    title="Risk and Fraud Detection Service",
    description="Analyzes transactions for fraudulent activity using an ML model.",
    version="0.1.0"
)

@app.on_event("startup")
async def on_startup():
    """
    Initialize the database connection and load the ML model on startup.
    """
    await init_db()
    global model
    try:
        model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        # This is a fallback for environments where the model file doesn't exist.
        # In a production setup, the build process should ensure the model is present.
        model = None


@app.post("/analyze")
async def analyze_transaction(transaction_features: TransactionFeatures):
    """
    Analyze a transaction and return a risk score.
    -1 indicates an anomaly (potential fraud), 1 indicates normal.
    """
    if model is None:
        return {"risk_score": 0, "prediction": "Model not loaded"}

    # The model expects a 2D array, so we reshape the input
    features_array = np.array(transaction_features.features).reshape(1, -1)

    # Use the model to predict
    prediction = model.predict(features_array)
    score = model.decision_function(features_array)

    # Convert numpy types to native Python types for JSON serialization
    return {
        "prediction": int(prediction[0]),
        "risk_score": float(score[0])
    }

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "risk-service", "model_loaded": model is not None}