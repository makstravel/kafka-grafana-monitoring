FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./producer/producer.py .
COPY ./producer/kafka_producer_client.py .

CMD ["python", "producer.py"]
