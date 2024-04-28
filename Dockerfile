# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables
ENV DBUser=""
ENV DBPassword=""
ENV DBServer=""
ENV DBPort=""
ENV DBName=""
ENV CreateToken=""
ENV DeleteToken=""
ENV GetToken=""

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to the outside world
EXPOSE 5000

# Run main.py when the container launches
CMD ["python", "main.py"]
