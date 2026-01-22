from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.recipe_service import get_recipes
from app.services.recipe_service import search_recipes
from app.schemas import PaginatedRecipesResponse
from app.schemas import RecipeResponse

router = APIRouter(prefix="/api/recipes", tags=["Recipes"])

@router.get("", response_model=PaginatedRecipesResponse)
def fetch_recipes(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
):
    total, recipes = get_recipes(db, page=page, limit=limit)

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": recipes,
    }

@router.get("/search", response_model=dict)
def search(
    title: str | None = None,
    cuisine: str | None = None,
    rating: str | None = None,
    total_time: str | None = None,
    calories: str | None = None,
    db: Session = Depends(get_db),
):
    results = search_recipes(
        db=db,
        title=title,
        cuisine=cuisine,
        rating=rating,
        total_time=total_time,
        calories=calories,
    )

    return {
        "data": [RecipeResponse.model_validate(r) for r in results]
    }