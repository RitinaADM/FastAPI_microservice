from abc import ABC, abstractmethod
from domain.entities.category import Category
from domain.value_objects.category_id import CategoryId
from typing import List, Optional


class CategoryRepository(ABC):
    """Outbound port for category persistence"""
    
    @abstractmethod
    def save(self, category: Category) -> Category:
        pass
    
    @abstractmethod
    def find_by_id(self, category_id: CategoryId) -> Optional[Category]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[Category]:
        pass
    
    @abstractmethod
    def update(self, category: Category) -> Category:
        pass
    
    @abstractmethod
    def delete(self, category_id: CategoryId) -> bool:
        pass