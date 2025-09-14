from domain.entities.category import Category
from domain.value_objects.category_id import CategoryId
from domain.ports.inbound.category_input_port import CategoryInputPort
from domain.ports.outbound.category_repository import CategoryRepository
from domain.ports.outbound.category_event_publisher import CategoryEventPublisher
from domain.exceptions.category_exceptions import CategoryNotFoundError, InvalidCategoryError
from domain.services.category_service import CategoryService
from typing import List, Optional, Dict, Any


class CategoryUseCase(CategoryInputPort):
    """Application layer use case for category management"""
    
    def __init__(self, repository: CategoryRepository, event_publisher: CategoryEventPublisher, cache_adapter=None):
        self.repository = repository
        self.event_publisher = event_publisher
        self.cache_adapter = cache_adapter
        self.category_service = CategoryService()
    
    def create_category(self, name: str, description: Optional[str] = None) -> Category:
        # Create category entity
        category = Category(id=None, name=name, description=description)
        
        # Validate category
        if not category.name or len(category.name.strip()) == 0:
            raise InvalidCategoryError("Category name cannot be empty")
        
        # Save category
        saved_category = self.repository.save(category)
        
        # Clear cache for all categories
        if self.cache_adapter:
            self.cache_adapter.delete("all_categories")
        
        # Publish event
        self.event_publisher.publish_category_created(saved_category)
        
        return saved_category
    
    def get_category(self, category_id: CategoryId) -> Category:
        # Try to get from cache first
        cache_key = f"category_{category_id}"
        if self.cache_adapter:
            cached_category = self.cache_adapter.get(cache_key)
            if cached_category:
                return Category(
                    id=CategoryId(cached_category['id']),
                    name=cached_category['name'],
                    description=cached_category['description']
                )
        
        # Get from repository
        category = self.repository.find_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(f"Category with id {category_id} not found")
        
        # Save to cache
        if self.cache_adapter:
            self.cache_adapter.set(cache_key, {
                'id': str(category.id),
                'name': category.name,
                'description': category.description
            }, expire=300)  # 5 minutes cache
        
        return category
    
    def get_all_categories(self) -> List[Category]:
        # Try to get from cache first
        if self.cache_adapter:
            cached_categories = self.cache_adapter.get("all_categories")
            if cached_categories:
                return [
                    Category(
                        id=CategoryId(cat['id']),
                        name=cat['name'],
                        description=cat['description']
                    ) for cat in cached_categories
                ]
        
        # Get from repository
        categories = self.repository.find_all()
        
        # Save to cache
        if self.cache_adapter:
            serialized_categories = [
                {
                    'id': str(category.id),
                    'name': category.name,
                    'description': category.description
                } for category in categories
            ]
            self.cache_adapter.set("all_categories", serialized_categories, expire=300)  # 5 minutes cache
        
        return categories
    
    def update_category(self, category_id: CategoryId, name: str, description: Optional[str] = None) -> Category:
        # Find existing category
        existing_category = self.repository.find_by_id(category_id)
        if not existing_category:
            raise CategoryNotFoundError(f"Category with id {category_id} not found")
        
        # Update category
        updated_category = Category(id=category_id, name=name, description=description)
        saved_category = self.repository.update(updated_category)
        
        # Clear cache
        if self.cache_adapter:
            self.cache_adapter.delete(f"category_{category_id}")
            self.cache_adapter.delete("all_categories")
        
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
        
        # Clear cache
        if self.cache_adapter:
            self.cache_adapter.delete(f"category_{category_id}")
            self.cache_adapter.delete("all_categories")
        
        # Publish event if deletion was successful
        if result:
            self.event_publisher.publish_category_deleted(category_id)
        
        return result
    
    def get_category_statistics(self) -> Dict[str, Any]:
        """Get statistics for all categories"""
        # Get all categories
        categories = self.get_all_categories()
        
        # Calculate statistics using domain service
        return self.category_service.calculate_category_statistics(categories)