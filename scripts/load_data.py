import json
import math
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Recipe

DATA_FILE = "data/US_recipes_null.Pdf.json"

#This block searches the JSON Data for float values (e.g: ratings)
def safe_float(value):
    try:
        if value is None:
            return None
        val = float(value)
        if math.isnan(val):  #used to handle null fields
            return None
        return val
    except (ValueError, TypeError):
        return None

#This block searches the JSON Data for integer values (e.g: prep_time, total_time)
def safe_int(value):
    try:
        if value is None:
            return None
        val = int(value)
        return val
    except (ValueError, TypeError):
        return None

#This block retrieves the fields from the input JSON data 
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
            continent = item.get("Contient"), #The arguement in the get() method must accurately match the name of the field specified in the input JSON data
            country_state = item.get("Country_State"),
            source_url = item.get("URL"),
            cuisine = item.get("cuisine"),
            title = item.get("title"),
            rating = safe_float(item.get("rating")),
            prep_time = safe_int(item.get("cook_time")),
            cook_time = safe_int(item.get("cook_time")),
            total_time = safe_int(item.get("total_time")),
            description = item.get("description"),
            ingredients = item.get("ingredients"),
            nutrients = item.get("nutrients"),
            instructions = item.get("instructions"),
            serves = item.get("serves"),
        )

        db.add(recipe) #Adds the obtained fields from the input JSON data into the Postgres Database
        inserted += 1  #Counts the total number of rows inserted

    db.commit()
    db.close()

    print(f" Successfully inserted {inserted} recipes")

if __name__ == "__main__":
    load_recipes()
