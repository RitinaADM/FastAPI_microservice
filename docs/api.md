# API документация

## Базовый URL

```
http://localhost:8000
```

## Эндпоинты

### Получить все категории

```
GET /categories/
```

**Ответ:**
```json
[
  {
    "id": "string",
    "name": "string",
    "description": "string"
  }
]
```

### Создать категорию

```
POST /categories/
```

**Тело запроса:**
```json
{
  "name": "string",
  "description": "string"
}
```

**Ответ:**
```json
{
  "id": "string",
  "name": "string",
  "description": "string"
}
```

### Получить категорию по ID

```
GET /categories/{id}
```

**Параметры:**
- `id` (string, required) - идентификатор категории

**Ответ:**
```json
{
  "id": "string",
  "name": "string",
  "description": "string"
}
```

### Обновить категорию

```
PUT /categories/{id}
```

**Параметры:**
- `id` (string, required) - идентификатор категории

**Тело запроса:**
```json
{
  "name": "string",
  "description": "string"
}
```

**Ответ:**
```json
{
  "id": "string",
  "name": "string",
  "description": "string"
}
```

### Удалить категорию

```
DELETE /categories/{id}
```

**Параметры:**
- `id` (string, required) - идентификатор категории

**Ответ:**
```json
{
  "message": "Category deleted successfully"
}
```

## Коды ошибок

- `200` - Успешный запрос
- `201` - Ресурс успешно создан
- `400` - Некорректный запрос
- `404` - Ресурс не найден
- `500` - Внутренняя ошибка сервера

## События

При изменении категорий сервис публикует события в RabbitMQ:

- `category.created` - категория создана
- `category.updated` - категория обновлена
- `category.deleted` - категория удалена