from typing import List, Optional, Dict, Any
import json
import os
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from fastapi import Depends

from backend.database.base import get_db
from backend.database.models.building import BuildingORM
from backend.service.building.model import Building, Coordinates



class BuildingRepository:
    """Repository for building data access"""
    
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
    
    async def get_all_buildings(self) -> List[Building]:
        """Get all buildings from the database"""
        buildings_orm = self.db.query(BuildingORM).all()
        return [self._convert_orm_to_model(b) for b in buildings_orm]
    
    async def get_building_by_id(self, building_id: str) -> Optional[Building]:
        """Get a specific building by ID"""
        building_orm = self.db.query(BuildingORM).filter(BuildingORM.id == building_id).first()
        if not building_orm:
            return None
        return self._convert_orm_to_model(building_orm)
    
    async def search_buildings_by_name(self, name_query: str) -> List[Building]:
        """Search buildings by name using database text search"""
        query = f"%{name_query}%"  # For LIKE operator
        buildings_orm = self.db.query(BuildingORM).filter(
            or_(
                BuildingORM.name.ilike(query),
                BuildingORM.short_name.ilike(query)
            )
        ).all()
        return [self._convert_orm_to_model(b) for b in buildings_orm]
    
    async def get_buildings_by_category(self, category: str) -> List[Building]:
        """Get buildings filtered by category"""
        buildings_orm = self.db.query(BuildingORM).filter(BuildingORM.category == category).all()
        return [self._convert_orm_to_model(b) for b in buildings_orm]
    
    async def get_buildings_by_department(self, department: str) -> List[Building]:
        """Get buildings filtered by department"""
        buildings_orm = self.db.query(BuildingORM).filter(BuildingORM.department == department).all()
        return [self._convert_orm_to_model(b) for b in buildings_orm]
    
    async def create_building(self, building: Building) -> Building:
        """Create a new building record"""
        building_orm = self._convert_model_to_orm(building)
        self.db.add(building_orm)
        self.db.commit()
        self.db.refresh(building_orm)
        return self._convert_orm_to_model(building_orm)
    
    async def update_building(self, building_id: str, building_data: Dict[str, Any]) -> Optional[Building]:
        """Update an existing building"""
        building_orm = self.db.query(BuildingORM).filter(BuildingORM.id == building_id).first()
        if not building_orm:
            return None
            
        # Update the ORM object with new data
        for key, value in building_data.items():
            if hasattr(building_orm, key):
                setattr(building_orm, key, value)
        
        building_orm.last_updated = datetime.now()
        self.db.commit()
        self.db.refresh(building_orm)
        return self._convert_orm_to_model(building_orm)
    
    async def delete_building(self, building_id: str) -> bool:
        """Delete a building by ID"""
        building_orm = self.db.query(BuildingORM).filter(BuildingORM.id == building_id).first()
        if not building_orm:
            return False
            
        self.db.delete(building_orm)
        self.db.commit()
        return True
    
    def _convert_orm_to_model(self, building_orm: BuildingORM) -> Building:
        """Convert ORM object to Pydantic model"""
        # Extract coordinate data from JSON
        coordinates_data = json.loads(building_orm.primary_coordinates)
        
        # Create a Building model
        return Building(
            id=building_orm.id,
            name=building_orm.name,
            short_name=building_orm.short_name,
            description=building_orm.description,
            primary_coordinates=Coordinates(**coordinates_data),
            department=building_orm.department,
            category=building_orm.category,
            facilities=json.loads(building_orm.facilities) if building_orm.facilities else [],
            keywords=json.loads(building_orm.keywords) if building_orm.keywords else [],
            #image_url=building_orm.image_url,
            #thumbnail_url=building_orm.thumbnail_url,
            entrances=json.loads(building_orm.entrances) if building_orm.entrances else [],
            floors=json.loads(building_orm.floors) if building_orm.floors else [],
            opening_hours=json.loads(building_orm.opening_hours) if building_orm.opening_hours else None,
            metadata=json.loads(building_orm.metadata) if building_orm.metadata else {},
            last_updated=building_orm.last_updated
        )
    
    def _convert_model_to_orm(self, building: Building) -> BuildingORM:
        """Convert Pydantic model to ORM object"""
        return BuildingORM(
            id=building.id,
            name=building.name,
            short_name=building.short_name,
            description=building.description,
            primary_coordinates=json.dumps(building.primary_coordinates.dict()),
            department=building.department,
            category=building.category,
            facilities=json.dumps(building.facilities) if building.facilities else None,
            keywords=json.dumps(building.keywords) if building.keywords else None,
            #image_url=building.image_url,
            #thumbnail_url=building.thumbnail_url,
            entrances=json.dumps([e.dict() for e in building.entrances]) if building.entrances else None,
            floors=json.dumps([f.dict() for f in building.floors]) if building.floors else None,
            opening_hours=json.dumps(building.opening_hours.dict()) if building.opening_hours else None,
            metadata=json.dumps(building.metadata) if building.metadata else None,
            last_updated=building.last_updated
        )


# Dependency to get a repository instance
def get_building_repository(db: Session = Depends(get_db)) -> BuildingRepository:
    return BuildingRepository(db)