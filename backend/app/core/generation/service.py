"""
AI-powered newsletter generation service
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
import logging
import os

from openai import AsyncOpenAI

from app.core.database import get_supabase, get_user_supabase
from app.core.trends.service import TrendService
from app.core.style.service import StyleService

logger = logging.getLogger(__name__)


class GenerationService:
    """Service for generating newsletters using AI."""
    
    def __init__(self, jwt_token: str = None):
        if jwt_token:
            self.supabase = get_user_supabase(jwt_token)
            self.trend_service = TrendService(jwt_token)
            self.style_service = StyleService(jwt_token)
        else:
            self.supabase = get_supabase()
            self.trend_service = TrendService()
            self.style_service = StyleService()
        
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.warning('OPENAI_API_KEY not set - generation will fail')
        self.openai_client = AsyncOpenAI(api_key=api_key) if api_key else None
    
    async def generate_newsletter(
        self,
        user_id: str,
        title: Optional[str] = None,
        num_items: int = 5,
        time_window_hours: int = 48
    ) -> Dict[str, Any]:
        """
        Generate a newsletter for a user based on trending content and their voice.
        """
        try:
            if not self.openai_client:
                raise ValueError('OpenAI API key not configured')
            
            # 1. Get top trending items
            logger.info(f"Fetching top {num_items} trending items for user {user_id}")
            trending_items = await self.trend_service.get_trending_items(
                user_id=user_id,
                time_window_hours=time_window_hours,
                limit=num_items
            )
            
            if not trending_items:
                return {
                    'success': False,
                    'message': 'No trending items found. Please add sources and fetch content first.'
                }
            
            # 2. Get user's voice profile
            logger.info(f"Fetching voice profile for user {user_id}")
            voice_profile = await self.style_service.get_voice_profile(user_id)
            voice_traits = voice_profile.get('voice_traits', [])
            
            # 3. Get trending keywords for insights section
            trending_keywords = await self.trend_service.get_trending_keywords(
                user_id=user_id,
                limit=5
            )
            
            # 4. Build the prompt
            prompt = self._build_generation_prompt(
                trending_items=trending_items,
                voice_traits=voice_traits,
                trending_keywords=trending_keywords
            )
            
            # 5. Generate newsletter title if not provided
            if not title:
                logger.info("Generating dynamic newsletter title")
                draft_title = await self._generate_newsletter_title(trending_items, trending_keywords)
            else:
                draft_title = title
            
            # 6. Generate newsletter using OpenAI
            logger.info("Generating newsletter with OpenAI")
            newsletter_md = await self._generate_with_llm(prompt)
            
            draft_data = {
                'user_id': user_id,
                'title': draft_title,
                'body_md': newsletter_md,
                'status': 'draft',
                'generation_metadata': {
                    'item_count': len(trending_items),
                    'time_window_hours': time_window_hours,
                    'voice_traits': voice_traits,
                    'model': 'gpt-4',
                    'generated_at': datetime.utcnow().isoformat()
                },
                'created_at': datetime.utcnow().isoformat()
            }
            
            draft_response = self.supabase.table('drafts').insert(draft_data).execute()
            
            if not draft_response.data:
                raise Exception('Failed to create draft')
            
            draft_id = draft_response.data[0]['id']
            
            # 7. Link items to draft
            for idx, item in enumerate(trending_items):
                self.supabase.table('draft_items').insert({
                    'draft_id': draft_id,
                    'item_id': item.id,
                    'position': idx
                }).execute()
            
            logger.info(f"Successfully generated newsletter draft {draft_id}")
            
            return {
                'success': True,
                'draft_id': draft_id,
                'title': draft_title,
                'body_md': newsletter_md,
                'items_included': len(trending_items),
                'word_count': len(newsletter_md.split())
            }
            
        except Exception as e:
            logger.error(f"Error generating newsletter: {str(e)}")
            raise
    
    def _build_generation_prompt(
        self,
        trending_items: List[Any],
        voice_traits: List[str],
        trending_keywords: List[Dict[str, Any]]
    ) -> str:
        """Build the prompt for LLM newsletter generation."""
        
        # Format trending items
        items_text = ""
        for idx, item in enumerate(trending_items, 1):
            items_text += f"\n{idx}. **{item.title}**\n"
            items_text += f"   - URL: {item.url}\n"
            items_text += f"   - Summary: {item.summary[:200] if item.summary else 'No summary'}...\n"
            items_text += f"   - Published: {item.published_at}\n"
            # Include image URL if available
            if hasattr(item, 'image_url') and item.image_url:
                items_text += f"   - Image: {item.image_url}\n"
        
        # Format voice traits
        voice_description = "conversational and engaging"
        if voice_traits:
            voice_description = ", ".join(voice_traits)
        
        # Format trending keywords
        keywords_text = ", ".join([kw.get('keyword', '') for kw in trending_keywords[:5]])
        
        # Build the prompt
        prompt = f"""You are a newsletter writer tasked with creating an engaging, informative newsletter.

