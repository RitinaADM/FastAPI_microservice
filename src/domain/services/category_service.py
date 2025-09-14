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
    
    def calculate_category_statistics(self, categories: List[Category]) -> dict:
        """Calculate statistics for categories"""
        if not categories:
            return {
                "total_count": 0,
                "average_name_length": 0,
                "longest_name": "",
                "shortest_name": ""
            }
        
        names = [cat.name for cat in categories if cat.name]
        if not names:
            return {
                "total_count": len(categories),
                "average_name_length": 0,
                "longest_name": "",
                "shortest_name": ""
            }
        
        name_lengths = [len(name) for name in names]
        
        return {
            "total_count": len(categories),
            "average_name_length": sum(name_lengths) / len(name_lengths),
            "longest_name": max(names, key=len),
            "shortest_name": min(names, key=len)
        }