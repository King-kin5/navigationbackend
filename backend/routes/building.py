from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Response
from sqlalchemy.orm import Session
import json
from backend.database.base import get_db
from backend.database.models.building import Building
from backend.database.models.schema import BuildingBase, BuildingCreate, BuildingUpdate
from backend.seed_data import slugify
from backend.utils.image_utils import save_image, delete_image, get_image_url
from typing import Optional

router = APIRouter()

# Add a new endpoint for image upload
@router.post("/{slug}/upload-image", response_model=BuildingBase)
async def upload_building_image(
    slug: str, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    building = db.query(Building).filter(Building.slug == slug).first()
    
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    # Save the image and get its URL
    image_url = await save_image(file, slug)
    
    # Update the building with the new image URL
    building.image = image_url
    db.commit()
    db.refresh(building)
    
    return {
        "id": building.id,
        "slug": building.slug,
        "name": building.name,
        "department": building.department,
        "description": building.description,
        "image": building.image,
        "facilities": building.facilities,
        "coordinates": building.coordinates if building.coordinates else {}
    }

# Add endpoint to get image URL for a building
@router.get("/{slug}/image")
def get_building_image(slug: str, db: Session = Depends(get_db)):
    # First check if building exists
    building = db.query(Building).filter(Building.slug == slug).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    # Get image URL from database first
    if building.image:
        return {"image_url": building.image}
    
    # Try to get from filesystem
    image_url = get_image_url(slug)
    if not image_url:
        raise HTTPException(status_code=404, detail="Image not found for this building")
    
    return {"image_url": image_url}

# Add endpoint to delete an image
@router.delete("/{slug}/image")
def delete_building_image(slug: str, db: Session = Depends(get_db)):
    # First check if building exists
    building = db.query(Building).filter(Building.slug == slug).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    # Delete image file
    deleted = delete_image(slug)
    
    # Update database record
    if building.image:
        building.image = None
        db.commit()
        db.refresh(building)
        return {"message": "Image deleted successfully"}
    
    if not deleted:
        raise HTTPException(status_code=404, detail="No image found to delete")
    
    return {"message": "Image deleted successfully"}

@router.post("/create", response_model=BuildingBase)
def create_building(building_data: BuildingCreate, db: Session = Depends(get_db)):
    # Generate a slug from the building name.
    slug = slugify(building_data.name)
    
    # Check if a building with the same slug already exists.
    existing = db.query(Building).filter(Building.slug == slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Building with this slug already exists")
    
    # If no image is provided, try to get one from the filesystem
    image_url = building_data.image
    if not image_url:
        image_url = get_image_url(slug)
    
    # Create a new Building instance.
    building = Building(
        id=slug,
        slug=slug,
        name=building_data.name,
        department=building_data.department,
        description=building_data.description,
        image=image_url,
        facilities=building_data.facilities,
        coordinates=building_data.coordinates  # Store directly as dict
    )
    db.add(building)
    db.commit()
    db.refresh(building)
    
    # Return the building data
    return {
        "id": building.id,
        "slug": building.slug,
        "name": building.name,
        "department": building.department,
        "description": building.description,
        "image": building.image,
        "facilities": building.facilities,
        "coordinates": building.coordinates if building.coordinates else {}
    }

@router.get("/", response_model=list[BuildingBase])
def get_all_buildings(db: Session = Depends(get_db)):
    buildings = db.query(Building).all()
    
    result = []
    for building in buildings:
        # If no image in database, try to get from filesystem
        image_url = building.image
        if not image_url:
            image_url = get_image_url(building.slug)
            
            # If image found, update the database
            if image_url and not building.image:
                building.image = image_url
                db.commit()
        
        result.append({
            "id": building.id,
            "slug": building.slug,
            "name": building.name,
            "department": building.department,
            "description": building.description,
            "image": image_url,
            "facilities": building.facilities,
            "coordinates": building.coordinates if building.coordinates else {}
        })
    
    return result

@router.get("/{slug}", response_model=BuildingBase)
def get_building_by_slug(slug: str, db: Session = Depends(get_db)):
    building = db.query(Building).filter(Building.slug == slug).first()
    
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    # If no image in database, try to get from filesystem
    image_url = building.image
    if not image_url:
        image_url = get_image_url(slug)
        
        # If image found, update the database
        if image_url:
            building.image = image_url
            db.commit()
            db.refresh(building)
    
    return {
        "id": building.id,
        "slug": building.slug,
        "name": building.name,
        "department": building.department,
        "description": building.description,
        "image": image_url,
        "facilities": building.facilities,
        "coordinates": building.coordinates if building.coordinates else {}
    }

@router.put("/{slug}", response_model=BuildingBase)
def update_building(slug: str, building_data: BuildingBase, db: Session = Depends(get_db)):
    building = db.query(Building).filter(Building.slug == slug).first()
    
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    # Check if we need to update the image
    image_url = building_data.image
    if not image_url:
        image_url = get_image_url(building_data.slug)
    
    # Update all fields.
    building.slug = building_data.slug
    building.name = building_data.name
    building.department = building_data.department
    building.description = building_data.description
    building.image = image_url
    building.facilities = building_data.facilities
    building.coordinates = building_data.coordinates  # Store directly as dict
    
    db.commit()
    db.refresh(building)
    
    return {
        "id": building.id,
        "slug": building.slug,
        "name": building.name,
        "department": building.department,
        "description": building.description,
        "image": building.image,
        "facilities": building.facilities,
        "coordinates": building.coordinates if building.coordinates else {}
    }

@router.patch("/{slug}", response_model=BuildingBase)
def partially_update_building(slug: str, building_data: BuildingUpdate, db: Session = Depends(get_db)):
    building = db.query(Building).filter(Building.slug == slug).first()
    
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    # Update only the provided fields.
    for key, value in building_data.dict(exclude_unset=True).items():
        if key == "coordinates" and value is not None:
            setattr(building, key, value)  # Store directly as dict
        elif hasattr(building, key) and key != "id":
            setattr(building, key, value)
    
    # If slug changed, check if we need to update the image
    if hasattr(building_data, "slug") and building_data.slug and building_data.slug != slug:
        if not building.image:
            image_url = get_image_url(building_data.slug)
            if image_url:
                building.image = image_url
    
    db.commit()
    db.refresh(building)
    
    return {
        "id": building.id,
        "slug": building.slug,
        "name": building.name,
        "department": building.department,
        "description": building.description,
        "image": building.image,
        "facilities": building.facilities,
        "coordinates": building.coordinates if building.coordinates else {}
    }