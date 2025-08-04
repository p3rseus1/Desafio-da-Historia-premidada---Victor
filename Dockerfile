# Use official Python image
FROM python:3.11-slim

# Argumentos de build para proxy
ARG PROXY

# Set working directory
WORKDIR /app

# Copy application files
COPY main.py requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run the application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]