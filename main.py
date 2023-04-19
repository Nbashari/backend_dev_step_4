import pymongo
from flask import Flask, jsonify, request
from bson import ObjectId
from datetime import datetime

# Connect to the MongoDB instance
client = pymongo.MongoClient(
    "mongodb+srv://<username>:<password>@cluster0.f8uco.mongodb.net/backend_dev_first_steps?retryWrites=true&w=majority"
)
db = client.backend_dev_first_steps

# Create a Flask app
app = Flask(__name__)

# Create endpoint to insert a billing record


@app.route("/billing", methods=["POST"])
def create_billing_record():
    data = request.json
    # Validate data types
    if not isinstance(data.get("customer_id"), int):
        return jsonify({"error": "customer_id must be an integer"}), 400
    if not isinstance(data.get("cost"), float):
        return jsonify({"error": "cost must be a float"}), 400
    if not isinstance(data.get("currency"), str):
        return jsonify({"error": "currency must be a string"}), 400
    if not isinstance(data.get("is_paid"), bool):
        return jsonify({"error": "is_paid must be a boolean"}), 400
    if not isinstance(data.get("goods"), list):
        return jsonify({"error": "goods must be a list"}), 400
    # Validate required fields
    if not data.get("customer_id") or not data.get("cost") or not data.get("currency") or not data.get("goods"):
        return jsonify({"error": "customer_id, cost, currency, and goods are required"}), 400
    # Validate goods list is not empty
    if not data.get("goods"):
        return jsonify({"error": "goods list cannot be empty"}), 400
    # Update pay_date if is_paid is true
    if data.get("is_paid"):
        data["pay_date"] = datetime.now()
    # Insert record into MongoDB
    result = db.billing_records.insert_one(data)
    return jsonify({"message": "Billing record created successfully", "id": str(result.inserted_id)}), 201

# Create endpoint to update a billing record


@app.route("/billing/<string:billing_id>", methods=["PUT"])
def update_billing_record(billing_id):
    data = request.json
    # Validate data types
    if data.get("customer_id") and not isinstance(data.get("customer_id"), int):
        return jsonify({"error": "customer_id must be an integer"}), 400
    if data.get("cost") and not isinstance(data.get("cost"), float):
        return jsonify({"error": "cost must be a float"}), 400
    if data.get("currency") and not isinstance(data.get("currency"), str):
        return jsonify({"error": "currency must be a string"}), 400
    if data.get("is_paid") and not isinstance(data.get("is_paid"), bool):
        return jsonify({"error": "is_paid must be a boolean"}), 400
    if data.get("goods") and not isinstance(data.get("goods"), list):
        return jsonify({"error": "goods must be a list"}), 400
    # Validate required fields
    if data.get("goods") and not data.get("goods"):
        return jsonify({"error": "goods list cannot be empty"}), 400
    # Find record by ID
