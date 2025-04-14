import json
from pydantic import BaseModel, validator
from typing import Optional, Dict, List

class BuildingBase(BaseModel):
    id: str
    slug: str
    name: str
    department: str
    description: str
    image: Optional[str] = None  # Will store base64 image data
    image_data: Optional[bytes] = None
    mime_type: Optional[str] = None
    facilities: Optional[List[str]] = None
    coordinates: Optional[Dict] = None

    @validator('coordinates')
    def validate_coordinates(cls, v):
        if v is not None and not isinstance(v, dict):
            raise ValueError('Coordinates must be a valid JSON object')
        return v

    class Config:
        orm_mode = True

class BuildingCreate(BaseModel):
    name: str
    department: str
    description: str
    facilities: List[str]
    coordinates: Dict[str, float]

    @validator('facilities')
    def validate_facilities(cls, v):
        if not isinstance(v, list):
            raise ValueError('Facilities must be a list')
        if not all(isinstance(item, str) for item in v):
            raise ValueError('All facilities must be strings')
        return v

    @validator('coordinates')
    def validate_coordinates(cls, v):
        if not isinstance(v, dict):
            raise ValueError('Coordinates must be a dictionary')
        if 'lat' not in v or 'lng' not in v:
            raise ValueError('Coordinates must contain lat and lng')
        if not isinstance(v['lat'], (int, float)) or not isinstance(v['lng'], (int, float)):
            raise ValueError('Coordinates values must be numbers')
        return v

class BuildingUpdate(BaseModel):
    id: Optional[str] = None
    slug: Optional[str] = None
    name: Optional[str] = None
    department: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    image_data: Optional[bytes] = None
    mime_type: Optional[str] = None
    facilities: Optional[List[str]] = None
    coordinates: Optional[Dict] = None

    @validator('coordinates')
    def validate_coordinates(cls, v):
        if v is not None and not isinstance(v, dict):
            raise ValueError('Coordinates must be a valid JSON object')
        return v

    @validator('facilities')
    def validate_facilities(cls, v):
        if v is not None:
            try:
                parsed = json.loads(v)
                if not isinstance(parsed, list):
                    raise ValueError('Facilities must be a valid JSON array')
            except json.JSONDecodeError:
                raise ValueError('Invalid facilities format')
        return v

    class Config:
        orm_mode = True

class Building(BuildingBase):
    pass
