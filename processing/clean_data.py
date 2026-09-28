import pandas as pd

WEATHER_FILE = "data/raw/weather_data.csv"
AIR_QUALITY_FILE = "data/raw/air_quality_data.csv"

WEATHER_OUTPUT = "data/staging/weather_cleaned.csv"
AIR_QUALITY_OUTPUT = "data/staging/air_quality_cleaned.csv"


def clean_weather_data():
    weather_df = pd.read_csv(WEATHER_FILE)

    # Convert time from string to datetime
    weather_df["time"] = pd.to_datetime(weather_df["time"])

    # Remove duplicate rows
    weather_df = weather_df.drop_duplicates()

    # Save cleaned data
    weather_df.to_csv(WEATHER_OUTPUT, index=False)

    print("Weather data cleaned and saved.")


def clean_air_quality_data():
    air_quality_df = pd.read_csv(AIR_QUALITY_FILE)

    # Convert time from string to datetime
    air_quality_df["time"] = pd.to_datetime(air_quality_df["time"])

    # Remove duplicate rows
    air_quality_df = air_quality_df.drop_duplicates()

    # Indicate whether air quality data is available
    air_quality_df["aqi_data_available"] = air_quality_df["pm2_5"].notna()

    # Save cleaned data
    air_quality_df.to_csv(AIR_QUALITY_OUTPUT, index=False)

    print("Air quality data cleaned and saved.")

def main():
    clean_weather_data()
    clean_air_quality_data()


if __name__ == "__main__":
    main()