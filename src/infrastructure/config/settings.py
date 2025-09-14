from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    mongodb_connection_string: str = "mongodb://localhost:27017"
    mongodb_database_name: str = "category_service"
    
    # RabbitMQ
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"
    rabbitmq_exchange_name: str = "category_events"
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    # Application
    app_name: str = "Category Service"
    debug: bool = False
    
    class Config:
        env_file = ".env"