from pydantic import BaseModel
from typing import Optional, Dict, Any, List

#This block of code declares the response fields to be returned by the API /api/recipes
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
    ingredients: Optional[List[str]]
    nutrients: Optional[Dict[str, Any]]
    instructions: Optional[List[str]]
    serves: Optional[str]

    class Config:
        from_attributes = True #segregates the values passed in the JSON response as fields matching the model's field names

class PaginatedRecipesResponse(BaseModel):
    page: int
    limit: int
    total: int
    data: List[RecipeResponse]
