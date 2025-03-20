FROM python:3.9-slim

WORKDIR /app

# requirements.txt лежит в корне
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы из папки consumer/
COPY ./consumer/consumer.py .
COPY ./consumer/kafka_consumer_client.py .
COPY ./consumer/database_service.py .

CMD ["python", "consumer.py"]
