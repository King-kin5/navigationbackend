from sqlalchemy import Column, String, Text, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class BuildingORM(Base):
    """SQLAlchemy ORM model for buildings"""
    __tablename__ = "buildings"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    short_name = Column(String, nullable=True, index=True)
    description = Column(Text, nullable=True)
    
    # Stored as JSON string: {"latitude": 40.123, "longitude": -74.456}
    primary_coordinates = Column(Text, nullable=False)
    
    department = Column(String, nullable=True, index=True)
    category = Column(String, nullable=True, index=True)
    
    # Stored as JSON array
    facilities = Column(Text, nullable=True)
    
    # Stored as JSON array of entrance objects
    entrances = Column(Text, nullable=True)
    
    # Stored as JSON array of floor objects
    floors = Column(Text, nullable=True)
    
    # Stored as JSON object
    opening_hours = Column(Text, nullable=True)
    
    #image_url = Column(String, nullable=True)
    #thumbnail_url = Column(String, nullable=True)
    
    # Stored as JSON array of strings
    keywords = Column(Text, nullable=True)
    
    # Stored as JSON object for extensibility
    metadata = Column(Text, nullable=True)
    
    last_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)