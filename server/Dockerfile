FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY server.py .

# Expose port
EXPOSE 8765

# Set environment variable for port
ENV PORT=8765

# Run the server
CMD ["python", "server.py"]
