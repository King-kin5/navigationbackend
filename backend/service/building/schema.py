from typing import Optional, List
from pydantic import BaseModel, Field


class UserLocation(BaseModel):
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")


class SearchQuery(BaseModel):
    query: Optional[str] = Field(None, description="Search text")
    current_location: Optional[UserLocation] = Field(None, description="User's current coordinates")
    category: Optional[str] = Field(None, description="Filter by building category")
    department: Optional[str] = Field(None, description="Filter by department")
    limit: Optional[int] = Field(10, ge=1, le=50, description="Maximum number of results")


class RouteRequest(BaseModel):
    start_location: UserLocation = Field(..., description="Starting coordinates")
    end_building_id: str = Field(..., description="Destination building ID")
    accessible_route: bool = Field(False, description="Require wheelchair accessible route")
    avoid_stairs: bool = Field(False, description="Avoid routes with stairs")
    prefer_indoor: bool = Field(False, description="Prefer indoor routes when available")


class RouteStep(BaseModel):
    instruction: str
    distance: float
    duration: float  # in seconds
    start_location: UserLocation
    end_location: UserLocation
    maneuver: Optional[str] = None
    indoor: bool = False


class RouteResponse(BaseModel):
    total_distance: float  # in meters
    total_duration: float  # in seconds
    start_location: UserLocation
    end_location: UserLocation
    steps: List[RouteStep]
    is_accessible: bool
    has_stairs: bool
    is_indoor: bool