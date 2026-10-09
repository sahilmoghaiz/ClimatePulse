
import csv
import json
import os

from kafka import KafkaConsumer

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC_NAME = "air_quality_data"

OUTPUT_FILE = "data/raw/air_quality_from_kafka.csv"
EXPECTED_MESSAGES = 31 * 168
CONSUMER_TIMEOUT_MS = 30000


def consume_air_quality_data():
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        consumer_timeout_ms=CONSUMER_TIMEOUT_MS,
    )

    rows = []

    try:
        for message in consumer:
            rows.append(message.value)
            print(
                f"Received message {len(rows)}/{EXPECTED_MESSAGES}",
                flush=True,
            )

            if len(rows) >= EXPECTED_MESSAGES:
                break
    finally:
        consumer.close()

    if not rows:
        raise RuntimeError("No air-quality messages received from Kafka.")

    if len(rows) != EXPECTED_MESSAGES:
        raise RuntimeError(
            f"Expected {EXPECTED_MESSAGES} air-quality messages, "
            f"but received {len(rows)}. Refusing to save incomplete data."
        )

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    fieldnames = rows[0].keys()

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Successfully consumed {len(rows)} messages.", flush=True)
    print(f"Saved to {OUTPUT_FILE}", flush=True)


if __name__ == "__main__":
    consume_air_quality_data()
