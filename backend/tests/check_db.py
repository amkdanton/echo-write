#!/usr/bin/env python3
"""
Quick script to check database state after test flow
"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv('backend/.env')

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("🔍 Checking Database State...")
print("="*60)

# Check sources
sources = supabase.table("sources").select("*").execute()
print(f"\n📡 SOURCES: {len(sources.data)} found")
for source in sources.data:
    print(f"   - {source.get('name')} ({source.get('type')}) - {source.get('handle')}")

# Check items
items = supabase.table("items").select("*").execute()
print(f"\n📰 ITEMS: {len(items.data)} found")
if items.data:
    for item in items.data[:5]:  # Show first 5
        print(f"   - {item.get('title')[:60]}...")
        print(f"     Published: {item.get('published_at')}, Score: {item.get('trend_score')}")
else:
    print("   ❌ No items found in database!")

# Check drafts
drafts = supabase.table("drafts").select("*").execute()
print(f"\n📝 DRAFTS: {len(drafts.data)} found")
if drafts.data:
    for draft in drafts.data:
        print(f"   - {draft.get('title')} (Status: {draft.get('status')})")
        print(f"     Created: {draft.get('created_at')}")
else:
    print("   ❌ No drafts found in database!")

print("\n" + "="*60)


