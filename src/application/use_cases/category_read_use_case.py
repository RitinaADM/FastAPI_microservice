from domain.entities.category import Category
from domain.value_objects.category_id import CategoryId
from domain.ports.outbound.category_repository import CategoryRepository
from domain.exceptions.category_exceptions import CategoryNotFoundError
from typing import List, Optional


class CategoryReadUseCase:
    """Application layer use case for reading category data"""
    
    def __init__(self, repository: CategoryRepository):
        self.repository = repository
    
    def get_category(self, category_id: CategoryId) -> Category:
        category = self.repository.find_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(f"Category with id {category_id} not found")
        
        return category
    
    def get_all_categories(self) -> List[Category]:
        categories = self.repository.find_all()
        return categories
