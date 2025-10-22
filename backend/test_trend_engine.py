#!/usr/bin/env python3
"""
Test script for trend engine functionality
"""

import asyncio
import os
import uuid
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.core.database import init_db, get_supabase
from app.core.trends.service import TrendService
from app.models.schemas import Item

async def test_trend_engine():
    """Test trend engine with sample data"""
    print("🧪 Testing Trend Engine...")
    
    # Load environment variables and initialize database
    load_dotenv()
    await init_db()
    print("✅ Database initialized")
    
    # Create sample items for testing
    supabase = get_supabase()
    
    # Create a test source first
    test_source = {
        'id': str(uuid.uuid4()),
        'user_id': '69a39d10-6c53-41e9-9910-0485fd20cba9',  # Your test user ID
        'type': 'rss',
        'handle': 'https://feeds.feedburner.com/TechCrunch',
        'name': 'TechCrunch Test Source',
        'is_active': True,
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    try:
        # Insert test source
        source_result = supabase.table("sources").insert(test_source).execute()
        if source_result.data:
            source_id = test_source['id']
            print(f"✅ Created test source: {source_id}")
        else:
            print("❌ Failed to create test source")
            return
    except Exception as e:
        print(f"❌ Error creating test source: {e}")
        return
    
    # Create sample items with different characteristics
    sample_items = [
        {
            'id': str(uuid.uuid4()),
            'source_id': source_id,
            'title': 'Breaking: OpenAI Announces New AI Model with Revolutionary Capabilities',
            'url': 'https://techcrunch.com/breaking-ai-model',
            'summary': 'OpenAI has announced a groundbreaking new AI model that promises to revolutionize the field of artificial intelligence with unprecedented capabilities in natural language processing and reasoning.',
            'published_at': (datetime.utcnow() - timedelta(minutes=30)).isoformat(),  # Very recent
            'created_at': datetime.utcnow().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'source_id': source_id,
            'title': 'How Machine Learning is Transforming Healthcare Industry',
            'url': 'https://techcrunch.com/ml-healthcare',
            'summary': 'A comprehensive guide on how machine learning algorithms are being used to improve patient care, drug discovery, and medical diagnosis across the healthcare sector.',
            'published_at': (datetime.utcnow() - timedelta(hours=2)).isoformat(),  # Recent
            'created_at': datetime.utcnow().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'source_id': source_id,
            'title': 'Bitcoin Reaches New All-Time High Amid Market Volatility',
            'url': 'https://techcrunch.com/bitcoin-high',
            'summary': 'Bitcoin has reached a new all-time high price point as cryptocurrency markets experience significant volatility and increased institutional adoption.',
            'published_at': (datetime.utcnow() - timedelta(hours=6)).isoformat(),  # Moderately recent
            'created_at': datetime.utcnow().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'source_id': source_id,
            'title': 'Regular Tech News Update',
            'url': 'https://example.com/regular-news',
            'summary': 'A regular technology news update covering various topics in the industry.',
            'published_at': (datetime.utcnow() - timedelta(days=2)).isoformat(),  # Older
            'created_at': datetime.utcnow().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'source_id': source_id,
            'title': 'Quantum Computing Breakthrough: New Qubit Technology Shows Promise',
            'url': 'https://techcrunch.com/quantum-breakthrough',
            'summary': 'Scientists have achieved a major breakthrough in quantum computing with a new qubit technology that could lead to more stable and scalable quantum systems.',
            'published_at': (datetime.utcnow() - timedelta(minutes=45)).isoformat(),  # Very recent
            'created_at': datetime.utcnow().isoformat()
        }
    ]
    
    # Insert sample items
    print("\n📝 Creating sample items for trend analysis...")
    inserted_items = []
    for item_data in sample_items:
        try:
            result = supabase.table("items").insert(item_data).execute()
            if result.data:
                inserted_items.append(Item(**item_data))
                print(f"   ✅ Created: {item_data['title'][:50]}...")
            else:
                print(f"   ❌ Failed to create item: {item_data['title'][:50]}...")
        except Exception as e:
            print(f"   ❌ Error creating item: {e}")
    
    if not inserted_items:
        print("❌ No items created, cannot test trend engine")
        return
    
    # Test trend engine
    print(f"\n📊 Testing trend engine with {len(inserted_items)} items...")
    trend_service = TrendService()
    
    # Test individual item scoring
    print("\n🔍 Individual Item Scoring:")
    for item in inserted_items:
        try:
            score = await trend_service._calculate_trend_score(item)
            print(f"   📈 {item.title[:60]}...")
            print(f"      Score: {score:.3f} | Published: {item.published_at}")
        except Exception as e:
            print(f"   ❌ Error scoring item: {e}")
    
    # Test trending items retrieval
    print(f"\n📈 Testing trending items retrieval...")
    try:
        trending_items = await trend_service.get_trending_items(
            user_id='69a39d10-6c53-41e9-9910-0485fd20cba9',
            time_window_hours=72,
            limit=10
        )
        print(f"   ✅ Found {len(trending_items)} trending items")
        for i, item in enumerate(trending_items, 1):
            print(f"   {i}. {item.title[:60]}... (Score: {getattr(item, 'trend_score', 'N/A')})")
    except Exception as e:
        print(f"   ❌ Error getting trending items: {e}")
    
    # Test analysis metadata
    print(f"\n📊 Testing analysis metadata...")
    try:
        metadata = await trend_service.get_analysis_metadata(
            user_id='69a39d10-6c53-41e9-9910-0485fd20cba9',
            time_window_hours=72
        )
        print(f"   ✅ Analysis metadata: {metadata}")
    except Exception as e:
        print(f"   ❌ Error getting analysis metadata: {e}")
    
    # Cleanup
    print(f"\n🗑️  Cleaning up test data...")
    try:
        # Delete sample items
        for item in inserted_items:
            supabase.table("items").delete().eq("id", item.id).execute()
        
        # Delete test source
        supabase.table("sources").delete().eq("id", source_id).execute()
        print("   ✅ Cleanup completed")
    except Exception as e:
        print(f"   ❌ Cleanup error: {e}")
    
    print("\n🎉 Trend engine test completed!")

if __name__ == "__main__":
    asyncio.run(test_trend_engine())
