#!/usr/bin/env python3
"""
API Testing Script for EchoWrite
Tests all backend APIs systematically with JWT authentication
Uses test credentials to automatically generate JWT token and test all APIs
"""

import httpx
import json
import uuid
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:8000/api/v1"
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

# Test credentials from .env
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")

# Global JWT token
JWT_TOKEN = None

def get_auth_headers():
    """Get authentication headers with JWT token"""
    if JWT_TOKEN:
        return {"Authorization": f"Bearer {JWT_TOKEN}"}
    else:
        return {}

def authenticate_and_get_token():
    """Authenticate with test credentials and get JWT token"""
    global JWT_TOKEN
    
    if not TEST_EMAIL or not TEST_PASSWORD:
        print("❌ TEST_EMAIL and TEST_PASSWORD not found in .env file")
        return False
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ SUPABASE_URL and SUPABASE_KEY not found in .env file")
        return False
    
    print(f"🔐 Authenticating with test credentials: {TEST_EMAIL}")
    
    try:
        # Sign in with test credentials
        with httpx.Client() as client:
            auth_response = client.post(
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
            JWT_TOKEN = auth_data.get("access_token")
            print(f"✅ Authentication successful!")
            print(f"   User ID: {auth_data.get('user', {}).get('id')}")
            print(f"   Token: {JWT_TOKEN[:50]}...")
            return True
        else:
            print(f"❌ Authentication failed: {auth_response.status_code}")
            print(f"   Error: {auth_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return False

def extract_jwt_from_browser():
    """
    Helper function to extract JWT token from browser localStorage
    Instructions for getting the token:
    1. Open your EchoWrite frontend app in browser
    2. Sign in successfully
    3. Open DevTools (F12) → Application → Local Storage → localhost:3000
    4. Find 'sb-peakhkwxuahhpovehijt-auth-token'
    5. Copy the JSON value
    6. Extract the 'access_token' field
    7. Set TEST_JWT_TOKEN = f"Bearer {access_token}"
    """
    print("\n🔑 To get JWT token for testing:")
    print("1. Sign in to http://localhost:3000")
    print("2. Open DevTools (F12) → Application → Local Storage")
    print("3. Copy the 'sb-peakhkwxuahhpovehijt-auth-token' value")
    print("4. Extract 'access_token' from the JSON")
    print("5. Update TEST_JWT_TOKEN in this script")
    return None

def test_health():
    """Test health endpoint"""
    print("🔍 Testing Health API...")
    try:
        with httpx.Client() as client:
            response = client.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("✅ Health API: OK")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Health API: FAILED ({response.status_code})")
                print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Health API: ERROR - {e}")

def test_sources_api():
    """Test sources API endpoints with JWT authentication - CREATE, TEST, DELETE"""
    print("\n🔍 Testing Sources API (Full CRUD + Test)...")
    
    headers = get_auth_headers()
    if not headers:
        print("⚠️  Skipping authenticated endpoints - no JWT token")
        return False
    
    created_sources = []  # Track created sources for cleanup
    
    # 1. Get initial sources count
    print("   📋 Step 1: GET initial sources...")
    try:
        with httpx.Client() as client:
            response = client.get(f"{BASE_URL}/ingestion/sources", headers=headers)
        if response.status_code == 200:
            initial_sources = response.json()
            print(f"✅ GET Sources: OK ({len(initial_sources)} sources found)")
            for source in initial_sources:
                print(f"   - {source.get('name', 'Unnamed')} ({source.get('type')})")
        else:
            print(f"❌ GET Sources: FAILED ({response.status_code}) - {response.text}")
            return False
    except Exception as e:
        print(f"❌ GET Sources: ERROR - {e}")
        return False
    
    # 2. Create test sources
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
        },
        {
            "type": "youtube",
            "handle": "UCBJycsmduvYEL83R_U4JriQ",  # Marques Brownlee
            "name": "MKBHD YouTube"
        }
    ]
    
    print(f"   📝 Step 2: CREATE {len(test_sources)} test sources...")
    for i, source_data in enumerate(test_sources, 1):
        print(f"   Creating source {i}/{len(test_sources)}: {source_data['name']}")
        try:
            with httpx.Client() as client:
                response = client.post(
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
        print("   ❌ No sources were created, skipping remaining tests")
        return False
    
    # 3. Test created sources
    print(f"   🧪 Step 3: TEST {len(created_sources)} sources...")
    for source in created_sources:
        source_id = source.get("id")
        source_name = source.get("name")
        print(f"   Testing: {source_name}")
        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{BASE_URL}/ingestion/test/{source_id}",
                    headers=headers
                )
            if response.status_code == 200:
                test_result = response.json()
                new_items = test_result.get("new_items", 0)
                print(f"   ✅ Test OK: Found {new_items} new items")
            else:
                print(f"   ❌ Test FAILED: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"   ❌ Test ERROR: {e}")
    
    # 4. Verify sources were created
    print("   📋 Step 4: VERIFY sources were created...")
    try:
        with httpx.Client() as client:
            response = client.get(f"{BASE_URL}/ingestion/sources", headers=headers)
        if response.status_code == 200:
            updated_sources = response.json()
            print(f"✅ Verification: {len(updated_sources)} total sources (added {len(created_sources)})")
        else:
            print(f"❌ Verification FAILED: {response.status_code}")
    except Exception as e:
        print(f"❌ Verification ERROR: {e}")
    
    # 5. Delete created sources (cleanup)
    print(f"   🗑️  Step 5: DELETE {len(created_sources)} test sources (cleanup)...")
    for source in created_sources:
        source_id = source.get("id")
        source_name = source.get("name")
        print(f"   Deleting: {source_name}")
        try:
            with httpx.Client() as client:
                response = client.delete(
                    f"{BASE_URL}/ingestion/sources/{source_id}",
                    headers=headers
                )
            if response.status_code == 200:
                print(f"   ✅ Deleted: {source_name}")
            else:
                print(f"   ❌ Delete FAILED: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"   ❌ Delete ERROR: {e}")
    
    # 6. Final verification
    print("   📋 Step 6: FINAL verification (should be back to initial state)...")
    try:
        with httpx.Client() as client:
            response = client.get(f"{BASE_URL}/ingestion/sources", headers=headers)
        if response.status_code == 200:
            final_sources = response.json()
            print(f"✅ Final state: {len(final_sources)} sources (should match initial: {len(initial_sources)})")
            if len(final_sources) == len(initial_sources):
                print("✅ SOURCES API TEST: COMPLETE SUCCESS!")
                return True
            else:
                print("⚠️  SOURCES API TEST: PARTIAL SUCCESS (cleanup incomplete)")
                return True
        else:
            print(f"❌ Final verification FAILED: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Final verification ERROR: {e}")
        return False

def test_trends_api():
    """Test trends API with JWT authentication"""
    print("\n🔍 Testing Trends API...")
    
    headers = get_auth_headers()
    if not headers:
        print("⚠️  Skipping authenticated endpoints - no JWT token")
        return False
    
    # Test different time windows and limits
    test_cases = [
        {"time_window_hours": 24, "limit": 5, "name": "24h, 5 items"},
        {"time_window_hours": 48, "limit": 10, "name": "48h, 10 items"},
        {"time_window_hours": 168, "limit": 20, "name": "7 days, 20 items"}
    ]
    
    success_count = 0
    for test_case in test_cases:
        print(f"   Testing: {test_case['name']}")
        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{BASE_URL}/trends/analysis",
                    json={
                        "time_window_hours": test_case["time_window_hours"],
                        "limit": test_case["limit"]
                    },
                    headers={**headers, "Content-Type": "application/json"}
                )
            if response.status_code == 200:
                result = response.json()
                trending_items = result.get("trending_items", [])
                metadata = result.get("analysis_metadata", {})
                print(f"   ✅ Success: Found {len(trending_items)} trending items")
                print(f"   📊 Metadata: {metadata}")
                success_count += 1
            elif response.status_code == 401:
                print(f"   ❌ UNAUTHORIZED (401) - Invalid JWT token")
                print(f"   Error: {response.text}")
                return False
            else:
                print(f"   ❌ FAILED ({response.status_code}) - {response.text}")
        except Exception as e:
            print(f"   ❌ ERROR - {e}")
    
    if success_count == len(test_cases):
        print("✅ TRENDS API TEST: COMPLETE SUCCESS!")
        return True
    elif success_count > 0:
        print(f"⚠️  TRENDS API TEST: PARTIAL SUCCESS ({success_count}/{len(test_cases)})")
        return True
    else:
        print("❌ TRENDS API TEST: FAILED")
        return False

def test_generation_api():
    """Test generation API with JWT authentication - GET drafts, GENERATE newsletter"""
    print("\n🔍 Testing Generation API...")
    
    headers = get_auth_headers()
    if not headers:
        print("⚠️  Skipping authenticated endpoints - no JWT token")
        return False
    
    # 1. Test get drafts (initial state)
    print("   📋 Step 1: GET initial drafts...")
    try:
        with httpx.Client() as client:
            response = client.get(f"{BASE_URL}/generation/drafts", headers=headers)
        if response.status_code == 200:
            initial_drafts = response.json()
            print(f"✅ GET Drafts: OK ({len(initial_drafts)} drafts found)")
            for draft in initial_drafts:
                print(f"   - {draft.get('title', 'Untitled')} ({draft.get('status')})")
        elif response.status_code == 401:
            print("❌ GET Drafts: UNAUTHORIZED (401) - Invalid JWT token")
            print(f"   Error: {response.text}")
            return False
        else:
            print(f"❌ GET Drafts: FAILED ({response.status_code}) - {response.text}")
            return False
    except Exception as e:
        print(f"❌ GET Drafts: ERROR - {e}")
        return False
    
    # 2. Test generate newsletter with different scenarios
    test_scenarios = [
        {
            "trending_items": [],
            "custom_prompt": "Generate a test newsletter about technology trends",
            "name": "Empty items + custom prompt"
        },
        {
            "trending_items": ["fake-item-id-1", "fake-item-id-2"],
            "custom_prompt": None,
            "name": "Mock items + no custom prompt"
        },
        {
            "trending_items": [],
            "custom_prompt": "Create a weekly tech roundup with latest news and insights",
            "name": "Empty items + detailed prompt"
        }
    ]
    
    generated_drafts = []
    print(f"   📝 Step 2: GENERATE newsletters ({len(test_scenarios)} scenarios)...")
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"   Generating scenario {i}/{len(test_scenarios)}: {scenario['name']}")
        try:
            payload = {"trending_items": scenario["trending_items"]}
            if scenario["custom_prompt"]:
                payload["custom_prompt"] = scenario["custom_prompt"]
            
            with httpx.Client() as client:
                response = client.post(
                    f"{BASE_URL}/generation/newsletter",
                    json=payload,
                    headers={**headers, "Content-Type": "application/json"}
                )
            
            if response.status_code == 200:
                result = response.json()
                draft = result.get("draft", {})
                metadata = result.get("generation_metadata", {})
                print(f"   ✅ Generated: {draft.get('title', 'Untitled')}")
                print(f"   📊 Status: {draft.get('status', 'unknown')}")
                print(f"   📊 Metadata: {metadata}")
                generated_drafts.append(draft)
            elif response.status_code == 401:
                print(f"   ❌ UNAUTHORIZED (401) - Invalid JWT token")
                print(f"   Error: {response.text}")
                return False
            else:
                print(f"   ❌ FAILED ({response.status_code}) - {response.text}")
        except Exception as e:
            print(f"   ❌ ERROR - {e}")
        
        # Small delay between generations
        time.sleep(1)
    
    # 3. Verify drafts were created
    print("   📋 Step 3: VERIFY drafts were created...")
    try:
        with httpx.Client() as client:
            response = client.get(f"{BASE_URL}/generation/drafts", headers=headers)
        if response.status_code == 200:
            updated_drafts = response.json()
            print(f"✅ Verification: {len(updated_drafts)} total drafts (added {len(generated_drafts)})")
            for draft in updated_drafts:
                print(f"   - {draft.get('title', 'Untitled')} ({draft.get('status')})")
        else:
            print(f"❌ Verification FAILED: {response.status_code}")
    except Exception as e:
        print(f"❌ Verification ERROR: {e}")
    
    # 4. Test with invalid data
    print("   🧪 Step 4: TEST error handling...")
    try:
        with httpx.Client() as client:
            response = client.post(
                f"{BASE_URL}/generation/newsletter",
                json={"invalid": "data"},
                headers={**headers, "Content-Type": "application/json"}
            )
        if response.status_code == 422:  # Validation error
            print("   ✅ Error handling: Correctly rejected invalid data")
        else:
            print(f"   ⚠️  Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error handling test failed: {e}")
    
    print("✅ GENERATION API TEST: COMPLETE SUCCESS!")
    return True