**Writing Style/Voice:**
{voice_description}

**Trending Topics to Cover:**
{keywords_text}

**Top Content to Feature:**
{items_text}

**Instructions:**
Create a well-structured newsletter in Markdown format with the following sections:

1. **📝 Executive Summary** (2-3 sentences)
   - Quick overview of this week's most important developments
   - Highlight key trends and themes
   - Set expectations for what readers will learn

2. **Introduction** (2-3 sentences)
   - Hook the reader with what's trending
   - Set the tone for the newsletter

3. **Top Picks** (3-5 items)
   - Feature the most interesting items from the list above
   - Include the title as a link: [Title](URL)
   - If an item has an Image URL, include it using markdown: ![alt text](image_url)
   - Place images BEFORE the article title for visual impact
   - Add 2-3 sentences explaining why each item matters
   - Make it engaging and relevant

4. **Trends to Watch** (2-3 quick insights)
   - Identify emerging patterns from the content
   - Brief bullet points about what's gaining traction

5. **💡 Did You Know?** (Fun trivia)
   - Share an interesting fact or trivia related to the newsletter's topics
   - Make it surprising, educational, or thought-provoking
   - Keep it concise (1-2 sentences)

6. **📊 By The Numbers** (Optional: 3-5 statistics)
   - Quick data points or metrics related to the content
   - Present as a simple list with numbers and context
   - Example: "🚀 143% - Growth in AI adoption this quarter"

7. **Closing**
   - Warm sign-off
   - Call-to-action or thought-provoking question

**Important:**
- Write in the specified voice/tone
- Keep it scannable with headers and bullets
- Include all URLs from the items
- IMPORTANT: Include images from items using markdown syntax ![](image_url)
- Place images prominently to make the newsletter visually engaging
- Aim for 400-600 words total
- Use Markdown formatting with emojis for section headers
- Be authentic and engaging
- Make the Executive Summary actionable and compelling
- Ensure trivia is relevant and interesting
- Use visual elements (images, emojis, formatting) to break up text

Generate the newsletter now:"""
        
        return prompt
    
    async def _generate_with_llm(self, prompt: str) -> str:
        """Generate newsletter content using OpenAI."""
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert newsletter writer who creates engaging, well-structured content that matches the writer's voice and style."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            newsletter_md = response.choices[0].message.content.strip()
            
            return newsletter_md
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}")
            raise
    
    async def _generate_newsletter_title(
        self,
        trending_items: List[Any],
        trending_keywords: List[Dict[str, Any]]
    ) -> str:
        """Generate a dynamic, catchy newsletter title based on content."""
        try:
            # Extract main topics from items and keywords
            topics = set()
            for item in trending_items[:3]:  # Focus on top 3 items
                title_words = item.title.split()
                # Extract meaningful words (skip common words)
                skip_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
                topics.update([word for word in title_words if word.lower() not in skip_words and len(word) > 3][:2])
            
            # Add trending keywords
            for kw in trending_keywords[:2]:
                topics.add(kw.get('keyword', ''))
            
            topics_text = ", ".join(list(topics)[:5])
            
            # Generate title with AI
            prompt = f"""Generate a catchy, professional newsletter title based on these trending topics:
{topics_text}

The title should be:
- Engaging and attention-grabbing
- Professional yet approachable
- 5-10 words maximum
- Include a relevant emoji or descriptor
- Follow this pattern: "[Topic] Weekly - [Key Theme]" or "[Descriptor] in [Topic]" or similar

Examples:
- "Tech Weekly - AI Breakthroughs & Startup Funding"
- "Your Science Digest - Climate & Space News"
- "Business Brief - Market Trends & IPO Updates"
- "AI Innovations - This Week's Big Wins"

