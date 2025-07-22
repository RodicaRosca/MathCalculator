import json
from kafka import KafkaProducer
import os

def log_to_kafka(log_data):
    try:
        producer = KafkaProducer(
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        producer.send('apilogs', log_data)
        producer.flush()
        producer.close()
    except Exception as e:
        print(f"Kafka logging failed: {e}")
