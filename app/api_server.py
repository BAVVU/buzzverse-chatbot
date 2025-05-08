from fastapi import FastAPI
from pydantic import BaseModel
import joblib

# Load trained model
model = joblib.load("models/campaign_success_model.pkl")

# Start FastAPI app
app = FastAPI()

# Define request body structure
class CampaignInput(BaseModel):
    ctr: float
    roas: float
    conv_rate: float
    cpa: float

# Define POST endpoint
@app.post("/predict")
def predict_campaign(data: CampaignInput):
    features = [[data.ctr, data.roas, data.conv_rate, data.cpa]]
    prediction = model.predict(features)
    return {"success": bool(prediction[0])}
