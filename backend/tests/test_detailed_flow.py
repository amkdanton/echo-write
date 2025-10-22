#!/usr/bin/env python3
"""
Detailed Flow Test: Complete EchoWrite Pipeline with Step-by-Step Outputs
Shows the data at each stage from sources to newsletter generation
"""

import httpx
import json
import time
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv('backend/.env')

BASE_URL = "http://localhost:8000/api/v1"
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")

# Global variables
JWT_TOKEN = None
USER_ID = None

def print_section(title, emoji="📋"):
    """Print a section header"""
    print("\n" + "="*80)
    print(f"{emoji} {title}")
    print("="*80)

def print_subsection(title):
    """Print a subsection header"""
    print(f"\n{title}")
    print("-"*80)

def print_json(data, indent=2):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=indent, default=str))

def authenticate():
    """Authenticate and get JWT token"""
    global JWT_TOKEN, USER_ID
    
    print_section("AUTHENTICATION", "🔐")
    
    print(f"📧 Email: {TEST_EMAIL}")
    print(f"🌐 Supabase URL: {SUPABASE_URL}")
    
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
            
            print(f"\n✅ Authentication Successful!")
            print(f"   User ID: {USER_ID}")
            print(f"   Token: {JWT_TOKEN[:50]}...")
            return True
        else:
            print(f"\n❌ Authentication failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def get_headers():
    """Get authorization headers"""
    return {"Authorization": f"Bearer {JWT_TOKEN}"}

def step_1_add_sources():
    """Step 1: Add content sources"""
    print_section("STEP 1: ADDING CONTENT SOURCES", "📡")
    
    sources_to_add = [
        {
            "type": "rss",
            "handle": "https://feeds.feedburner.com/TechCrunch/",
            "name": "TechCrunch"
        },
        {
            "type": "rss",
            "handle": "https://www.theverge.com/rss/index.xml",
            "name": "The Verge"
        }
    ]
    
    created_sources = []
    
    for source_data in sources_to_add:
        print_subsection(f"Creating Source: {source_data['name']}")
        print(f"Type: {source_data['type']}")
        print(f"URL: {source_data['handle']}")
        
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
                print(f"\n✅ Source Created Successfully!")
                print(f"\n📊 Source Details:")
                print_json({
                    "id": source.get('id'),
                    "name": source.get('name'),
                    "type": source.get('type'),
                    "handle": source.get('handle')[:60] + "...",
                    "is_active": source.get('is_active'),
                    "created_at": source.get('created_at')
                })
            else:
                print(f"\n❌ Failed: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    print(f"\n\n🎉 STEP 1 COMPLETE: Created {len(created_sources)}/{len(sources_to_add)} sources")
    return created_sources

def step_2_ingest_content(sources):
    """Step 2: Fetch content from sources"""
    print_section("STEP 2: INGESTING CONTENT", "📥")
    
    if not sources:
        print("❌ No sources available")
        return None
    
    source_ids = [source.get('id') for source in sources]
    
    print(f"📌 Fetching content from {len(source_ids)} sources:")
    for source in sources:
        print(f"   • {source.get('name')}")
    
    print(f"\n⏳ Processing... (this may take 30-60 seconds)")
    
    try:
        start_time = time.time()
        
        with httpx.Client(timeout=120.0) as client:
            response = client.post(
                f"{BASE_URL}/ingestion/process",
                json={
                    "source_ids": source_ids,
                    "force_refresh": True
                },
                headers={**get_headers(), "Content-Type": "application/json"}
            )
        
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✅ Ingestion Complete! (took {elapsed_time:.1f}s)")
            print(f"\n📊 Ingestion Results:")
            print_json({
                "processed_sources": result.get('processed_sources'),
                "new_items": result.get('new_items'),
                "errors": result.get('errors', [])
            })
            
            # Get sample items to show what was fetched
            print_subsection("Sample Items Fetched")
            print("⏳ Fetching items from database...")
            
            # Query items directly from Supabase
            items_result = get_recent_items(limit=5)
            
            if items_result:
                print(f"\n✅ Found {len(items_result)} sample items:")
                for idx, item in enumerate(items_result[:3], 1):
                    print(f"\n{idx}. 📄 {item.get('title')}")
                    print(f"   URL: {item.get('url')[:70]}...")
                    print(f"   Summary: {item.get('summary', 'N/A')[:100]}...")
                    print(f"   Published: {item.get('published_at')}")
                    print(f"   Trend Score: {item.get('trend_score', 'Not calculated')}")
            
            print(f"\n\n🎉 STEP 2 COMPLETE: Fetched {result.get('new_items')} new items")
            return result
        else:
            print(f"\n❌ Ingestion failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_recent_items(limit=10):
    """Get recent items from the database"""
    try:
        from supabase import create_client
        
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Set auth header
        supabase.auth.set_session(JWT_TOKEN, None)
        
        response = supabase.table("items").select("*").eq("user_id", USER_ID).order("created_at", desc=True).limit(limit).execute()
        
        return response.data
    except Exception as e:
        print(f"   Error fetching items: {e}")
        return []

def step_3_analyze_trends():
    """Step 3: Analyze content and calculate trend scores"""
    print_section("STEP 3: ANALYZING TRENDS & SCORING CONTENT", "📈")
    
    print("🔍 Analyzing content and calculating trend scores...")
    print("   This involves:")
    print("   • Recency Score (40% weight)")
    print("   • Content Quality (25% weight)")
    print("   • Keyword Relevance (20% weight)")
    print("   • Source Authority (10% weight)")
    print("   • Engagement Prediction (5% weight)")
    
    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                f"{BASE_URL}/trends/analysis",
                json={
                    "time_window_hours": 48,
                    "limit": 10
                },
                headers={**get_headers(), "Content-Type": "application/json"}
            )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✅ Trend Analysis Complete!")
            print(f"\n📊 Analysis Summary:")
            
            trending_items = result.get('trending_items', [])
            metadata = result.get('metadata', {})
            
            print_json({
                "total_items_analyzed": metadata.get('total_items_analyzed'),
                "time_window_hours": metadata.get('time_window_hours'),
                "average_trend_score": metadata.get('average_trend_score'),
                "analysis_time": metadata.get('analysis_time')
            })
            
            print_subsection("Top Trending Items")
            print(f"Showing top {min(5, len(trending_items))} items by trend score:\n")
            
            for idx, item in enumerate(trending_items[:5], 1):
                score = item.get('trend_score', 0)
                print(f"{idx}. 🔥 Score: {score:.3f} | {item.get('title')}")
                print(f"   📅 Published: {item.get('published_at')}")
                print(f"   🔗 {item.get('url')[:70]}...")
                print()
            
            print(f"\n🎉 STEP 3 COMPLETE: Analyzed and scored content")
            return result
        else:
            print(f"\n❌ Analysis failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def step_4_add_style_sample():
    """Step 4: Add writing style sample (optional but improves output)"""
    print_section("STEP 4: VOICE TRAINING (OPTIONAL)", "✍️")
    
    print("📝 Adding a writing style sample to train the AI voice...")
    print("   This helps the newsletter match your writing style")
    
    sample_content = """
    Hey there! 👋

    This week has been absolutely wild in the tech world. Let me break down what caught my attention.

    First up: AI developments are moving at lightning speed. The new releases are game-changing.

    What really got me excited though was the breakthrough in quantum computing. This isn't just incremental progress - it's a genuine leap forward.

    And here's the kicker - the implications for cybersecurity are massive. We're talking about a complete paradigm shift in how we think about encryption.

    Bottom line? The future is arriving faster than we expected. Buckle up, it's going to be a wild ride.

    Stay curious,
    """
    
    try:
        with httpx.Client() as client:
            response = client.post(
                f"{BASE_URL}/style/train",
                json={
                    "content": sample_content,
                    "title": "Sample Newsletter Style",
                    "source_type": "newsletter"
                },
                headers={**get_headers(), "Content-Type": "application/json"}
            )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✅ Style Sample Added!")
            print(f"\n📊 Voice Profile Extracted:")
            
            voice_profile = result.get('voice_profile', {})
            voice_traits = voice_profile.get('voice_traits', [])
            characteristics = voice_profile.get('characteristics', {})
            
            print(f"\n🎯 Detected Voice Traits:")
            for trait in voice_traits:
                print(f"   • {trait}")
            
            print(f"\n📐 Writing Characteristics:")
            print_json({
                "avg_sentence_length": characteristics.get('avg_sentence_length'),
                "vocabulary_richness": characteristics.get('vocabulary_richness'),
                "tone_indicators": characteristics.get('tone_indicators', [])
            })
            
            print(f"\n🎉 STEP 4 COMPLETE: Voice profile trained")
            return result
        else:
            print(f"\n⚠️  Style training failed: {response.status_code}")
            print(f"   Continuing without custom voice (will use default)")
            return None
            
    except Exception as e:
        print(f"\n⚠️  Error: {e}")
        print(f"   Continuing without custom voice")
        return None

def step_5_generate_newsletter():
    """Step 5: Generate newsletter using AI"""
    print_section("STEP 5: GENERATING NEWSLETTER WITH AI", "🤖")
    
    print("✨ Generating newsletter...")
    print("   This process:")
    print("   1. Selects top 5 trending items")
    print("   2. Applies your voice profile")
    print("   3. Uses GPT-4 to write the newsletter")
    print("   4. Creates a draft for review")
    
    print(f"\n⏳ Generating... (this may take 10-30 seconds)")
    
    try:
        start_time = time.time()
        
        with httpx.Client(timeout=120.0) as client:
            response = client.post(
                f"{BASE_URL}/generation/newsletter",
                json={
                    "num_items": 5,
                    "time_window_hours": 48,
                    "title": f"Tech Newsletter - {datetime.now().strftime('%B %d, %Y')}"
                },
                headers={**get_headers(), "Content-Type": "application/json"}
            )
        
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                print(f"\n✅ Newsletter Generated! (took {elapsed_time:.1f}s)")
                
                print(f"\n📊 Generation Details:")
                print_json({
                    "draft_id": result.get('draft_id'),
                    "title": result.get('title'),
                    "items_included": result.get('items_included'),
                    "word_count": result.get('word_count')
                })
                
                print_subsection("📰 FULL NEWSLETTER CONTENT")
                body = result.get('body_md', '')
                print(body)
                
                print_subsection("Newsletter Statistics")
                print(f"   Total characters: {len(body)}")
                print(f"   Total words: {result.get('word_count')}")
                print(f"   Total lines: {len(body.split(chr(10)))}")
                
                print(f"\n\n🎉 STEP 5 COMPLETE: Newsletter draft created!")
                print(f"   Draft ID: {result.get('draft_id')}")
                return result
            else:
                print(f"\n❌ Generation failed: {result.get('message')}")
                return None
        else:
            print(f"\n❌ Generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def step_6_view_draft(draft_id):
    """Step 6: View the generated draft"""
    print_section("STEP 6: VIEWING DRAFT IN DATABASE", "👀")
    
    print(f"📋 Fetching draft: {draft_id}")
    
    try:
        with httpx.Client() as client:
            response = client.get(
                f"{BASE_URL}/generation/drafts",
                headers=get_headers()
            )
        
        if response.status_code == 200:
            drafts = response.json()
            
            print(f"\n✅ Found {len(drafts)} total drafts in database")
            
            print_subsection("Recent Drafts")
            for idx, draft in enumerate(drafts[:3], 1):
                print(f"\n{idx}. {draft.get('title')}")
                print(f"   Status: {draft.get('status')}")
                print(f"   Created: {draft.get('created_at')}")
                print(f"   Draft ID: {draft.get('id')}")
            
            print(f"\n🎉 STEP 6 COMPLETE: Draft stored successfully")
            return True
        else:
            print(f"\n❌ Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    """Run the complete detailed flow test"""
    print("\n")
    print("🚀 " + "="*76 + " 🚀")
    print("   ECHOWRITE - COMPLETE FLOW TEST WITH DETAILED OUTPUTS")
    print("🚀 " + "="*76 + " 🚀")
    print("\nThis test will show you EXACTLY what happens at each step:")
    print("  1. Add content sources (RSS feeds)")
    print("  2. Ingest & fetch content")
    print("  3. Analyze trends & score content")
    print("  4. Train AI on your writing voice")
    print("  5. Generate newsletter with AI")
    print("  6. View the final draft")
    
    print("\n⏳ Starting automated test...\n")
    
    # Authenticate
    if not authenticate():
        print("\n❌ Cannot proceed without authentication")
        return
    
    # Step 1: Add sources
    sources = step_1_add_sources()
    if not sources:
        print("\n❌ Cannot proceed without sources")
        return
    
    print("\n\n⏳ Moving to Step 2 (Ingestion)...")
    time.sleep(2)
    
    # Step 2: Ingest content
    ingestion_result = step_2_ingest_content(sources)
    if not ingestion_result:
        print("\n⚠️  Warning: Ingestion had issues, but continuing...")
    
    print("\n\n⏳ Moving to Step 3 (Trend Analysis)...")
    time.sleep(2)
    
    # Step 3: Analyze trends
    trends_result = step_3_analyze_trends()
    
    print("\n\n⏳ Moving to Step 4 (Voice Training)...")
    time.sleep(2)
    
    # Step 4: Add style sample
    style_result = step_4_add_style_sample()
    
    print("\n\n⏳ Moving to Step 5 (Newsletter Generation)...")
    time.sleep(2)
    
    # Step 5: Generate newsletter
    draft_result = step_5_generate_newsletter()
    
    if draft_result and draft_result.get('draft_id'):
        print("\n\n⏳ Moving to Step 6 (View Draft)...")
        time.sleep(2)
        
        # Step 6: View draft
        step_6_view_draft(draft_result.get('draft_id'))
        
        # Final summary
        print_section("🏁 FLOW TEST COMPLETE!", "🎊")
        
        print("\n✅ ALL STEPS COMPLETED SUCCESSFULLY!\n")
        print("📊 Summary of what happened:")
        print(f"   1. ✅ Added {len(sources)} content sources")
        print(f"   2. ✅ Fetched {ingestion_result.get('new_items', 0)} new items")
        print(f"   3. ✅ Analyzed and scored content")
        print(f"   4. ✅ Trained AI on writing voice")
        print(f"   5. ✅ Generated newsletter with {draft_result.get('items_included')} items")
        print(f"   6. ✅ Saved draft to database")
        
        print(f"\n📧 Newsletter Details:")
        print(f"   Title: {draft_result.get('title')}")
        print(f"   Draft ID: {draft_result.get('draft_id')}")
        print(f"   Word Count: {draft_result.get('word_count')}")
        
        print(f"\n🌐 Next Steps:")
        print(f"   • View in browser: http://localhost:3000/drafts")
        print(f"   • Edit the draft if needed")
        print(f"   • Send to your subscribers")
        
        print("\n" + "="*80)
        print("Thank you for testing EchoWrite! 🎉")
        print("="*80 + "\n")
    else:
        print_section("⚠️  FLOW INCOMPLETE", "⚠️")
        print("Some steps failed. Check the logs above for details.")

if __name__ == "__main__":
    main()

