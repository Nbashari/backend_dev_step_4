import json
import unittest
from main import app, db
from datetime import datetime
from bson import ObjectId


class BillingRecordTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test client and a test billing record
        self.client = app.test_client()
        self.billing_record = {
            "customer_id": 123456,
            "cost": 99.99,
            "currency": "USD",
            "is_paid": False,
            "goods": ["Awesome Product", "Another Awesome Product"]
        }

    def tearDown(self):
        # Remove the test billing record from the database
        db.billing_records.delete_one({"_id": ObjectId(self.billing_record["_id"])})

    def test_create_billing_record(self):
        # Send a POST request to the /billing endpoint with the test billing record
        response = self.client.post("/billing", data=json.dumps(self.billing_record), content_type="application/json")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Billing record created successfully", data["message"])
        self.assertIsNotNone(data["id"])
        # Store the inserted ID for later use
        self.billing_record["_id"] = ObjectId(data["id"])

    def test_create_billing_record_missing_fields(self):
        # Send a POST request to the /billing endpoint with a billing record missing required fields
        billing_record = {"customer_id": 123456}
        response = self.client.post("/billing", data=json.dumps(billing_record), content_type="application/json")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("customer_id, cost, currency, and goods are required", data["error"])

    def test_create_billing_record_empty_goods(self):
        # Send a POST request to the /billing endpoint with a billing record that has an empty goods list
        billing_record = {
            "customer_id": 123456,
            "cost": 99.99,
            "currency": "USD",
            "is_paid": False,
            "goods": []
        }
        response = self.client.post("/billing", data=json.dumps(billing_record), content_type="application/json")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("goods list cannot be empty", data["error"])

    def test_create_billing_record_invalid_types(self):
        # Send a POST request to the /billing endpoint with a billing record with invalid data types
        billing_record = {
            "customer_id": "123456",
            "cost": 99,
            "currency": 123,
            "is_paid": "false",
            "goods": "Awesome Product"
        }
        response = self.client.post("/billing", data=json.dumps(billing_record), content_type="application/json")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("customer_id must be an integer", data["error"])
        self.assertIn("cost must be a float", data["error"])
        self.assertIn("currency must be a string", data["error"])
        self.assertIn("is_paid must be a boolean", data["error"])
        self.assertIn("goods must be a list", data["error"])

    def test_update_billing_record(self):
        # Create a test billing record
        response = self.client.post("/billing", data=json.dumps(self.billing_record), content_type="application/json")
        data = json.loads(response.data)
        # Send a PUT request to the /billing/{id} endpoint with the updated billing record
        updated_billing_record = {
            "customer_id": 987}

