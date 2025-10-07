# Use official lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn transformers torch

# Expose the FastAPI port
EXPOSE 8000

# Run the API with uvicorn
CMD ["uvicorn", "main:API", "--host", "0.0.0.0", "--port", "8000"]
