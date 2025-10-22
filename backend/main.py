"""
EchoWrite FastAPI Backend
AI-powered newsletter generation and content curation
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import os
from dotenv import load_dotenv

from app.api.v1 import ingestion, trends, style, generation, delivery, feedback, health
from app.core.database import init_db

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="EchoWrite API",
    description="AI-powered newsletter generation and content curation",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

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
