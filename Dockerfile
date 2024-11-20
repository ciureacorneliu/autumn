# Use a base image with Python installed
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY app.py /app/

# Install Flask
RUN pip install flask flask-cors

# Expose the port Flask will run on
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]
