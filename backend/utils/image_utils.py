import os
import shutil
from fastapi import UploadFile, HTTPException
import aiofiles
from typing import Optional
import uuid
from PIL import Image
import io

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

async def process_uploaded_image(file: UploadFile) -> tuple[str, bytes, str]:
    """
    Process an uploaded image file and return (filename, binary_data, mime_type)
    """
    try:
        # Read file content
        contents = await file.read()
        
        # Detect MIME type
        mime_type = "image/png"  # Default
        if file.content_type:
            mime_type = file.content_type
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{file_extension}"
        
        # Optimize image if possible
        try:
            # Open image with PIL
            img = Image.open(io.BytesIO(contents))
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                img = img.convert('RGB')
            
            # Optimize image
            output = io.BytesIO()
            img.save(output, format='JPEG' if mime_type == 'image/jpeg' else 'PNG', 
                    quality=85, optimize=True)
            optimized_data = output.getvalue()
        except Exception:
            # If optimization fails, use original data
            optimized_data = contents
        
        return filename, optimized_data, mime_type
        
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")

def validate_image_file(file: UploadFile) -> bool:
    """
    Validate if the uploaded file is an image
    """
    if not file.content_type:
        return False
    
    allowed_types = ['image/jpeg', 'image/png', 'image/gif']
    return file.content_type in allowed_types