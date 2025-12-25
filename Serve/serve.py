from fastapi import FastAPI
import mlflow
import pandas as pd
from pydantic import BaseModel
import os
from dotenv import load_dotenv

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

app = FastAPI()

class WineFeatures(BaseModel):
    features: dict
    
@app.get('/health')
def health():
    return{"status": "okay"}

@app.post('/predict')
def predict(data: WineFeatures):
    df = pd.DataFrame([data.features])
    preds = model.predict(df)
    return {"prediction": float(preds[0])}