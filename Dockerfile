FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y libpq5 && rm -rf /var/lib/apt/lists/*
# Copy project files and source
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install dependencies from pyproject.toml
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Environment variables with defaults
ENV DB_HOST=db
ENV DB_PORT=5432
ENV DB_NAME=supermarkt_db
ENV DB_USER=postgres
ENV DB_PASSWORD=supermarkt123
ENV PORT=8000

EXPOSE 8000

CMD ["python", "src/server_sse.py"]
