from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("OPENAQ_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please check your .env file.")


from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title="Pollution Map API")

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
