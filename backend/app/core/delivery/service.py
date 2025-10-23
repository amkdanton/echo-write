"""
Email delivery service using Resend
"""

import os
import resend
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

from app.core.database import get_supabase, get_user_supabase
from .templates import get_newsletter_html_template, markdown_to_email_html

logger = logging.getLogger(__name__)

# Configure Resend
resend.api_key = os.getenv("RESEND_API_KEY")

class DeliveryService:
    def __init__(self, jwt_token: str = None):
        if jwt_token:
            self.supabase = get_user_supabase(jwt_token)
        else:
            self.supabase = get_supabase()
    
    async def send_newsletter(
        self, 
        draft_id: str, 
        user_id: str,
        recipient_email: str,
        send_immediately: bool = True
    ) -> Dict[str, Any]:
        """
        Send newsletter via email using Resend
        
        Args:
            draft_id: ID of the draft to send
            user_id: ID of the user sending the newsletter
            recipient_email: Email address to send to
            send_immediately: Whether to send immediately or schedule
        
        Returns:
            Dictionary with success status and delivery info
        """
        try:
            # Get draft content
            draft_response = self.supabase.table("drafts").select("*").eq("id", draft_id).eq("user_id", user_id).execute()
            
            if not draft_response.data:
                raise Exception("Draft not found or not owned by user")
            
            draft = draft_response.data[0]
            
            # Convert markdown to HTML
            newsletter_body_html = markdown_to_email_html(draft.get("body_md", ""))
            newsletter_title = draft.get("title", "Your Newsletter")
            
            # Generate complete email HTML
            email_html = get_newsletter_html_template(
                newsletter_title=newsletter_title,
                newsletter_body_html=newsletter_body_html,
                unsubscribe_url="#",  # TODO: Implement unsubscribe functionality
                draft_id=draft_id
            )
            
            # Send email via Resend
            logger.info(f"Sending newsletter {draft_id} to {recipient_email}")
            
            params = {
                "from": "EchoWrite <newsletter@resend.dev>",  # Update with your verified domain
                "to": [recipient_email],
                "subject": newsletter_title,
                "html": email_html,
            }
            
            email_result = resend.Emails.send(params)
            
            # Update draft status
            self.supabase.table("drafts").update({
                "status": "sent",
                "sent_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }).eq("id", draft_id).execute()
            
            # Log delivery
            delivery_record = {
                "draft_id": draft_id,
                "user_id": user_id,
                "recipient_email": recipient_email,
                "resend_email_id": email_result.get("id"),
                "status": "sent",
                "sent_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Newsletter sent successfully: {email_result}")
            
            return {
                "success": True,
                "delivery_id": email_result.get("id"),
                "message": "Newsletter sent successfully",
                "sent_to": recipient_email
            }
            
        except Exception as e:
            logger.error(f"Failed to send newsletter: {str(e)}")
            raise Exception(f"Failed to send newsletter: {str(e)}")
    
    async def get_delivery_status(self, delivery_id: str) -> Dict[str, Any]:
        """Get delivery status for a newsletter"""
        try:
            # In a production environment, you'd query Resend's API or your database
            # For now, return basic status
            return {
                "status": "delivered",
                "delivered_at": datetime.utcnow().isoformat(),
                "recipients": 1
            }
        except Exception as e:
            logger.error(f"Failed to get delivery status: {str(e)}")
            return {
                "status": "unknown",
                "error": str(e)
            }
    
    async def schedule_delivery(self, draft_id: str, scheduled_time: str, user_id: str) -> Dict[str, Any]:
        """Schedule newsletter delivery for a specific time"""
        # TODO: Implement with APScheduler or Celery
        return {
            "job_id": f"scheduled_{draft_id}",
            "scheduled_time": scheduled_time,
            "message": "Scheduling not yet implemented"
        }
    
    async def cancel_scheduled_delivery(self, job_id: str, user_id: str) -> None:
        """Cancel a scheduled newsletter delivery"""
        # TODO: Implement with APScheduler or Celery
        pass
    
    async def get_delivery_history(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get delivery history for a user"""
        try:
            # Get sent drafts
            response = self.supabase.table("drafts").select("*").eq("user_id", user_id).eq("status", "sent").order("sent_at", desc=True).limit(limit).execute()
            
            return response.data
        except Exception as e:
            logger.error(f"Failed to get delivery history: {str(e)}")
            return []
    
    async def send_test_email(self, user_id: str, email: str) -> Dict[str, Any]:
        """Send a test email to verify delivery settings"""
        try:
            test_html = get_newsletter_html_template(
                newsletter_title="Test Email from EchoWrite",
                newsletter_body_html="""
                    <h2>🎉 Your Email Setup is Working!</h2>
                    <p>This is a test email to verify that your EchoWrite newsletter delivery is configured correctly.</p>
                    <p>You're all set to start sending beautiful newsletters! ✨</p>
                """,
                unsubscribe_url="#"
            )
            
            params = {
                "from": "EchoWrite <newsletter@resend.dev>",
                "to": [email],
                "subject": "Test Email from EchoWrite",
                "html": test_html,
            }
            
            email_result = resend.Emails.send(params)
            
            return {
                "delivery_id": email_result.get("id"),
                "message": "Test email sent successfully",
                "sent_to": email
            }
        except Exception as e:
            logger.error(f"Failed to send test email: {str(e)}")
            raise Exception(f"Failed to send test email: {str(e)}")
