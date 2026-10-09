
import os
import boto3

BUCKET_NAME = "climatepulse-sahil-2026"
REGION = "eu-west-1"

LOCAL_FILE = "data/processed/climate_processed.parquet"
S3_KEY = "processed/climate_processed.parquet"


def upload_to_s3():
    if not os.path.isfile(LOCAL_FILE):
        raise FileNotFoundError(
            f"Processed Parquet file not found: {LOCAL_FILE}. "
            "Run the transformation task successfully before uploading."
        )

    s3 = boto3.client("s3", region_name=REGION)

    s3.upload_file(
        LOCAL_FILE,
        BUCKET_NAME,
        S3_KEY,
    )

    print(
        f"Processed data successfully uploaded to "
        f"s3://{BUCKET_NAME}/{S3_KEY}"
    )


if __name__ == "__main__":
    upload_to_s3()