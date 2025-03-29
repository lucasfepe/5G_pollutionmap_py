import json
import sys
from pollution_api import PollutionAPI

sys.stdout.reconfigure(encoding="utf-8")

def fetch_latest_measurements():
    api = PollutionAPI.get_instance()
    return api.fetch_latest_measurements()

if __name__ == "__main__":
    try:
        data = fetch_latest_measurements()

        # Write the data to a new file
        with open("latest_measurements.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

        # Print the data to stdout for the Node.js process
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)