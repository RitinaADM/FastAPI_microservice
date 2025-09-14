from dataclasses import dataclass
from datetime import datetime
from domain.value_objects.category_id import CategoryId


@dataclass
class CategoryCreated:
    category_id: CategoryId
    name: str
    description: str
    timestamp: datetime


@dataclass
class CategoryUpdated:
    category_id: CategoryId
    name: str
    description: str
    timestamp: datetime


@dataclass
class CategoryDeleted:
    category_id: CategoryId
    timestamp: datetime
