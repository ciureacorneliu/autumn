from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes and origins
# CORS(app)
# CORS(app, resources={r"/*": {"origins": ["http://autumn.com"]}})
CORS(app, resources={r"/*": {"origins": "http://autumn.com"}})



# Define a hard-coded API token for authentication
API_TOKEN = "my_secret_token"

# In-memory data store for testing purposes
data_store = {}

# Decorator for token authentication
def require_api_token(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token != f"Bearer {API_TOKEN}":
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# GET method - Retrieve a greeting message
@app.route('/greet', methods=['GET'])
@require_api_token
def greet():
    name = request.args.get("name", "World")
    return jsonify({"message": f"Hello, {name}!"}), 200

# POST method - Create a new item
@app.route('/items', methods=['POST'])
@require_api_token
def create_item():
    item = request.json
    if not item or 'id' not in item or 'value' not in item:
        return jsonify({"error": "Please provide 'id' and 'value' in the JSON body"}), 400
    data_store[item['id']] = item['value']
    return jsonify({"message": "Item created", "item": item}), 201

# PUT method - Update an existing item
@app.route('/items/<int:item_id>', methods=['PUT'])
@require_api_token
def update_item(item_id):
    if item_id not in data_store:
        return jsonify({"error": "Item not found"}), 404
    item = request.json
    if not item or 'value' not in item:
        return jsonify({"error": "Please provide 'value' in the JSON body"}), 400
    data_store[item_id] = item['value']
    return jsonify({"message": "Item updated", "item": {"id": item_id, "value": item['value']}}), 200

# DELETE method - Delete an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
@require_api_token
def delete_item(item_id):
    if item_id not in data_store:
        return jsonify({"error": "Item not found"}), 404
    del data_store[item_id]
    return jsonify({"message": "Item deleted"}), 200

# PATCH method - Partially update an item
@app.route('/items/<int:item_id>', methods=['PATCH'])
@require_api_token
def patch_item(item_id):
    if item_id not in data_store:
        return jsonify({"error": "Item not found"}), 404
    patch_data = request.json
    if not patch_data or 'value' not in patch_data:
        return jsonify({"error": "Please provide 'value' in the JSON body"}), 400
    data_store[item_id] = patch_data['value']
    return jsonify({"message": "Item partially updated", "item": {"id": item_id, "value": patch_data['value']}}), 200

# Health Check Endpoint
@app.route('/health', methods=['GET'])
@require_api_token
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
