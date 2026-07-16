import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_forecast(latitude, longitude):
    Key1 = os.getenv("Api_key")
    headers = {
        "X-RapidAPI-Key": Key1,
    }
    url = "https://open-weather13.p.rapidapi.com/fivedaysforcast"
    response = requests.get(url, headers=headers, params={"latitude": latitude, "longitude": longitude})
    return response.json()