# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir celery redis smtplib

# Define environment variable
ENV CELERY_BROKER_URL=redis://redis:6379/0

# Run Celery worker when the container launches
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
