"""
FastAPI Model Deployment Example
This app loads a pre-trained scikit-learn Iris classifier and exposes a /predict endpoint with API key authentication.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import numpy as np
import joblib
import os

API_KEY = "secret123"  # In production, use environment variables or a secrets manager
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

app = FastAPI()

# Dummy model training and saving (for demo purposes)
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

def train_and_save_model():
    iris = load_iris()
    X, y = iris.data, iris.target
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    joblib.dump(model, "iris_model.joblib")
    return model

if not os.path.exists("iris_model.joblib"):
    train_and_save_model()

model = joblib.load("iris_model.joblib")

class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    return api_key

@app.post("/predict")
def predict(features: IrisFeatures, api_key: str = Depends(get_api_key)):
    X = np.array([[features.sepal_length, features.sepal_width, features.petal_length, features.petal_width]])
    pred = model.predict(X)[0]
    return {"predicted_class": int(pred)} 