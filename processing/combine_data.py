import pandas as pd

WEATHER_FILE = "data/staging/weather_cleaned.csv"
AIR_QUALITY_FILE = "data/staging/air_quality_cleaned.csv"

OUTPUT_FILE = "data/staging/climate_combined.csv"


def combine_data():
    weather_df = pd.read_csv(WEATHER_FILE)
    air_quality_df = pd.read_csv(AIR_QUALITY_FILE)

    # Convert time to datetime
    weather_df["time"] = pd.to_datetime(weather_df["time"])
    air_quality_df["time"] = pd.to_datetime(air_quality_df["time"])

    # Combine Weather and Air Quality using timestamp
    combined_df = pd.merge(
        weather_df,
        air_quality_df,
        on="time",
        how="left"
    )

    # Save combined dataset
    combined_df.to_csv(OUTPUT_FILE, index=False)

    print("Weather and air quality data successfully combined.")
    print(f"Rows: {len(combined_df)}")
    print(f"Columns: {len(combined_df.columns)}")


if __name__ == "__main__":
    combine_data()