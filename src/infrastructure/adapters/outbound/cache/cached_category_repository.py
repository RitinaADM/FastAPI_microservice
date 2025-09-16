from domain.entities.category import Category
from domain.value_objects.category_id import CategoryId
from domain.ports.outbound.category_repository import CategoryRepository
from typing import List, Optional
from .redis_adapter import RedisCacheAdapter


class CachedCategoryRepository(CategoryRepository):
    """Cached decorator for CategoryRepository"""
    
    def __init__(self, repository: CategoryRepository, cache_adapter: RedisCacheAdapter):
        self.repository = repository
        self.cache_adapter = cache_adapter
    
    def create(self, category: Category) -> Category:
        # Create in the underlying repository
        result = self.repository.create(category)
        
        # Invalidate cache for all categories since we added a new one
        if self.cache_adapter:
            self.cache_adapter.delete("all_categories")
        
        return result
    
    def find_by_id(self, category_id: CategoryId) -> Optional[Category]:
        # Try to get from cache first
        cache_key = f"category_{category_id}"
        if self.cache_adapter:
            cached_category = self.cache_adapter.get(cache_key)
            # Check if cached_category is not None and is a dict (not a Mock object)
            if cached_category and isinstance(cached_category, dict):
                return Category(
                    id=CategoryId(cached_category['id']),
                    name=cached_category['name'],
                    description=cached_category['description']
                )
        
        # Get from underlying repository
        category = self.repository.find_by_id(category_id)
        if not category:
            return None
        
        # Save to cache
        if self.cache_adapter:
            self.cache_adapter.set(cache_key, {
                'id': str(category.id),
                'name': category.name,
                'description': category.description
            }, expire=300)  # 5 minutes cache
        
        return category
    
    def find_all(self) -> List[Category]:
        # Try to get from cache first
        if self.cache_adapter:
            cached_categories = self.cache_adapter.get("all_categories")
            # Check if cached_categories is not None and is a list (not a Mock object)
            if cached_categories and isinstance(cached_categories, list):
                return [
                    Category(
                        id=CategoryId(cat['id']),
                        name=cat['name'],
                        description=cat['description']
                    ) for cat in cached_categories
                    if isinstance(cat, dict)  # Additional check for each item
                ]
        
        # Get from underlying repository
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
    
    def update(self, category: Category) -> Category:
        # Update in the underlying repository
        result = self.repository.update(category)
        
        # Invalidate cache for this category and all categories
        if self.cache_adapter:
            self.cache_adapter.delete(f"category_{category.id}")
            self.cache_adapter.delete("all_categories")
        
        return result
    
    def delete(self, category_id: CategoryId) -> bool:
        # Delete from the underlying repository
        result = self.repository.delete(category_id)
        
        # If deletion was successful, invalidate cache
        if result and self.cache_adapter:
            self.cache_adapter.delete(f"category_{category_id}")
            self.cache_adapter.delete("all_categories")
        
        return result