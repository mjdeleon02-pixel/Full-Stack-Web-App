from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from crud import init_db

auth_bp = Blueprint('auth', __name__)
db = init_db()  # Connects to MongoDB database

# Collection for users
users_col = db.users

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    if users_col.find_one({'username': username}):
        return jsonify({'error': 'Username already exists'}), 400

    hashed_pw = generate_password_hash(password)
    users_col.insert_one({'username': username, 'password': hashed_pw})
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    user = users_col.find_one({'username': username})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid username or password'}), 401

    return jsonify({'message': 'Login successful'}), 200
