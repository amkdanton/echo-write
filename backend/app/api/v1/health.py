"""
Health check endpoints
"""

from fastapi import APIRouter
from datetime import datetime
import os

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with service status"""
    from app.core.database import get_supabase
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "services": {}
    }
    
    # Check database connection
    try:
        supabase = get_supabase()
        # Simple query to test connection
        supabase.table("users").select("id").limit(1).execute()
        health_status["services"]["database"] = "healthy"
    except Exception as e:
        health_status["services"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check external services
    health_status["services"]["openai"] = "not_configured"  # Will be updated when implemented
    health_status["services"]["resend"] = "not_configured"  # Will be updated when implemented
    
    return health_status
