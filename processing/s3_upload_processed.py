import boto3

BUCKET_NAME = "climatepulse-sahil-2026"
REGION = "eu-west-1"

LOCAL_FILE = "data/processed/climate_processed.parquet"
S3_KEY = "processed/climate_processed.parquet"


def upload_to_s3():
    s3 = boto3.client("s3", region_name=REGION)

    s3.upload_file(
        LOCAL_FILE,
        BUCKET_NAME,
        S3_KEY
    )

    print("Processed data successfully uploaded to S3.")


if __name__ == "__main__":
    upload_to_s3()