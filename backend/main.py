"""
EchoWrite FastAPI Backend
AI-powered newsletter generation and content curation
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv

from app.api.v1 import ingestion, trends, style, generation, delivery, feedback, health, credits
from app.core.database import init_db

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="EchoWrite API",
    description="AI-powered newsletter generation and content curation",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_tags=[
        {"name": "health", "description": "Health check endpoints"},
        {"name": "ingestion", "description": "Content ingestion and source management"},
        {"name": "trends", "description": "Trend analysis and scoring"},
        {"name": "style", "description": "Voice training and style analysis"},
        {"name": "generation", "description": "Newsletter generation and drafts"},
        {"name": "delivery", "description": "Email delivery and scheduling"},
        {"name": "feedback", "description": "User feedback and analytics"},
        {"name": "credits", "description": "Credit system management"},
    ]
)

# Add security scheme for JWT authentication
security = HTTPBearer()

# Custom OpenAPI schema to include security definitions
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    from fastapi.openapi.utils import get_openapi
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your Supabase JWT token"
        }
    }
    
    # Add security requirement to all endpoints
    openapi_schema["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for production
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.vercel.app", "*.onrender.com"]
)

# Include API routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(ingestion.router, prefix="/api/v1", tags=["ingestion"])
app.include_router(trends.router, prefix="/api/v1", tags=["trends"])
app.include_router(style.router, prefix="/api/v1", tags=["style"])
app.include_router(generation.router, prefix="/api/v1", tags=["generation"])
app.include_router(delivery.router, prefix="/api/v1", tags=["delivery"])
app.include_router(feedback.router, prefix="/api/v1", tags=["feedback"])
app.include_router(credits.router, prefix="/api/v1", tags=["credits"])

@app.on_event("startup")
async def startup_event():
    """Initialize database and services on startup"""
    await init_db()
    print("🚀 EchoWrite API started successfully!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 EchoWrite API shutting down...")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "EchoWrite API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/api/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
