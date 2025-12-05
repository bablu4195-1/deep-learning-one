FROM python:3.13-slim

# Install system libraries needed by Pillow‑HEIF (libheif dependencies)
RUN apt-get update && apt-get install -y libglib2.0-0 libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

# Create a non‑root user for security
RUN useradd -m appuser
WORKDIR /app
USER appuser

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI will listen on (DigitalOcean injects $PORT at runtime)
EXPOSE 8000

# Start the app – DigitalOcean will override the port via $PORT if needed
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
