from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class RecipeResponse(BaseModel):
    id: int
    continent: Optional[str]
    country_state: Optional[str]
    source_url: Optional[str]
    title: Optional[str]
    cuisine: Optional[str]
    rating: Optional[float]
    prep_time: Optional[int]
    cook_time: Optional[int]
    total_time: Optional[int]
    description: Optional[str]
    nutrients: Optional[Dict[str, Any]]
    instructions: Optional[List[str]]
    serves: Optional[str]

    class Config:
        from_attributes = True

class PaginatedRecipesResponse(BaseModel):
    page: int
    limit: int
    total: int
    data: List[RecipeResponse]
