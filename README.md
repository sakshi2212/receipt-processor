# Fetch Receipt Processor Challenge

**Language Selection:** Python (Flask)

A Flask-based web service that processes receipts and calculates points based on a set of rules. This project includes a simple front-end (via `templates/index.html`) for uploading a JSON receipt and displaying the unique receipt ID and calculated points.

---

## Project Overview

The service provides two main API endpoints:

1. **Process Receipt**  
   - **Endpoint:** `/receipts/process`
   - **Method:** `POST`
   - **Input:** A JSON receipt
   - **Output:** A JSON object containing a unique receipt ID

2. **Get Points**  
   - **Endpoint:** `/receipts/{id}/points`
   - **Method:** `GET`
   - **Output:** A JSON object containing the number of points awarded

The front-end located in `templates/index.html` allows users to upload a JSON file representing the receipt, then displays the unique ID and points awarded by the service.

---

## Files Description

- **Dockerfile:**  
  Docker configuration to containerize the application.

- **api.py:**  
  The main Flask application that defines the API endpoints and handles receipt processing and point calculation.

- **requirements.txt:**  
  Lists all Python dependencies required to run the application.

- **templates/index.html:**  
  The front-end page that accepts a JSON receipt file and displays the unique ID and points returned from the API.

- **test_api.py:**  
  Contains automated tests (using pytest) to verify the API’s functionality and ensure compliance with the specification.

---

## API Input and Output

### Process Receipt

- **URL:** `/receipts/process`
- **Method:** `POST`
- **Input Example:**

  ```json
  {
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
      { "shortDescription": "Mountain Dew 12PK", "price": "6.49" },
      { "shortDescription": "Emils Cheese Pizza", "price": "12.25" }
    ],
    "total": "35.35"
  }

- **Output Example:**

   ```json
   { "id": "7fb1377b-b223-49d9-a31a-5a02701dd310" }

### Get Points

- **URL:** `/receipts/{id}/points`
- **Method:** `GET`
- **Output Example:**
  
  ```json
  { "points": 28 }

---

## Point Calculation Rules

Points for each receipt are calculated based on the following rules:

- Award **1 point** for every alphanumeric character in the `retailer` name.
- Add **50 points** if the `total` is a round dollar amount with no cents.
- Add **25 points** if the `total` is a multiple of 0.25.
- Award **5 points** for every two `items` on the receipt.
- For each item, if the trimmed length of `shortDescription` is a multiple of 3, multiply the item price by 0.2, round up to the nearest integer, and add that many points.
- Add **6 points** if the day (from `purchaseDate`) is odd.
- Add **10 points** if the `purchaseTime` is after 2:00 PM and before 4:00 PM.

---

## Important Notes

### Data Persistence
- All receipt data and calculated points are stored in memory. Restarting the application will reset this data.

### Front-End Interaction
- The front-end (`templates/index.html`) takes a JSON receipt as input and displays both the unique receipt ID and the corresponding points awarded.

---

## Running the Application with Docker

Follow these steps to run the application using Docker:

```bash
git clone https://github.com/sakshi2212/receipt-processor.git

docker build -t receipt-processor .

docker run -p 5000:5000 receipt-processor
```
The service will be accessible at http://localhost:5000.

---

## Example Curl Requests

### Process a Receipt

To process a receipt, use the following curl command:

```bash
curl -X POST http://localhost:5000/receipts/process \
     -H "Content-Type: application/json" \
     -d '{
           "retailer": "Target",
           "purchaseDate": "2022-01-01",
           "purchaseTime": "13:01",
           "items": [
             { "shortDescription": "Mountain Dew 12PK", "price": "6.49" },
             { "shortDescription": "Emils Cheese Pizza", "price": "12.25" }
           ],
           "total": "35.35"
         }'
```

### Get Points 

After processing a receipt, use the returned receipt ID to retrieve the points:

```bash
curl http://localhost:5000/receipts/<receipt_id>/points
```


  
