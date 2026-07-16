from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from city_name import get_location
from weather import get_forecast

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI"}

@app.get("/weather")
def get_weather(city: str):
    location = get_location(city)
    if not location:
        raise HTTPException(status_code=404, detail="City not found")
        
    latitude = location.latitude
    longitude = location.longitude
    
    try:
        response_data = get_forecast(latitude, longitude)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    list_keys = ["temp", "feels_like", "temp_min", "temp_max", "pressure", "sea_level", "grnd_level", "humidity", "temp_kf"]
    
    forecast_data = []
    forecast_list = response_data.get("list", [])
    
    for item in forecast_list:
        main = item.get("main", {})
        weather = item.get("weather", [{}])
        clouds = item.get("clouds", {})
        visibility = item.get("visibility", 0)
        dt_txt = item.get("dt_txt", "")
        
        values1 = {key: main[key] for key in main.keys() if key in list_keys}
        values2 = {key: weather[0].get(key) for key in ["id", "main", "description", "icon"]}
        values3 = {key: clouds.get(key) for key in ["all"]}
        values4 = {"visibility": visibility}
        
        icon = values2.get("icon")
        icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png" if icon else ""

        forecast_item = {
            "dt_txt": dt_txt,
            "main": values1,
            "weather": values2,
            "clouds": values3,
            "visibility": values4,
            "icon_url": icon_url
        }
        forecast_data.append(forecast_item)

    return {
        "city_name": city,
        "latitude": latitude,
        "longitude": longitude,
        "forecast": forecast_data
    }
