from datetime import datetime, timezone

import pandas as pd
import requests

from config.locations import LOCATIONS


def fetch_weather_data(location):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "hourly": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m,"
            "wind_direction_10m,"
            "surface_pressure,"
            "precipitation,"
            "cloud_cover,"
            "shortwave_radiation"
        ),
        "timezone": "auto",
        "forecast_days": 7
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()


def main():
    all_weather_data = []

    for location in LOCATIONS:
        print(
            f"Fetching weather data for "
            f"{location['city']}, {location['state']}..."
        )

        data = fetch_weather_data(location)
        hourly_data = data["hourly"]

        df = pd.DataFrame(hourly_data)

        df["state"] = location["state"]
        df["city"] = location["city"]
        df["latitude"] = location["latitude"]
        df["longitude"] = location["longitude"]
        df["location_type"] = location["location_type"]
        df["ingested_at"] = datetime.now(timezone.utc).isoformat()

        all_weather_data.append(df)

    final_df = pd.concat(all_weather_data, ignore_index=True)

    final_df.to_csv(
        "data/raw/weather_data.csv",
        index=False
    )

    print("\nWeather data successfully saved.")
    print(f"Locations processed: {len(LOCATIONS)}")
    print(f"Total rows: {len(final_df)}")
    print(final_df.head())


if __name__ == "__main__":
    main()