#!/bin/bash
echo "Building EBAD API Docker image..."
docker build -t ebad-api:latest .

echo "Starting EBAD API container..."
docker run -d \
  --name ebad-api-container \
  -p 8000:8000 \
  --env-file .env \
  --restart unless-stopped \
  ebad-api:latest

echo "EBAD API deployed successfully!"
echo "Access the API at: http://localhost:8000"
echo "View documentation at: http://localhost:8000/docs"
