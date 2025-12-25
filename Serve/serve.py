from fastapi import FastAPI
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
    PREDICTION_COUNT.inc()
    return {"prediction": float(preds[0])}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)