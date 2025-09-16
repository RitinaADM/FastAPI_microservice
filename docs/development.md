# Руководство по разработке

## Структура проекта

```
ritina_app/
├── src/
│   ├── application/         # Слой приложения
│   │   ├── dtos/            # Объекты передачи данных
│   │   └── use_cases/       # Сценарии использования
│   ├── domain/              # Доменный слой
│   │   ├── entities/        # Сущности
│   │   ├── value_objects/   # Объекты-значения
│   │   ├── services/        # Доменные сервисы
│   │   ├── ports/           # Порты
│   │   │   ├── inbound/     # Входящие порты
│   │   │   └── outbound/    # Исходящие порты
│   │   └── exceptions/      # Исключения
│   └── infrastructure/      # Инфраструктурный слой
│       ├── adapters/        # Адаптеры
│       │   ├── inbound/     # Входящие адаптеры
│       │   └── outbound/    # Исходящие адаптеры
│       ├── config/          # Конфигурация
│       ├── di/              # Внедрение зависимостей
│       └── mappers/         # Мапперы
├── tests/                   # Тесты
│   ├── unit/                # Модульные тесты
│   └── integration/         # Интеграционные тесты
├── docs/                    # Документация
├── Dockerfile               # Docker-образ приложения
├── docker-compose.yml       # Оркестрация Docker-контейнеров
├── requirements.txt         # Зависимости проекта
└── main.py                  # Точка входа в приложение
```

## Роль доменных сервисов

Доменные сервисы содержат сложную бизнес-логику, которая не помещается в сущности. Вот когда стоит использовать доменные сервисы:

1. **Сложные вычисления**: Когда бизнес-логика требует сложных вычислений, которые не являются естественной частью сущностей
2. **Бизнес-правила, затрагивающие несколько сущностей**: Когда правило бизнес-логики затрагивает несколько сущностей
3. **Алгоритмы**: Когда необходимо реализовать алгоритмы, которые оперируют сущностями

Пример доменного сервиса:

```python
# src/domain/services/category_service.py
class CategoryService:
    """Пример доменного сервиса для работы с категориями"""
    
    def calculate_category_statistics(self, categories: List[Category]) -> Dict[str, Any]:
        """Вычисляет статистику по категориям"""
        # Сложная бизнес-логика вычисления статистики
        pass
    
    def validate_category_hierarchy(self, category: Category, parent_category: Category) -> bool:
        """Проверяет корректность иерархии категорий"""
        # Бизнес-логика проверки иерархии
        pass
```

