# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# Note: Ensure your requirements.txt includes Flask and any other dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5003 available to the world outside this container
EXPOSE 5003

# Define environment variable to configure Flask
ENV FLASK_APP=data_storage.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Run data_storage.py when the container launches
CMD ["flask", "run", "--port=5003"]
