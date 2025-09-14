# Развертывание

## Подготовка к развертыванию

Перед развертыванием убедитесь, что:

1. Установлен Docker и Docker Compose
2. Все зависимости указаны в `requirements.txt`
3. Файл конфигурации `.env` содержит корректные значения

## Многоступенчатая сборка Docker

Dockerfile использует многоступенчатую сборку для уменьшения размера финального образа:

1. **Этап сборки** - устанавливает зависимости и компилирует необходимые компоненты
2. **Этап выполнения** - копирует только необходимые файлы и зависимости

## Docker Compose

Для развертывания используется Docker Compose, который запускает все необходимые сервисы:

```bash
docker-compose up -d
```

## Масштабирование

Для масштабирования сервиса можно использовать встроенные возможности Docker Compose:

```bash
docker-compose up -d --scale category-service=3
```

## Мониторинг

### RabbitMQ

RabbitMQ Management интерфейс доступен по адресу: http://localhost:15672
Учетные данные по умолчанию: guest/guest

### MongoDB

MongoDB доступна по адресу: mongodb://localhost:27017

### Redis

Redis доступен по адресу: localhost:6379

## Резервное копирование

### MongoDB

Для создания резервной копии MongoDB:

```bash
docker exec ritina_app-mongodb-1 mongodump --db category_service --out /backup
```

### Восстановление MongoDB

Для восстановления из резервной копии:

```bash
docker exec ritina_app-mongodb-1 mongorestore --db category_service /backup/category_service
```

## Обновление

Для обновления сервиса:

1. Остановите текущие сервисы:
   ```bash
   docker-compose down
   ```

2. Получите последние изменения:
   ```bash
   git pull
   ```

3. Пересоберите и запустите сервисы:
   ```bash
   docker-compose up -d --build
   ```