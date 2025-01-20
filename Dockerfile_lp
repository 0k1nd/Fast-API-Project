FROM python:3.10-slim

WORKDIR /line_provider

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["sh", "-c", "while ! nc -z db2 5432; do sleep 1; done; uvicorn line_provider.main:app --host 0.0.0.0 --port 8001 --reload"]

