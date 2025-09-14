from domain.entities.category import Category
from domain.value_objects.category_id import CategoryId
from typing import List


class CategoryService:
    """Domain service for category business logic"""
    
    def validate_category(self, category: Category) -> bool:
        """Validate category business rules"""
        if not category.name or len(category.name.strip()) == 0:
            return False
        # Add more validation rules as needed
        return True
    
    def can_delete_category(self, category: Category, has_products: bool) -> bool:
        """Check if category can be deleted"""
        # A category with associated products cannot be deleted
        return not has_products