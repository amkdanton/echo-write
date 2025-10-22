"""
Content ingestion service for RSS, YouTube, and Twitter feeds
"""

import asyncio
import feedparser
import httpx
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

from app.core.database import get_supabase, get_user_supabase
from app.models.schemas import Source, SourceCreate, Item, ItemCreate, SourceType

logger = logging.getLogger(__name__)

class IngestionService:
    def __init__(self, jwt_token: str = None):
        if jwt_token:
            self.supabase = get_user_supabase(jwt_token)
        else:
            self.supabase = get_supabase()
    
    async def process_feeds(self, source_ids: List[str], force_refresh: bool = False) -> Dict[str, Any]:
        """Process multiple feeds concurrently"""
        results = {
            "processed_sources": 0,
            "new_items": 0,
            "errors": []
        }
        
        # Create tasks for concurrent processing
        tasks = []
        for source_id in source_ids:
            task = self.process_single_feed(source_id, force_refresh)
            tasks.append(task)
        
        # Execute all tasks concurrently
        feed_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Aggregate results
        for result in feed_results:
            if isinstance(result, Exception):
                results["errors"].append(str(result))
                logger.error(f"Feed processing error: {result}")
            else:
                results["processed_sources"] += 1
                results["new_items"] += result.get("new_items", 0)
                if result.get("error"):
                    results["errors"].append(result["error"])
        
        return results
    
    async def process_single_feed(self, source_id: str, force_refresh: bool = False) -> Dict[str, Any]:
        """Process a single feed source"""
        try:
            # Get source details
            source_response = self.supabase.table("sources").select("*").eq("id", source_id).execute()
            if not source_response.data:
                raise ValueError(f"Source {source_id} not found")
            
            source = source_response.data[0]
            source_type = source["type"]
            
            # Check if we need to refresh (skip if recent and not forced)
            if not force_refresh:
                last_fetched_at = source.get("last_fetched_at")
                if last_fetched_at:
                    # Use source's fetch_frequency (in seconds), default to 1 hour
                    fetch_frequency_seconds = source.get("fetch_frequency", 3600)
                    
                    last_fetched_dt = datetime.fromisoformat(last_fetched_at.replace('Z', '+00:00'))
                    time_since_fetch = (datetime.utcnow() - last_fetched_dt).total_seconds()
                    
                    if time_since_fetch < fetch_frequency_seconds:
                        logger.info(f"Skipping source {source['name']}: fetched {time_since_fetch:.0f}s ago, frequency is {fetch_frequency_seconds}s")
                        return {
                            "new_items": 0, 
                            "message": f"Skipped - fetched {time_since_fetch:.0f}s ago (frequency: {fetch_frequency_seconds}s)"
                        }
            
            # Process based on source type
            if source_type == SourceType.RSS:
                return await self._process_rss_feed(source)
            elif source_type == SourceType.YOUTUBE:
                return await self._process_youtube_feed(source)
            elif source_type == SourceType.TWITTER:
                return await self._process_twitter_feed(source)
            else:
                raise ValueError(f"Unsupported source type: {source_type}")
                
        except Exception as e:
            logger.error(f"Error processing feed {source_id}: {e}")
            return {"error": str(e), "new_items": 0}
    
    async def _process_rss_feed(self, source: Dict[str, Any]) -> Dict[str, Any]:
        """Process RSS feed"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(source["handle"])
                response.raise_for_status()
                
                # Parse RSS feed
                feed = feedparser.parse(response.text)
                
                if feed.bozo:
                    logger.warning(f"RSS feed parsing warning: {feed.bozo_exception}")
                
                new_items = 0
                for entry in feed.entries[:20]:  # Limit to 20 most recent items
                    # Extract item data
                    item_data = {
                        "title": entry.get("title", ""),
                        "url": entry.get("link", ""),
                        "summary": self._extract_summary(entry),
                        "published_at": self._parse_date(entry.get("published")).isoformat(),
                        "source_id": source["id"],
                        "user_id": source["user_id"],
                        "image_url": self._extract_image_from_rss(entry),
                        "image_alt": entry.get("title", "")  # Use title as alt text
                    }
                    
                    # Check if item already exists
                    existing = self.supabase.table("items").select("id").eq("url", item_data["url"]).execute()
                    if existing.data:
                        continue  # Skip duplicate
                    
                    # Insert new item
                    result = self.supabase.table("items").insert(item_data).execute()
                    if result.data:
                        new_items += 1
                
                # Update source last_fetched_at timestamp
                self.supabase.table("sources").update({
                    "last_fetched_at": datetime.utcnow().isoformat()
                }).eq("id", source["id"]).execute()
                
                return {"new_items": new_items}
                
        except Exception as e:
            raise Exception(f"RSS processing failed: {str(e)}")
    
    async def _process_youtube_feed(self, source: Dict[str, Any]) -> Dict[str, Any]:
        """Process YouTube channel RSS feed"""
        try:
            # YouTube channels have RSS feeds at: https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}
            # Need to resolve handle to channel ID first
            handle = source["handle"]
            channel_id = await self._resolve_youtube_channel_id(handle)
            
            if not channel_id:
                raise Exception(f"Could not resolve YouTube channel ID for handle: {handle}")
            
            rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
            logger.info(f"Fetching YouTube RSS feed: {rss_url}")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(rss_url)
                response.raise_for_status()
                
                # Parse RSS feed (YouTube uses standard RSS)
                feed = feedparser.parse(response.text)
                
                new_items = 0
                for entry in feed.entries[:10]:  # Limit to 10 most recent videos
                    # Extract video ID from URL and generate thumbnail
                    video_id = self._extract_youtube_video_id(entry.get("link", ""))
                    thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg" if video_id else None
                    
                    item_data = {
                        "title": entry.get("title", ""),
                        "url": entry.get("link", ""),
                        "summary": entry.get("summary", ""),
                        "published_at": self._parse_date(entry.get("published")).isoformat(),
                        "source_id": source["id"],
                        "user_id": source["user_id"],
                        "image_url": thumbnail_url,
                        "image_alt": f"Thumbnail for {entry.get('title', '')}"
                    }
                    
                    # Check for duplicates
                    existing = self.supabase.table("items").select("id").eq("url", item_data["url"]).execute()
                    if existing.data:
                        continue
                    
                    # Insert new item
                    result = self.supabase.table("items").insert(item_data).execute()
                    if result.data:
                        new_items += 1
                
                # Update source timestamp
                self.supabase.table("sources").update({
                    "last_fetched_at": datetime.utcnow().isoformat()
                }).eq("id", source["id"]).execute()
                
                return {"new_items": new_items}
                
        except Exception as e:
            raise Exception(f"YouTube processing failed: {str(e)}")
    
    async def _process_twitter_feed(self, source: Dict[str, Any]) -> Dict[str, Any]:
        """Process Twitter/X feed (placeholder - requires Twitter API)"""
        # This would require Twitter API v2 integration
        # For now, return a placeholder
        return {"new_items": 0, "message": "Twitter integration not yet implemented"}
    
    def _extract_summary(self, entry: Dict[str, Any]) -> str:
        """Extract summary from RSS entry"""
        # Try different fields for summary
        summary = entry.get("summary", "") or entry.get("description", "") or entry.get("content", "")
        
        # Clean HTML tags and limit length
        import re
        summary = re.sub(r'<[^>]+>', '', summary)
        return summary[:500] if summary else ""
    
    def _parse_date(self, date_str: Optional[str]) -> datetime:
        """Parse date string to datetime"""
        if not date_str:
            return datetime.utcnow()
        
        try:
            # Handle various date formats
            import dateutil.parser
            return dateutil.parser.parse(date_str)
        except:
            return datetime.utcnow()
    
    def _extract_image_from_rss(self, entry: Dict[str, Any]) -> Optional[str]:
        """Extract image URL from RSS entry"""
        # Try different methods to extract image
        
        # 1. Check for media:thumbnail or media:content (common in RSS)
        if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            return entry.media_thumbnail[0].get('url')
        
        if hasattr(entry, 'media_content') and entry.media_content:
            for media in entry.media_content:
                if media.get('medium') == 'image' or 'image' in media.get('type', ''):
                    return media.get('url')
        
        # 2. Check for enclosures (podcast/blog images)
        if hasattr(entry, 'enclosures') and entry.enclosures:
            for enclosure in entry.enclosures:
                if enclosure.get('type', '').startswith('image/'):
                    return enclosure.get('href') or enclosure.get('url')
        
        # 3. Try to extract from content/description HTML
        content = entry.get('content', [{}])[0].get('value', '') if entry.get('content') else ''
        content = content or entry.get('summary', '') or entry.get('description', '')
        
        if content:
            import re
            # Look for <img> tags
            img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content)
            if img_match:
                return img_match.group(1)
        
        return None
    
    async def _resolve_youtube_channel_id(self, handle: str) -> Optional[str]:
        """Resolve YouTube handle/username to channel ID"""
        import re
        
        try:
            # If it's already a channel ID (starts with UC and is 24 chars), return it
            clean_handle = handle.strip()
            if clean_handle.startswith('UC') and len(clean_handle) == 24:
                return clean_handle
            
            # Remove @ if present
            clean_handle = clean_handle.replace('@', '')
            
            # Try to fetch the channel page and extract the channel ID
            channel_urls = [
                f"https://www.youtube.com/@{clean_handle}",
                f"https://www.youtube.com/c/{clean_handle}",
                f"https://www.youtube.com/user/{clean_handle}",
            ]
            
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                for url in channel_urls:
                    try:
                        logger.info(f"Trying to resolve YouTube channel: {url}")
                        response = await client.get(url)
                        response.raise_for_status()
                        
                        # Look for channel ID in the page HTML
                        # Channel ID appears in various places like:
                        # "channelId":"UCbfYPyITQ-7l4upoX8nvctg"
                        # "externalId":"UCbfYPyITQ-7l4upoX8nvctg"
                        # /channel/UCbfYPyITQ-7l4upoX8nvctg
                        
                        patterns = [
                            r'"channelId":"(UC[^"]+)"',
                            r'"externalId":"(UC[^"]+)"',
                            r'/channel/(UC[a-zA-Z0-9_-]{22})',
                            r'<link rel="canonical" href="https://www\.youtube\.com/channel/(UC[^"]+)"',
                        ]
                        
                        for pattern in patterns:
                            match = re.search(pattern, response.text)
                            if match:
                                channel_id = match.group(1)
                                logger.info(f"Resolved YouTube channel ID: {channel_id}")
                                return channel_id
                    except Exception as e:
                        logger.debug(f"Failed to resolve from {url}: {e}")
                        continue
            
            logger.error(f"Could not resolve YouTube channel ID for: {handle}")
            return None
            
        except Exception as e:
            logger.error(f"Error resolving YouTube channel: {e}")
            return None
    
    def _extract_youtube_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL"""
        import re
        
        # Match different YouTube URL formats
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?]+)',
            r'youtube\.com\/embed\/([^&\n?]+)',
            r'youtube\.com\/v\/([^&\n?]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    async def get_user_sources(self, user_id: str) -> List[Source]:
        """Get all sources for a user"""
        response = self.supabase.table("sources").select("*").eq("user_id", user_id).execute()
        return [Source(**source) for source in response.data]
    
    async def create_source(self, user_id: str, source_data: SourceCreate) -> Source:
        """Create a new source"""
        source_dict = source_data.dict()
        source_dict["user_id"] = user_id
        source_dict["created_at"] = datetime.utcnow().isoformat()
        source_dict["updated_at"] = datetime.utcnow().isoformat()
        
        response = self.supabase.table("sources").insert(source_dict).execute()
        if not response.data:
            raise Exception("Failed to create source")
        
        return Source(**response.data[0])
    
    async def delete_source(self, user_id: str, source_id: str) -> None:
        """Delete a source"""
        response = self.supabase.table("sources").delete().eq("id", source_id).eq("user_id", user_id).execute()
        if not response.data:
            raise Exception("Source not found or not owned by user")
    
    async def update_source(self, user_id: str, source_id: str, update_data: Dict[str, Any]) -> Source:
        """Update a source"""
        # Add updated_at timestamp
        update_dict = {k: v for k, v in update_data.items() if v is not None}
        update_dict["updated_at"] = datetime.utcnow().isoformat()
        
        response = self.supabase.table("sources").update(update_dict).eq("id", source_id).eq("user_id", user_id).execute()
        if not response.data:
            raise Exception("Source not found or not owned by user")
        
        return Source(**response.data[0])
    
    async def test_source(self, user_id: str, source_id: str) -> Dict[str, Any]:
        """Test a source and return sample data"""
        try:
            result = await self.process_single_feed(source_id, force_refresh=True)
            return {
                "success": True,
                "new_items": result.get("new_items", 0),
                "message": "Source tested successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_source_items(self, user_id: str, source_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent items from a specific source"""
        try:
            # Verify source belongs to user
            source_response = self.supabase.table("sources").select("id").eq("id", source_id).eq("user_id", user_id).execute()
            if not source_response.data:
                raise Exception("Source not found or not owned by user")
            
            # Get items from this source
            response = self.supabase.table("items").select("*").eq("source_id", source_id).order("published_at", desc=True).limit(limit).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error getting items for source {source_id}: {e}")
            raise
    
    async def get_status(self) -> Dict[str, Any]:
        """Get ingestion service status"""
        return {
            "status": "running",
            "last_check": datetime.utcnow().isoformat(),
            "queued_jobs": 0,  # Will be updated when Celery is implemented
            "active_workers": 1
        }
