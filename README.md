📊 Kafka + PostgreSQL + Grafana Monitoring

📝 Описание проекта

Этот проект реализует сбор, хранение и визуализацию данных, поступающих из Kafka. Данные записываются в PostgreSQL, а затем отображаются в Grafana в виде графиков.

🏗 Компоненты проекта:

Kafka – брокер сообщений

PostgreSQL – база данных для хранения данных

Grafana – визуализация данных

Producer – отправляет данные в Kafka

Consumer – читает данные из Kafka и записывает их в PostgreSQL

🚀 Запуск проекта

1️⃣ Клонируйте репозиторий
```
git clone https://github.com/makstravel/kafka-grafana-monitoring.git
```

```
cd kafka-grafana-monitoring
```

2️⃣ Запустите контейнеры с помощью Docker Compose

```
docker-compose up -d --build
```

3️⃣ Проверка работы сервисов

📌 Проверить запущенные контейнеры:

```
docker ps
```

Ожидаемый список:

IMAGE                           
kafka-grafana-monitoring_consumer           
kafka-grafana-monitoring_producer              
confluentinc/cp-kafka:latest   
confluentinc/cp-zookeeper:latest 
postgres:14                      
grafana/grafana:latest        

4️⃣ Проверка Kafka

📌 Просмотреть список топиков в Kafka:

```
docker exec -it kafka kafka-topics --bootstrap-server kafka:9092 --list
```

Ожидаемый результат:


__consumer_offsets
sensor_data


📌 Протестировать отправку данных в Kafka:
```
echo '{"created_at": "2025-03-19T21:00:00Z", "parameter_name": "temperature", "value": 23.5}' | docker exec -i producer python producer.py
```

📌 Прослушать сообщения из Kafka:
```
docker exec -it kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic test_topic --from-beginning
```
5️⃣ Проверка PostgreSQL

📌 Зайти в PostgreSQL и проверить данные:
```
docker exec -it postgres psql -U postgres -d kafka_demo -c "SELECT * FROM sensor_readings LIMIT 10;"
```

6️⃣ Настройка Grafana

Откройте Grafana в браузере: http://localhost:3000

Войдите (по умолчанию admin / admin)

Перейдите в Connections → Data Sources

Добавьте PostgreSQL в качестве источника данных:

Host: postgres:5432

Database: kafka_demo

User: postgres

Password: postgres

SSL Mode: disable

🔧 Полезные команды

📌 Остановить и удалить контейнеры:
```
docker-compose down
```
📌 Пересобрать контейнеры и перезапустить:
```
docker-compose up -d --build
```

📌 Посмотреть логи продюсера Kafka:
```
docker logs -f producer
```

📌 Посмотреть логи потребителя Kafka:
```
docker logs -f consumer
```
📌 Проверить содержимое таблицы:
```
docker exec -it postgres psql -U postgres -d kafka_demo -c "SELECT * FROM sensor_readings;"
```
📷 Скриншоты дашбордов


