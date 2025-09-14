from pydantic import BaseModel
from typing import Optional
from domain.value_objects.category_id import CategoryId


class CategoryCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryUpdateRequest(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True