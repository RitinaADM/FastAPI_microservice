from pydantic import BaseModel
from typing import Optional
from domain.value_objects.category_id import CategoryId


class CategoryDTO(BaseModel):
    id: Optional[CategoryId] = None
    name: str
    description: Optional[str] = None