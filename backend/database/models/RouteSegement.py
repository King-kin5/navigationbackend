from sqlalchemy import Boolean, Column, Float, String, Text
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class RouteSegmentORM(Base):
    """For pre-computed route segments between buildings"""
    __tablename__ = "route_segments"
    
    id = Column(String, primary_key=True)
    start_building_id = Column(String, index=True)
    end_building_id = Column(String, index=True)
    
    # Route geometry stored as GeoJSON or WKT
    geometry = Column(Text)
    
    distance = Column(Float)
    duration = Column(Float)
    is_accessible = Column(Boolean, default=True)
    has_stairs = Column(Boolean, default=False)
    is_indoor = Column(Boolean, default=False)