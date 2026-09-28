import pandas as pd

WEATHER_FILE = "data/staging/weather_cleaned.csv"
AIR_QUALITY_FILE = "data/staging/air_quality_cleaned.csv"
COMBINED_FILE = "data/staging/climate_combined.csv"
PROCESSED_FILE = "data/processed/climate_processed.parquet"

def inspect_data():
    weather_df = pd.read_csv(WEATHER_FILE)
    air_quality_df = pd.read_csv(AIR_QUALITY_FILE)

    weather_df["time"] = pd.to_datetime(weather_df["time"])
    air_quality_df["time"] = pd.to_datetime(air_quality_df["time"])


    print("WEATHER DATA")
    print(weather_df.head())
    print(weather_df.info())

    print("\nAIR QUALITY DATA")
    print(air_quality_df.head())
    print(air_quality_df.info())

    print("\nWEATHER DUPLICATES:", weather_df.duplicated().sum())
    print("AIR QUALITY DUPLICATES:", air_quality_df.duplicated().sum())

    print("\nAIR QUALITY MISSING VALUES")
    print(air_quality_df.isnull().sum())

    print("\nMISSING AIR QUALITY ROWS")
    print(
        air_quality_df[
            air_quality_df["pm2_5"].isnull()
        ][["time", "pm2_5", "us_aqi"]].head(10)
    )

    print("\nLAST COMPLETE AQI ROW")
    print(
        air_quality_df[
            air_quality_df["pm2_5"].notnull()
        ].tail(1)
    )

    print("\nFIRST MISSING AQI ROW")
    print(
        air_quality_df[
            air_quality_df["pm2_5"].isnull()
        ].head(1)
    )

    print("\nTIMESTAMP CHECK")
    print("Weather start:", weather_df["time"].min())
    print("Weather end:", weather_df["time"].max())
    print("AQI start:", air_quality_df["time"].min())
    print("AQI end:", air_quality_df["time"].max())

    print("\nAQI VALUE CHECK")
    print(air_quality_df.loc[113, "us_aqi"])
    print(type(air_quality_df.loc[113, "us_aqi"]))


def inspect_combined_data():
    combined_df = pd.read_csv(COMBINED_FILE)

    combined_df["time"] = pd.to_datetime(combined_df["time"])

    print("\nCOMBINED CLIMATE DATA")
    print(combined_df.head())
    print(combined_df.info())

    print("\nCOMBINED DUPLICATES:",
          combined_df.duplicated().sum())

    print("\nMISSING VALUES")
    print(combined_df.isnull().sum())

    print("\nTIMESTAMP CHECK")
    print("Start:", combined_df["time"].min())
    print("End:", combined_df["time"].max())


def inspect_processed_data():
    processed_df = pd.read_parquet(PROCESSED_FILE)

    print("\nPROCESSED CLIMATE DATA")
    print(processed_df.head())
    print(processed_df.info())

    print("\nPROCESSED DUPLICATES:",
          processed_df.duplicated().sum())

    print("\nMISSING VALUES")
    print(processed_df.isnull().sum())

    print("\nAQI CATEGORIES")
    print(processed_df["aqi_category"].value_counts(dropna=False))

    print("\nRAIN VALUES")
    print(processed_df["is_raining"].value_counts(dropna=False))

    print("\nTEMPERATURE CATEGORIES")
    print(processed_df["temperature_category"].value_counts(dropna=False))

    print("\nTIMESTAMP CHECK")
    print("Start:", processed_df["time"].min())
    print("End:", processed_df["time"].max())


if __name__ == "__main__":
    inspect_data()
    inspect_combined_data()
    inspect_processed_data()