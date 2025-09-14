from dataclasses import dataclass
from typing import Optional
from domain.value_objects.category_id import CategoryId
from domain.exceptions.category_exceptions import InvalidCategoryError


@dataclass
class Category:
    id: Optional[CategoryId]
    name: str
    description: Optional[str] = None

    def __post_init__(self):
        if not self.name:
            raise InvalidCategoryError("Category name cannot be empty")