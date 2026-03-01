from pymongo import MongoClient
import os
from bson import ObjectId

def init_db():
    uri = os.environ.get('MONGO_URI')  # Get the connection URI from the environment
    client = MongoClient(uri)
    db_name = os.environ.get('MONGO_DB', 'flaskappdocker')  # Default DB name if not set
    return client[db_name]

def get_items(db):
    return [{"_id": str(doc['_id']), "name": doc['name']} for doc in db.items.find()]

def add_item(db, data):
    result = db.items.insert_one({"name": data['name']})
    return {"inserted_id": str(result.inserted_id)}

def delete_item(db, item_id):
    db.items.delete_one({'_id': ObjectId(item_id)})
    return {"status": "deleted"}
