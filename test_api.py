import json
import pytest
from api import app, receipts

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_valid_receipt(client):
    # Check the validity of receipt, output id if valid
    receipt_data = {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [
            { "shortDescription": "Gatorade", "price": "2.25" },
            { "shortDescription": "Gatorade", "price": "2.25" },
            { "shortDescription": "Gatorade", "price": "2.25" },
            { "shortDescription": "Gatorade", "price": "2.25" }
        ],
        "total": "9.00"
    }
    response = client.post('/receipts/process', data=json.dumps(receipt_data), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert "id" in data

def test_get_points(client):
    # First, process a valid receipt to get an ID, then check for points
    receipt_data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            { "shortDescription": "Mountain Dew 12PK", "price": "6.49" },
            { "shortDescription": "Emils Cheese Pizza", "price": "12.25" },
            { "shortDescription": "Knorr Creamy Chicken", "price": "1.26" },
            { "shortDescription": "Doritos Nacho Cheese", "price": "3.35" },
            { "shortDescription": "Klarbrunn 12-PK 12 FL OZ", "price": "12.00" }
        ],
        "total": "35.35"
    }
    process_response = client.post('/receipts/process', data=json.dumps(receipt_data), content_type='application/json')
    data = process_response.get_json()
    receipt_id = data["id"]

    points_response = client.get(f'/receipts/{receipt_id}/points')
    assert points_response.status_code == 200
    points_data = points_response.get_json()
    assert "points" in points_data

def test_receipt_invalid(client):
    # Test missing required field ('retailer' is missing)
    receipt_data = {
        # "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [{ "shortDescription": "Item", "price": "1.00" }],
        "total": "10.00"
    }
    response = client.post('/receipts/process', data=json.dumps(receipt_data), content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_receipt_not_found(client):
    # Test retrieval of points with a non-existent receipt ID
    response = client.get('/receipts/non-existent-id/points')
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "No receipt found for that ID."
