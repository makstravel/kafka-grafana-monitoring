import json
from datetime import datetime
from kafka_consumer_client import KafkaConsumerClient
from database_service import DatabaseService

class MessageHandler:
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service

    def handle_message(self, message: dict):
        """
        Основная логика обработки сообщения:
        - Берём created_at, parameter_name, value из входного сообщения,
        - Фиксируем текущее время ts_now,
        - Сохраняем в базу данных.
        """
        try:
            created_at = message["created_at"]
            parameter_name = message["parameter_name"]
            value = message["value"]
            ts_now = datetime.utcnow().isoformat()

            # Записываем в БД
            self.db_service.insert_record(
                created_at=created_at,
                parameter_name=parameter_name,
                value=value,
                ts_now=ts_now
            )
        except KeyError as e:
            # Обработка ошибки, если в сообщении нет нужного поля
            print(f"Ошибка в структуре сообщения: отсутствует поле {e}")

def on_receive_message(db_service: DatabaseService, raw_msg):
    """Callback для обработки "сырого" сообщения"""
    if raw_msg is None:
        return
    data = json.loads(raw_msg.value())
    handler = MessageHandler(db_service)
    handler.handle_message(data)

if __name__ == "__main__":
    # Настраиваем подключения
    db_service = DatabaseService(
        host='postgres',
        port=5432,
        dbname='kafka_demo',
        user='postgres',
        password='postgres'
    )

    consumer_client = KafkaConsumerClient(
        bootstrap_servers="kafka:9092",
        group_id="sensor_group",
        topics=["sensor_data"],
        on_message=lambda msg: on_receive_message(db_service, msg)
    )

    consumer_client.start_listening()
