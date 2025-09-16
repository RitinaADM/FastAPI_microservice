from abc import ABC, abstractmethod
from domain.entities.category import Category
from domain.value_objects.category_id import CategoryId
from typing import List, Optional


class CategoryRepository(ABC):
    """Outbound port for category persistence"""
    
    @abstractmethod
    def create(self, category: Category) -> Category:
        """
        Create a new category.
        
        Args:
            category: Category to create. If category.id is None, a new ID will be generated.
            
        Returns:
            The created category with its ID.
            
        Raises:
            ValueError: If a category with the same ID already exists.
        """
        pass
    
    @abstractmethod
    def find_by_id(self, category_id: CategoryId) -> Optional[Category]:
        """
        Find a category by its ID.
        
        Args:
            category_id: The ID of the category to find.
            
        Returns:
            The category if found, None otherwise.
        """
        pass
    
    @abstractmethod
    def find_all(self) -> List[Category]:
        """
        Find all categories.
        
        Returns:
            A list of all categories.
        """
        pass
    
    @abstractmethod
    def update(self, category: Category) -> Category:
        """
        Update an existing category.
        
        Args:
            category: Category to update. Must have a valid ID.
            
        Returns:
            The updated category.
            
        Raises:
            ValueError: If category ID is None or if no category with the given ID exists.
        """
        pass
    
    @abstractmethod
    def delete(self, category_id: CategoryId) -> bool:
        """
        Delete a category by its ID.
        
        Args:
            category_id: The ID of the category to delete.
            
        Returns:
            True if the category was deleted, False if it didn't exist.
        """
        pass