from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Response, Body, Request
from sqlalchemy.orm import Session
import json
import base64
import uuid
import os
from backend.database.base import get_db
from backend.database.models.building import Building
from backend.database.models.schema import BuildingBase, BuildingCreate, BuildingUpdate
from backend.seed_data import slugify
from backend.utils.image_utils import process_uploaded_image, validate_image_file
from typing import Optional, List, Dict
from fastapi.staticfiles import StaticFiles

router = APIRouter()

# Add a new endpoint for image upload

# Add endpoint to serve the image from database


# Add endpoint to delete an image
@router.delete("/{slug}/image")
def delete_building_image(slug: str, db: Session = Depends(get_db)):
    # Check if building exists
    building = db.query(Building).filter(Building.slug == slug).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    # Update database record
    if building.image:
        building.image = None
        db.commit()
        db.refresh(building)
        return {"message": "Image deleted successfully"}
    
    raise HTTPException(status_code=404, detail="No image found to delete")

@router.post("/buildings/create", response_model=BuildingBase)
async def create_building(
    building_data: BuildingCreate,
    db: Session = Depends(get_db)
):
    # Generate slug from name
    slug = slugify(building_data.name)
    
    # Check for existing building
    existing = db.query(Building).filter(Building.slug == slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Building with this slug already exists")

    # Create building object
    building = Building(
        id=slug,
        slug=slug,
        name=building_data.name,
        department=building_data.department,
        description=building_data.description or "",
        facilities=building_data.facilities or [],
        coordinates=building_data.coordinates or {"lat": 0, "lng": 0}
    )
    
    try:
        db.add(building)
        db.commit()
        db.refresh(building)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving building: {str(e)}")

    return {
        "id": building.id,
        "slug": building.slug,
        "name": building.name,
        "department": building.department,
        "description": building.description,
        "image": None,
        "facilities": building.facilities,
        "coordinates": building.coordinates
    }

@router.post("/buildings/{slug}/image", response_model=BuildingBase)
async def add_building_image(
    slug: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Find the building
    building = db.query(Building).filter(Building.slug == slug).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")

    try:
        # Validate image file
        if not validate_image_file(file):
            raise HTTPException(status_code=400, detail="Invalid image file type")
        
        # Process the image
        filename, image_data, mime_type = await process_uploaded_image(file)
        
        # Update building with image data
        building.image = filename
        building.image_data = image_data
        building.mime_type = mime_type
        
        db.commit()
        db.refresh(building)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    return {
        "id": building.id,
        "slug": building.slug,
        "name": building.name,
        "department": building.department,
        "description": building.description,
        "image": f"/api/buildings/image/{building.image}",
        "facilities": building.facilities,
        "coordinates": building.coordinates
    }

@router.get("/buildings/image/{filename}")
async def get_building_image(filename: str, db: Session = Depends(get_db)):
    # Find building with this image filename
    building = db.query(Building).filter(Building.image == filename).first()
    
    if not building or not building.image_data:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return Response(
        content=building.image_data,
        media_type=building.mime_type or "image/png"
    )

@router.get("/buildings", response_model=list[BuildingBase])
def get_all_buildings(db: Session = Depends(get_db)):
    buildings = db.query(Building).all()
    
    result = []
    for building in buildings:
        # Generate image URL if image_data exists
        image_url = None
        if building.image_data:
            image_url = f"/api/buildings/image/{building.image}"
        
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
    
    # Generate image URL if image_data exists
    image_url = None
    if building.image_data:
        image_url = f"/api/buildings/image/{building.image}"
    
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
async def update_building(
    slug: str,
    request: Request,
    file: Optional[UploadFile] = File(None, description="Optional image file"),
    db: Session = Depends(get_db)
):
    building = db.query(Building).filter(Building.slug == slug).first()
    
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    # Get JSON data from request body
    try:
        data = await request.json()
    except Exception:
        data = {}
    
    # Process image if uploaded
    if file and file.filename:
        try:
            # Validate image file
            if not validate_image_file(file):
                raise HTTPException(status_code=400, detail="Invalid image file type")
            
            # Process the image
            filename, image_data, mime_type = await process_uploaded_image(file)
            
            # Update building with new image data
            building.image = filename
            building.image_data = image_data
            building.mime_type = mime_type
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
    
    # Update only the fields that were provided
    if "name" in data:
        building.name = data["name"]
    if "department" in data:
        building.department = data["department"]
    if "description" in data:
        building.description = data["description"]
    if "facilities" in data:
        building.facilities = data["facilities"]
    if "coordinates" in data:
        coords = data["coordinates"]
        if not isinstance(coords, dict):
            raise HTTPException(status_code=400, detail="Coordinates must be a dictionary")
        if "lat" not in coords or "lng" not in coords:
            raise HTTPException(status_code=400, detail="Coordinates must contain 'lat' and 'lng' keys")
        if not isinstance(coords["lat"], (int, float)) or not isinstance(coords["lng"], (int, float)):
            raise HTTPException(status_code=400, detail="Coordinates values must be numbers")
        building.coordinates = coords
    
    db.commit()
    db.refresh(building)
    
    # Generate image URL
    image_url = f"/api/buildings/image/{building.image}" if building.image_data else None
    
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

@router.put("/{slug}/data", response_model=BuildingBase)
async def update_building_data(
    slug: str,
    name: Optional[str] = Body(None),
    department: Optional[str] = Body(None),
    description: Optional[str] = Body(None),
    facilities: Optional[List[str]] = Body(None),
    coordinates: Optional[Dict[str, float]] = Body(None),
    db: Session = Depends(get_db)
):
    # Find the building
    building = db.query(Building).filter(Building.slug == slug).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")

    # Update only the provided fields
    if name is not None:
        building.name = name
        # Update slug if name changes
        building.slug = slugify(name)
    if department is not None:
        building.department = department
    if description is not None:
        building.description = description
    if facilities is not None:
        building.facilities = facilities
    if coordinates is not None:
        building.coordinates = coordinates

    try:
        db.commit()
        db.refresh(building)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating building: {str(e)}")

    return {
        "id": building.id,
        "slug": building.slug,
        "name": building.name,
        "department": building.department,
        "description": building.description,
        "image": f"/api/buildings/image/{building.image}" if building.image else None,
        "facilities": building.facilities,
        "coordinates": building.coordinates
    }
