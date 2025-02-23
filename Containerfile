# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY a-link.py /app/a-link.py
COPY agents /app/agents
COPY requirements.txt /app/requirements.txt

# Install the required Python packages
RUN pip install -r requirements.txt

# Set the entry point to run the application
ENTRYPOINT ["python", "a-link.py"]