# Multi-stage build for Python application

# Build stage
FROM python:3.12-slim as builder

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies to local directory
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.12-slim as production

WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Add src to Python path
ENV PYTHONPATH=/app/src:$PYTHONPATH

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "src/main.py"]