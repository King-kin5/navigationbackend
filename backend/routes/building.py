from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Response
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
from typing import Optional, List
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
    name: str = Form(...),
    department: str = Form(...),
    description: str = Form(...),
    facilities: str = Form(...),
    coordinates: str = Form(...),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # Generate slug from name
    slug = slugify(name)
    
    # Check for existing building
    existing = db.query(Building).filter(Building.slug == slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Building with this slug already exists")

    # Process image if uploaded
    image_filename = None
    image_url = None
    
    if file:
        try:
            # Validate image file
            if not validate_image_file(file):
                raise HTTPException(status_code=400, detail="Invalid image file type")
            
            # Process the image
            filename, image_data, mime_type = await process_uploaded_image(file)
            
            # Create building object with image data
            building = Building(
                id=slug,
                slug=slug,
                name=name,
                department=department,
                description=description,
                image=filename,  # Store filename
                image_data=image_data,  # Store binary data
                mime_type=mime_type,  # Store MIME type
                facilities=json.loads(facilities),
                coordinates=json.loads(coordinates)
            )
            
            # Save to database
            db.add(building)
            db.commit()
            db.refresh(building)
            
            # Generate image URL
            image_url = f"/api/buildings/image/{filename}"
            
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
    else:
        # Create building without image
        building = Building(
            id=slug,
            slug=slug,
            name=name,
            department=department,
            description=description,
            facilities=json.loads(facilities),
            coordinates=json.loads(coordinates)
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
        "image": image_url,
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
    name: Optional[str] = Form(None),
    department: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    facilities: Optional[List[str]] = Form(None),
    coordinates: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None, description="Optional image file"),
    db: Session = Depends(get_db)
):
    building = db.query(Building).filter(Building.slug == slug).first()
    
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
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
    if name is not None:
        building.name = name
    if department is not None:
        building.department = department
    if description is not None:
        building.description = description
    if facilities is not None:
        building.facilities = facilities
    if coordinates is not None:
        try:
            building.coordinates = json.loads(coordinates)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid coordinates format")
    
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
