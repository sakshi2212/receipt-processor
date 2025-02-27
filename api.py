from flask import Flask, request, jsonify, render_template
import uuid
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

receipts = {}

# Function to generate ID
def generate_id():
    return str(uuid.uuid4())

# Function to calculate points
def calculate_points(receipt):
    points = 0

    # One point for every alphanumeric character in the retailer name.
    points += sum(c.isalnum() for c in receipt['retailer'])
    
    total = float(receipt['total'])
    
    # 50 points if the total is a round dollar amount with no cents.
    if total.is_integer():
        points += 50
        
    # 25 points if the total is a multiple of 0.25.
    if total % 0.25 == 0:
        points += 25

    # 5 points for every two items on the receipt.
    items = receipt['items']
    points += (len(items) // 2) * 5
    
    # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    for item in items:
        description_len = len(item['shortDescription'].strip())
        if description_len % 3 == 0:
            item_points = math.ceil(float(item['price']) * 0.2)
            points += item_points
    
    # 6 points if the day in the purchase date is odd.
    day = int(receipt['purchaseDate'].split('-')[-1])
    if day % 2 == 1:
        points += 6
    
    # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    time = int(receipt['purchaseTime'].split(':')[0])
    if 14 <= time < 16:
        points += 10
    
    return points

# Function to process receipt and generate ID
@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    try:
        receipt = request.json
        receipt_id = generate_id()
        receipts[receipt_id] = {
            "receipt": receipt,
            "points": calculate_points(receipt)
        }
        return jsonify({"id": receipt_id}), 200
    except Exception as e:
        return jsonify({"error": "The receipt is invalid."}), 400

# Function to get points for a particular ID
@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    if receipt_id in receipts:
        return jsonify({"points": receipts[receipt_id]['points']})
    else:
        return jsonify({"error": "No receipt found for that ID."}), 404

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

