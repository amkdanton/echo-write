"""
Authentication utilities for API endpoints
"""

from fastapi import HTTPException, Header
import jwt


async def get_current_user_id(authorization: str = Header(None)) -> str:
    """Extract user ID from JWT token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        # Remove "Bearer " prefix
        token = authorization.replace("Bearer ", "")
        
        # Decode JWT token (Supabase uses HS256)
        # For now, we'll extract from the token payload without verification
        # In production, you should verify the signature
        decoded = jwt.decode(token, options={"verify_signature": False})
        user_id = decoded.get("sub")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: no user ID")
        
        return user_id
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")


async def get_jwt_token(authorization: str = Header(None)) -> str:
    """Extract JWT token from Authorization header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="No authorization header")
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    return parts[1]

