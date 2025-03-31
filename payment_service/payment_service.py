from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
import asyncio

app = FastAPI()

# Kafka Configuration
KAFKA_BROKER_URL = "localhost:9092"
ORDER_TOPIC = "order_topic"
PAYMENT_TOPIC = "payment_topic"

async def consume_orders():
    """Asynchronous Kafka Consumer"""
    consumer = AIOKafkaConsumer(
        ORDER_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )
    await consumer.start()

    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    await producer.start()

    try:
        async for message in consumer:
            order = message.value
            order["status"] = "payment_processed"
            
            await producer.send(PAYMENT_TOPIC, value=order)
    finally:
        await consumer.stop()
        await producer.stop()

@app.on_event("startup")
async def start_consumer():
    """Run Kafka consumer in the background"""
    asyncio.create_task(consume_orders())

@app.get("/")
async def home():
    return {"message": "Payment Service Running"}
