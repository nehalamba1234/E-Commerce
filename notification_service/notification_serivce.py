from fastapi import FastAPI
from kafka import KafkaConsumer
import json

app = FastAPI()

# Kafka Configuration
KAFKA_BROKER_URL = "localhost:9092"
PAYMENT_TOPIC = "payment_topic"

consumer = KafkaConsumer(
    PAYMENT_TOPIC,
    bootstrap_servers=KAFKA_BROKER_URL,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

@app.on_event("startup")
async def process_notifications():
    for message in consumer:
        order = message.value
        print(f"Notification sent for order {order['order_id']} - Status: {order['status']}")

@app.get("/")
async def home():
    return {"message": "Notification Service Running"}
