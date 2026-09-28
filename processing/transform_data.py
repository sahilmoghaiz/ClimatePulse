import pandas as pd

INPUT_FILE = "data/staging/climate_combined.csv"
OUTPUT_FILE = "data/processed/climate_processed.parquet"


def transform_data():
    df = pd.read_csv(INPUT_FILE)

    # Convert time to datetime
    df["time"] = pd.to_datetime(df["time"])

    # Create AQI category
    def classify_aqi(aqi):
        if pd.isna(aqi):
            return "Unavailable"
        elif aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Moderate"
        elif aqi <= 150:
            return "Unhealthy for Sensitive Groups"
        elif aqi <= 200:
            return "Unhealthy"
        elif aqi <= 300:
            return "Very Unhealthy"
        else:
            return "Hazardous"

    df["aqi_category"] = df["us_aqi"].apply(classify_aqi)

    # Create rain indicator
    df["is_raining"] = df["precipitation"] > 0

    # Create temperature category
    def classify_temperature(temp):
        if temp < 20:
            return "Cool"
        elif temp < 30:
            return "Moderate"
        else:
            return "Hot"

    df["temperature_category"] = df["temperature_2m"].apply(
        classify_temperature
    )

    # Save processed data as Parquet
    df.to_parquet(OUTPUT_FILE, index=False)

    print("Data transformation completed.")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")


if __name__ == "__main__":
    transform_data()