Generate ONE title only, no quotes or explanations:"""
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a expert at creating catchy newsletter titles."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=50
            )
            
            title = response.choices[0].message.content.strip()
            # Remove quotes if AI added them
            title = title.strip('"\'')
            
            # Fallback if title is too long or empty
            if not title or len(title) > 100:
                today = datetime.utcnow().strftime('%B %d, %Y')
                main_topic = list(topics)[0] if topics else "Tech"
                title = f"{main_topic} Weekly - {today}"
            
            logger.info(f"Generated title: {title}")
            return title
            
        except Exception as e:
            logger.error(f"Error generating title: {str(e)}")
            # Fallback to date-based title
            return f"Newsletter - {datetime.utcnow().strftime('%B %d, %Y')}"
    
    async def regenerate_draft(
        self,
        user_id: str,
        draft_id: str,
        feedback: Optional[str] = None
    ) -> Dict[str, Any]:
        """Regenerate an existing draft with optional feedback."""
        try:
            # Get the original draft
            draft_response = self.supabase.table('drafts').select('*').eq('id', draft_id).eq('user_id', user_id).execute()
            
            if not draft_response.data:
                raise ValueError('Draft not found')
            
            draft = draft_response.data[0]
            metadata = draft.get('generation_metadata', {})
            
            # Get the items that were used
            items_response = self.supabase.table('draft_items').select("""
                item_id,
                items!inner(*)
            """).eq('draft_id', draft_id).execute()
            
            item_ids = [item['item_id'] for item in items_response.data]
            
            # Get fresh trending items or use the same ones
            trending_items = await self.trend_service.get_trending_items(
                user_id=user_id,
                time_window_hours=metadata.get('time_window_hours', 48),
                limit=metadata.get('item_count', 5)
            )
            
            # Get voice profile
            voice_profile = await self.style_service.get_voice_profile(user_id)
            voice_traits = voice_profile.get('voice_traits', [])
            
            # Get trending keywords
            trending_keywords = await self.trend_service.get_trending_keywords(user_id, limit=5)
            
            # Build prompt with feedback
            prompt = self._build_generation_prompt(
                trending_items=trending_items,
                voice_traits=voice_traits,
                trending_keywords=trending_keywords
            )
            
            if feedback:
                prompt += f"\n\n**User Feedback on Previous Draft:**\n{feedback}\n\nPlease incorporate this feedback in the regenerated newsletter."
            
            # Generate new version
            newsletter_md = await self._generate_with_llm(prompt)
            
            # Update the draft
            update_data = {
                'body_md': newsletter_md,
                'updated_at': datetime.utcnow().isoformat(),
                'generation_metadata': {
                    **metadata,
                    'regenerated': True,
                    'regenerated_at': datetime.utcnow().isoformat(),
                    'feedback': feedback
                }
            }
            
            self.supabase.table('drafts').update(update_data).eq('id', draft_id).execute()
            
            logger.info(f"Regenerated draft {draft_id}")
            
            return {
                'success': True,
                'draft_id': draft_id,
                'body_md': newsletter_md,
                'regenerated': True
            }
            
        except Exception as e:
            logger.error(f"Error regenerating draft: {str(e)}")
            raise
    
    async def get_draft(self, user_id: str, draft_id: str) -> Dict[str, Any]:
        """Get a specific draft with its items."""
        try:
            # Get draft
            draft_response = self.supabase.table('drafts').select('*').eq('id', draft_id).eq('user_id', user_id).execute()
            
            if not draft_response.data:
                raise ValueError('Draft not found')
            
            draft = draft_response.data[0]
            
            # Get associated items
            items_response = self.supabase.table('draft_items').select("""
                position,
                items!inner(*)
            """).eq('draft_id', draft_id).order('position').execute()
            
            draft['items'] = [item['items'] for item in items_response.data]
            
            return draft
            
        except Exception as e:
            logger.error(f"Error getting draft: {str(e)}")
            raise
    
    async def list_drafts(
        self,
        user_id: str,
        status: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """List drafts for a user."""
        try:
            query = self.supabase.table('drafts').select('*').eq('user_id', user_id)
            
            if status:
                query = query.eq('status', status)
            
            response = query.order('created_at', desc=True).limit(limit).execute()
            
            return response.data
            
        except Exception as e:
            logger.error(f"Error listing drafts: {str(e)}")
            raise
    
    async def delete_draft(self, user_id: str, draft_id: str) -> Dict[str, Any]:
        """Delete a draft."""
        try:
            response = self.supabase.table('drafts').delete().eq('id', draft_id).eq('user_id', user_id).execute()
            
            if not response.data:
                raise ValueError('Draft not found')
            
            return {'success': True, 'draft_id': draft_id}
            
        except Exception as e:
            logger.error(f"Error deleting draft: {str(e)}")
            raise
    
    async def get_user_drafts(
        self, 
        user_id: str, 
        limit: int = 20, 
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get drafts for a user (alias for list_drafts for API compatibility)."""
        return await self.list_drafts(user_id, status, limit)
