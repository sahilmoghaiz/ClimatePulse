import requests
import pandas as pd

LATITUDE = 13.0827
LONGITUDE = 80.2707

def fetch_air_quality_data():
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude":LATITUDE,
        "longitude":LONGITUDE,
        "hourly":(
            "pm2_5,"
            "pm10,"
            "carbon_monoxide,"
            "nitrogen_dioxide,"
            "sulphur_dioxide,"
            "ozone,"
            "us_aqi,"
            "european_aqi"
        ),
        "timezone":"auto",
        "forecast_days":7
    }
    response = requests.get(url,params=params)
    response.raise_for_status()
    data=response.json()
    return data


def main():
    data = fetch_air_quality_data()
    hourly_data = data["hourly"]
    df = pd.DataFrame(hourly_data)
    df.to_csv("data/raw/air_quality_data.csv",index = False)
    print("Air quality data sucessfully saved.")
    print(df.head())

if __name__ == "__main__":
    main()