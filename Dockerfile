# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies including Rust for phonetisaurus-g2p-py
RUN apt-get update && apt-get install -y \
    git \
    wget \
    unzip \
    gcc \
    g++ \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Rust (needed for phonetisaurus-g2p-py compilation)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app

# Copy requirements first for better layer caching
COPY requirements.txt requirements-production.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-production.txt

# Copy application code
COPY . .

# Create necessary directories and download resources using existing script
RUN mkdir -p data/g2p-nb data/nb_samtale download && \
    chmod +x download_resources.bash && \
    ./download_resources.bash

# Set proper ownership and permissions
RUN chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/', timeout=10)" || exit 1

# Run the application with Gunicorn
CMD ["gunicorn", "--config", "gunicorn.conf.py", "server:app"]
