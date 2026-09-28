import requests
import pandas as pd

LATITUDE = 13.0827
LONGITUDE = 80.2707

def fetch_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
    "latitude":LATITUDE,
     "longitude":LONGITUDE,
     "hourly":(
         "temperature_2m,"
         "relative_humidity_2m,"
         "wind_speed_10m,"
         "wind_direction_10m,"
         "surface_pressure,"
         "precipitation,"
         "cloud_cover,"
         "shortwave_radiation"
     ),
     "timezone":"auto",
     "forecast_days":7
    }
    response = requests.get(url,params=params)
    response.raise_for_status()
    data = response.json()
    return data

def main():
    data = fetch_weather_data()
    hourly_data = data["hourly"]
    df=pd.DataFrame(hourly_data)
    df.to_csv("data/raw/weather_data.csv", index = False)
    print("Weather data successfully saved.")
    print(df.head())
if __name__ == "__main__":
    main()
    
    
