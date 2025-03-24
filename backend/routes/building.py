from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from backend.database.base import get_db
from backend.database.models.building import Building
from backend.database.models.schema import BuildingBase, BuildingCreate, BuildingUpdate
from backend.seed_data import slugify

router = APIRouter()

@router.post("/create", response_model=BuildingBase)
def create_building(building_data: BuildingCreate, db: Session = Depends(get_db)):
    # Generate a slug from the building name.
    slug = slugify(building_data.name)
    
    # Check if a building with the same slug already exists.
    existing = db.query(Building).filter(Building.slug == slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Building with this slug already exists")
    
    # Create a new Building instance.
    # Convert the coordinates dict to a JSON string for storage.
    building = Building(
        id=slug,  # Use slug as id or generate an appropriate id.
        slug=slug,
        name=building_data.name,
        department=building_data.department,
        description=building_data.description,
        facilities=building_data.facilities,
        coordinates=json.dumps(building_data.coordinates)
    )
    db.add(building)
    db.commit()
    db.refresh(building)
    
    # Return the building data converting the stored JSON back to a dict.
    return {
        "id": building.id,
        "slug": building.slug,
        "name": building.name,
        "department": building.department,
        "description": building.description,
        "facilities": building.facilities,
        "coordinates": json.loads(building.coordinates) if building.coordinates else {}
    }

@router.get("/", response_model=list[BuildingBase])
def get_all_buildings(db: Session = Depends(get_db)):
    buildings = db.query(Building).all()
    
    result = []
    for building in buildings:
        result.append({
            "id": building.id,
            "slug": building.slug,
            "name": building.name,
            "department": building.department,
            "description": building.description,
            "facilities": building.facilities,
            "coordinates": json.loads(building.coordinates) if building.coordinates else {}
        })
    
    return result

@router.get("/{slug}", response_model=BuildingBase)
def get_building_by_slug(slug: str, db: Session = Depends(get_db)):
    building = db.query(Building).filter(Building.slug == slug).first()
    
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    return {
        "id": building.id,
        "slug": building.slug,
        "name": building.name,
        "department": building.department,
        "description": building.description,
        "facilities": building.facilities,
        "coordinates": json.loads(building.coordinates) if building.coordinates else {}
    }

@router.put("/{slug}", response_model=BuildingBase)
def update_building(slug: str, building_data: BuildingBase, db: Session = Depends(get_db)):
    building = db.query(Building).filter(Building.slug == slug).first()
    
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    # Update all fields.
    building.slug = building_data.slug
    building.name = building_data.name
    building.department = building_data.department
    building.description = building_data.description
    building.facilities = building_data.facilities
    building.coordinates = json.dumps(building_data.coordinates)
    
    db.commit()
    db.refresh(building)
    
    return {
        "id": building.id,
        "slug": building.slug,
        "name": building.name,
        "department": building.department,
        "description": building.description,
        "facilities": building.facilities,
        "coordinates": json.loads(building.coordinates) if building.coordinates else {}
    }

@router.patch("/{slug}", response_model=BuildingBase)
def partially_update_building(slug: str, building_data: BuildingUpdate, db: Session = Depends(get_db)):
    building = db.query(Building).filter(Building.slug == slug).first()
    
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    # Update only the provided fields.
    for key, value in building_data.dict(exclude_unset=True).items():
        if key == "coordinates" and value is not None:
            setattr(building, key, json.dumps(value))
        elif hasattr(building, key) and key != "id":
            setattr(building, key, value)
    
    db.commit()
    db.refresh(building)
    
    return {
        "id": building.id,
        "slug": building.slug,
        "name": building.name,
        "department": building.department,
        "description": building.description,
        "facilities": building.facilities,
        "coordinates": json.loads(building.coordinates) if building.coordinates else {}
    }
