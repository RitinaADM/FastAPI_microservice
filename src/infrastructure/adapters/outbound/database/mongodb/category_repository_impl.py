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
    
    def save(self, category: Category) -> Category:
        # If category has no ID, generate one
        if category.id is None:
            category.id = CategoryId.new()
        
        # Convert to dict for MongoDB
        category_dict = {
            "_id": str(category.id),
            "name": category.name,
            "description": category.description
        }
        
        # Save to MongoDB
        self.collection.replace_one(
            {"_id": str(category.id)},
            category_dict,
            upsert=True
        )
        
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
        if category.id is None:
            raise ValueError("Category ID is required for update")
        
        category_dict = {
            "_id": str(category.id),
            "name": category.name,
            "description": category.description
        }
        
        result = self.collection.replace_one(
            {"_id": str(category.id)},
            category_dict
        )
        
        if result.matched_count == 0:
            raise ValueError(f"Category with id {category.id} not found")
        
        return category
    
    def delete(self, category_id: CategoryId) -> bool:
        result = self.collection.delete_one({"_id": str(category_id)})
        return result.deleted_count > 0