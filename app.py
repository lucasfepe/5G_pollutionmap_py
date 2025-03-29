from flask import Flask, jsonify
from fetch_pollution import fetch_latest_measurements
from dotenv import load_dotenv
import os

load_dotenv()
print(os.getenv("NEXT_PUBLIC_OPENAQ_API_KEY"))
app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Flask Backend Server!"

@app.route("/about")
def about():
    return "This is the About page."

@app.route("/api/pollution", methods=["GET"])
def get_pollution_data():
    try:
        data = fetch_latest_measurements()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500