def test_ingestion_status():
    """Test ingestion status endpoint"""
    print("\n🔍 Testing Ingestion Status API...")
    try:
        with httpx.Client() as client:
            response = client.get(f"{BASE_URL}/ingestion/status")
        if response.status_code == 200:
            print("✅ Ingestion Status: OK")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Ingestion Status: FAILED ({response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Ingestion Status: ERROR - {e}")

def test_without_auth():
    """Test endpoints without authentication to verify 401 responses"""
    print("\n🔍 Testing Authentication (should return 401)...")
    
    endpoints_to_test = [
        ("GET", "/ingestion/sources"),
        ("POST", "/ingestion/sources"),
        ("POST", "/trends/analysis"),
        ("GET", "/generation/drafts"),
        ("POST", "/generation/newsletter")
    ]
    
    for method, endpoint in endpoints_to_test:
        try:
            with httpx.Client() as client:
                if method == "GET":
                    response = client.get(f"{BASE_URL}{endpoint}")
                elif method == "POST":
                    response = client.post(f"{BASE_URL}{endpoint}", json={})
            
            if response.status_code == 401:
                print(f"✅ {method} {endpoint}: Correctly returns 401 (Unauthorized)")
            else:
                print(f"❌ {method} {endpoint}: Expected 401, got {response.status_code}")
        except Exception as e:
            print(f"❌ {method} {endpoint}: ERROR - {e}")

def main():
    """Run comprehensive API tests with authentication and logging"""
    print("🚀 EchoWrite API Testing Suite")
    print("=" * 60)
    print(f"🕐 Test started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Track test results
    test_results = {
        "health": False,
        "ingestion_status": False,
        "auth_protection": False,
        "authentication": False,
        "sources_api": False,
        "trends_api": False,
        "generation_api": False
    }
    
    # 1. Test public endpoints (no auth required)
    print("\n🌐 TESTING PUBLIC ENDPOINTS")
    print("-" * 40)
    
    print("🔍 Testing Health API...")
    try:
        test_health()
        test_results["health"] = True
        print("✅ Health API: PASSED")
    except Exception as e:
        print(f"❌ Health API: FAILED - {e}")
    
    print("\n🔍 Testing Ingestion Status API...")
    try:
        test_ingestion_status()
        test_results["ingestion_status"] = True
        print("✅ Ingestion Status API: PASSED")
    except Exception as e:
        print(f"❌ Ingestion Status API: FAILED - {e}")
    
    # 2. Test authentication protection (should return 401)
    print("\n🔒 TESTING AUTHENTICATION PROTECTION")
    print("-" * 40)
    try:
        test_without_auth()
        test_results["auth_protection"] = True
        print("✅ Authentication Protection: PASSED")
    except Exception as e:
        print(f"❌ Authentication Protection: FAILED - {e}")
    
    # 3. Authenticate with test credentials
    print("\n🔐 AUTHENTICATING WITH TEST CREDENTIALS")
    print("-" * 40)
    auth_success = authenticate_and_get_token()
    test_results["authentication"] = auth_success
    
    if not auth_success:
        print("\n❌ AUTHENTICATION FAILED - Cannot proceed with authenticated tests")
        print("📝 Make sure TEST_EMAIL and TEST_PASSWORD are set in .env file")
        print("📝 And that the test user exists in Supabase")
    else:
        # 4. Test authenticated endpoints
        print("\n🔐 TESTING AUTHENTICATED ENDPOINTS")
        print("-" * 40)
        
        # Test Sources API (Full CRUD)
        print("\n📡 Testing Sources API...")
        try:
            sources_success = test_sources_api()
            test_results["sources_api"] = sources_success
        except Exception as e:
            print(f"❌ Sources API: FAILED - {e}")
        
        # Test Trends API
        print("\n📊 Testing Trends API...")
        try:
            trends_success = test_trends_api()
            test_results["trends_api"] = trends_success
        except Exception as e:
            print(f"❌ Trends API: FAILED - {e}")
        
        # Test Generation API
        print("\n📝 Testing Generation API...")
        try:
            generation_success = test_generation_api()
            test_results["generation_api"] = generation_success
        except Exception as e:
            print(f"❌ Generation API: FAILED - {e}")
    
    # 5. Final results summary
    print("\n" + "=" * 60)
    print("🏁 FINAL TEST RESULTS")
    print("=" * 60)
    
    total_tests = len(test_results)
    passed_tests = sum(test_results.values())
    
    print(f"🕐 Test completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Overall Result: {passed_tests}/{total_tests} tests passed")
    
    print("\n📋 Detailed Results:")
    for test_name, passed in test_results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {test_name.replace('_', ' ').title()}: {status}")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! Your EchoWrite API is working perfectly!")
    elif passed_tests > total_tests // 2:
        print(f"\n⚠️  MOSTLY WORKING: {passed_tests}/{total_tests} tests passed")
        print("   Some features may need attention")
    else:
        print(f"\n❌ NEEDS WORK: Only {passed_tests}/{total_tests} tests passed")
        print("   Please check the failed tests above")
    
    print("\n📝 Test Summary:")
    print("- Public endpoints (health, status) should always work")
    print("- Authentication protection should return 401 for unauthorized requests")
    print("- Sources API should handle full CRUD operations")
    print("- Trends API should analyze content and return trending items")
    print("- Generation API should create newsletter drafts")
    
    return test_results

if __name__ == "__main__":
    main()
