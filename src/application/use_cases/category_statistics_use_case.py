from domain.entities.category import Category
from domain.services.category_service import CategoryService
from application.use_cases.category_read_use_case import CategoryReadUseCase
from typing import Dict, Any


class CategoryStatisticsUseCase:
    """Application layer use case for category statistics"""
    
    def __init__(self, read_use_case: CategoryReadUseCase):
        self.read_use_case = read_use_case
        self.category_service = CategoryService()
    
    def get_category_statistics(self) -> Dict[str, Any]:
        """Get statistics for all categories"""
        # Get all categories using read use case
        categories = self.read_use_case.get_all_categories()
        
        # Calculate statistics using domain service
        return self.category_service.calculate_category_statistics(categories)