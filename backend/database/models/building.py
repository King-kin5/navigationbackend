from sqlalchemy import Column, Integer, String, Float, ARRAY, JSON, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from backend.database.base import Base

class Building(Base):
    __tablename__ = "buildings"

    id = Column(String, primary_key=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String, nullable=True)
    image_data = Column(LargeBinary, nullable=True)
    mime_type = Column(String, nullable=True)
    facilities = Column(ARRAY(String), nullable=True)
    coordinates = Column(JSON, nullable=True)
    