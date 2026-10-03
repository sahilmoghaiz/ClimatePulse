from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, max, min, round, to_date, when

# 1. Create Spark session
spark = SparkSession.builder \
    .appName("ClimatePulse") \
    .master("local[*]") \
    .getOrCreate()

# 2. Read combined climate data
df = spark.read.csv(
    "data/staging/climate_combined.csv",
    header=True,
    inferSchema=True
)

print("Data loaded successfully.")
df.printSchema()

# 3. Select important columns
climate_df = df.select(
    "state",
    "city",
    "time",
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "precipitation",
    "pm2_5",
    "pm10",
    "us_aqi"
)

print("Selected climate data:")
climate_df.show(5)

# 4. Filter high AQI records
high_aqi_df = climate_df.filter(
    climate_df.us_aqi > 100
)

print("High AQI records:")
high_aqi_df.show(5)

# 5. Add date and AQI category
transformed_df = climate_df.withColumn(
    "date",
    to_date("time")
).withColumn(
    "aqi_category",
    when(climate_df.us_aqi.isNull(), "Unavailable")
    .when(climate_df.us_aqi <= 50, "Good")
    .when(climate_df.us_aqi <= 100, "Moderate")
    .when(climate_df.us_aqi <= 150, "Unhealthy for Sensitive Groups")
    .when(climate_df.us_aqi <= 200, "Unhealthy")
    .when(climate_df.us_aqi <= 300, "Very Unhealthy")
    .otherwise("Hazardous")
)

print("Transformed climate data:")
transformed_df.show(5)

# 6. Create daily climate summary
daily_summary = transformed_df.groupBy("state", "city", "date").agg(
    round(avg("us_aqi"), 2).alias("average_aqi"),
    round(max("us_aqi"), 2).alias("maximum_aqi"),
    round(min("us_aqi"), 2).alias("minimum_aqi"),
    round(avg("temperature_2m"), 2).alias("average_temperature"),
    round(max("temperature_2m"), 2).alias("maximum_temperature"),
    round(avg("precipitation"), 2).alias("average_precipitation"),
    round(avg("wind_speed_10m"), 2).alias("average_wind_speed"),
    round(avg("pm2_5"), 2).alias("average_pm2_5")
)

# 7. Add category based on daily average AQI
final_df = daily_summary.withColumn(
    "aqi_category",
    when(daily_summary.average_aqi.isNull(), "Unavailable")
    .when(daily_summary.average_aqi <= 50, "Good")
    .when(daily_summary.average_aqi <= 100, "Moderate")
    .when(daily_summary.average_aqi <= 150, "Unhealthy for Sensitive Groups")
    .when(daily_summary.average_aqi <= 200, "Unhealthy")
    .when(daily_summary.average_aqi <= 300, "Very Unhealthy")
    .otherwise("Hazardous")
)

print("Final Climate Data:")
final_df.show()

output_path = "data/processed/climate_final.parquet"

final_df.write \
    .mode("overwrite") \
    .parquet(output_path)

print("Final Parquet file written successfully.")
print(f"Output path: {output_path}")

spark.stop()