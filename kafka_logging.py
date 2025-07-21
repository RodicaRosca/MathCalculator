from kafka import KafkaProducer
import json
import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def log_to_kafka(log_data):
    try:
        producer.send('apilogs', log_data)
        producer.flush()
    except Exception as e:
        print(f"Kafka logging failed: {e}")
