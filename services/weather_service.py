import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path="secrets.env")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def weather_onecall(lat, lon):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json()
