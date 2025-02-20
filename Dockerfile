# Use official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy files and install dependencies
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port and run app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
