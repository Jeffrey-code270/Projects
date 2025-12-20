FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"

# Copy application code
COPY . .
RUN mkdir -p logs && chown -R app:app /app

# Switch to non-root user
USER app

# Health check
HEALTHCHECK --interval=60s --timeout=30s --start-period=5s --retries=3 \
    CMD python app/health_check.py

EXPOSE 8000

CMD ["python", "app/process_pdfs.py"]