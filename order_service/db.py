from pymongo import MongoClient

client = MongoClient("mongodb+srv://nehalamba331:nehalamba331@e-commerce.t5g8txo.mongodb.net/")
print(client)
db = client["E-Commerce"] #database
orders_collection = db["orders"] #collection


def insert_order(order_data: dict):
    """Insert a new order into the MongoDB collection"""
    order_data["_id"]=order_data["order_id"]
    result=orders_collection.insert_one(order_data)
    return result.inserted_id

def get_order(order_id: str) -> dict:
    """Retrieve a single order by order_id"""
    return orders_collection.find_one({"_id": order_id})

def update_order_status(order_id: str, status: str):
    """Update the status of an existing order"""
    orders_collection.update_one(
        {"_id": order_id},
        {"$set": {"status": status}}
    )

def get_all_orders() -> list:
    """Retrieve all orders from the collection"""
    return list(orders_collection.find({}))