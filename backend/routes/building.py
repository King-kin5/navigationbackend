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
            "coordinates":building.coordinates

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
        "coordinates":building.coordinates
    }
    
    return result

@router.put("/{slug}", response_model=BuildingBase)
def update_building(slug: str, building_data: BuildingBase, db: Session = Depends(get_db)):
    # Find the existing building
    building = db.query(Building).filter(Building.slug == slug).first()
    
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    # Update all fields
    building.slug = building_data.slug
    building.name = building_data.name
    building.department = building_data.department
    building.description = building_data.description
    building.facilities = building_data.facilities
    building.coordinates=building_data.coordinates
    # Commit changes
    db.commit()
    db.refresh(building)
    
    # Convert database model to Pydantic schema
    result = {
        "id": building.id,
        "slug": building.slug,
        "name": building.name,
        "department": building.department,
        "description": building.description,
        #"image": building.image,
        "facilities": building.facilities,
        "coordinates":building.coordinates
    }
    
    return result

@router.patch("/{slug}", response_model=BuildingBase)
def partially_update_building(slug: str, building_data: dict, db: Session = Depends(get_db)):
    # Find the existing building
    building = db.query(Building).filter(Building.slug == slug).first()
    
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    # Update only provided fields
    for key, value in building_data.items():
        if hasattr(building, key) and key != "id":  # Prevent updating id
            setattr(building, key, value)
    
    # Commit changes
    db.commit()
    db.refresh(building)
    
    # Convert database model to Pydantic schema
    result = {
        "id": building.id,
        "slug": building.slug,
        "name": building.name,
        "department": building.department,
        "description": building.description,
        #"image": building.image,
        "facilities": building.facilities,
        "coordinates":building.coordinates
    }
    
    return result