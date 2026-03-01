from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from crud import init_db, get_items, add_item, delete_item
from auth import auth_bp

app = Flask(__name__)
CORS(app)

# Initialize the database
db = init_db()

# Register auth blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def home_page():
    return redirect(url_for('login_page'))  # Redirect to login page

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/app')
def app_page():
    return render_template('index.html') 

# API routes for items
@app.route('/api/items', methods=['GET'])
def read_items():
    items = get_items(db)
    return jsonify(items)

@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = add_item(db, data)
    return jsonify(new_item)

@app.route('/api/items/<item_id>', methods=['DELETE'])
def delete_item_route(item_id):
    response = delete_item(db, item_id)
    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host='0.0.0.0', port=port)
