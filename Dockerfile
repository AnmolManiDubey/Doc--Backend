# ---------- Stage 1: Build dependencies ----------
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build tools (for numpy, sentence-transformers etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements and install into /app/venv
COPY requirements.txt .
RUN python -m venv /app/venv
RUN /app/venv/bin/pip install -r requirements.txt

# Pre-download sentence-transformers model into cache
RUN mkdir -p /app/cache && chmod -R 777 /app/cache
ENV TRANSFORMERS_CACHE=/app/cache
ENV HF_HOME=/app/cache
ENV TORCH_HOME=/app/cache
RUN /app/venv/bin/python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# ---------- Stage 2: Runtime ----------
FROM python:3.12-slim

WORKDIR /app

# Copy virtualenv from builder stage
COPY --from=builder /app/venv /app/venv

# Copy pre-downloaded model cache
COPY --from=builder /app/cache /app/cache

# Copy application code
COPY . .

# Set environment variables
ENV TRANSFORMERS_CACHE=/app/cache
ENV HF_HOME=/app/cache
ENV TORCH_HOME=/app/cache
ENV PATH="/app/venv/bin:$PATH"

# (Optional) create non-root user and switch
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
USER appuser

# Expose port for HF Spaces
EXPOSE 7860

# Start FastAPI using uvicorn
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "7860"]
