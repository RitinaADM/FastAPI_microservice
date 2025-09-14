# Category Service

Микросервис для управления категориями, реализованный по паттерну гексагональной архитектуры.

## Документация

Полная документация доступна в директории [docs](docs/):

- [Архитектура](docs/architecture.md)
- [Руководство по разработке](docs/development.md)
- [Установка и запуск](docs/installation.md)
- [API документация](docs/api.md)
- [Тестирование](docs/testing.md)
- [Конфигурация](docs/configuration.md)
- [Развертывание](docs/deployment.md)

## Архитектура

Этот сервис следует паттерну гексагональной архитектуры (портов и адаптеров) с четким разделением ответственностей:

```
[REST API (Pydantic schema)]
      |
      v
[Inbound Adapter]
      |
      v
[Mapper: Pydantic -> Internal DTO]
      |
      v
[Application Layer / Use Case]
      |
      v
[Mapper: Internal DTO -> Domain Entities]
      |
      v
[Domain Entities + Domain Services]
      |
      v
[Mapper: Domain Entities -> Internal DTO]
      |
      v
[Outbound Adapter]
      |
      v
[External DTO (Pydantic / Kafka schema)]
```

### Слои

1. **Доменный слой**: Содержит основную бизнес-логику, сущности, объекты-значения, события и порты
2. **Слой приложения**: Содержит сценарии использования, которые координируют доменную логику
3. **Инфраструктурный слой**: Содержит адаптеры для внешних систем (REST API, база данных, шина сообщений)

## Структура проекта

```
category-service/
│
├── domain/
│   ├── entities/
│   │   └── category.py
│   ├── value_objects/
│   │   └── category_id.py
│   ├── services/
│   │   └── category_service.py
│   ├── events/
│   │   └── category_events.py
│   ├── ports/
│   │   ├── inbound/
│   │   │   └── category_input_port.py
│   │   └── outbound/
│   │       ├── category_repository.py
│   │       └── category_event_publisher.py
│   └── exceptions/
│       └── category_exceptions.py
│
├── application/
│   ├── use_cases/
│   │   └── category_use_case.py
│   └── dtos/
│       ├── category_dto.py
│       ├── create_category_dto.py
│       └── update_category_dto.py
│
├── infrastructure/
│   ├── adapters/
│   │   ├── inbound/
│   │   │   └── rest/
│   │   │       ├── category_controller.py
│   │   │       └── schemas/
│   │   │           ├── category_schemas.py
│   │   │           └── category_response.py
│   │   └── outbound/
│   │       ├── database/
│   │       │   └── mongodb/
│   │       │       └── category_repository_impl.py
│   │       ├── message_bus/
│   │       │   └── rabbitmq_publisher.py
│   │       └── cache/
│   │           └── redis_adapter.py
│   │
│   ├── mappers/
│   │   └── category_mappers.py
│   │
│   ├── di/
│   │   ├── containers.py
│   │   └── providers.py
│   │
│   └── config/
│       └── settings.py
│
├── tests/
│   ├── unit/
│   │   └── test_category_use_case.py
│   └── integration/
│   │   └── test_category_api.py
│
├── docs/
│   ├── index.md
│   ├── architecture.md
│   ├── development.md
│   ├── installation.md
│   ├── api.md
│   ├── testing.md
│   ├── configuration.md
│   └── deployment.md
│
├── src/
│   └── main.py
├── Dockerfile
├── Dockerfile.test
├── docker-compose.yml
├── Makefile
├── .env
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml
```

## Основные технологии

- **Python 3.12**: Язык программирования
- **FastAPI**: Веб-фреймворк для создания API
- **Pydantic**: Валидация данных и управление настройками
- **MongoDB**: База данных для постоянного хранения
- **Redis**: Кэширование данных
- **RabbitMQ**: Брокер сообщений для публикации событий
- **Docker**: Платформа контейнеризации
- **Dishka 1.6**: Фреймворк для внедрения зависимостей

## Начало работы

### Системные требования

- Python 3.12
- Docker (опционально, для контейнеризированного развертывания)

### Установка

1. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите приложение:
   ```bash
   python src/main.py
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

### Запуск тестов в Docker

Для удобного запуска тестов в Docker мы предоставляем Makefile с несколькими командами:

1. Запустить все тесты:
   ```bash
   make test
   ```

2. Запустить только unit-тесты:
   ```bash
   make test-unit
   ```

3. Запустить только интеграционные тесты:
   ```bash
   make test-integration
   ```

4. Запустить тесты с измерением покрытия кода:
   ```bash
   make test-coverage
   ```

Также можно запустить тесты напрямую через docker-compose:
```bash
docker-compose run --rm test-runner
```

## Эндпоинты API

- `POST /categories/` - Создать новую категорию
- `GET /categories/{id}` - Получить категорию по ID
- `GET /categories/` - Получить все категории
- `PUT /categories/{id}` - Обновить категорию
- `DELETE /categories/{id}` - Удалить категорию
- `GET /categories/statistics` - Получить статистику по категориям

## Лицензия

MIT