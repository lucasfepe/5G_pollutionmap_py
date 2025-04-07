from fastapi import APIRouter, HTTPException
from app.services.data_analysis import PollutionAnalyzer
from app.models.schemas import PredictionResponse
from app.api.pollution_api import OpenAQClient
import os
import json

router = APIRouter()
openaq_client = OpenAQClient()
analyzer = PollutionAnalyzer()

@router.get("/latest/{city}")
async def get_latest_pollution(city: str):
    data = await openaq_client.get_latest_measurements(city)
    if not data.get('results'):
        raise HTTPException(status_code=404, detail="No data found for this city")
    return data

@router.get("/forecast/{city}")
async def get_pollution_forecast(city: str):
    # Check if historical data file exists and has content
    file_path = 'historical_data.txt'
    historical_data = None
    
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
                if file_content:
                    print("Using cached data from file")
                    historical_data = json.loads(file_content)
        except Exception as e:
            print(f"Warning: Could not read from file: {e}")
    
    # If we don't have data from file, fetch it from API
    if not historical_data:
        print("Fetching new data from API")
        historical_data = await openaq_client.get_historical_data(city)
        # Save the new data to file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(historical_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Warning: Could not write debug file: {e}")
    
    if not historical_data.get('results'):
        raise HTTPException(status_code=404, detail="No historical data found")

    # Process data using Pandas
    processed_data = analyzer.process_historical_data(historical_data)
    
    # Generate predictions
    predictions = analyzer.generate_predictions(processed_data)
    
    # Convert predictions dictionary to serializable format
    predictions_dict = {
        pollutant: values.to_dict() 
        for pollutant, values in predictions.items()
    }
    
    # Analyze trends
    analysis = analyzer.analyze_trends(processed_data)

    return {
        "historical_data": processed_data.to_dict(),
        "predictions": predictions_dict,
        "analysis": analysis
    }
