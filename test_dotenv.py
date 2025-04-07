# test_dotenv.py
from dotenv import load_dotenv
import os
from pathlib import Path

print("Testing dotenv functionality...")

# Get the directory containing this file
current_dir = Path(__file__).parent
env_path = current_dir / '.env'

print(f"Looking for .env file at: {env_path}")
print(f".env file exists: {env_path.exists()}")

if env_path.exists():
    print("\nContents of .env file:")
    with open(env_path, 'r') as f:
        print(f.read())

print("\nTrying to load environment variables...")
load_dotenv(env_path)

api_key = os.getenv("OPENAQ_API_KEY")
print(f"API Key loaded: {bool(api_key)}")
print(f"API Key value: {api_key if api_key else 'Not found'}")

print("\nAll environment variables:")
for key, value in os.environ.items():
    if 'API' in key:
        print(f"{key}: {value}")
