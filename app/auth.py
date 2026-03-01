from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from crud import init_db  # or wherever your DB helper is

auth_bp = Blueprint('auth', __name__)
db = init_db()  # get the database

# Register route
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    
    if db.users.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400
    
    hashed_pw = generate_password_hash(password)
    db.users.insert_one({"username": username, "password": hashed_pw})
    return jsonify({"message": "User registered successfully"})

# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    
    user = db.users.find_one({"username": username})
    if user and check_password_hash(user['password'], password):
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"error": "Invalid credentials"}), 401
