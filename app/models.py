from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    continent = Column(String(100))
    country_state = Column(String(100))
    cuisine = Column(String(255))
    title = Column(String(255), index=True)
    rating = Column(Float, nullable=True)
    prep_time = Column(Integer, nullable=True)
    cook_time = Column(Integer, nullable=True)
    total_time = Column(Integer, nullable=True)
    description = Column(Text)
    nutrients = Column(JSONB)
    instructions = Column(JSONB)
    serves = Column(String(100))
    source_url = Column(Text)
