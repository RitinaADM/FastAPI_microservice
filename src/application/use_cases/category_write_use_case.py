from domain.entities.category import Category
from domain.value_objects.category_id import CategoryId
from domain.ports.outbound.category_repository import CategoryRepository
from domain.ports.outbound.category_event_publisher import CategoryEventPublisher
from domain.exceptions.category_exceptions import CategoryNotFoundError, InvalidCategoryError
from typing import List, Optional


class CategoryWriteUseCase:
    """Application layer use case for writing category data"""
    
    def __init__(self, repository: CategoryRepository, event_publisher: CategoryEventPublisher):
        self.repository = repository
        self.event_publisher = event_publisher
    
    def create_category(self, name: str, description: Optional[str] = None) -> Category:
        # Validate category
        if not name or len(name.strip()) == 0:
            raise InvalidCategoryError("Category name cannot be empty")
        
        # Create category entity
        category = Category(id=None, name=name, description=description)
        
        # Save category
        saved_category = self.repository.create(category)
        
        # Publish event
        self.event_publisher.publish_category_created(saved_category)
        
        return saved_category
    
    def update_category(self, category_id: CategoryId, name: str, description: Optional[str] = None) -> Category:
        # Find existing category
        existing_category = self.repository.find_by_id(category_id)
        if not existing_category:
            raise CategoryNotFoundError(f"Category with id {category_id} not found")
        
        # Validate category
        if not name or len(name.strip()) == 0:
            raise InvalidCategoryError("Category name cannot be empty")
        
        # Update category
        updated_category = Category(id=category_id, name=name, description=description)
        saved_category = self.repository.update(updated_category)
        
        # Publish event
        self.event_publisher.publish_category_updated(saved_category)
        
        return saved_category
    
    def delete_category(self, category_id: CategoryId) -> bool:
        # Check if category exists
        existing_category = self.repository.find_by_id(category_id)
        if not existing_category:
            raise CategoryNotFoundError(f"Category with id {category_id} not found")
        
        # Delete category
        result = self.repository.delete(category_id)
        
        # Publish event if deletion was successful
        if result:
            self.event_publisher.publish_category_deleted(category_id)
        
        return result