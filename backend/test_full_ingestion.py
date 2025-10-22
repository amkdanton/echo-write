#!/usr/bin/env python3
"""
Test full content ingestion workflow using the API
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:8000/api/v1"
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")

def authenticate_and_get_token():
    """Authenticate with test credentials and get JWT token"""
    print(f"🔐 Authenticating with test credentials: {TEST_EMAIL}")
    
    try:
        # Sign in with test credentials
        auth_response = requests.post(
            f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
            headers={
                "apikey": SUPABASE_KEY,
                "Content-Type": "application/json"
            },
            json={
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            }
        )
        
        if auth_response.status_code == 200:
            auth_data = auth_response.json()
            jwt_token = auth_data.get("access_token")
            print(f"✅ Authentication successful!")
            print(f"   User ID: {auth_data.get('user', {}).get('id')}")
            return f"Bearer {jwt_token}"
        else:
            print(f"❌ Authentication failed: {auth_response.status_code}")
            print(f"   Error: {auth_response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return None

def test_full_ingestion_workflow():
    """Test the complete ingestion workflow"""
    print("🚀 Testing Full Content Ingestion Workflow")
    print("=" * 50)
    
    # 1. Authenticate
    auth_token = authenticate_and_get_token()
    if not auth_token:
        print("❌ Cannot proceed without authentication")
        return
    
    headers = {"Authorization": auth_token}
    
    # 2. Create test sources
    print("\n📝 Step 1: Creating test sources...")
    test_sources = [
        {
            "type": "rss",
            "handle": "https://feeds.feedburner.com/TechCrunch",
            "name": "TechCrunch RSS"
        },
        {
            "type": "rss", 
            "handle": "https://rss.cnn.com/rss/edition.rss",
            "name": "CNN Top Stories"
        }
    ]
    
    created_sources = []
    for source_data in test_sources:
        try:
            response = requests.post(
                f"{BASE_URL}/ingestion/sources", 
                json=source_data,
                headers={**headers, "Content-Type": "application/json"}
            )
            if response.status_code == 200:
                source_result = response.json()
                created_sources.append(source_result)
                print(f"   ✅ Created: {source_result.get('name')} (ID: {source_result.get('id')})")
            else:
                print(f"   ❌ Failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    if not created_sources:
        print("❌ No sources created, cannot test ingestion")
        return
    
    # 3. Test source ingestion
    print(f"\n🧪 Step 2: Testing ingestion for {len(created_sources)} sources...")
    for source in created_sources:
        source_id = source.get("id")
        source_name = source.get("name")
        print(f"   Testing ingestion for: {source_name}")
        try:
            response = requests.post(
                f"{BASE_URL}/ingestion/test/{source_id}",
                headers=headers
            )
            if response.status_code == 200:
                result = response.json()
                new_items = result.get("new_items", 0)
                print(f"   ✅ Success: Found {new_items} new items")
            else:
                print(f"   ❌ Failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # 4. Check ingestion status
    print("\n📊 Step 3: Checking ingestion status...")
    try:
        response = requests.get(f"{BASE_URL}/ingestion/status")
        if response.status_code == 200:
            status = response.json()
            print(f"   ✅ Status: {status}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 5. Cleanup - delete created sources
    print(f"\n🗑️  Step 4: Cleaning up {len(created_sources)} test sources...")
    for source in created_sources:
        source_id = source.get("id")
        source_name = source.get("name")
        try:
            response = requests.delete(
                f"{BASE_URL}/ingestion/sources/{source_id}",
                headers=headers
            )
            if response.status_code == 200:
                print(f"   ✅ Deleted: {source_name}")
            else:
                print(f"   ❌ Delete failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Delete error: {e}")
    
    print("\n🎉 Full ingestion workflow test completed!")

if __name__ == "__main__":
    test_full_ingestion_workflow()
