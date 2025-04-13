import os
import shutil
from fastapi import UploadFile, HTTPException
import aiofiles
from typing import Optional

# Configure these variables according to your project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, "static", "images", "buildings")
# Use relative URL that will work in any deployment
IMAGE_BASE_URL = "/images/buildings"

# Ensure the images directory exists
os.makedirs(IMAGES_DIR, exist_ok=True)

async def save_image(file: UploadFile, slug: str) -> str:
    """Save an uploaded image and return its URL."""
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Get file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ['.jpg', '.jpeg', '.png', '.gif']:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    # Create filename based on slug
    filename = f"{slug}{file_ext}"
    file_path = os.path.join(IMAGES_DIR, filename)
    
    # Save the file
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save image: {str(e)}")
    
    # Return the URL
    return f"{IMAGE_BASE_URL}/{filename}"

def delete_image(slug: str) -> bool:
    """Delete an image for a given slug if it exists."""
    for ext in ['.jpg', '.jpeg', '.png', '.gif']:
        file_path = os.path.join(IMAGES_DIR, f"{slug}{ext}")
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    return False

def get_image_url(slug: str) -> Optional[str]:
    """Get the URL for an image with the given slug if it exists."""
    for ext in ['.jpg', '.jpeg', '.png', '.gif']:
        file_path = os.path.join(IMAGES_DIR, f"{slug}{ext}")
        if os.path.exists(file_path):
            return f"{IMAGE_BASE_URL}/{slug}{ext}"
    return None