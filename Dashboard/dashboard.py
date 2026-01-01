from fastapi import FastAPI, Form
import requests

app = FastAPI()

MODEL_URI = "http://mlops.dakshsawhneyy.online/predict"

@app.get("/")
def form():
    return """
    <html>
        <body>
            <h2>Wine Prediction Model UI </h2>
            <form actions="/predict" method="post">
                Alcohol: <input type="number" step="any" name="Alcohol"><br><br>
                Malic Acid: <input type="number" step="any" name="Malic_acid"><br><br>
                Ash: <input type="number" step="any" name="Ash"><br><br>
                <button type="submit">Predict</button>
            </form>
        </body>
    </html>
    """
    
@app.post("/predict")
def predict(
    Alcohol: float = Form(...),
    Malic_acid: float = Form(...),
    Ash: float = Form(...)
):
    payload = {
        "features": {
            "Alcohol": Alcohol,
            "Malic.acid": Malic_acid,
            "Ash": Ash
        }
    }

    response = requests.post(MODEL_API_URL, json=payload)
    result = response.json()

    return {
        "input": payload,
        "model_response": result
    }