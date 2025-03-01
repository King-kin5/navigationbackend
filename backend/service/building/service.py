from typing import List, Optional, Dict, Tuple
import re
from backend.core.repository import get_building_repository
from backend.service.building.model import Building, BuildingSearchResult, Coordinates
from fuzzywuzzy import fuzz, process
from geopy.distance import geodesic
from fastapi import Depends




class BuildingSearchService:
    def __init__(self, building_repository=Depends(get_building_repository)):
        self.building_repository = building_repository
    
    async def search_buildings(
        self,
        query: str,
        current_location: Optional[Coordinates] = None,
        limit: int = 10,
        category: Optional[str] = None,
        department: Optional[str] = None
    ) -> List[BuildingSearchResult]:
        """
        Search for buildings based on name, description, and keywords.
        Optionally filter by category, department and sort by distance from current location.
        """
        if not query and not category and not department:
            # If no search criteria provided, return buildings near the user
            if current_location:
                return await self._get_nearest_buildings(current_location, limit)
            else:
                # Return a default set of popular/important buildings
                return await self._get_popular_buildings(limit)
        
        # Get all buildings (in a real app, implement pagination or database query filters)
        all_buildings = await self.building_repository.get_all_buildings()
        
        # Apply category and department filters if specified
        filtered_buildings = all_buildings
        if category:
            filtered_buildings = [b for b in filtered_buildings if b.category == category]
        if department:
            filtered_buildings = [b for b in filtered_buildings if b.department == department]
        
        # If there's no text query, just apply filters
        if not query:
            return self._convert_to_search_results(filtered_buildings, current_location, limit)
        
        # Score buildings based on the search query
        scored_buildings = self._score_buildings_by_query(filtered_buildings, query)
        
        # Sort by score (highest first) and take the top results
        sorted_buildings = [building for _, building in sorted(
            scored_buildings, key=lambda x: x[0], reverse=True
        )]
        
        # Convert to search results format
        return self._convert_to_search_results(sorted_buildings, current_location, limit)
    
    def _score_buildings_by_query(self, buildings: List[Building], query: str) -> List[Tuple[float, Building]]:
        """Score buildings based on their match to the search query"""
        query = query.lower()
        query_tokens = set(re.findall(r'\w+', query))
        scored_buildings = []
        
        for building in buildings:
            score = 0
            
            # Check exact matches first (highest priority)
            if query == building.name.lower() or query == building.short_name.lower():
                score = 100
            else:
                # Name match (high priority) using fuzzy matching
                name_score = fuzz.partial_ratio(query, building.name.lower())
                short_name_score = 0
                if building.short_name:
                    short_name_score = fuzz.partial_ratio(query, building.short_name.lower())
                score = max(score, max(name_score, short_name_score))
                
                # Keyword matches (medium priority)
                keyword_scores = [fuzz.ratio(query, keyword.lower()) for keyword in building.keywords]
                if keyword_scores:
                    keyword_score = max(keyword_scores)
                    score = max(score, keyword_score * 0.7)  # Slightly lower priority
                
                # Description match (lower priority)
                if building.description:
                    desc_score = fuzz.partial_ratio(query, building.description.lower())
                    score = max(score, desc_score * 0.5)  # Lower priority
                
                # Check for token matches (words in the query)
                for token in query_tokens:
                    if token in building.name.lower() or (building.short_name and token in building.short_name.lower()):
                        score = max(score, 80)
                    elif any(token in keyword.lower() for keyword in building.keywords):
                        score = max(score, 70)
            
            scored_buildings.append((score, building))
        
        return scored_buildings
    
    async def _get_nearest_buildings(self, location: Coordinates, limit: int) -> List[BuildingSearchResult]:
        """Get buildings nearest to the specified location"""
        all_buildings = await self.building_repository.get_all_buildings()
        return self._convert_to_search_results(all_buildings, location, limit)
    
    async def _get_popular_buildings(self, limit: int) -> List[BuildingSearchResult]:
        """Get popular or important buildings (could be based on usage analytics)"""
        # This would be replaced with actual logic in a real system
        all_buildings = await self.building_repository.get_all_buildings()
        # Here you might sort by a popularity metric or return a predefined list
        return self._convert_to_search_results(all_buildings, None, limit)
    
    def _convert_to_search_results(
        self, 
        buildings: List[Building], 
        current_location: Optional[Coordinates] = None,
        limit: int = 10
    ) -> List[BuildingSearchResult]:
        """Convert Building models to BuildingSearchResult and calculate distances if location provided"""
        results = []
        
        for building in buildings:
            # Calculate distance if current location is provided
            distance = None
            if current_location:
                distance = geodesic(
                    (current_location.latitude, current_location.longitude),
                    (building.primary_coordinates.latitude, building.primary_coordinates.longitude)
                ).kilometers
            
            result = BuildingSearchResult(
                id=building.id,
                name=building.name,
                short_name=building.short_name,
                description=building.description,
                primary_coordinates=building.primary_coordinates,
                category=building.category,
                department=building.department,
                thumbnail_url=building.thumbnail_url,
                distance=distance
            )
            results.append(result)
        
        # Sort by distance if available
        if current_location:
            results.sort(key=lambda x: x.distance if x.distance is not None else float('inf'))
        
        # Return the top results
        return results[:limit]