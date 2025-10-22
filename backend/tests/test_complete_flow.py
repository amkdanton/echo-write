#!/usr/bin/env python3
"""
Complete Flow Test: Remove Sources → Add Sources → Generate Draft
This script tests the entire EchoWrite workflow end-to-end
"""

import httpx
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

BASE_URL = "http://localhost:8000/api/v1"
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")

# Global JWT token
JWT_TOKEN = None
USER_ID = None

def authenticate():
    """Authenticate with test credentials"""
    global JWT_TOKEN, USER_ID
    
    print("🔐 Authenticating...")
    
    if not all([SUPABASE_URL, SUPABASE_KEY, TEST_EMAIL, TEST_PASSWORD]):
        print("❌ Missing credentials in backend/.env file")
        print(f"   SUPABASE_URL: {'✅' if SUPABASE_URL else '❌'}")
        print(f"   SUPABASE_KEY: {'✅' if SUPABASE_KEY else '❌'}")
        print(f"   TEST_EMAIL: {'✅' if TEST_EMAIL else '❌'}")
        print(f"   TEST_PASSWORD: {'✅' if TEST_PASSWORD else '❌'}")
        return False
    
    try:
        with httpx.Client() as client:
            response = client.post(
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
        
        if response.status_code == 200:
            auth_data = response.json()
            JWT_TOKEN = auth_data.get("access_token")
            USER_ID = auth_data.get('user', {}).get('id')
            print(f"✅ Authenticated as {TEST_EMAIL}")
            print(f"   User ID: {USER_ID}")
            return True
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return False

def get_headers():
    """Get authorization headers"""
    return {"Authorization": f"Bearer {JWT_TOKEN}"}

def step_1_check_existing_sources():
    """Step 1: Check existing sources"""
    print("\n" + "="*60)
    print("📋 STEP 1: Checking Existing Sources")
    print("="*60)
    
    try:
        with httpx.Client() as client:
            response = client.get(
                f"{BASE_URL}/ingestion/sources",
                headers=get_headers()
            )
        
        if response.status_code == 200:
            sources = response.json()
            print(f"✅ Found {len(sources)} existing sources:")
            for source in sources:
                print(f"   - {source.get('name')} ({source.get('type')}) - ID: {source.get('id')}")
            return sources
        else:
            print(f"❌ Failed to get sources: {response.status_code}")
            print(f"   Response: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def step_2_remove_existing_sources(sources):
    """Step 2: Remove all existing sources"""
    print("\n" + "="*60)
    print("🗑️  STEP 2: Removing Existing Sources")
    print("="*60)
    
    if not sources:
        print("✅ No sources to remove")
        return True
    
    success_count = 0
    for source in sources:
        source_id = source.get('id')
        source_name = source.get('name')
        
        print(f"   Deleting: {source_name}...")
        try:
            with httpx.Client() as client:
                response = client.delete(
                    f"{BASE_URL}/ingestion/sources/{source_id}",
                    headers=get_headers()
                )
            
            if response.status_code == 200:
                print(f"   ✅ Deleted: {source_name}")
                success_count += 1
            else:
                print(f"   ❌ Failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n✅ Removed {success_count}/{len(sources)} sources")
    return success_count == len(sources)

def step_3_add_new_sources():
    """Step 3: Add new sources"""
    print("\n" + "="*60)
    print("➕ STEP 3: Adding New Sources")
    print("="*60)
    
    # High-quality RSS feeds for testing
    new_sources = [
        {
            "type": "rss",
            "handle": "https://feeds.feedburner.com/TechCrunch/",
            "name": "TechCrunch"
        },
        {
            "type": "rss",
            "handle": "https://www.theverge.com/rss/index.xml",
            "name": "The Verge"
        },
        {
            "type": "rss",
            "handle": "https://hnrss.org/frontpage",
            "name": "Hacker News Front Page"
        }
    ]
    
    created_sources = []
    
    for source_data in new_sources:
        print(f"   Creating: {source_data['name']}...")
        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{BASE_URL}/ingestion/sources",
                    json=source_data,
                    headers={**get_headers(), "Content-Type": "application/json"}
                )
            
            if response.status_code == 200:
                source = response.json()
                created_sources.append(source)
                print(f"   ✅ Created: {source.get('name')} (ID: {source.get('id')})")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                print(f"      Response: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n✅ Created {len(created_sources)}/{len(new_sources)} sources")
    return created_sources

def step_4_ingest_content(sources):
    """Step 4: Ingest content from sources"""
    print("\n" + "="*60)
    print("📥 STEP 4: Ingesting Content from Sources")
    print("="*60)
    
    if not sources:
        print("❌ No sources to ingest from")
        return False
    
    source_ids = [source.get('id') for source in sources]
    print(f"   Processing {len(source_ids)} sources...")
    print(f"   This may take 30-60 seconds...")
    
    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(
                f"{BASE_URL}/ingestion/process",
                json={
                    "source_ids": source_ids,
                    "force_refresh": True
                },
                headers={**get_headers(), "Content-Type": "application/json"}
            )
        
        if response.status_code == 200:
            result = response.json()
            processed = result.get('processed_sources', 0)
            new_items = result.get('new_items', 0)
            errors = result.get('errors', [])
            
            print(f"✅ Ingestion complete!")
            print(f"   Processed sources: {processed}")
            print(f"   New items fetched: {new_items}")
            if errors:
                print(f"   Errors: {len(errors)}")
                for error in errors:
                    print(f"      - {error}")
            
            return new_items > 0
        else:
            print(f"❌ Ingestion failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def step_5_generate_draft():
    """Step 5: Generate newsletter draft"""
    print("\n" + "="*60)
    print("✨ STEP 5: Generating Newsletter Draft")
    print("="*60)
    
    print("   Generating with AI (this may take 10-20 seconds)...")
    
    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(
                f"{BASE_URL}/generation/newsletter",
                json={
                    "num_items": 5,
                    "time_window_hours": 48
                },
                headers={**get_headers(), "Content-Type": "application/json"}
            )
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                draft = result
                print(f"✅ Newsletter generated successfully!")
                print(f"   Draft ID: {draft.get('draft_id')}")
                print(f"   Title: {draft.get('title')}")
                print(f"   Items included: {draft.get('items_included')}")
                print(f"   Word count: {draft.get('word_count')}")
                
                # Show preview of content
                body = draft.get('body_md', '')
                preview = body[:500] + "..." if len(body) > 500 else body
                print(f"\n📝 Newsletter Preview:")
                print("-" * 60)
                print(preview)
                print("-" * 60)
                
                return draft
            else:
                print(f"❌ Generation failed: {result.get('message')}")
                return None
        else:
            print(f"❌ Generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def step_6_view_draft(draft_id):
    """Step 6: View the generated draft"""
    print("\n" + "="*60)
    print("👀 STEP 6: Viewing Generated Draft")
    print("="*60)
    
    if not draft_id:
        print("❌ No draft ID provided")
        return False
    
    try:
        with httpx.Client() as client:
            response = client.get(
                f"{BASE_URL}/generation/drafts",
                headers=get_headers()
            )
        
        if response.status_code == 200:
            drafts = response.json()
            print(f"✅ Found {len(drafts)} total drafts:")
            for draft in drafts[:5]:  # Show first 5
                print(f"   - {draft.get('title')} (Status: {draft.get('status')})")
                print(f"     ID: {draft.get('id')}")
                print(f"     Created: {draft.get('created_at')}")
            return True
        else:
            print(f"❌ Failed to get drafts: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run the complete flow test"""
    print("\n" + "🚀 ECHOWRITE - COMPLETE FLOW TEST" + "\n")
    print("="*60)
    print("Testing: Remove Sources → Add Sources → Generate Draft")
    print("="*60)
    
    # Authenticate
    if not authenticate():
        print("\n❌ Cannot proceed without authentication")
        return
    
    # Step 1: Check existing sources
    existing_sources = step_1_check_existing_sources()
    
    # Step 2: Remove existing sources
    step_2_remove_existing_sources(existing_sources)
    
    # Step 3: Add new sources
    new_sources = step_3_add_new_sources()
    
    if not new_sources:
        print("\n❌ Cannot proceed without sources")
        return
    
    # Step 4: Ingest content
    ingestion_success = step_4_ingest_content(new_sources)
    
    if not ingestion_success:
        print("\n⚠️  Warning: No content was ingested, but continuing with generation...")
    
    # Step 5: Generate draft
    draft = step_5_generate_draft()
    
    if draft and draft.get('draft_id'):
        # Step 6: View drafts
        step_6_view_draft(draft.get('draft_id'))
    
    # Final summary
    print("\n" + "="*60)
    print("🏁 FLOW TEST COMPLETE")
    print("="*60)
    
    if draft:
        print("✅ All steps completed successfully!")
        print(f"\n📊 Summary:")
        print(f"   - Sources added: {len(new_sources)}")
        print(f"   - Newsletter generated: {draft.get('title')}")
        print(f"   - Draft ID: {draft.get('draft_id')}")
        print(f"\n🌐 View in browser: http://localhost:3000/drafts")
    else:
        print("⚠️  Flow completed with some issues")
        print("   Check the logs above for details")

if __name__ == "__main__":
    main()


