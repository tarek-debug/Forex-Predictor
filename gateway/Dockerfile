# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Define environment variables for service URLs
ENV PREDICTION_SERVICE_URL=http://localhost:5002
ENV DATA_STORAGE_SERVICE_URL=http://localhost:5003

# Run gateway_api.py when the container launches
CMD ["python", "gateway_api.py"]
