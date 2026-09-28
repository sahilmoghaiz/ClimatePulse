import csv
from kafka import KafkaProducer, JsonSerializer

KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "weather_data"
CSV_FILE = "data/raw/weather_data.csv"


def create_producer():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=JsonSerializer()
    )

    return producer


def send_weather_data(producer):
    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            producer.send(TOPIC_NAME, value=row)
            print(f"Sent: {row}")

    producer.flush()


def main():
    producer = create_producer()
    send_weather_data(producer)
    producer.close()

    print("Weather data successfully sent to Kafka.")


if __name__ == "__main__":
    main()