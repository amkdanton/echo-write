"""
Content ingestion endpoints for RSS, YouTube, and Twitter feeds
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Header
from typing import List, Optional
import asyncio

from app.models.schemas import (
    IngestionRequest, 
    IngestionResponse,
    SourceCreate,
    SourceUpdate,
    Source,
    SourceType
)
from app.core.ingestion import IngestionService
from app.api.v1.auth import get_current_user_id, get_jwt_token

router = APIRouter()

@router.post("/ingestion/process", response_model=IngestionResponse)
async def process_feeds(
    request: IngestionRequest,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(get_current_user_id),
    jwt_token: str = Depends(get_jwt_token)
):
    """
    Process RSS, YouTube, and Twitter feeds to extract content items
    """
    try:
        ingestion_service = IngestionService(jwt_token)
        
        # Process feeds in background for better performance
        background_tasks.add_task(
            ingestion_service.process_feeds,
            request.source_ids,
            request.force_refresh
        )
        
        # Return immediate response
        return IngestionResponse(
            processed_sources=len(request.source_ids),
            new_items=0,  # Will be updated by background task
            errors=[]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process feeds: {str(e)}")

@router.get("/ingestion/sources", response_model=List[Source])
async def get_sources(
    user_id: str = Depends(get_current_user_id),
    jwt_token: str = Depends(get_jwt_token)
):
    """Get all configured sources for a user"""
    try:
        ingestion_service = IngestionService(jwt_token)
        sources = await ingestion_service.get_user_sources(user_id)
        return sources
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch sources: {str(e)}")

@router.post("/ingestion/sources", response_model=Source)
async def create_source(
    source: SourceCreate, 
    user_id: str = Depends(get_current_user_id),
    jwt_token: str = Depends(get_jwt_token)
):
    """Add a new content source"""
    try:
        ingestion_service = IngestionService(jwt_token)
        new_source = await ingestion_service.create_source(user_id, source)
        return new_source
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create source: {str(e)}")

@router.put("/ingestion/sources/{source_id}", response_model=Source)
async def update_source(
    source_id: str,
    source_update: SourceUpdate,
    user_id: str = Depends(get_current_user_id),
    jwt_token: str = Depends(get_jwt_token)
):
    """Update a content source (name, is_active, fetch_frequency)"""
    try:
        ingestion_service = IngestionService(jwt_token)
        updated_source = await ingestion_service.update_source(user_id, source_id, source_update.dict(exclude_unset=True))
        return updated_source
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update source: {str(e)}")

@router.delete("/ingestion/sources/{source_id}")
async def delete_source(
    source_id: str, 
    user_id: str = Depends(get_current_user_id),
    jwt_token: str = Depends(get_jwt_token)
):
    """Delete a content source"""
    try:
        ingestion_service = IngestionService(jwt_token)
        await ingestion_service.delete_source(user_id, source_id)
        return {"message": "Source deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete source: {str(e)}")

@router.post("/ingestion/test/{source_id}")
async def test_source(
    source_id: str, 
    user_id: str = Depends(get_current_user_id),
    jwt_token: str = Depends(get_jwt_token)
):
    """Test a source connection and fetch sample items"""
    try:
        ingestion_service = IngestionService(jwt_token)
        result = await ingestion_service.test_source(user_id, source_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to test source: {str(e)}")

@router.get("/ingestion/sources/{source_id}/items")
async def get_source_items(
    source_id: str,
    limit: int = 10,
    user_id: str = Depends(get_current_user_id),
    jwt_token: str = Depends(get_jwt_token)
):
    """Get recent items from a specific source"""
    try:
        ingestion_service = IngestionService(jwt_token)
        items = await ingestion_service.get_source_items(user_id, source_id, limit)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get items: {str(e)}")

@router.get("/ingestion/status")
async def get_ingestion_status():
    """Get current ingestion status and queue information"""
    try:
        ingestion_service = IngestionService()
        status = await ingestion_service.get_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")
