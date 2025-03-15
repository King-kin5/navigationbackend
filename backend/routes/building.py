from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database.base import get_db
from backend.database.models.building import Building
from backend.database.models.schema import BuildingBase


router = APIRouter()

@router.get("/", response_model=List[BuildingBase])
def get_all_buildings(db: Session = Depends(get_db)):
    buildings = db.query(Building).all()
    
    # Convert database model to Pydantic schema
    result = []
    for building in buildings:
        result.append({
            "id": building.id,
            "slug": building.slug,
            "name": building.name,
            "department": building.department,
            "description": building.description,
            #"image": building.image,
            "facilities": building.facilities,
            "lat": building.lat,
            "lng": building.lng,

        })
    
    return result

@router.get("/{slug}", response_model=BuildingBase)
def get_building_by_slug(slug: str, db: Session = Depends(get_db)):
    building = db.query(Building).filter(Building.slug == slug).first()
    
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    # Convert database model to Pydantic schema
    result = {
        "id": building.id,
        "slug": building.slug,
        "name": building.name,
        "department": building.department,
        "description": building.description,
        #"image": building.image,
        "facilities": building.facilities,
        "lat": building.lat,
        "lng": building.lng,
    }
    
    return result