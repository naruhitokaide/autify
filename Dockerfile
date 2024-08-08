# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir requests beautifulsoup4

# Make fetch.py executable
RUN chmod +x fetch.py

# Run fetch.py when the container launches
ENTRYPOINT ["python", "./fetch.py"]
