import json
from pydantic import BaseModel, validator
from typing import Optional, List

class BuildingBase(BaseModel):
    name: str
    department: str
    description: str
    #image: Optional[str] = None
    facilities: Optional[List[str]] = None
    coordinates: dict  # Now a dictionary

    # If coordinates come in as a JSON string, convert them to a dict.
    @validator("coordinates", pre=True)
    def validate_coordinates(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:
                raise ValueError("Invalid JSON for coordinates")
        return v

class BuildingCreate(BuildingBase):
    pass

class BuildingUpdate(BaseModel):
    slug: Optional[str] = None
    name: Optional[str] = None
    department: Optional[str] = None
    description: Optional[str] = None
    facilities: Optional[List[str]] = None
    coordinates: Optional[dict] = None  # Now a dictionary

class Building(BuildingBase):
    class Config:
        orm_mode = True
