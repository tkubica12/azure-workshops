# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Create a non-root user
RUN useradd -m appuser

# Set the working directory in the container
WORKDIR /home/appuser

# Copy the Python script and any other necessary files into the container
COPY . .

# Install any needed packages specified in a requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Switch to the non-root user
USER appuser

# Set the default command to run the Python program
CMD ["python", "main.py"]