"""
Voice training and style extraction service
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
import logging
import re
from collections import Counter

from app.core.database import get_supabase, get_user_supabase

logger = logging.getLogger(__name__)


class StyleService:
    """Service for extracting and managing writing style/voice."""
    
    def __init__(self, jwt_token: str = None):
        if jwt_token:
            self.supabase = get_user_supabase(jwt_token)
        else:
            self.supabase = get_supabase()
    
    async def train_voice(self, user_id: str, samples: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Train voice model using provided writing samples.
        This is the main entry point for voice training.
        """
        try:
            # First, add all samples to the database
            for sample in samples:
                await self.add_style_sample(
                    user_id=user_id,
                    content=sample.content,
                    title=getattr(sample, 'title', None),
                    source_type=sample.sample_type
                )
            
            # Then extract voice profile from all samples
            voice_profile = await self.extract_voice_profile(user_id)
            
            # Calculate confidence score based on sample count and characteristics
            confidence = min(0.95, 0.5 + (len(samples) * 0.1) + (len(voice_profile.get('voice_traits', [])) * 0.05))
            
            return {
                'user_id': user_id,
                'traits': voice_profile.get('voice_traits', []),
                'confidence': round(confidence, 2),
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error training voice: {str(e)}")
            raise

    async def extract_voice_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Extract voice profile from all active style samples for a user.
        Returns tone descriptors and writing characteristics.
        """
        try:
            # Get all active style samples for the user
            response = self.supabase.table('style_samples').select('*').eq('user_id', user_id).eq('is_active', True).execute()
            
            samples = response.data
            
            if not samples:
                return {
                    'user_id': user_id,
                    'voice_traits': [],
                    'characteristics': {},
                    'sample_count': 0,
                    'message': 'No style samples found. Please upload writing samples first.'
                }
            
            # Aggregate all sample content
            all_text = ' '.join([sample.get('content', '') for sample in samples])
            
            # Extract characteristics
            characteristics = {
                'avg_sentence_length': self._calculate_avg_sentence_length(all_text),
                'vocabulary_richness': self._calculate_vocabulary_richness(all_text),
                'punctuation_style': self._analyze_punctuation(all_text),
                'paragraph_structure': self._analyze_paragraphs(all_text),
                'tone_indicators': self._extract_tone_indicators(all_text)
            }
            
            # Generate voice traits (simplified - in production would use LLM)
            voice_traits = self._generate_voice_traits(characteristics)
            
            # Update user profile with voice traits
            self.supabase.table('user_profiles').update({
                'voice_traits': voice_traits,
                'updated_at': datetime.utcnow().isoformat()
            }).eq('id', user_id).execute()
            
            logger.info(f"Extracted voice profile for user {user_id} from {len(samples)} samples")
            
            return {
                'user_id': user_id,
                'voice_traits': voice_traits,
                'characteristics': characteristics,
                'sample_count': len(samples),
                'last_updated': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error extracting voice profile: {str(e)}")
            raise
    
    def _calculate_avg_sentence_length(self, text: str) -> float:
        """Calculate average sentence length in words."""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0.0
        
        total_words = sum(len(sentence.split()) for sentence in sentences)
        return round(total_words / len(sentences), 1)
    
    def _calculate_vocabulary_richness(self, text: str) -> float:
        """Calculate vocabulary richness (unique words / total words)."""
        words = re.findall(r'\b\w+\b', text.lower())
        
        if not words:
            return 0.0
        
        unique_words = len(set(words))
        total_words = len(words)
        
        return round(unique_words / total_words, 3)
    
    def _analyze_punctuation(self, text: str) -> Dict[str, Any]:
        """Analyze punctuation usage patterns."""
        exclamation_count = text.count('!')
        question_count = text.count('?')
        dash_count = text.count('—') + text.count('--')
        semicolon_count = text.count(';')
        colon_count = text.count(':')
        
        total_chars = len(text)
        
        return {
            'exclamation_frequency': round(exclamation_count / max(total_chars / 1000, 1), 2),
            'question_frequency': round(question_count / max(total_chars / 1000, 1), 2),
            'uses_dashes': dash_count > 0,
            'uses_semicolons': semicolon_count > 0,
            'uses_colons': colon_count > 0
        }
    
    def _analyze_paragraphs(self, text: str) -> Dict[str, Any]:
        """Analyze paragraph structure."""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        if not paragraphs:
            return {
                'avg_paragraph_length': 0,
                'short_paragraphs': False
            }
        
        avg_length = sum(len(p.split()) for p in paragraphs) / len(paragraphs)
        
        return {
            'avg_paragraph_length': round(avg_length, 1),
            'short_paragraphs': avg_length < 50,
            'total_paragraphs': len(paragraphs)
        }
    
    def _extract_tone_indicators(self, text: str) -> List[str]:
        """Extract indicators of writing tone."""
        tone_keywords = {
            'casual': ['yeah', 'gonna', 'kinda', 'stuff', 'things', 'pretty much'],
            'formal': ['therefore', 'furthermore', 'nevertheless', 'consequently', 'moreover'],
            'enthusiastic': ['amazing', 'fantastic', 'incredible', 'awesome', 'love', 'great'],
            'analytical': ['data', 'analysis', 'research', 'study', 'findings', 'evidence'],
            'storytelling': ['once', 'then', 'suddenly', 'finally', 'meanwhile', 'story'],
            'conversational': ['you know', 'right?', 'I mean', 'honestly', 'basically'],
            'professional': ['implementation', 'strategy', 'framework', 'methodology', 'objective']
        }
        
        text_lower = text.lower()
        detected_tones = []
        
        for tone, keywords in tone_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            if matches >= 2:  # Need at least 2 keywords to indicate a tone
                detected_tones.append(tone)
        
        return detected_tones
    
    def _generate_voice_traits(self, characteristics: Dict[str, Any]) -> List[str]:
        """Generate voice trait descriptors based on characteristics."""
        traits = []
        
        # Sentence length
        avg_sentence = characteristics.get('avg_sentence_length', 0)
        if avg_sentence < 12:
            traits.append('concise')
        elif avg_sentence > 20:
            traits.append('detailed')
        
        # Vocabulary richness
        vocab = characteristics.get('vocabulary_richness', 0)
        if vocab > 0.6:
            traits.append('varied vocabulary')
        
        # Punctuation style
        punct = characteristics.get('punctuation_style', {})
        if punct.get('exclamation_frequency', 0) > 2:
            traits.append('enthusiastic')
        if punct.get('uses_dashes'):
            traits.append('conversational')
        if punct.get('uses_semicolons'):
            traits.append('sophisticated')
        
        # Paragraph structure
        para = characteristics.get('paragraph_structure', {})
        if para.get('short_paragraphs'):
            traits.append('scannable')
        
        # Tone indicators
        tone_indicators = characteristics.get('tone_indicators', [])
        traits.extend(tone_indicators[:3])  # Add up to 3 tone indicators
        
        # Return top 5 traits
        return traits[:5]
    
    async def add_style_sample(
        self,
        user_id: str,
        content: str,
        title: Optional[str] = None,
        source_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add a new style sample for the user."""
        try:
            sample_data = {
                'user_id': user_id,
                'title': title or f'Sample {datetime.utcnow().strftime("%Y-%m-%d %H:%M")}',
                'content': content,
                'source_type': source_type or 'other',
                'is_active': True,
                'created_at': datetime.utcnow().isoformat()
            }
            
            response = self.supabase.table('style_samples').insert(sample_data).execute()
            
            if not response.data:
                raise Exception('Failed to add style sample')
            
            # Re-extract voice profile with new sample
            voice_profile = await self.extract_voice_profile(user_id)
            
            logger.info(f"Added style sample for user {user_id}")
            
            return {
                'sample_id': response.data[0]['id'],
                'voice_profile_updated': True,
                'new_traits': voice_profile.get('voice_traits', [])
            }
            
        except Exception as e:
            logger.error(f"Error adding style sample: {str(e)}")
            raise
    
    async def get_style_samples(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all style samples for a user."""
        try:
            response = self.supabase.table('style_samples').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
            
            return response.data
            
        except Exception as e:
            logger.error(f"Error getting style samples: {str(e)}")
            raise
    
    async def delete_style_sample(self, user_id: str, sample_id: str) -> Dict[str, Any]:
        """Delete a style sample and re-extract voice profile."""
        try:
            response = self.supabase.table('style_samples').delete().eq('id', sample_id).eq('user_id', user_id).execute()
            
            if not response.data:
                raise ValueError('Style sample not found or not owned by user')
            
            # Re-extract voice profile
            voice_profile = await self.extract_voice_profile(user_id)
            
            logger.info(f"Deleted style sample {sample_id} for user {user_id}")
            
            return {
                'deleted': True,
                'voice_profile_updated': True,
                'remaining_samples': voice_profile.get('sample_count', 0)
            }
            
        except Exception as e:
            logger.error(f"Error deleting style sample: {str(e)}")
            raise
    
    async def get_voice_profile(self, user_id: str) -> Dict[str, Any]:
        """Get the current voice profile for a user."""
        try:
            response = self.supabase.table('user_profiles').select('voice_traits, confidence, created_at, updated_at').eq('id', user_id).execute()
            
            if not response.data:
                return {
                    'user_id': user_id,
                    'traits': [],
                    'confidence': 0.0,
                    'created_at': datetime.utcnow().isoformat(),
                    'updated_at': datetime.utcnow().isoformat()
                }
            
            profile_data = response.data[0]
            voice_traits = profile_data.get('voice_traits', [])
            confidence = profile_data.get('confidence', 0.0)
            created_at = profile_data.get('created_at', datetime.utcnow().isoformat())
            updated_at = profile_data.get('updated_at', datetime.utcnow().isoformat())
            
            return {
                'user_id': user_id,
                'traits': voice_traits,  # Map voice_traits to traits
                'confidence': confidence,
                'created_at': created_at,
                'updated_at': updated_at
            }
            
        except Exception as e:
            logger.error(f"Error getting voice profile: {str(e)}")
            raise
    
    async def toggle_sample_status(self, user_id: str, sample_id: str, is_active: bool) -> Dict[str, Any]:
        """Toggle the active status of a style sample."""
        try:
            response = self.supabase.table('style_samples').update({
                'is_active': is_active,
                'updated_at': datetime.utcnow().isoformat()
            }).eq('id', sample_id).eq('user_id', user_id).execute()
            
            if not response.data:
                raise ValueError('Style sample not found or not owned by user')
            
            # Re-extract voice profile
            voice_profile = await self.extract_voice_profile(user_id)
            
            return {
                'updated': True,
                'is_active': is_active,
                'voice_profile_updated': True
            }
            
        except Exception as e:
            logger.error(f"Error toggling sample status: {str(e)}")
            raise

    async def retrain_voice(self, user_id: str) -> Dict[str, Any]:
        """Retrain voice profile with existing samples."""
        try:
            # Re-extract voice profile from all active samples
            voice_profile = await self.extract_voice_profile(user_id)
            
            # Calculate confidence score
            confidence = min(0.95, 0.5 + (voice_profile.get('sample_count', 0) * 0.1) + (len(voice_profile.get('voice_traits', [])) * 0.05))
            
            return {
                'user_id': user_id,
                'traits': voice_profile.get('voice_traits', []),
                'confidence': round(confidence, 2),
                'sample_count': voice_profile.get('sample_count', 0),
                'updated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error retraining voice: {str(e)}")
            raise
