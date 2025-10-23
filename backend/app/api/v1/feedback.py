"""
Feedback endpoints for newsletter improvement
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional

from app.models.schemas import (
    FeedbackCreate,
    Feedback
)
from app.core.feedback import FeedbackService
from app.api.v1.auth import get_current_user_id, get_jwt_token

router = APIRouter()

@router.post("/feedback", response_model=Feedback)
async def submit_feedback(
    feedback: FeedbackCreate,
    user_id: str = Depends(get_current_user_id),
    jwt_token: str = Depends(get_jwt_token)
):
    """
    Submit feedback for a newsletter draft
    """
    try:
        feedback_service = FeedbackService(jwt_token)
        
        # Create feedback record
        new_feedback = await feedback_service.create_feedback(feedback, user_id)
        
        # Process feedback for learning (background task)
        await feedback_service.process_feedback_for_learning(feedback.draft_id)
        
        return new_feedback
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit feedback: {str(e)}")

@router.get("/feedback/public", response_model=dict)
async def submit_public_feedback(
    draft_id: str,
    reaction: str,
    source: str = "email"
):
    """
    Submit feedback from email recipients (public endpoint)
    """
    try:
        # Validate reaction
        if reaction not in ['👍', '👎', 'positive', 'negative']:
            raise HTTPException(status_code=400, detail="Invalid reaction")
        
        # Convert to emoji format
        emoji_reaction = '👍' if reaction in ['👍', 'positive'] else '👎'
        
        # Get the draft to find the user_id
        from app.core.database import get_supabase
        supabase = get_supabase()
        
        draft_response = supabase.table("drafts").select("user_id").eq("id", draft_id).execute()
        if not draft_response.data:
            raise HTTPException(status_code=404, detail="Draft not found")
        
        user_id = draft_response.data[0]["user_id"]
        
        # Create feedback record using service account
        feedback_data = {
            "user_id": user_id,
            "draft_id": draft_id,
            "reaction": emoji_reaction,
            "notes": f"Feedback from {source}",
            "metadata": {"source": source}
        }
        
        response = supabase.table("feedback").insert(feedback_data).execute()
        
        if not response.data:
            raise ValueError("Failed to create feedback")
        
        # Return HTML page for better user experience
        html_response = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Thank You for Your Feedback!</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    margin: 0;
                    padding: 0;
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                .container {{
                    background: white;
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    text-align: center;
                    max-width: 500px;
                    margin: 20px;
                }}
                .emoji {{
                    font-size: 4rem;
                    margin-bottom: 20px;
                }}
                h1 {{
                    color: #1f2937;
                    margin-bottom: 15px;
                    font-size: 2rem;
                }}
                p {{
                    color: #6b7280;
                    font-size: 1.1rem;
                    line-height: 1.6;
                    margin-bottom: 30px;
                }}
                .button {{
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 12px 30px;
                    border-radius: 10px;
                    text-decoration: none;
                    font-weight: 600;
                    transition: transform 0.3s ease;
                }}
                .button:hover {{
                    transform: translateY(-2px);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="emoji">{emoji_reaction}</div>
                <h1>Thank You for Your Feedback!</h1>
                <p>Your feedback helps us improve future newsletters. We appreciate you taking the time to share your thoughts!</p>
                <a href="https://echowrite.ai" class="button">Visit EchoWrite</a>
            </div>
        </body>
        </html>
        """
        
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=html_response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit feedback: {str(e)}")

@router.get("/feedback/draft/{draft_id}", response_model=List[Feedback])
async def get_draft_feedback(
    draft_id: str,
    jwt_token: str = Depends(get_jwt_token)
):
    """Get all feedback for a specific draft"""
    try:
        feedback_service = FeedbackService(jwt_token)
        feedback_list = await feedback_service.get_draft_feedback(draft_id)
        return feedback_list
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get draft feedback: {str(e)}")

@router.get("/feedback/user/{user_id}", response_model=List[Feedback])
async def get_user_feedback(
    user_id: str, 
    limit: int = 20,
    jwt_token: str = Depends(get_jwt_token)
):
    """Get feedback history for a user"""
    try:
        feedback_service = FeedbackService(jwt_token)
        feedback_list = await feedback_service.get_user_feedback(user_id, limit)
        return feedback_list
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user feedback: {str(e)}")

@router.get("/feedback/analytics/{user_id}")
async def get_feedback_analytics(
    user_id: str, 
    days: int = 30,
    jwt_token: str = Depends(get_jwt_token)
):
    """Get feedback analytics and insights"""
    try:
        feedback_service = FeedbackService(jwt_token)
        analytics = await feedback_service.get_feedback_analytics(user_id, days)
        return analytics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get feedback analytics: {str(e)}")

@router.put("/feedback/{feedback_id}")
async def update_feedback(
    feedback_id: str, 
    notes: Optional[str] = None,
    jwt_token: str = Depends(get_jwt_token)
):
    """Update feedback notes"""
    try:
        feedback_service = FeedbackService(jwt_token)
        updated_feedback = await feedback_service.update_feedback(feedback_id, notes)
        return {"message": "Feedback updated successfully", "feedback": updated_feedback}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update feedback: {str(e)}")

@router.delete("/feedback/{feedback_id}")
async def delete_feedback(
    feedback_id: str, 
    user_id: str,
    jwt_token: str = Depends(get_jwt_token)
):
    """Delete feedback"""
    try:
        feedback_service = FeedbackService(jwt_token)
        await feedback_service.delete_feedback(feedback_id, user_id)
        return {"message": "Feedback deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete feedback: {str(e)}")

@router.post("/feedback/learn")
async def trigger_learning_from_feedback(
    user_id: str,
    jwt_token: str = Depends(get_jwt_token)
):
    """Trigger learning process from recent feedback"""
    try:
        feedback_service = FeedbackService(jwt_token)
        result = await feedback_service.trigger_learning_process(user_id)
        return {
            "message": "Learning process triggered successfully",
            "feedback_processed": result.get("feedback_count", 0),
            "improvements_suggested": result.get("improvements", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger learning: {str(e)}")
