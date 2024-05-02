# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /pred
WORKDIR /pred

# Copy the current directory contents into the container at /pred
COPY . /pred

# Install system dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libhdf5-dev \
    python3-dev \
    gcc \
    gfortran \
    build-essential

# Upgrade pip and install Python packages
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Make port 5002 available to the world outside this container
EXPOSE 5002

# Define environment variables
ENV FLASK_APP=./pred.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5002

# Run pred.py when the container launches
CMD ["python", "pred.py"]
