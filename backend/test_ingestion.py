#!/usr/bin/env python3
"""
Test script for content ingestion functionality
"""

import asyncio
import os
from dotenv import load_dotenv
from app.core.database import init_db
from app.core.ingestion.service import IngestionService

async def test_ingestion():
    """Test content ingestion with real RSS feeds"""
    print("🧪 Testing Content Ingestion...")
    
    # Load environment variables
    load_dotenv()
    print("✅ Environment variables loaded")
    
    # Initialize database
    await init_db()
    print("✅ Database initialized")
    
    # Test RSS feed parsing without database operations
    service = IngestionService()
    
    # Test RSS feed parsing with a real UUID
    test_source = {
        'id': '00000000-0000-0000-0000-000000000001',  # Valid UUID format
        'handle': 'https://feeds.feedburner.com/TechCrunch',
        'type': 'rss'
    }
    
    try:
        print("📡 Testing RSS feed parsing...")
        result = await service._process_rss_feed(test_source)
        print(f"✅ RSS Ingestion Test: {result}")
        
        if result.get('new_items', 0) > 0:
            print(f"🎉 Successfully ingested {result['new_items']} new items!")
        else:
            print("ℹ️  No new items found (likely already processed or feed empty)")
            
    except Exception as e:
        print(f"❌ RSS Ingestion Test Failed: {e}")
    
    # Test another RSS feed
    test_source2 = {
        'id': '00000000-0000-0000-0000-000000000002',  # Valid UUID format
        'handle': 'https://rss.cnn.com/rss/edition.rss',
        'type': 'rss'
    }
    
    try:
        print("\n📡 Testing CNN RSS feed...")
        result2 = await service._process_rss_feed(test_source2)
        print(f"✅ CNN RSS Test: {result2}")
        
        if result2.get('new_items', 0) > 0:
            print(f"🎉 Successfully ingested {result2['new_items']} new items from CNN!")
        
    except Exception as e:
        print(f"❌ CNN RSS Test Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_ingestion())