В текущем проекте [CategoryService](file:///c:/Users/dev/Documents/ritina_app/src/domain/services/category_service.py#L6-L17) уже содержит методы для валидации категорий и проверки возможности удаления категории.

## Различие между сценариями использования и доменными сервисами

### Сценарии использования (Use Cases)

Сценарии использования находятся в слое приложения и отвечают за координацию выполнения бизнес-логики:

- Получают данные из внешних источников (через порты)
- Вызывают доменные сервисы для выполнения бизнес-логики
- Сохраняют результаты через порты
- Публикуют события при необходимости

Пример: [CategoryUseCase](file:///c:/Users/dev/Documents/ritina_app/src/application/use_cases/category_use_case.py#L11-L130) координирует создание категории, вызывая валидацию в [CategoryService](file:///c:/Users/dev/Documents/ritina_app/src/domain/services/category_service.py#L6-L17), сохраняя данные через [CategoryRepository](file:///c:/Users/dev/Documents/ritina_app/src/domain/ports/outbound/category_repository.py#L6-L26) и публикуя события через [CategoryEventPublisher](file:///c:/Users/dev/Documents/ritina_app/src/domain/ports/outbound/category_event_publisher.py#L6-L17).

### Доменные сервисы (Domain Services)

Доменные сервисы находятся в доменном слое и содержат чистую бизнес-логику:

- Не зависят от внешних систем
- Работают только с сущностями и объектами-значениями
- Могут вызываться из сценариев использования

## Добавление нового функционала

### 1. Определение требований

Перед началом разработки определите:
- Какие сущности нужно создать или изменить
- Какие порты необходимы
- Какая бизнес-логика требуется
- Нужно ли создавать доменный сервис

### 2. Реализация доменного слоя

#### Создание сущностей
```python
# src/domain/entities/example.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Example:
    id: Optional[str]
    name: str
    # другие поля
```

#### Создание объектов-значений
```python
# src/domain/value_objects/example_id.py
import uuid
from dataclasses import dataclass

@dataclass(frozen=True)
class ExampleId:
    value: str
    
    @classmethod
    def new(cls):
        return cls(str(uuid.uuid4()))
```

#### Создание исключений
```python
# src/domain/exceptions/example_exceptions.py
class ExampleNotFoundError(Exception):
    pass
```

#### Создание портов
```python
# src/domain/ports/inbound/example_input_port.py
from abc import ABC, abstractmethod

class ExampleInputPort(ABC):
    @abstractmethod
    def create_example(self, name: str) -> Example:
        pass
```

### 3. Реализация слоя приложения

#### Создание DTO
```python
# src/application/dtos/example_dto.py
from pydantic import BaseModel

class ExampleDTO(BaseModel):
    id: Optional[str]
    name: str
```

#### Создание сценариев использования
```python
# src/application/use_cases/example_use_case.py
class ExampleUseCase(ExampleInputPort):
    def __init__(self, repository: ExampleRepository, example_service: ExampleService):
        self.repository = repository
        self.example_service = example_service
    
    def create_example(self, name: str) -> Example:
        # Координация: создание, валидация, сохранение
        example = Example(id=None, name=name)
        
        # Вызов доменного сервиса для валидации
        if not self.example_service.validate_example(example):
            raise InvalidExampleError("Example validation failed")
        
        # Сохранение через порт
        return self.repository.create(example)
```

### 4. Реализация инфраструктурного слоя

#### Создание адаптеров
```python
# src/infrastructure/adapters/outbound/database/mongodb/example_repository_impl.py
class MongoExampleRepository(ExampleRepository):
    def create(self, example: Example) -> Example:
        # Реализация создания в MongoDB
        pass
```

#### Создание REST-контроллера
```python
# src/infrastructure/adapters/inbound/rest/example_controller.py
@router.post("/", response_model=ExampleResponse)
@inject
async def create_example(
    request: ExampleCreateRequest,
    use_case: FromDishka[ExampleUseCase]
):
    example = use_case.create_example(request.name)
    return ExampleResponse(id=str(example.id), name=example.name)
```

### 5. Настройка внедрения зависимостей

```python
# src/infrastructure/di/providers.py
class AdaptersProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_mongo_example_repository(self, settings: Settings) -> MongoExampleRepository:
        return MongoExampleRepository(
            connection_string=settings.mongodb_connection_string,
            database_name=settings.mongodb_database_name
        )

class InteractorProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_example_use_case(
        self,
        repository: MongoExampleRepository,
        example_service: ExampleService
    ) -> ExampleUseCase:
        return ExampleUseCase(repository, example_service)
```

### 6. Тестирование

#### Модульные тесты
```python
# tests/unit/test_example_use_case.py
class TestExampleUseCase:
    def test_create_example_success(self, use_case, mock_repository, mock_example_service):
        # Тест создания примера
        pass
```

#### Интеграционные тесты
```python
# tests/integration/test_example_api.py
class TestExampleAPI:
    def test_create_example_success(self, client):
        # Тест REST API
        pass
```

## Лучшие практики

1. **Следуйте принципам SOLID**
2. **Используйте внедрение зависимостей**
3. **Пишите тесты для всего бизнес-функционала**
4. **Соблюдайте принципы гексагональной архитектуры**
5. **Используйте типизацию для повышения надежности кода**
6. **Пишите понятную документацию**