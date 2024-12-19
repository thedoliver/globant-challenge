# Use the official Python 3.9 image as the base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory's content to the container's working directory
COPY . /app

# Install required Python packages
RUN pip install -r requirements.txt

# Specify the entry point for the script
ENTRYPOINT ["python", "EC2_remove_SSM_policy.py"]
