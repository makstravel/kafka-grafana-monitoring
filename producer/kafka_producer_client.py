from confluent_kafka import Producer
import json


class KafkaProducerClient:
    def __init__(self, bootstrap_servers: str):
        self.producer = Producer({
            'bootstrap.servers': bootstrap_servers
        })

    def delivery_report(self, err, msg):
        """Вызывается при подтверждении отправки сообщения брокером."""
        if err is not None:
            print(f"Ошибка при доставке сообщения: {err}")
        else:
            print(f"Сообщение доставлено, Partition: {msg.partition()}, Offset: {msg.offset()}")

    def send(self, topic: str, message: dict):
        """Сериализуем в JSON и отправляем."""
        data = json.dumps(message).encode('utf-8')
        self.producer.poll(0)
        self.producer.produce(topic, data, callback=self.delivery_report)
        self.producer.flush()
