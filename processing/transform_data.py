
import os
import pandas as pd

INPUT_FILE = "data/staging/climate_combined.csv"
OUTPUT_FILE = "data/processed/climate_processed.parquet"


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


def classify_temperature(temp):
    if pd.isna(temp):
        return "Unavailable"
    elif temp < 20:
        return "Cool"
    elif temp < 30:
        return "Moderate"
    else:
        return "Hot"


def transform_data():
    df = pd.read_csv(INPUT_FILE)

    # Convert time to datetime
    df["time"] = pd.to_datetime(df["time"])

    # Create AQI category
    df["aqi_category"] = df["us_aqi"].apply(classify_aqi)

    # Create rain indicator; preserve missing precipitation values
    df["is_raining"] = df["precipitation"].gt(0).astype("boolean")
    df.loc[df["precipitation"].isna(), "is_raining"] = pd.NA

    # Create temperature category
    df["temperature_category"] = df["temperature_2m"].apply(
        classify_temperature
    )

    # Create output directory if it does not exist
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # Save processed data as Parquet
    df.to_parquet(OUTPUT_FILE, index=False, engine="pyarrow")

    print("Data transformation completed.")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Output: {OUTPUT_FILE}")
    print("\nAQI categories:")
    print(df["aqi_category"].value_counts(dropna=False))
    print("\nTemperature categories:")
    print(df["temperature_category"].value_counts(dropna=False))


if __name__ == "__main__":
    transform_data()