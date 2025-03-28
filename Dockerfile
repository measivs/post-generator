FROM python:3.12

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create a non-root user
RUN useradd -m django && \
    chown -R django:django /app
USER django

EXPOSE 8000

# Default command (can be overridden in compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]