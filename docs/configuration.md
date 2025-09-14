# Конфигурация

## Файл конфигурации

Конфигурация приложения осуществляется через файл `.env` и класс `Settings` в модуле `infrastructure.config.settings`.

## Переменные окружения

### База данных (MongoDB)

- `MONGODB_CONNECTION_STRING` - строка подключения к MongoDB (по умолчанию: `mongodb://localhost:27017`)
- `MONGODB_DATABASE_NAME` - имя базы данных (по умолчанию: `category_service`)

### Брокер сообщений (RabbitMQ)

- `RABBITMQ_URL` - URL подключения к RabbitMQ (по умолчанию: `amqp://guest:guest@localhost:5672/`)
- `RABBITMQ_EXCHANGE_NAME` - имя exchange для публикации событий (по умолчанию: `category_events`)

### Кэш (Redis)

- `REDIS_HOST` - хост Redis (по умолчанию: `localhost`)
- `REDIS_PORT` - порт Redis (по умолчанию: `6379`)
- `REDIS_DB` - номер базы данных Redis (по умолчанию: `0`)

### Приложение

- `APP_NAME` - имя приложения (по умолчанию: `Category Service`)
- `DEBUG` - режим отладки (по умолчанию: `False`)

## Docker Compose

Конфигурация сервисов в Docker Compose определена в файле `docker-compose.yml`. Включает:

- `category-service` - основной сервис приложения
- `mongodb` - база данных MongoDB
- `rabbitmq` - брокер сообщений RabbitMQ
- `redis` - кэш Redis

## Проверка состояния сервисов

Docker Compose включает проверки состояния для всех сервисов:

- MongoDB: проверка возможности подключения через mongosh
- RabbitMQ: проверка статуса через rabbitmqctl
- Redis: проверка через команду ping