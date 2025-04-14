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
    coordinates: Dict

    @validator('coordinates')
    def validate_coordinates(cls, v):
        if not isinstance(v, dict):
            raise ValueError('Coordinates must be a valid JSON object')
        return v

    class Config:
        orm_mode = True

class BuildingCreate(BuildingBase):
    pass

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

class Building(BuildingBase):
    pass
