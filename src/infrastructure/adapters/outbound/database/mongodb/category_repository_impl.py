from domain.entities.category import Category
from domain.value_objects.category_id import CategoryId
from domain.ports.outbound.category_repository import CategoryRepository
from typing import List, Optional
import pymongo
from bson import ObjectId


class MongoCategoryRepository(CategoryRepository):
    """MongoDB implementation of CategoryRepository"""
    
    def __init__(self, connection_string: str, database_name: str):
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db.categories
    
    def create(self, category: Category) -> Category:
        # Create should only create new categories
        if category.id is None:
            category.id = CategoryId.new()
        else:
            # If ID exists, check that category doesn't already exist
            existing = self.collection.find_one({"_id": str(category.id)})
            if existing:
                raise ValueError(f"Category with id {category.id} already exists")
        
        # Convert to dict for MongoDB
        category_dict = {
            "_id": str(category.id),
            "name": category.name,
            "description": category.description
        }
        
        # Insert new category
        self.collection.insert_one(category_dict)
        
        return category
    
    def find_by_id(self, category_id: CategoryId) -> Optional[Category]:
        doc = self.collection.find_one({"_id": str(category_id)})
        if not doc:
            return None
        
        return Category(
            id=CategoryId(doc["_id"]),
            name=doc["name"],
            description=doc.get("description")
        )
    
    def find_all(self) -> List[Category]:
        categories = []
        for doc in self.collection.find():
            categories.append(Category(
                id=CategoryId(doc["_id"]),
                name=doc["name"],
                description=doc.get("description")
            ))
        return categories
    
    def update(self, category: Category) -> Category:
        # Update should only update existing categories
        if category.id is None:
            raise ValueError("Category ID is required for update")
        
        # Check that category exists
        existing = self.collection.find_one({"_id": str(category.id)})
        if not existing:
            raise ValueError(f"Category with id {category.id} not found")
        
        category_dict = {
            "_id": str(category.id),
            "name": category.name,
            "description": category.description
        }
        
        # Update existing category
        self.collection.replace_one(
            {"_id": str(category.id)},
            category_dict
        )
        
        return category
    
    def delete(self, category_id: CategoryId) -> bool:
        result = self.collection.delete_one({"_id": str(category_id)})
        return result.deleted_count > 0