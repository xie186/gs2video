FROM python:3.12.9-slim

WORKDIR /app

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser -m appuser

# Install system dependencies required for moviepy and other packages
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
#COPY slides_to_video.py .

# Create a directory for credentials
#RUN mkdir -p /app/credentials

# Set environment variables for credentials if needed
#ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/credentials.json

# Create volume mount points for credentials and output
#VOLUME ["/app/credentials", "/app/output"]


# Set correct ownership of the application directory
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Set working directory as the default output location
WORKDIR /app/


