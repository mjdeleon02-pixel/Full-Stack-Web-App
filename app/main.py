from flask import Flask, jsonify, render_template
from flask_cors import CORS
from crud import init_db, get_items, add_item, delete_item
from auth import auth_bp

app = Flask(__name__)
CORS(app)

db = init_db()

# Register auth blueprint with /auth prefix
app.register_blueprint(auth_bp, url_prefix='/auth')

# Page routes
@app.route('/')
def home_page():
    return render_template('login.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/app')
def app_page():
    return render_template('index.html')

# API routes
@app.route('/api/items', methods=['GET'])
def read_items():
    return jsonify(get_items(db))

@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    return jsonify(add_item(db, data))

@app.route('/api/items/<item_id>', methods=['DELETE'])
def delete_item_route(item_id):
    return jsonify(delete_item(db, item_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
