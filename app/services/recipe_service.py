from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models import Recipe
from sqlalchemy import and_
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import cast, Float


import re


def get_recipes(db: Session, page: int=1, limit: int=10):
    offset = (page-1)*limit

    total = db.query(Recipe).count()

    recipes = (
        db.query(Recipe)
        .order_by(desc(Recipe.rating))
        .offset(offset)
        .limit(limit)
        .all()
    )

    return total, recipes


def parse_operator(value: str):
    """Parses expressions(like >=4.5, <=120, =300) and Returns: (operator, numeric_value)"""

    match = re.match(r"(>=|<=|=)(\d+(\.\d+)?)", value)
    if not match:
        return None, None
    
    op, number, _ = match.groups()
    return op, float(number)

def search_recipes(
        db: Session,
        title: str | None = None,
        cuisine: str | None = None,
        rating: str | None = None,
        total_time: str | None = None,
        calories: str | None = None,
):
    query = db.query(Recipe)

    #Title (partial match)
    if title: 
        query = query.filter(Recipe.title.ilike(f"%{title}%"))

    #Cuisine (exact match)
    if cuisine:
        query = query.filer(Recipe.cuisine == cuisine)

    #Rating filter
    if rating:
        op, value = parse_operator(rating)
        if op == ">=":
            query = query.filter(Recipe.rating >= value)
        elif op == "<=":
            query = query.filter(Recipe.rating <= value)
        elif op == "=":
            query = query.filer(Recipe.rating == value)
        
    #Total time filter
    if total_time:
        op, value = parse_operator(total_time)
        if op == ">=":
            query = query.filter(Recipe.total_time >= value)
        elif op == "<=":
            query = query.filter(Recipe.total_time <= value)
        elif op == "=":
            query = query.filter(Recipe.total_time == value)
    
    #Calories filter
    if calories:
        op, value = parse_operator(calories)

        calories_expr = cast(
            Recipe.nutrients["calories"].astext.replace(" kcal", ""),
            Float
        )

        if op == ">=":
            query = query.filter(calories_expr >= value)
        elif op == "<=":
            query = query.filter(calories_expr <= value)
        elif op == "=":
            query = query.filter(calories_expr == value)
    
    return query.all()