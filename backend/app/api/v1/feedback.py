"""
Feedback endpoints for newsletter improvement
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional

from app.models.schemas import (
    FeedbackCreate,
    Feedback
)
from app.core.feedback import FeedbackService

router = APIRouter()

@router.post("/feedback", response_model=Feedback)
async def submit_feedback(feedback: FeedbackCreate):
    """
    Submit feedback for a newsletter draft
    """
    try:
        feedback_service = FeedbackService()
        
        # Create feedback record
        new_feedback = await feedback_service.create_feedback(feedback)
        
        # Process feedback for learning (background task)
        await feedback_service.process_feedback_for_learning(feedback.draft_id)
        
        return new_feedback
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit feedback: {str(e)}")

@router.get("/feedback/draft/{draft_id}", response_model=List[Feedback])
async def get_draft_feedback(draft_id: str):
    """Get all feedback for a specific draft"""
    try:
        feedback_service = FeedbackService()
        feedback_list = await feedback_service.get_draft_feedback(draft_id)
        return feedback_list
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get draft feedback: {str(e)}")

@router.get("/feedback/user/{user_id}", response_model=List[Feedback])
async def get_user_feedback(user_id: str, limit: int = 20):
    """Get feedback history for a user"""
    try:
        feedback_service = FeedbackService()
        feedback_list = await feedback_service.get_user_feedback(user_id, limit)
        return feedback_list
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user feedback: {str(e)}")

@router.get("/feedback/analytics/{user_id}")
async def get_feedback_analytics(user_id: str, days: int = 30):
    """Get feedback analytics and insights"""
    try:
        feedback_service = FeedbackService()
        analytics = await feedback_service.get_feedback_analytics(user_id, days)
        return analytics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get feedback analytics: {str(e)}")

@router.put("/feedback/{feedback_id}")
async def update_feedback(feedback_id: str, notes: Optional[str] = None):
    """Update feedback notes"""
    try:
        feedback_service = FeedbackService()
        updated_feedback = await feedback_service.update_feedback(feedback_id, notes)
        return {"message": "Feedback updated successfully", "feedback": updated_feedback}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update feedback: {str(e)}")

@router.delete("/feedback/{feedback_id}")
async def delete_feedback(feedback_id: str, user_id: str):
    """Delete feedback"""
    try:
        feedback_service = FeedbackService()
        await feedback_service.delete_feedback(feedback_id, user_id)
        return {"message": "Feedback deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete feedback: {str(e)}")

@router.post("/feedback/learn")
async def trigger_learning_from_feedback(user_id: str):
    """Trigger learning process from recent feedback"""
    try:
        feedback_service = FeedbackService()
        result = await feedback_service.trigger_learning_process(user_id)
        return {
            "message": "Learning process triggered successfully",
            "feedback_processed": result.get("feedback_count", 0),
            "improvements_suggested": result.get("improvements", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger learning: {str(e)}")
