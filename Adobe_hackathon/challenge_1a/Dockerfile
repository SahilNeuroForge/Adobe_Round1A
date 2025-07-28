# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code and the input files into the container
COPY . .

# Create a directory for the output files
RUN mkdir ./output

# Define the command to run the application
CMD ["python", "app/main.py"]