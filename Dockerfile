# Start from an official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (for psycopg2)
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Ensure config.json exists (copy from example if missing)
RUN if [ ! -f config.json ]; then cp config.json.example config.json; fi

# Expose the port (default FastAPI/Uvicorn port)
EXPOSE 3000

# Start the server using uvicorn
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "3000"]
