import json
from pydantic import BaseModel, validator
from typing import Optional, List
class BuildingBase(BaseModel):
    name: str
    department: str
    description: str
    #image: Optional[str] = None
    facilities: Optional[List[str]] = None
    coordinates:str

    # Validator to handle coordinate conversion
    @validator("coordinates", pre=True)
    def validate_coordinates(cls, v):
        if isinstance(v, dict):
            return json.dumps(v)  # Convert dict to JSON string
        return v

class BuildingUpdate(BaseModel):
    slug: Optional[str] = None
    name: Optional[str] = None
    department: Optional[str] = None
    description: Optional[str] = None
    facilities: Optional[List[str]] = None
    coordinates: Optional[str] = None

class BuildingCreate(BuildingBase):
    pass




class Building(BuildingBase):
    class Config:
        orm_mode = True