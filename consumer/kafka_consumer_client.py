from confluent_kafka import Consumer

class KafkaConsumerClient:
    def __init__(self, bootstrap_servers: str, group_id: str, topics: list, on_message):
        self.on_message = on_message
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })
        self.topics = topics

    def start_listening(self):
        self.consumer.subscribe(self.topics)
        print(f"Подписались на топики: {self.topics}")
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    print(f"Ошибка потребителя: {msg.error()}")
                    continue
                self.on_message(msg)
        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()
