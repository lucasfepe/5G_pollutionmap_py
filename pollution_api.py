import os
import json
from openaq import OpenAQ

class PollutionAPI:
    _instance = None
    
    def __init__(self):
        self.api_key = os.getenv("NEXT_PUBLIC_OPENAQ_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found in environment variables")
        self.api = OpenAQ(api_key=self.api_key)
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def fetch_latest_measurements(self):
        locations_response = self.api.locations.list(coordinates=("51.0447,-114.0719"), radius=25_000).json()
        locations_response = json.loads(locations_response)
        locations = locations_response["results"]

        pollution_data = []
        for location in locations:
            location_id = location["id"]
            location_name = location["name"]
            coordinates = location["coordinates"]

            measurements_response = self.api.locations.latest(location_id).json()
            measurements_response = json.loads(measurements_response)
            measurements = measurements_response["results"]

            for measurement in measurements:
                sensor = next((sensor for sensor in location["sensors"] 
                             if sensor["id"] == measurement["sensorsId"]), None)

                if sensor:
                    pollution_data.append({
                        "id": location_id,
                        "name": location_name,
                        "lat": coordinates["latitude"],
                        "lon": coordinates["longitude"],
                        "pollutant": sensor["parameter"]["displayName"],
                        "value": measurement["value"],
                        "unit": sensor["parameter"]["units"],
                    })

        return pollution_data
    
    def __del__(self):
        if hasattr(self, 'api'):
            self.api.close()
    
    @classmethod
    def cleanup(cls):
        if cls._instance is not None:
            cls._instance.api.close()
            cls._instance = None