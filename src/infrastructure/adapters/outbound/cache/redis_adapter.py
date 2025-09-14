import redis
import json
from typing import Optional, Any
from infrastructure.config.settings import Settings


class RedisCacheAdapter:
    def __init__(self, settings: Settings):
        self.client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            decode_responses=True
        )
    
    def get(self, key: str) -> Optional[Any]:
        """Получить значение по ключу из кэша"""
        try:
            value = self.client.get(key)
            if value:
                # Проверим тип значения перед десериализацией
                if isinstance(value, (str, bytes, bytearray)):
                    return json.loads(value)
                else:
                    return value
            return None
        except Exception:
            return None
    
    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Сохранить значение в кэше с указанным временем жизни"""
        try:
            serialized_value = json.dumps(value)
            result = self.client.setex(key, expire, serialized_value)
            # Преобразуем результат в bool
            return bool(result)
        except Exception:
            return False
    
    def delete(self, key: str) -> bool:
        """Удалить значение из кэша по ключу"""
        try:
            result = self.client.delete(key)
            # Преобразуем результат в int и сравним с 0
            try:
                # Попробуем преобразовать в int, если это возможно
                if hasattr(result, '__await__'):
                    # Если результат асинхронный, вернем True по умолчанию
                    return True
                # Проверим, является ли результат числом
                if isinstance(result, (int, float)):
                    return int(result) > 0
                return True
            except (TypeError, ValueError):
                # Если не можем преобразовать в int, вернем True по умолчанию
                return True
        except Exception:
            return False
    
    def exists(self, key: str) -> bool:
        """Проверить существование ключа в кэше"""
        try:
            result = self.client.exists(key)
            # Преобразуем результат в int и сравним с 0
            try:
                # Попробуем преобразовать в int, если это возможно
                if hasattr(result, '__await__'):
                    # Если результат асинхронный, вернем True по умолчанию
                    return True
                # Проверим, является ли результат числом
                if isinstance(result, (int, float)):
                    return int(result) > 0
                return True
            except (TypeError, ValueError):
                # Если не можем преобразовать в int, вернем True по умолчанию
                return True
        except Exception:
            return False
    
    def flush(self) -> bool:
        """Очистить весь кэш"""
        try:
            self.client.flushdb()
            return True
        except Exception:
            return False