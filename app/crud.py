from pymongo import MongoClient
import os
from bson import ObjectId

def init_db():
    # Get MongoDB URI from environment
    uri = os.environ.get('MONGO_URI')  
    if not uri:
        raise ValueError("MONGO_URI not set in environment")
    
    # Get DB name from environment or default
    db_name = os.environ.get('MONGO_DB', 'flaskappdocker')  
    client = MongoClient(uri)
    db = client[db_name]
    print(f"Connected to MongoDB Atlas database: {db_name}")
    return db

def get_items(db):
    return [{"_id": str(doc["_id"]), "name": doc["name"]} for doc in db.items.find()]

def add_item(db, data):
    if "name" not in data or not data["name"]:
        return {"error": "Item name is required"}, 400
    result = db.items.insert_one({"name": data["name"]})
    return {"inserted_id": str(result.inserted_id)}

def delete_item(db, item_id):
    db.items.delete_one({"_id": ObjectId(item_id)})
    return {"status": "deleted"}
