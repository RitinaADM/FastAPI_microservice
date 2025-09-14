from pydantic import BaseModel
from typing import Optional
from domain.value_objects.category_id import CategoryId


class UpdateCategoryDTO(BaseModel):
    id: CategoryId
    name: str
    description: Optional[str] = None