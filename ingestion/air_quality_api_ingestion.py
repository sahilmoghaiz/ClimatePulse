import requests
import pandas as pd
from datetime import datetime, timezone

from config.locations import LOCATIONS


def fetch_air_quality_data(location):
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "hourly": (
            "pm2_5,"
            "pm10,"
            "carbon_monoxide,"
            "nitrogen_dioxide,"
            "sulphur_dioxide,"
            "ozone,"
            "us_aqi,"
            "european_aqi"
        ),
        "timezone": "auto",
        "forecast_days": 7
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    return data


def main():
    all_air_quality_data = []

    for location in LOCATIONS:
        print(
            f"Fetching air quality data for "
            f"{location['city']}, {location['state']}..."
        )

        data = fetch_air_quality_data(location)
        hourly_data = data["hourly"]

        df = pd.DataFrame(hourly_data)

        df["state"] = location["state"]
        df["city"] = location["city"]
        df["latitude"] = location["latitude"]
        df["longitude"] = location["longitude"]
        df["location_type"] = location["location_type"]
        df["ingested_at"] = datetime.now(timezone.utc).isoformat()

        all_air_quality_data.append(df)

    final_df = pd.concat(
        all_air_quality_data,
        ignore_index=True
    )

    final_df.to_csv(
        "data/raw/air_quality_data.csv",
        index=False
    )

    print("\nAir quality data successfully saved.")
    print(f"Locations processed: {len(LOCATIONS)}")
    print(f"Total rows: {len(final_df)}")
    print(final_df.head())


if __name__ == "__main__":
    main()