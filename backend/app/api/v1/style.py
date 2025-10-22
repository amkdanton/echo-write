"""
Voice training and style analysis endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import List

from app.models.schemas import (
    StyleTrainingRequest,
    StyleTrainingResponse,
    VoiceProfile,
    StyleSampleCreate
)
from app.core.style import StyleService

router = APIRouter()

@router.post("/style/train", response_model=StyleTrainingResponse)
async def train_voice(request: StyleTrainingRequest):
    """
    Train AI voice model using user's writing samples
    """
    try:
        style_service = StyleService()
        
        # Process and analyze writing samples
        voice_profile = await style_service.train_voice(
            user_id=request.user_id,
            samples=request.samples
        )
        
        return StyleTrainingResponse(
            voice_profile=voice_profile,
            confidence_score=voice_profile.confidence
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to train voice: {str(e)}")

@router.get("/style/profile", response_model=VoiceProfile)
async def get_voice_profile(user_id: str):
    """Get user's current voice profile"""
    try:
        style_service = StyleService()
        profile = await style_service.get_voice_profile(user_id)
        
        if not profile:
            raise HTTPException(status_code=404, detail="Voice profile not found")
        
        return profile
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get voice profile: {str(e)}")

@router.post("/style/samples")
async def add_style_sample(user_id: str, sample: StyleSampleCreate):
    """Add a new writing sample for voice training"""
    try:
        style_service = StyleService()
        result = await style_service.add_style_sample(user_id, sample)
        return {"message": "Sample added successfully", "sample_id": result.get("id")}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add sample: {str(e)}")

@router.delete("/style/samples/{sample_id}")
async def delete_style_sample(sample_id: str, user_id: str):
    """Delete a writing sample"""
    try:
        style_service = StyleService()
        await style_service.delete_style_sample(user_id, sample_id)
        return {"message": "Sample deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete sample: {str(e)}")

@router.get("/style/samples", response_model=List[StyleSampleCreate])
async def get_style_samples(user_id: str):
    """Get all writing samples for a user"""
    try:
        style_service = StyleService()
        samples = await style_service.get_style_samples(user_id)
        return samples
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get samples: {str(e)}")

@router.post("/style/retrain")
async def retrain_voice(user_id: str):
    """Retrain voice profile with existing samples"""
    try:
        style_service = StyleService()
        result = await style_service.retrain_voice(user_id)
        return {
            "message": "Voice profile retrained successfully",
            "confidence_score": result.get("confidence", 0),
            "traits": result.get("traits", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrain voice: {str(e)}")
