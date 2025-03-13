#!/bin/bash

# Stop and remove existing container if it exists
echo "Stopping and removing existing container..."
docker rm -f bookworks-container 2>/dev/null || true

# Remove existing image
echo "Removing existing image..."
docker rmi bookworks 2>/dev/null || true

# Build new image
echo "Building new image..."
docker build -t bookworks .

# Run new container
echo "Starting new container..."
docker run -d -p 5001:5000 --name bookworks-container bookworks

echo "Done! Application should be available at http://localhost:5001"