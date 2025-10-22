"""
Trend analysis endpoints for content scoring and ranking
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from typing import List
import asyncio

from app.models.schemas import (
    TrendAnalysisRequest,
    TrendAnalysisResponse,
    Item
)
from app.core.trends import TrendService
from app.api.v1.auth import get_current_user_id, get_jwt_token

router = APIRouter()

@router.post("/trends/analysis", response_model=TrendAnalysisResponse)
async def analyze_trends(
    request: TrendAnalysisRequest,
    user_id: str = Depends(get_current_user_id),
    jwt_token: str = Depends(get_jwt_token)
):
    """
    Analyze content trends and return top trending items
    """
    try:
        trend_service = TrendService(jwt_token)
        
        # Get trending items for the user
        trending_items = await trend_service.get_trending_items(
            user_id=user_id,
            time_window_hours=request.time_window_hours,
            limit=request.limit
        )
        
        # Calculate trend metadata
        analysis_metadata = await trend_service.get_analysis_metadata(
            user_id=user_id,
            time_window_hours=request.time_window_hours
        )
        
        return TrendAnalysisResponse(
            trending_items=trending_items,
            analysis_metadata=analysis_metadata
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze trends: {str(e)}")

@router.get("/trends/score/{item_id}")
async def get_item_trend_score(item_id: str):
    """Get trend score for a specific item"""
    try:
        trend_service = TrendService()
        score = await trend_service.get_item_score(item_id)
        return {"item_id": item_id, "trend_score": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get trend score: {str(e)}")

@router.post("/trends/recalculate")
async def recalculate_trends(user_id: str):
    """Recalculate trend scores for all items"""
    try:
        trend_service = TrendService()
        result = await trend_service.recalculate_all_scores(user_id)
        return {
            "message": "Trend scores recalculated",
            "items_processed": result.get("items_processed", 0),
            "time_taken": result.get("time_taken", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to recalculate trends: {str(e)}")

@router.get("/trends/keywords")
async def get_trending_keywords(user_id: str, limit: int = 10):
    """Get trending keywords across user's content"""
    try:
        trend_service = TrendService()
        keywords = await trend_service.get_trending_keywords(user_id, limit)
        return {"trending_keywords": keywords}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get trending keywords: {str(e)}")
