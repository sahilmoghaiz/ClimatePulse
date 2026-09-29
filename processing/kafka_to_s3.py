import os
import csv
import json
from kafka import KafkaConsumer

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC_NAME = "weather_data"

OUTPUT_FILE = "data/raw/weather_from_kafka.csv"
EXPECTED_MESSAGES = 168


def consume_weather_data():
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    rows = []

    for message in consumer:
        rows.append(message.value)

        print(f"Received message {len(rows)}/{EXPECTED_MESSAGES}")

        if len(rows) >= EXPECTED_MESSAGES:
            break

    consumer.close()

    if not rows:
        print("No messages received.")
        return

    fieldnames = rows[0].keys()

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(rows)

    print(f"Successfully consumed {len(rows)} messages.")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    consume_weather_data()