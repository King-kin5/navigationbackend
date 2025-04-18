from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend import seed_data
from fastapi.staticfiles import StaticFiles
from backend.database.config import init_database, test_database_connection
from backend.routes import building
from backend.core.config import settings
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)

def create_application() -> FastAPI:
    """Application factory function"""
    # Create FastAPI app instance
    app = FastAPI(
        title="Navigation system",
        description="Navigation",
        version="0.1.0",
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins in development
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )
    
    # Create static directories
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, "static")
    os.makedirs(os.path.join(STATIC_DIR, "images", "buildings"), exist_ok=True)
    
    # Mount static files
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    
    # Include the API routes
    app.include_router(building.router, prefix="/api", tags=["buildings"])
    
    return app

# Create the application
app = create_application()

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    try:
        init_database()
        if not test_database_connection():
            logger.error("Failed to connect to database during startup")
            raise Exception("Database connection failed")
        logger.info("Application startup complete")
    except Exception as e:
        logger.error(f"Application startup failed: {e}")
        raise
    try:
        seed_data.seed_database()
        logger.info("Database seeded successfully")
    except Exception as e:
        logger.error(f"Error seeding database: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    try:
        logger.info("Application shutdown complete")
    except Exception as e:
        logger.error(f"Application shutdown failed: {e}")
        raise

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )