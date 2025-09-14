from abc import ABC, abstractmethod
from domain.entities.category import Category
from domain.value_objects.category_id import CategoryId
from typing import List, Optional, Dict, Any


class CategoryInputPort(ABC):
    """Inbound port for category operations"""
    
    @abstractmethod
    def create_category(self, name: str, description: Optional[str] = None) -> Category:
        pass
    
    @abstractmethod
    def get_category(self, category_id: CategoryId) -> Category:
        pass
    
    @abstractmethod
    def get_all_categories(self) -> List[Category]:
        pass
    
    @abstractmethod
    def update_category(self, category_id: CategoryId, name: str, description: Optional[str] = None) -> Category:
        pass
    
    @abstractmethod
    def delete_category(self, category_id: CategoryId) -> bool:
        pass
    
    @abstractmethod
    def get_category_statistics(self) -> Dict[str, Any]:
        """Get statistics for all categories"""
        pass