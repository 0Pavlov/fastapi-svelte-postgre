# Use an official Python image
FROM python:3.11-slim

# Working directory inside the container
WORKDIR /app

# Copy the requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Expose the port
EXPOSE 8000

# Run the dev mode
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
