"""
Database configuration and connection management
"""

import os
from supabase import create_client, Client
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")

# Global Supabase client (service account)
supabase: Optional[Client] = None

async def init_db():
    """Initialize database connection"""
    global supabase
    
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise ValueError("Supabase URL and Key must be provided")
    
    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    print("✅ Database connection initialized")

def get_supabase() -> Client:
    """Get Supabase client instance (service account)"""
    if supabase is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return supabase

def get_user_supabase(jwt_token: str) -> Client:
    """Get Supabase client instance for authenticated user"""
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise ValueError("Supabase URL and Key must be provided")
    
    # Create client with user's JWT token
    client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    
    # Set the user's JWT token for authenticated requests
    # For API calls, we can set the session with just the access token
    # and a dummy refresh token since we're not doing token refresh
    client.auth.set_session(jwt_token, "dummy_refresh_token")
    
    return client

# Database table names
class Tables:
    USERS = "users"
    SOURCES = "sources"
    ITEMS = "items"
    STYLE_SAMPLES = "style_samples"
    DRAFTS = "drafts"
    FEEDBACK = "feedback"
