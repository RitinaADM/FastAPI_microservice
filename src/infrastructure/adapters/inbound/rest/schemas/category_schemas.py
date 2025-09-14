from pydantic import BaseModel
from typing import Optional, Dict, Any


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


class CategoryStatisticsResponse(BaseModel):
    total_count: int
    average_name_length: float
    longest_name: str
    shortest_name: str
    
    class Config:
        from_attributes = True