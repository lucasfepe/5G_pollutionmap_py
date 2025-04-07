from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Measurement(BaseModel):
    parameter: str
    value: float
    unit: str
    location: str
    city: str
    country: str
    timestamp: datetime

class PredictionResponse(BaseModel):
    historical_data: List[Measurement]
    predictions: List[dict]
    analysis: dict
