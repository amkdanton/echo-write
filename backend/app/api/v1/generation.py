"""
Newsletter generation endpoints
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Header
from typing import List, Optional

from app.models.schemas import (
    GenerationRequest,
    GenerationResponse,
    Draft,
    DraftCreate
)
from app.core.generation import GenerationService
from app.api.v1.auth import get_current_user_id, get_jwt_token

router = APIRouter()

@router.post("/generation/newsletter")
async def generate_newsletter(
    request: GenerationRequest,
    user_id: str = Depends(get_current_user_id),
    jwt_token: str = Depends(get_jwt_token)
):
    """
    Generate AI-powered newsletter from trending content
    """
    try:
        generation_service = GenerationService(jwt_token)
        
        # Generate newsletter synchronously (it's fast enough)
        result = await generation_service.generate_newsletter(
            user_id=user_id,
            title=request.custom_prompt if request.custom_prompt else None,
            num_items=len(request.trending_items) if request.trending_items else 5,
            time_window_hours=48
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate newsletter: {str(e)}")

@router.get("/generation/drafts", response_model=List[Draft])
async def get_drafts(
    limit: int = 20, 
    status: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    jwt_token: str = Depends(get_jwt_token)
):
    """Get user's newsletter drafts"""
    try:
        generation_service = GenerationService(jwt_token)
        drafts = await generation_service.get_user_drafts(user_id, limit, status)
        return drafts
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get drafts: {str(e)}")

@router.get("/generation/drafts/{draft_id}", response_model=Draft)
async def get_draft(draft_id: str, user_id: str):
    """Get a specific draft by ID"""
    try:
        generation_service = GenerationService()
        draft = await generation_service.get_draft(draft_id, user_id)
        
        if not draft:
            raise HTTPException(status_code=404, detail="Draft not found")
        
        return draft
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get draft: {str(e)}")

@router.put("/generation/drafts/{draft_id}")
async def update_draft(draft_id: str, user_id: str, draft_data: DraftCreate):
    """Update a draft"""
    try:
        generation_service = GenerationService()
        updated_draft = await generation_service.update_draft(draft_id, user_id, draft_data)
        return {"message": "Draft updated successfully", "draft": updated_draft}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update draft: {str(e)}")

@router.delete("/generation/drafts/{draft_id}")
async def delete_draft(draft_id: str, user_id: str):
    """Delete a draft"""
    try:
        generation_service = GenerationService()
        await generation_service.delete_draft(draft_id, user_id)
        return {"message": "Draft deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete draft: {str(e)}")

@router.post("/generation/regenerate/{draft_id}")
async def regenerate_draft(draft_id: str, user_id: str):
    """Regenerate a draft with current trending content"""
    try:
        generation_service = GenerationService()
        new_draft = await generation_service.regenerate_draft(draft_id, user_id)
        return {"message": "Draft regenerated successfully", "draft": new_draft}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to regenerate draft: {str(e)}")

@router.get("/generation/status/{job_id}")
async def get_generation_status(job_id: str):
    """Get status of a newsletter generation job"""
    try:
        generation_service = GenerationService()
        status = await generation_service.get_generation_status(job_id)
        return status
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get generation status: {str(e)}")
