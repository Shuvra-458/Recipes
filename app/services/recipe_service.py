from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models import Recipe
from sqlalchemy import and_
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import cast, Float, func


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

    #This is used to match the recipe containing the input words from the user
    if title: 
        query = query.filter(Recipe.title.ilike(f"%{title}%"))

    #This is used to match the name of the cuisine
    if cuisine:
        query = query.filter(Recipe.cuisine == cuisine)

    #This block is used to filter recipes on the basis of operator and rating
    if rating:
        op, value = parse_operator(rating)
        if op == ">=":
            query = query.filter(Recipe.rating >= value)
        elif op == "<=":
            query = query.filter(Recipe.rating <= value)
        elif op == "=":
            query = query.filter(Recipe.rating == value)
        
    #This block is used to filter recipes on the basis of total time taken
    if total_time:
        op, value = parse_operator(total_time)
        if op == ">=":
            query = query.filter(Recipe.total_time >= value)
        elif op == "<=":
            query = query.filter(Recipe.total_time <= value)
        elif op == "=":
            query = query.filter(Recipe.total_time == value)
    
    #This block filters recipes on the basis of operators and desired value of calories
    if calories:
        op, value = parse_operator(calories)

        calories_expr = cast(
            func.replace(
                Recipe.nutrients["calories"].astext,
                " kcal",
                ""
            ),
            Float
        )

        if op == ">=":
            query = query.filter(calories_expr >= value)
        elif op == "<=":
            query = query.filter(calories_expr <= value)
        elif op == "=":
            query = query.filter(calories_expr == value)
    
    return query.all()
