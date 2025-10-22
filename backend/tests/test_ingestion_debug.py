#!/usr/bin/env python3
"""
Test ingestion service with detailed logging
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add backend to path
sys.path.insert(0, 'backend')

load_dotenv('backend/.env')

from app.core.ingestion.service import IngestionService
from app.core.database import init_db

# Initialize database (sets env vars)
os.environ['SUPABASE_URL'] = os.getenv("SUPABASE_URL")
os.environ['SUPABASE_ANON_KEY'] = os.getenv("SUPABASE_ANON_KEY")
init_db()

async def test_ingestion():
    print("🔍 Testing Ingestion Service with Debug Output")
    print("="*70)
    
    # Get JWT token
    import httpx
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
    TEST_EMAIL = os.getenv("TEST_EMAIL")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD")
    
    with httpx.Client() as client:
        auth_response = client.post(
            f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
            headers={"apikey": SUPABASE_KEY, "Content-Type": "application/json"},
            json={"email": TEST_EMAIL, "password": TEST_PASSWORD}
        )
    
    JWT_TOKEN = auth_response.json().get("access_token")
    USER_ID = auth_response.json().get('user', {}).get('id')
    
    print(f"✅ Authenticated as {USER_ID}")
    
    # Create service with JWT token
    service = IngestionService(jwt_token=JWT_TOKEN)
    
    # Get sources
    from app.core.database import get_user_supabase
    supabase = get_user_supabase(JWT_TOKEN)
    sources_response = supabase.table("sources").select("*").eq("user_id", USER_ID).execute()
    sources = sources_response.data
    
    print(f"\n📡 Found {len(sources)} sources")
    
    if not sources:
        print("❌ No sources found!")
        return
    
    # Test processing first source in detail
    source = sources[0]
    print(f"\n🔍 Testing source: {source['name']}")
    print(f"   Type: {source['type']}")
    print(f"   Handle: {source['handle']}")
    print(f"   Source ID: {source['id']}")
    
    try:
        print("\n📥 Processing feed...")
        result = await service.process_single_feed(source['id'], force_refresh=True)
        
        print(f"\n✅ Result:")
        print(f"   New items: {result.get('new_items', 0)}")
        if result.get('error'):
            print(f"   Error: {result['error']}")
        if result.get('message'):
            print(f"   Message: {result['message']}")
            
    except Exception as e:
        print(f"\n❌ Exception: {e}")
        import traceback
        traceback.print_exc()
    
    # Check database for items
    print(f"\n📊 Checking items in database...")
    items_response = supabase.table("items").select("id, title, url, source_id").eq("source_id", source['id']).execute()
    print(f"   Found {len(items_response.data)} items for this source")
    
    for item in items_response.data[:3]:
        print(f"   - {item['title'][:60]}...")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    asyncio.run(test_ingestion())

