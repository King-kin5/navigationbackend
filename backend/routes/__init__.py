from fastapi import APIRouter
from .building import router as building_router

api_router = APIRouter()

# Include all routes
api_router.include_router(building_router, prefix="/api/buildings", tags=["buildings"]) 