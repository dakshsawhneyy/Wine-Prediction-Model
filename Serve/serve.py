from fastapi import FastAPI, Response
import mlflow
import pandas as pd
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time

load_dotenv()

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")

MODEL_NAME = "wine_rf_model"
MODEL_STAGE = "None"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("MLFLOW_TRACKING_USERNAME")
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("MLFLOW_TRACKING_PASSWORD")

model = mlflow.pyfunc.load_model(
    model_uri=f"models:/{MODEL_NAME}/{MODEL_STAGE}"
)

# Prometheus Metrics
PREDICTION_COUNT = Counter("prediction_requests_total", "Total predictions made")
PREDICTION_LATENCY = Histogram("prediction_latency_seconds", "Latency for predictions")

# feature logging
FEATURE_HISTOGRAMS = {
    "Alcohol": Histogram("feature_alcohol", "Alcohol distribution"),
    "Malic.acid": Histogram("feature_malic_acid", "Malic acid distribution"),
}

# prediction logging
PRED_HIST = Histogram(
    "model_prediction",
    "Prediction distribution"
)

app = FastAPI()

class WineFeatures(BaseModel):
    features: dict
    
@app.get('/health')
def health():
    return{"status": "okay"}

@app.post('/predict')
@PREDICTION_LATENCY.time()
def predict(data: WineFeatures):
    df = pd.DataFrame([data.features])
    
    preds = model.predict(df)
    PRED_HIST.observe(float(preds[0]))
    
    PREDICTION_COUNT.inc()
    
    # Drift Detection
    for f, hist in FEATURE_HISTOGRAMS.items():
        if f in data.features:
            hist.observe(float(data.features[f]))
    
    return {"prediction": float(preds[0])}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)