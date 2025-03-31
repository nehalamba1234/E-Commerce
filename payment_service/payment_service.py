from fastapi import FastAPI
from kafka import KafkaConsumer, KafkaProducer
import json
import asyncio

app = FastAPI()

# Kafka Configuration
KAFKA_BROKER_URL = "localhost:9092"
ORDER_TOPIC = "order_topic"
PAYMENT_TOPIC = "payment_topic"

consumer = KafkaConsumer(
    ORDER_TOPIC,
    bootstrap_servers=KAFKA_BROKER_URL,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

async def consume_orders():
    """Continuously consume orders and process payments"""
    for message in consumer:
        order = message.value
        order["status"] = "payment_processed"

        producer.send(PAYMENT_TOPIC, order)
        producer.flush()

@app.on_event("startup")
async def start_consumer():
    """Run Kafka consumer in the background"""
    loop = asyncio.get_event_loop()
    loop.create_task(consume_orders())

@app.get("/")
async def home():
    return {"message": "Payment Service Running"}
