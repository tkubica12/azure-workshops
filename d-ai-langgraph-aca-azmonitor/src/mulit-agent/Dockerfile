# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Set environment variables (optional, uncomment if needed)
# ENV PYTHONUNBUFFERED=1

# Run Streamlit app
CMD ["streamlit", "run", "webapp.py", "--server.port=8501", "--server.address=0.0.0.0"]
