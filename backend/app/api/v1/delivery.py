"""
Newsletter delivery endpoints
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Header
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.models.schemas import DeliveryResponse
from app.core.delivery import DeliveryService
from app.api.v1.auth import get_current_user_id, get_jwt_token

router = APIRouter()


class SendNewsletterRequest(BaseModel):
    draft_id: str
    recipient_email: EmailStr
    send_immediately: bool = True


@router.post("/delivery/send", response_model=DeliveryResponse)
async def send_newsletter(
    request: SendNewsletterRequest,
    user_id: str = Depends(get_current_user_id),
    jwt_token: str = Depends(get_jwt_token)
):
    """
    Send newsletter via email
    
    Requires authentication. Sends the specified draft to the recipient email.
    """
    try:
        delivery_service = DeliveryService(jwt_token=jwt_token)
        
        # Send email
        result = await delivery_service.send_newsletter(
            draft_id=request.draft_id,
            user_id=user_id,
            recipient_email=request.recipient_email,
            send_immediately=request.send_immediately
        )
        
        return DeliveryResponse(
            success=True,
            delivery_id=result.get("delivery_id"),
            error=None
        )
        
    except Exception as e:
        return DeliveryResponse(
            success=False,
            delivery_id=None,
            error=str(e)
        )

@router.get("/delivery/status/{delivery_id}")
async def get_delivery_status(delivery_id: str):
    """Get delivery status for a newsletter"""
    try:
        delivery_service = DeliveryService()
        status = await delivery_service.get_delivery_status(delivery_id)
        return status
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get delivery status: {str(e)}")

@router.post("/delivery/schedule")
async def schedule_delivery(
    draft_id: str,
    scheduled_time: str,
    user_id: str
):
    """Schedule newsletter delivery for a specific time"""
    try:
        delivery_service = DeliveryService()
        result = await delivery_service.schedule_delivery(draft_id, scheduled_time, user_id)
        return {
            "message": "Newsletter scheduled successfully",
            "scheduled_time": scheduled_time,
            "job_id": result.get("job_id")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to schedule delivery: {str(e)}")

@router.delete("/delivery/schedule/{job_id}")
async def cancel_scheduled_delivery(job_id: str, user_id: str):
    """Cancel a scheduled newsletter delivery"""
    try:
        delivery_service = DeliveryService()
        await delivery_service.cancel_scheduled_delivery(job_id, user_id)
        return {"message": "Scheduled delivery cancelled successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel delivery: {str(e)}")

@router.get("/delivery/history")
async def get_delivery_history(
    limit: int = 20,
    user_id: str = Depends(get_current_user_id),
    jwt_token: str = Depends(get_jwt_token)
):
    """Get delivery history for a user"""
    try:
        delivery_service = DeliveryService(jwt_token=jwt_token)
        history = await delivery_service.get_delivery_history(user_id, limit)
        return {"delivery_history": history}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get delivery history: {str(e)}")


class TestEmailRequest(BaseModel):
    email: EmailStr


@router.post("/delivery/test")
async def test_delivery(
    request: TestEmailRequest,
    user_id: str = Depends(get_current_user_id),
    jwt_token: str = Depends(get_jwt_token)
):
    """Send a test email to verify delivery settings"""
    try:
        delivery_service = DeliveryService(jwt_token=jwt_token)
        result = await delivery_service.send_test_email(user_id, request.email)
        return {
            "message": "Test email sent successfully",
            "delivery_id": result.get("delivery_id"),
            "sent_to": result.get("sent_to")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send test email: {str(e)}")
