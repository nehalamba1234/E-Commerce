from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
import asyncio
import json
import logging
import os

app = FastAPI()

# Kafka Configuration
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
PAYMENT_TOPIC = os.getenv("PAYMENT_TOPIC", "payment_topic")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def consume_notifications():
    """Asynchronous Kafka consumer for payment notifications."""
    while True:  # Retry mechanism in case of failure
        try:
            consumer = AIOKafkaConsumer(
                PAYMENT_TOPIC,
                bootstrap_servers=KAFKA_BROKER_URL,
                value_deserializer=lambda v: json.loads(v.decode("utf-8"))
            )
            await consumer.start()
            logger.info("Kafka consumer started for notifications.")

            async for message in consumer:
                order = message.value
                logger.info(f"Notification sent for Order {order['order_id']} - Status: {order['status']}")

        except Exception as e:
            logger.error(f"Kafka Consumer Error: {e}")
            await asyncio.sleep(5)  # Wait before retrying

        finally:
            await consumer.stop()

@app.on_event("startup")
async def start_consumer():
    """Start Kafka consumer in the background."""
    asyncio.create_task(consume_notifications())

@app.get("/")
async def home():
    return {"message": "Notification Service Running"}
