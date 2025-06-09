import json
import time
import random
from kafka import KafkaProducer

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

events = ['page_view', 'add_to_cart', 'purchase', 'logout']

# Send simulated events
def generate_events():
    user_ids = [101, 102, 103]
    while True:
        event = {
            'user_id': random.choice(user_ids),
            'event': random.choice(events),
            'timestamp': time.time()
        }
        print(f"Producing: {event}")
        producer.send('user-events', value=event)
        time.sleep(1)

if __name__ == "__main__":
    generate_events()
