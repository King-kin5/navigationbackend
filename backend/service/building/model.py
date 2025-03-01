from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class Coordinates(BaseModel):
    latitude: float
    longitude: float


class BuildingEntrance(BaseModel):
    name: str
    coordinates: Coordinates
    is_accessible: bool = True
    description: Optional[str] = None


class BuildingFloor(BaseModel):
    floor_number: str  # Using string to handle formats like "G", "B1", etc.
    facilities: List[str] = []
    has_elevator: bool = False
    has_restrooms: bool = False
    has_accessible_restrooms: bool = False
    map_image_url: Optional[str] = None


class BuildingHours(BaseModel):
    monday: Optional[str] = None
    tuesday: Optional[str] = None
    wednesday: Optional[str] = None
    thursday: Optional[str] = None
    friday: Optional[str] = None
    saturday: Optional[str] = None
    sunday: Optional[str] = None
    holidays: Optional[str] = None
    additional_info: Optional[str] = None


class Building(BaseModel):
    id: str = Field(..., description="Unique identifier for the building")
    name: str = Field(..., description="Official name of the building")
    short_name: Optional[str] = Field(None, description="Abbreviated or common name")
    description: Optional[str] = Field(None, description="General description of the building")
    primary_coordinates: Coordinates = Field(..., description="Main coordinates for map placement")
    entrances: List[BuildingEntrance] = Field(default_factory=list, description="List of building entrances")
    floors: List[BuildingFloor] = Field(default_factory=list, description="Floors in the building")
    
    department: Optional[str] = None
    category: Optional[str] = None  # Academic, Administrative, Residential, etc.
    facilities: List[str] = Field(default_factory=list, description="Available facilities")
    
    opening_hours: Optional[BuildingHours] = None
    
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    
    # For search optimization
    keywords: List[str] = Field(default_factory=list, description="Keywords to improve search results")
    
    last_updated: datetime = Field(default_factory=datetime.now)

    # Additional metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Extensible field for additional data")


class BuildingSearchResult(BaseModel):
    id: str
    name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    primary_coordinates: Coordinates
    category: Optional[str] = None
    department: Optional[str] = None
    thumbnail_url: Optional[str] = None
    distance: Optional[float] = None  # Distance from search point if applicable