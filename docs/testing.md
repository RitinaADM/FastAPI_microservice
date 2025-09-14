# Тестирование

## Типы тестов

### Модульные тесты

Модульные тесты проверяют отдельные компоненты приложения в изоляции.

**Запуск модульных тестов локально:**
```bash
python -m pytest tests/unit
```

**Запуск модульных тестов в Docker:**
```bash
make test-unit
# или
docker-compose run --rm test-runner python -m pytest tests/unit/ -v
```

### Интеграционные тесты

Интеграционные тесты проверяют взаимодействие между компонентами и внешними системами.

**Запуск интеграционных тестов локально:**
```bash
python -m pytest tests/integration
```

**Запуск интеграционных тестов в Docker:**
```bash
make test-integration
# или
docker-compose run --rm test-runner python -m pytest tests/integration/ -v
```

### Запуск всех тестов

**Запуск всех тестов локально:**
```bash
python -m pytest
```

**Запуск всех тестов в Docker:**
```bash
make test
# или
docker-compose run --rm test-runner
```

## Покрытие кода

Для измерения покрытия кода тестами можно использовать следующую команду:

**Локально:**
```bash
python -m pytest --cov=.
```

**В Docker:**
```bash
make test-coverage
# или
docker-compose run --rm test-runner python -m pytest tests/ --cov=src/ --cov-report=html --cov-report=term
```

## Форматирование кода

Для форматирования кода используется Black:

```bash
black .
```

## Проверка кода

Для проверки кода на соответствие стандартам используется Flake8:

```bash
flake8 .
```

## Аннотации типов

Для проверки аннотаций типов используется MyPy:

```bash
mypy .
```

## Контейнеризация тестов

Для удобного запуска тестов в изолированной среде мы используем Docker. Это обеспечивает:

1. Единообразную среду выполнения тестов
2. Автоматическую установку всех зависимостей
3. Изоляцию от локальной среды разработки
4. Возможность запуска тестов в CI/CD пайплайнах

### Docker-образы

- `Dockerfile` - основной образ приложения
- `Dockerfile.test` - образ для запуска тестов (включает dev-зависимости)

### Docker Compose сервисы

- `category-service` - основной сервис приложения
- `test-runner` - сервис для запуска тестов
- `mongodb` - база данных MongoDB
- `rabbitmq` - брокер сообщений RabbitMQ
- `redis` - хранилище ключ-значение Redis

### Makefile команды

Для удобного управления тестами мы предоставляем Makefile с командами:

```bash
make test              # Запустить все тесты
make test-unit         # Запустить unit-тесты
make test-integration  # Запустить интеграционные тесты
make test-coverage     # Запустить тесты с измерением покрытия
make up               # Запустить все сервисы
make down             # Остановить все сервисы
```