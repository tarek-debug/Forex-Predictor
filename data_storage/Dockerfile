# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for h5py and other packages
RUN apt-get update && apt-get install -y \
    gcc \
    libhdf5-dev \
    libhdf5-103 \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5003 available to the world outside this container
EXPOSE 5003

# Define environment variable
ENV NAME World

# Run data_storage.py when the container launches
CMD ["python", "data_storage.py"]
