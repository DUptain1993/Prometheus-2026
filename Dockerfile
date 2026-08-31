FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Create necessary directories
RUN mkdir -p output logs config

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PROMETHEUS_CONFIG=/app/config/config.json

# Expose the API port
EXPOSE 5000

# Run the application
CMD ["python", "-m", "api.routes"]
