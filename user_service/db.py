from pymongo import MongoClient

client = MongoClient("mongodb+srv://nehalamba331:nehalamba331@e-commerce.t5g8txo.mongodb.net/")
print(client)
db = client["E-Commerce"] #database
users_collection = db["users"] #collection

def insert_user(user_data):
    user_data["_id"] = user_data["username"]
    users_collection.insert_one(user_data)

def get_user(username):
    return users_collection.find_one({"_id": username})

def validate_user(username, password):
    user = users_collection.find_one({"_id": username})
    if user and user.get("password") == password:
        return True
    return False