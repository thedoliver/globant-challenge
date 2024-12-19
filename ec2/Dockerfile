# Use the official Python 3.9 image as the base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only necessary files to the container's working directory
COPY requirements.txt /app/
COPY app /app/

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Specify the entry point for the script
ENTRYPOINT ["python", "/app/EC2_remove_SSM_policy.py"]

