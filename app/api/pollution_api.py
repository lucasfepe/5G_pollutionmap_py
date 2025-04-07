import os
import json
from openaq import OpenAQ
from datetime import datetime, timedelta

class OpenAQClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAQ_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found in environment variables")
        self.api = OpenAQ(api_key=self.api_key)

    async def get_latest_measurements(self, city):
        try:
            # Get locations using coordinates and radius like in the working example
            locations_response = self.api.locations.list(
                coordinates=("51.0447,-114.0719"),  # Calgary coordinates
                radius=25_000  # 25km radius
            ).json()
            locations_response = json.loads(locations_response)
            locations = locations_response.get("results", [])

            if not locations:
                return {"results": []}

            measurements_data = []
            for location in locations:
                location_id = location["id"]
                location_name = location["name"]
                coordinates = location["coordinates"]

                # Get latest measurements for each location
                measurements_response = self.api.locations.latest(location_id).json()
                measurements_response = json.loads(measurements_response)
                measurements = measurements_response.get("results", [])

                for measurement in measurements:
                    sensor = next((sensor for sensor in location["sensors"] 
                                if sensor["id"] == measurement.get("sensorsId")), None)

                    if sensor:
                        measurements_data.append({
                            "id": location_id,
                            "name": location_name,
                            "lat": coordinates["latitude"],
                            "lon": coordinates["longitude"],
                            "pollutant": sensor["parameter"]["displayName"],
                            "value": measurement["value"],
                            "unit": sensor["parameter"]["units"],
                            "lastUpdated": measurement.get("lastUpdated")
                        })

            return {"results": measurements_data}

        except Exception as e:
            print(f"Error fetching latest measurements: {e}")
            return {"results": []}

    async def get_historical_data(self, city, days=7):
        try:
            # Get locations first
            locations_response = self.api.locations.list(
                coordinates=("51.0447,-114.0719"),  # Calgary coordinates
                radius=25_000  # 25km radius
            ).json()
            locations_response = json.loads(locations_response)
            locations = locations_response.get("results", [])

            if not locations:
                return {"results": []}

            historical_data = []
            for location in locations:
                # Get sensors from the location
                for sensor in location["sensors"]:
                    sensor_id = sensor["id"]
                    
                    # Get measurements for each sensor using the correct parameters
                    measurements_response = self.api.measurements.list(
                        sensors_id=sensor_id,  # Required parameter
                        datetime_from=(datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d"),
                        datetime_to=datetime.now().strftime("%Y-%m-%d"),
                        limit=1000
                    ).json()
                    
                    measurements_response = json.loads(measurements_response)
                    measurements = measurements_response.get("results", [])

                    for measurement in measurements:
                        historical_data.append({
                            "id": location["id"],
                            "name": location["name"],
                            "lat": location["coordinates"]["latitude"],
                            "lon": location["coordinates"]["longitude"],
                            "pollutant": sensor["parameter"]["displayName"],
                            "value": measurement["value"],
                            "unit": sensor["parameter"]["units"],
                            "timestamp": measurement.get('coverage').get('datetimeFrom').get('utc')
                        })

            return {"results": historical_data}

        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return {"results": []}

    def __del__(self):
        if hasattr(self, 'api'):
            self.api.close()
