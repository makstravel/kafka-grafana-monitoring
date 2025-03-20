import time
import random
from datetime import datetime
from kafka_producer_client import KafkaProducerClient

PARAMETERS = ["плотность", "давление", "температура"]

class MessageGenerator:
    def __init__(self, kafka_producer: KafkaProducerClient):
        self.kafka_producer = kafka_producer

    def generate_message(self):
        # Выбираем случайный параметр для примера
        parameter_name = random.choice(PARAMETERS)
        # Генерируем случайное значение
        value = round(random.uniform(0.0, 100.0), 2)
        # Время создания сообщения
        created_at = datetime.utcnow().isoformat()
        message = {
            "created_at": created_at,
            "parameter_name": parameter_name,
            "value": value
        }
        return message

    def start_sending(self, topic: str, interval_seconds: int = 5):
        """Отправляем сообщение каждые interval_seconds секунд."""
        while True:
            msg = self.generate_message()
            print(f"Отправка сообщения: {msg}")
            self.kafka_producer.send(topic, msg)
            time.sleep(interval_seconds)


if __name__ == "__main__":
    producer_client = KafkaProducerClient(
        bootstrap_servers="kafka:9092"
    )
    generator = MessageGenerator(producer_client)
    generator.start_sending("sensor_data", interval_seconds=5)
