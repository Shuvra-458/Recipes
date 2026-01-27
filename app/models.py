from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base

#Creates the table in the Postgres Database
class Recipe(Base):
    __tablename__ = "recipes" #Name of the table

    id = Column(Integer, primary_key=True, index=True) 
    continent = Column(String(100))
    country_state = Column(String(100)) 
    cuisine = Column(String(255))
    title = Column(String(255), index=True) #index=true adds index to the title column, which helps in improving the querying performance
    rating = Column(Float, nullable=True)  #nullable=True allows for null value from the json data to be inserted in the columns
    prep_time = Column(Integer, nullable=True)
    cook_time = Column(Integer, nullable=True)
    total_time = Column(Integer, nullable=True)
    description = Column(Text)
    ingredients = Column(JSONB)
    nutrients = Column(JSONB)
    instructions = Column(JSONB)
    serves = Column(String(100))
    source_url = Column(Text)
