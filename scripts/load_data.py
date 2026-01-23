import json
import math
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Recipe

DATA_FILE = "data/US_recipes_null.Pdf.json"

def safe_float(value):
    try:
        if value is None:
            return None
        val = float(value)
        if math.isnan(val):
            return None
        return val
    except (ValueError, TypeError):
        return None

def safe_int(value):
    try:
        if value is None:
            return None
        val = float(value)
        if math.isnan(val):
            return None
        return val
    except (ValueError, TypeError):
        return None
    
def safe_int(value):
    try:
        if value is None:
            return None
        val = int(value)
        return val
    except (ValueError, TypeError):
        return None
    
def load_recipes():
    db: Session = SessionLocal()
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    if isinstance(raw_data, dict):
        data = raw_data.values()
    elif isinstance(raw_data, list):
        data = raw_data
    else:
        raise ValueError("Unsupported JSON format")
    
    inserted = 0

    for item in data:
        recipe = Recipe(
            continent = item.get("Contient"),
            country_state = item.get("Country_State"),
            source_url = item.get("URL"),
            cuisine = item.get("cuisine"),
            title = item.get("title"),
            rating = safe_float(item.get("rating")),
            prep_time = safe_int(item.get("cook_time")),
            cook_time = safe_int(item.get("cook_time")),
            total_time = safe_int(item.get("total_time")),
            description = item.get("description"),
            nutrients = item.get("nutrients"),
            instructions = item.get("instructions"),
            serves = item.get("serves"),
        )

        db.add(recipe)
        inserted += 1

    db.commit()
    db.close()

    print(f" Successfully inserted {inserted} recipes")

if __name__ == "__main__":
    load_recipes()
