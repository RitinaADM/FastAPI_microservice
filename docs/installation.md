# Установка и запуск

## Системные требования

- Python 3.12
- Docker (опционально, для контейнеризированного развертывания)
- Docker Compose (опционально, для контейнеризированного развертывания)

## Установка зависимостей

### Использование pip

1. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Для разработки также установите зависимости для разработки:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Запуск приложения

### Локальный запуск

1. Активируйте виртуальное окружение:
   ```bash
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   ```

2. Запустите приложение:
   ```bash
   python main.py
   ```

### Запуск с помощью Docker

1. Соберите и запустите с помощью Docker Compose:
   ```bash
   docker-compose up --build
   ```

2. Остановите сервисы:
   ```bash
   docker-compose down
   ```

## Переменные окружения

Приложение использует файл `.env` для конфигурации. Основные переменные:

- `MONGODB_CONNECTION_STRING` - строка подключения к MongoDB
- `MONGODB_DATABASE_NAME` - имя базы данных MongoDB
- `RABBITMQ_URL` - URL подключения к RabbitMQ
- `RABBITMQ_EXCHANGE_NAME` - имя exchange в RabbitMQ
- `REDIS_HOST` - хост Redis
- `REDIS_PORT` - порт Redis
- `REDIS_DB` - номер базы данных Redis
- `APP_NAME` - имя приложения
- `DEBUG` - режим отладки

## Проверка работы

После запуска приложение будет доступно по адресу: http://localhost:8000

Документация API доступна по адресу: http://localhost:8000/docs