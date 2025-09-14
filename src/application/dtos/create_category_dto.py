from pydantic import BaseModel
from typing import Optional


class CreateCategoryDTO(BaseModel):
    name: str
    description: Optional[str] = None