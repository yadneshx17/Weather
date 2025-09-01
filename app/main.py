from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from app.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WEATHER_API_URL = settings.weather_api_url
WEATHER_API_KEY = settings.weather_api_KEY

@app.get("/weather/{city}")
async def get_weather(city: str):
    params = {
    "q": f"{city}",
    "appid": WEATHER_API_KEY,
    "units": "metric"
    }
    async with httpx.AsyncClient() as client: # AsyncClient client of httpx.
        try:
            response = await client.get(WEATHER_API_URL, params=params)
            print(response.status_code)  # Should be 200
            return response.json() 
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Error fetching weather data")