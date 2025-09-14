from abc import ABC, abstractmethod
from domain.entities.category import Category
from domain.value_objects.category_id import CategoryId


class CategoryEventPublisher(ABC):
    """Outbound port for category event publishing"""
    
    @abstractmethod
    def publish_category_created(self, category: Category) -> None:
        pass
    
    @abstractmethod
    def publish_category_updated(self, category: Category) -> None:
        pass
    
    @abstractmethod
    def publish_category_deleted(self, category_id: CategoryId) -> None:
        pass