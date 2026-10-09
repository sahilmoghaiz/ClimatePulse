import os
import pandas as pd

WEATHER_FILE = "data/staging/weather_cleaned.csv"
AIR_QUALITY_FILE = "data/staging/air_quality_cleaned.csv"

OUTPUT_FILE = "data/staging/climate_combined.csv"

MERGE_KEYS = ["state", "city", "time"]


def combine_data():
    weather_df = pd.read_csv(WEATHER_FILE)
    air_quality_df = pd.read_csv(AIR_QUALITY_FILE)

    # Convert timestamps to datetime
    weather_df["time"] = pd.to_datetime(weather_df["time"])
    air_quality_df["time"] = pd.to_datetime(air_quality_df["time"])

    # Validate merge keys
    for name, df in [
        ("Weather", weather_df),
        ("Air quality", air_quality_df),
    ]:
        missing_columns = set(MERGE_KEYS) - set(df.columns)
        if missing_columns:
            raise ValueError(
                f"{name} data is missing merge columns: "
                f"{sorted(missing_columns)}"
            )

        duplicate_keys = df.duplicated(subset=MERGE_KEYS).sum()
        if duplicate_keys:
            raise ValueError(
                f"{name} data contains {duplicate_keys} duplicate "
                f"location-timestamp keys."
            )

    # Combine weather with matching air-quality records
    combined_df = pd.merge(
        weather_df,
        air_quality_df,
        on=MERGE_KEYS,
        how="left",
        suffixes=("_weather", "_air_quality"),
        validate="one_to_one",
    )

    # Create output directory if it does not exist
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    combined_df.to_csv(OUTPUT_FILE, index=False)

    print("Weather and air quality data successfully combined.")
    print(f"Rows: {len(combined_df)}")
    print(f"Columns: {len(combined_df.columns)}")
    print(
        "Rows without matching AQI data:",
        combined_df["pm2_5"].isna().sum()
        if "pm2_5" in combined_df.columns
        else "pm2_5 column not found",
    )


if __name__ == "__main__":
    combine_data()