# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Define environment variables
ENV FLASK_APP=./pred.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001

# Run app.py when the container launches
CMD ["flask", "run"]
