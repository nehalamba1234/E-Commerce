from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.websockets import WebSocket
from kafka import KafkaProducer
from pydantic import BaseModel
import json
import logging
import db

app = FastAPI()

# Kafka Configuration
KAFKA_BROKER_URL = "localhost:9092"
ORDER_TOPIC = "order_topic"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# WebSockets for real-time updates
clients = []

# Jinja2 Templates
templates = Jinja2Templates(directory="templates")

# Serve static files
#app.mount("/static", StaticFiles(directory="static"), name="static")

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Order Model
class OrderRequest(BaseModel):
    order_id: str
    user_id: str
    product_id: str
    quantity: int

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        clients.remove(websocket)

@app.post("/place_order/")
@app.post("/place_order")
async def place_order(order: OrderRequest):
    """API to place a new order and publish event to Kafka"""
    order_event = order.dict()
    order_event["status"] = "order_placed"
    logging.info(f'order info{order_event}')

    # Store order in MongoDB
    db.insert_order(order_event)
    logger.info(f'Order saved in MongoDB: {order_event}')

    producer.send(ORDER_TOPIC, order_event)
    logger.info('order info sent to order_topic')
    producer.flush()

    # Send real-time update via WebSockets
    for client in clients:
        await client.send_json(order_event)

    return {"message": "Order placed successfully!", "order": order_event}

@app.get("/orders/")
async def get_orders():
    """API to fetch all orders from MongoDB"""
    orders = list(db.orders_collection.find({}) ) # Exclude MongoDB's default _id
    return {"orders": orders}
