#!/usr/bin/env python3
"""
Test script for trend scoring algorithms (without database operations)
"""

import asyncio
from datetime import datetime, timedelta
from app.core.trends.service import TrendService
from app.models.schemas import Item

async def test_trend_scoring():
    """Test trend scoring algorithms with mock data"""
    print("🧪 Testing Trend Scoring Algorithms...")
    
    # Create mock items with different characteristics
    mock_items = [
        Item(
            id="1",
            source_id="test-source",
            title="Breaking: OpenAI Announces New AI Model with Revolutionary Capabilities",
            url="https://techcrunch.com/breaking-ai-model",
            summary="OpenAI has announced a groundbreaking new AI model that promises to revolutionize the field of artificial intelligence with unprecedented capabilities in natural language processing and reasoning.",
            published_at=(datetime.utcnow() - timedelta(minutes=30)).isoformat(),
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        ),
        Item(
            id="2", 
            source_id="test-source",
            title="How Machine Learning is Transforming Healthcare Industry",
            url="https://techcrunch.com/ml-healthcare",
            summary="A comprehensive guide on how machine learning algorithms are being used to improve patient care, drug discovery, and medical diagnosis across the healthcare sector.",
            published_at=(datetime.utcnow() - timedelta(hours=2)).isoformat(),
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        ),
        Item(
            id="3",
            source_id="test-source", 
            title="Bitcoin Reaches New All-Time High Amid Market Volatility",
            url="https://techcrunch.com/bitcoin-high",
            summary="Bitcoin has reached a new all-time high price point as cryptocurrency markets experience significant volatility and increased institutional adoption.",
            published_at=(datetime.utcnow() - timedelta(hours=6)).isoformat(),
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        ),
        Item(
            id="4",
            source_id="test-source",
            title="Regular Tech News Update",
            url="https://example.com/regular-news",
            summary="A regular technology news update covering various topics in the industry.",
            published_at=(datetime.utcnow() - timedelta(days=2)).isoformat(),
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        ),
        Item(
            id="5",
            source_id="test-source",
            title="Quantum Computing Breakthrough: New Qubit Technology Shows Promise",
            url="https://techcrunch.com/quantum-breakthrough", 
            summary="Scientists have achieved a major breakthrough in quantum computing with a new qubit technology that could lead to more stable and scalable quantum systems.",
            published_at=(datetime.utcnow() - timedelta(minutes=45)).isoformat(),
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )
    ]
    
    # Test trend scoring (without database)
    from app.core.trends.service import TrendService
    
    # Create a mock trend service that doesn't need database
    class MockTrendService:
        def _calculate_content_quality(self, item: Item) -> float:
            score = 0.5  # Base score
            title = str(item.title or "")
            if len(title) > 20 and len(title) < 100:
                score += 0.1
            if any(word in title.lower() for word in ['breaking', 'exclusive', 'update', 'announces']):
                score += 0.1
            summary = str(item.summary or "")
            if len(summary) > 100:
                score += 0.1
            if len(summary) > 300:
                score += 0.1
            url_str = str(item.url or "")
            if any(domain in url_str.lower() for domain in ['techcrunch.com', 'cnn.com', 'bbc.com', 'reuters.com']):
                score += 0.1
            return min(score, 1.0)
        
        def _calculate_keyword_relevance(self, item: Item) -> float:
            tech_keywords = [
                'ai', 'artificial intelligence', 'machine learning', 'blockchain',
                'cryptocurrency', 'bitcoin', 'ethereum', 'nft', 'metaverse',
                'vr', 'ar', 'quantum', '5g', 'iot', 'cybersecurity',
                'startup', 'venture capital', 'ipo', 'merger', 'acquisition'
            ]
            content = f"{str(item.title or '')} {str(item.summary or '')}".lower()
            matches = sum(1 for keyword in tech_keywords if keyword in content)
            if matches == 0:
                return 0.3
            elif matches == 1:
                return 0.6
            elif matches >= 2:
                return 0.9
            else:
                return 0.5
        
        def _calculate_source_authority(self, item: Item) -> float:
            url_str = str(item.url or "")
            domain = url_str.split('/')[2].lower() if '//' in url_str else ""
            authority_map = {
                'techcrunch.com': 0.95,
                'cnn.com': 0.90,
                'bbc.com': 0.90,
                'reuters.com': 0.95,
                'example.com': 0.3,
            }
            return authority_map.get(domain, 0.5)
        
        def _predict_engagement(self, item: Item) -> float:
            score = 0.5
            title = str(item.title or "")
            summary = str(item.summary or "")
            if any(word in title.lower() for word in ['how', 'why', 'what', 'when', 'where']):
                score += 0.1
            if any(word in title.lower() for word in ['top', 'best', 'worst', 'amazing', 'shocking']):
                score += 0.1
            if any(word in title.lower() for word in ['guide', 'tutorial', 'tips', 'tricks']):
                score += 0.1
            if 50 < len(summary) < 500:
                score += 0.1
            return min(score, 1.0)
        
        async def _calculate_trend_score(self, item: Item) -> float:
            import math
            # Handle ISO format datetime string
            pub_str = str(item.published_at)
            if pub_str.endswith('Z'):
                pub_str = pub_str.replace('Z', '+00:00')
            published_at = datetime.fromisoformat(pub_str)
            hours_ago = (datetime.utcnow() - published_at).total_seconds() / 3600
            
            if hours_ago <= 1:
                recency_score = 1.0
            elif hours_ago <= 6:
                recency_score = 0.9
            elif hours_ago <= 24:
                recency_score = math.exp(-hours_ago / 12)
            elif hours_ago <= 72:
                recency_score = math.exp(-hours_ago / 36)
            else:
                recency_score = math.exp(-hours_ago / 168)
            
            quality_score = self._calculate_content_quality(item)
            relevance_score = self._calculate_keyword_relevance(item)
            authority_score = self._calculate_source_authority(item)
            engagement_score = self._predict_engagement(item)
            
            trend_score = (
                recency_score * 0.40 +
                quality_score * 0.25 +
                relevance_score * 0.20 +
                authority_score * 0.10 +
                engagement_score * 0.05
            )
            
            if trend_score > 0.8:
                trend_score = min(trend_score * 1.1, 1.0)
            
            return min(max(trend_score, 0), 1)
    
    trend_service = MockTrendService()
    
    print("\n📊 Trend Scoring Results:")
    print("=" * 80)
    
    scored_items = []
    for item in mock_items:
        try:
            print(f"\n🔍 Debugging item: {item.title[:50]}...")
            print(f"   Item type: {type(item)}")
            print(f"   Title type: {type(item.title)}")
            print(f"   Summary type: {type(item.summary)}")
            print(f"   URL type: {type(item.url)}")
            
            # Calculate comprehensive trend score
            trend_score = await trend_service._calculate_trend_score(item)
            
            # Calculate individual component scores
            recency_score = await calculate_recency_score(item)
            quality_score = trend_service._calculate_content_quality(item)
            relevance_score = trend_service._calculate_keyword_relevance(item)
            authority_score = trend_service._calculate_source_authority(item)
            engagement_score = trend_service._predict_engagement(item)
            
            scored_items.append({
                'item': item,
                'trend_score': trend_score,
                'components': {
                    'recency': recency_score,
                    'quality': quality_score,
                    'relevance': relevance_score,
                    'authority': authority_score,
                    'engagement': engagement_score
                }
            })
            
            print(f"\n📰 {item.title}")
            print(f"   🔗 URL: {item.url}")
            print(f"   ⏰ Published: {item.published_at}")
            print(f"   📈 Overall Trend Score: {trend_score:.3f}")
            print(f"   📊 Component Scores:")
            print(f"      • Recency (40%): {recency_score:.3f}")
            print(f"      • Quality (25%): {quality_score:.3f}")
            print(f"      • Relevance (20%): {relevance_score:.3f}")
            print(f"      • Authority (10%): {authority_score:.3f}")
            print(f"      • Engagement (5%): {engagement_score:.3f}")
            
        except Exception as e:
            import traceback
            print(f"❌ Error scoring item {item.id}: {e}")
            print(f"   Full traceback: {traceback.format_exc()}")
    
    # Sort by trend score and show ranking
    scored_items.sort(key=lambda x: x['trend_score'], reverse=True)
    
    print(f"\n🏆 TRENDING ITEMS RANKING:")
    print("=" * 80)
    for i, item_data in enumerate(scored_items, 1):
        item = item_data['item']
        score = item_data['trend_score']
        print(f"{i}. {item.title[:70]}...")
        print(f"   Score: {score:.3f} | Published: {item.published_at}")
    
    print(f"\n✅ Trend scoring test completed!")
    print(f"📊 Analyzed {len(scored_items)} items with comprehensive scoring algorithm")

async def calculate_recency_score(item: Item) -> float:
    """Calculate recency score (copied from the service for testing)"""
    import math
    # Handle ISO format datetime string
    pub_str = str(item.published_at)
    if pub_str.endswith('Z'):
        pub_str = pub_str.replace('Z', '+00:00')
    published_at = datetime.fromisoformat(pub_str)
    hours_ago = (datetime.utcnow() - published_at).total_seconds() / 3600
    
    if hours_ago <= 1:
        return 1.0
    elif hours_ago <= 6:
        return 0.9
    elif hours_ago <= 24:
        return math.exp(-hours_ago / 12)
    elif hours_ago <= 72:
        return math.exp(-hours_ago / 36)
    else:
        return math.exp(-hours_ago / 168)

if __name__ == "__main__":
    asyncio.run(test_trend_scoring())
