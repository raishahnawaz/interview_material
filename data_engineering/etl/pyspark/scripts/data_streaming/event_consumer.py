from kafka import KafkaConsumer
import json

# Initialize consumer for topic 'user-events'
consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='event-tracker',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Listening to 'user-events'...")

for message in consumer:
    event = message.value
    print(f"Consumed event: {event}")
