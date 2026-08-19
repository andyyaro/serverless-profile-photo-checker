FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python script
COPY interact.py .

# Copy test images
COPY goodphoto.jpeg .
COPY badphoto.png .

# Set the entry point
ENTRYPOINT ["python", "interact.py"]
