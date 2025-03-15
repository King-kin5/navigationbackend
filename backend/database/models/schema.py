from pydantic import BaseModel
from typing import Optional, List

class BuildingBase(BaseModel):
    slug: str
    name: str
    department: str
    description: str
    #image: Optional[str] = None
    facilities: Optional[List[str]] = None
    lat: float
    lng: float



class BuildingCreate(BuildingBase):
    pass

class Coordinates(BaseModel):
    lat: float
    lng: float
class BuildingResponse(BuildingBase):
    name: str
    department: str
    description: str
    #image: Optional[str] = None
    facilities: Optional[List[str]] = None
    lat: float
    lng: float


class Building(BuildingBase):
    class Config:
        orm_mode = True