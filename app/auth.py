from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
from pymongo import MongoClient

auth_bp = Blueprint('auth', __name__)
MONGO_URI = os.environ.get('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client["flaskappdocker"]

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if db.users.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 400

    hashed_pw = generate_password_hash(password)
    db.users.insert_one({"username": username, "password": hashed_pw})

    return jsonify({"status": "registered"}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    user = db.users.find_one({"username": username})
    
    if not user:
        return jsonify({"error": "Invalid username or password"}), 400
    
    if not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid username or password"}), 400
    
    return jsonify({"message": "Login successful"}), 200
