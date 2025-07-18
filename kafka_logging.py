from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def log_to_kafka(log_data):
    producer.send('apilogs', log_data)
    producer.flush()
