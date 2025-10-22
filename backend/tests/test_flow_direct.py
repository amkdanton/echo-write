#!/usr/bin/env python3
"""
Test the complete flow directly with proper authentication
"""

import httpx
import json
import os
import time
from dotenv import load_dotenv

load_dotenv('backend/.env')

BASE_URL = "http://localhost:8000/api/v1"
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")

print("🔐 Step 1: Authenticating...")
with httpx.Client() as client:
    auth_response = client.post(
        f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
        headers={"apikey": SUPABASE_KEY, "Content-Type": "application/json"},
        json={"email": TEST_EMAIL, "password": TEST_PASSWORD}
    )

if auth_response.status_code != 200:
    print(f"❌ Auth failed: {auth_response.text}")
    exit(1)

JWT_TOKEN = auth_response.json().get("access_token")
USER_ID = auth_response.json().get('user', {}).get('id')
headers = {"Authorization": f"Bearer {JWT_TOKEN}"}

print(f"✅ Authenticated as {TEST_EMAIL} (User ID: {USER_ID})")

# Step 2: Check sources
print("\n📡 Step 2: Checking sources...")
with httpx.Client() as client:
    sources_response = client.get(f"{BASE_URL}/ingestion/sources", headers=headers)
    sources = sources_response.json()
    print(f"✅ Found {len(sources)} sources")
    for source in sources:
        print(f"   - {source.get('name')} (ID: {source.get('id')})")

if not sources:
    print("❌ No sources found! Test stopped.")
    exit(1)

# Step 3: Test ingestion
print("\n📥 Step 3: Testing ingestion (this may take 30-60 seconds)...")
source_ids = [s['id'] for s in sources]
print(f"   Processing {len(source_ids)} sources...")

with httpx.Client(timeout=120.0) as client:
    ingest_response = client.post(
        f"{BASE_URL}/ingestion/process",
        json={"source_ids": source_ids, "force_refresh": True},
        headers={**headers, "Content-Type": "application/json"}
    )

if ingest_response.status_code != 200:
    print(f"❌ Ingestion failed: {ingest_response.status_code}")
    print(f"   Response: {ingest_response.text}")
    exit(1)

ingest_result = ingest_response.json()
print(f"✅ Ingestion complete!")
print(f"   Processed sources: {ingest_result.get('processed_sources')}")
print(f"   New items: {ingest_result.get('new_items')}")
print(f"   Errors: {ingest_result.get('errors', [])}")

if ingest_result.get('new_items') == 0:
    print("\n⚠️  WARNING: No items were fetched from sources!")
    print("   Checking detailed errors...")
    for error in ingest_result.get('errors', []):
        print(f"   - {error}")

# Step 4: Test generation
print("\n✨ Step 4: Testing newsletter generation...")
print("   This will use AI to generate content (may take 10-20 seconds)...")

with httpx.Client(timeout=120.0) as client:
    gen_response = client.post(
        f"{BASE_URL}/generation/newsletter",
        json={"trending_items": [], "custom_prompt": None},
        headers={**headers, "Content-Type": "application/json"}
    )

print(f"   Response status: {gen_response.status_code}")

if gen_response.status_code != 200:
    print(f"❌ Generation failed: {gen_response.status_code}")
    print(f"   Response: {gen_response.text}")
else:
    result = gen_response.json()
    print(f"\n📝 Generation Response:")
    print(json.dumps(result, indent=2))
    
    if result.get('success'):
        print(f"\n✅ SUCCESS! Newsletter generated!")
        print(f"   Draft ID: {result.get('draft_id')}")
        print(f"   Title: {result.get('title')}")
        print(f"   Items: {result.get('items_included')}")
        print(f"   Words: {result.get('word_count')}")
    else:
        print(f"\n❌ Generation returned success=False")
        print(f"   Message: {result.get('message')}")

# Step 5: Check drafts
print("\n📋 Step 5: Checking drafts...")
with httpx.Client() as client:
    drafts_response = client.get(f"{BASE_URL}/generation/drafts", headers=headers)
    drafts = drafts_response.json()
    print(f"✅ Found {len(drafts)} drafts")
    for draft in drafts:
        print(f"   - {draft.get('title')} (Status: {draft.get('status')})")

print("\n" + "="*60)
print("🏁 TEST COMPLETE")
print("="*60)


