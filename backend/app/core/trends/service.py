"""
Trend analysis service for content scoring and ranking
"""

import math
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

from app.core.database import get_supabase, get_user_supabase
from app.models.schemas import Item

logger = logging.getLogger(__name__)

class TrendService:
    def __init__(self, jwt_token: str = None):
        if jwt_token:
            self.supabase = get_user_supabase(jwt_token)
        else:
            self.supabase = get_supabase()
    
    async def get_trending_items(
        self, 
        user_id: str, 
        time_window_hours: int = 48, 
        limit: int = 20
    ) -> List[Item]:
        """Get trending items for a user within specified time window"""
        try:
            # Get items from user's sources within time window
            cutoff_time = datetime.utcnow() - timedelta(hours=time_window_hours)
            
            # First get user's sources
            sources_response = self.supabase.table("sources").select("id").eq("user_id", user_id).execute()
            source_ids = [source["id"] for source in sources_response.data]
            
            if not source_ids:
                return []
            
            # Then get items from those sources
            response = self.supabase.table("items").select("*").in_(
                "source_id", source_ids
            ).gte(
                "published_at", cutoff_time.isoformat()
            ).order("published_at", desc=True).limit(limit * 2).execute()
            
            items = [Item(**item) for item in response.data]
            
            # Calculate trend scores
            for item in items:
                item.trend_score = await self._calculate_trend_score(item)
            
            # Sort by trend score and return top items
            items.sort(key=lambda x: x.trend_score or 0, reverse=True)
            return items[:limit]
            
        except Exception as e:
            logger.error(f"Error getting trending items: {e}")
            raise
    
    async def _calculate_trend_score(self, item: Item) -> float:
        """Calculate comprehensive trend score for an item"""
        try:
            # 1. Recency Score (40% weight)
            published_at = datetime.fromisoformat(item.published_at.replace('Z', '+00:00'))
            hours_ago = (datetime.utcnow() - published_at).total_seconds() / 3600
            
            # Exponential decay with different time windows
            if hours_ago <= 1:
                recency_score = 1.0  # Very recent (last hour)
            elif hours_ago <= 6:
                recency_score = 0.9  # Recent (last 6 hours)
            elif hours_ago <= 24:
                recency_score = math.exp(-hours_ago / 12)  # Decay over 12 hours
            elif hours_ago <= 72:
                recency_score = math.exp(-hours_ago / 36)  # Decay over 36 hours
            else:
                recency_score = math.exp(-hours_ago / 168)  # Decay over 7 days
            
            # 2. Content Quality Score (25% weight)
            quality_score = self._calculate_content_quality(item)
            
            # 3. Keyword Relevance Score (20% weight)
            relevance_score = self._calculate_keyword_relevance(item)
            
            # 4. Source Authority Score (10% weight)
            authority_score = self._calculate_source_authority(item)
            
            # 5. Engagement Prediction Score (5% weight)
            engagement_score = self._predict_engagement(item)
            
            # Weighted combination
            trend_score = (
                recency_score * 0.40 +
                quality_score * 0.25 +
                relevance_score * 0.20 +
                authority_score * 0.10 +
                engagement_score * 0.05
            )
            
            # Apply trending boost for items with high scores
            if trend_score > 0.8:
                trend_score = min(trend_score * 1.1, 1.0)  # 10% boost for high-quality content
            
            return min(max(trend_score, 0), 1)
            
        except Exception as e:
            logger.error(f"Error calculating trend score: {e}")
            return 0.5  # Default score
    
    def _calculate_content_quality(self, item: Item) -> float:
        """Calculate content quality score based on title and summary"""
        try:
            score = 0.5  # Base score
            
            # Title quality indicators
            title = item.title or ""
            if len(title) > 20 and len(title) < 100:  # Optimal title length
                score += 0.1
            if any(word in title.lower() for word in ['breaking', 'exclusive', 'update', 'announces']):
                score += 0.1  # News value indicators
            
            # Summary quality
            summary = item.summary or ""
            if len(summary) > 100:  # Substantial content
                score += 0.1
            if len(summary) > 300:  # Detailed content
                score += 0.1
            
            # URL quality indicators
            url = item.url or ""
            if any(domain in url.lower() for domain in ['techcrunch.com', 'cnn.com', 'bbc.com', 'reuters.com']):
                score += 0.1  # Known quality sources
            
            return min(score, 1.0)
            
        except Exception:
            return 0.5
    
    def _calculate_keyword_relevance(self, item: Item) -> float:
        """Calculate keyword relevance score"""
        try:
            # Trending technology keywords
            tech_keywords = [
                'ai', 'artificial intelligence', 'machine learning', 'blockchain',
                'cryptocurrency', 'bitcoin', 'ethereum', 'nft', 'metaverse',
                'vr', 'ar', 'quantum', '5g', 'iot', 'cybersecurity',
                'startup', 'venture capital', 'ipo', 'merger', 'acquisition'
            ]
            
            # Combine title and summary for analysis
            content = f"{item.title or ''} {item.summary or ''}".lower()
            
            # Count keyword matches
            matches = sum(1 for keyword in tech_keywords if keyword in content)
            
            # Score based on keyword density
            if matches == 0:
                return 0.3  # No trending keywords
            elif matches == 1:
                return 0.6  # Some relevance
            elif matches >= 2:
                return 0.9  # High relevance
            else:
                return 0.5
                
        except Exception:
            return 0.5
    
    def _calculate_source_authority(self, item: Item) -> float:
        """Calculate source authority score"""
        try:
            url = item.url or ""
            domain = url.split('/')[2].lower() if '//' in url else ""
            
            # Authority scores for known domains
            authority_map = {
                'techcrunch.com': 0.95,
                'cnn.com': 0.90,
                'bbc.com': 0.90,
                'reuters.com': 0.95,
                'bloomberg.com': 0.90,
                'wsj.com': 0.90,
                'nytimes.com': 0.85,
                'wired.com': 0.85,
                'theverge.com': 0.80,
                'arstechnica.com': 0.80,
                'engadget.com': 0.75,
                'mashable.com': 0.70,
                'medium.com': 0.60,
                'substack.com': 0.65,
            }
            
            return authority_map.get(domain, 0.5)  # Default for unknown domains
            
        except Exception:
            return 0.5
    
    def _predict_engagement(self, item: Item) -> float:
        """Predict engagement based on content characteristics"""
        try:
            score = 0.5  # Base score
            
            title = item.title or ""
            summary = item.summary or ""
            
            # Engagement indicators in title
            if any(word in title.lower() for word in ['how', 'why', 'what', 'when', 'where']):
                score += 0.1  # Question-based titles
            
            if any(word in title.lower() for word in ['top', 'best', 'worst', 'amazing', 'shocking']):
                score += 0.1  # Emotional/clickbait indicators
            
            if any(word in title.lower() for word in ['guide', 'tutorial', 'tips', 'tricks']):
                score += 0.1  # Educational content
            
            # Length-based predictions
            if 50 < len(summary) < 500:  # Optimal length for engagement
                score += 0.1
            
            return min(score, 1.0)
            
        except Exception:
            return 0.5
    
    async def get_item_score(self, item_id: str) -> float:
        """Get trend score for a specific item"""
        try:
            response = self.supabase.table("items").select("*").eq("id", item_id).execute()
            if not response.data:
                raise ValueError(f"Item {item_id} not found")
            
            item = Item(**response.data[0])
            return await self._calculate_trend_score(item)
            
        except Exception as e:
            logger.error(f"Error getting item score: {e}")
            raise
    
    async def recalculate_all_scores(self, user_id: str) -> Dict[str, Any]:
        """Recalculate trend scores for all items from user's sources"""
        start_time = datetime.utcnow()
        
        try:
            # Get all items from user's sources
            response = self.supabase.table("items").select("""
                *,
                sources!inner(user_id)
            """).eq("sources.user_id", user_id).execute()
            
            items = [Item(**item) for item in response.data]
            processed_count = 0
            
            # Update scores for each item
            for item in items:
                new_score = await self._calculate_trend_score(item)
                
                # Update in database
                self.supabase.table("items").update({
                    "trend_score": new_score,
                    "updated_at": datetime.utcnow().isoformat()
                }).eq("id", item.id).execute()
                
                processed_count += 1
            
            end_time = datetime.utcnow()
            time_taken = (end_time - start_time).total_seconds()
            
            return {
                "items_processed": processed_count,
                "time_taken": time_taken
            }
            
        except Exception as e:
            logger.error(f"Error recalculating scores: {e}")
            raise
    
    async def get_trending_keywords(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get trending keywords across user's content"""
        try:
            # This would implement keyword extraction and frequency analysis
            # For now, return mock data
            return [
                {"keyword": "AI", "frequency": 15, "trend": "up"},
                {"keyword": "machine learning", "frequency": 12, "trend": "up"},
                {"keyword": "blockchain", "frequency": 8, "trend": "down"},
                {"keyword": "cloud computing", "frequency": 10, "trend": "stable"},
                {"keyword": "cybersecurity", "frequency": 7, "trend": "up"},
            ][:limit]
            
        except Exception as e:
            logger.error(f"Error getting trending keywords: {e}")
            raise
    
    async def get_analysis_metadata(
        self, 
        user_id: str, 
        time_window_hours: int
    ) -> Dict[str, Any]:
        """Get metadata about the trend analysis"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=time_window_hours)
            
            # Get statistics
            response = self.supabase.table("items").select("""
                *,
                sources!inner(user_id)
            """).eq("sources.user_id", user_id).gte(
                "published_at", cutoff_time.isoformat()
            ).execute()
            
            total_items = len(response.data)
            avg_score = sum(item.get("trend_score", 0.5) for item in response.data) / max(total_items, 1)
            
            return {
                "analysis_time": datetime.utcnow().isoformat(),
                "time_window_hours": time_window_hours,
                "total_items_analyzed": total_items,
                "average_trend_score": round(avg_score, 3),
                "analysis_version": "1.0"
            }
            
        except Exception as e:
            logger.error(f"Error getting analysis metadata: {e}")
            return {
                "analysis_time": datetime.utcnow().isoformat(),
                "time_window_hours": time_window_hours,
                "error": str(e)
            }
