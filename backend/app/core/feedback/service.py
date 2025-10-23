"""
Feedback collection and analysis service
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from app.core.database import get_user_supabase
from app.models.schemas import FeedbackCreate, Feedback
import logging

logger = logging.getLogger(__name__)

class FeedbackService:
    def __init__(self, jwt_token: str):
        self.supabase = get_user_supabase(jwt_token)
    
    async def create_feedback(self, feedback: FeedbackCreate, user_id: str) -> Feedback:
        """Create feedback record"""
        try:
            # Insert feedback into database
            response = self.supabase.table("feedback").insert({
                "user_id": user_id,
                "draft_id": feedback.draft_id,
                "reaction": feedback.reaction,
                "notes": feedback.notes,
                "metadata": {}
            }).execute()
            
            if not response.data:
                raise ValueError("Failed to create feedback")
            
            feedback_data = response.data[0]
            return Feedback(
                id=feedback_data["id"],
                draft_id=feedback_data["draft_id"],
                reaction=feedback_data["reaction"],
                notes=feedback_data["notes"],
                user_id=feedback_data["user_id"],
                created_at=feedback_data["created_at"]
            )
            
        except Exception as e:
            logger.error(f"Error creating feedback: {e}")
            raise
    
    async def process_feedback_for_learning(self, draft_id: str) -> None:
        """Process feedback for learning and improvement"""
        # Placeholder implementation for MVP
        pass
    
    async def get_draft_feedback(self, draft_id: str) -> List[Feedback]:
        """Get all feedback for a specific draft"""
        try:
            response = self.supabase.table("feedback").select("*").eq("draft_id", draft_id).order("created_at", desc=True).execute()
            
            return [
                Feedback(
                    id=item["id"],
                    draft_id=item["draft_id"],
                    reaction=item["reaction"],
                    notes=item["notes"],
                    user_id=item["user_id"],
                    created_at=item["created_at"]
                )
                for item in response.data
            ]
        except Exception as e:
            logger.error(f"Error getting draft feedback: {e}")
            return []
    
    async def get_user_feedback(self, user_id: str, limit: int = 20) -> List[Feedback]:
        """Get feedback history for a user"""
        try:
            response = self.supabase.table("feedback").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(limit).execute()
            
            return [
                Feedback(
                    id=item["id"],
                    draft_id=item["draft_id"],
                    reaction=item["reaction"],
                    notes=item["notes"],
                    user_id=item["user_id"],
                    created_at=item["created_at"]
                )
                for item in response.data
            ]
        except Exception as e:
            logger.error(f"Error getting user feedback: {e}")
            return []
    
    async def get_feedback_analytics(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get feedback analytics and insights"""
        try:
            # Get feedback from the last N days
            from datetime import datetime, timedelta
            cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
            
            response = self.supabase.table("feedback").select("*").eq("user_id", user_id).gte("created_at", cutoff_date).execute()
            
            total_feedback = len(response.data)
            positive_count = len([f for f in response.data if f["reaction"] in ["👍", "positive"]])
            positive_ratio = positive_count / total_feedback if total_feedback > 0 else 0.0
            
            return {
                "total_feedback": total_feedback,
                "positive_ratio": positive_ratio,
                "improvement_areas": []
            }
        except Exception as e:
            logger.error(f"Error getting feedback analytics: {e}")
            return {
                "total_feedback": 0,
                "positive_ratio": 0.0,
                "improvement_areas": []
            }
    
    async def update_feedback(self, feedback_id: str, notes: Optional[str] = None) -> Feedback:
        """Update feedback notes"""
        try:
            # Update feedback in database
            response = self.supabase.table("feedback").update({
                "notes": notes
            }).eq("id", feedback_id).execute()
            
            if not response.data:
                raise ValueError("Feedback not found")
            
            feedback_data = response.data[0]
            return Feedback(
                id=feedback_data["id"],
                draft_id=feedback_data["draft_id"],
                reaction=feedback_data["reaction"],
                notes=feedback_data["notes"],
                user_id=feedback_data["user_id"],
                created_at=feedback_data["created_at"]
            )
        except Exception as e:
            logger.error(f"Error updating feedback: {e}")
            raise
    
    async def delete_feedback(self, feedback_id: str, user_id: str) -> None:
        """Delete feedback"""
        try:
            # Delete feedback from database
            response = self.supabase.table("feedback").delete().eq("id", feedback_id).eq("user_id", user_id).execute()
            
            if not response.data:
                raise ValueError("Feedback not found or not authorized")
                
        except Exception as e:
            logger.error(f"Error deleting feedback: {e}")
            raise
    
    async def trigger_learning_process(self, user_id: str) -> Dict[str, Any]:
        """Trigger learning process from recent feedback"""
        # Placeholder implementation for MVP
        return {
            "feedback_count": 0,
            "improvements": []
        }
