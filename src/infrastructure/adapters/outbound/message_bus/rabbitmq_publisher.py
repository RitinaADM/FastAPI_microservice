from domain.entities.category import Category
from domain.value_objects.category_id import CategoryId
from domain.ports.outbound.category_event_publisher import CategoryEventPublisher
import json
import pika
from datetime import datetime


class RabbitMQCategoryEventPublisher(CategoryEventPublisher):
    """RabbitMQ implementation of CategoryEventPublisher"""
    
    def __init__(self, rabbitmq_connection_params: pika.ConnectionParameters, exchange_name: str = "category_events"):
        self.connection_params = rabbitmq_connection_params
        self.exchange_name = exchange_name
        self._connection = None
        self._channel = None
    
    def _get_channel(self):
        """Get or create a RabbitMQ channel"""
        if self._connection is None or not self._connection.is_open:
            self._connection = pika.BlockingConnection(self.connection_params)
            self._channel = self._connection.channel()
            # Declare exchange
            self._channel.exchange_declare(exchange=self.exchange_name, exchange_type='topic', durable=True)
        elif self._channel is None or self._channel.is_closed:
            self._channel = self._connection.channel()
            # Declare exchange
            self._channel.exchange_declare(exchange=self.exchange_name, exchange_type='topic', durable=True)
        return self._channel
    
    def publish_category_created(self, category: Category) -> None:
        event = {
            "event_type": "category_created",
            "category_id": str(category.id),
            "name": category.name,
            "description": category.description,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        channel = self._get_channel()
        channel.basic_publish(
            exchange=self.exchange_name,
            routing_key="category.created",
            body=json.dumps(event),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
    
    def publish_category_updated(self, category: Category) -> None:
        event = {
            "event_type": "category_updated",
            "category_id": str(category.id),
            "name": category.name,
            "description": category.description,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        channel = self._get_channel()
        channel.basic_publish(
            exchange=self.exchange_name,
            routing_key="category.updated",
            body=json.dumps(event),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
    
    def publish_category_deleted(self, category_id: CategoryId) -> None:
        event = {
            "event_type": "category_deleted",
            "category_id": str(category_id),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        channel = self._get_channel()
        channel.basic_publish(
            exchange=self.exchange_name,
            routing_key="category.deleted",
            body=json.dumps(event),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
    
    def close(self):
        """Close RabbitMQ connection"""
        if self._connection and self._connection.is_open:
            self._connection.close()