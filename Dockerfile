# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /receipt-processor

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 5000

# Run the Flask application
CMD ["python", "api.py"]
