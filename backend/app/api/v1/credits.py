"""
Credit management endpoints for user credits and generation tracking
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from app.core.database import get_user_supabase
from app.api.v1.auth import get_current_user_id, get_jwt_token

router = APIRouter()

class CreditInfo(BaseModel):
    credits: int
    total_generations: int
    last_generation_at: Optional[str] = None

class CreditTransaction(BaseModel):
    id: str
    transaction_type: str
    amount: int
    description: str = None
    created_at: str

class AddCreditsRequest(BaseModel):
    credit_amount: int
    description: str = "Credit refill"

@router.get("/credits", response_model=CreditInfo)
async def get_user_credits(
    user_id: str = Depends(get_current_user_id),
    jwt_token: str = Depends(get_jwt_token)
):
    """Get user's current credit information"""
    try:
        supabase = get_user_supabase(jwt_token)
        
        # Get user profile with credit information
        result = supabase.table('user_profiles').select(
            'credits, total_generations, last_generation_at'
        ).eq('id', user_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        profile = result.data[0]
        
        return CreditInfo(
            credits=profile.get('credits', 0),
            total_generations=profile.get('total_generations', 0),
            last_generation_at=profile.get('last_generation_at')
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user credits: {str(e)}")

@router.get("/credits/transactions", response_model=List[CreditTransaction])
async def get_credit_transactions(
    limit: int = 20,
    user_id: str = Depends(get_current_user_id),
    jwt_token: str = Depends(get_jwt_token)
):
    """Get user's credit transaction history"""
    try:
        supabase = get_user_supabase(jwt_token)
        
        # Get credit transactions for the user
        result = supabase.table('credit_transactions').select(
            'id, transaction_type, amount, description, created_at'
        ).eq('user_id', user_id).order('created_at', desc=True).limit(limit).execute()
        
        transactions = []
        for tx in result.data:
            transactions.append(CreditTransaction(
                id=tx['id'],
                transaction_type=tx['transaction_type'],
                amount=tx['amount'],
                description=tx.get('description'),
                created_at=tx['created_at']
            ))
        
        return transactions
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get credit transactions: {str(e)}")

@router.post("/credits/add")
async def add_credits(
    request: AddCreditsRequest,
    user_id: str = Depends(get_current_user_id),
    jwt_token: str = Depends(get_jwt_token)
):
    """Add credits to user account (admin function)"""
    try:
        supabase = get_user_supabase(jwt_token)
        
        # Call the add_user_credits function
        result = supabase.rpc('add_user_credits', {
            'user_uuid': user_id,
            'credit_amount': request.credit_amount,
            'description': request.description
        }).execute()
        
        return {
            "success": True,
            "message": f"Added {request.credit_amount} credits to user account",
            "credits_added": request.credit_amount
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add credits: {str(e)}")

@router.get("/credits/check")
async def check_credits_for_generation(
    required_credits: int = 1,
    user_id: str = Depends(get_current_user_id),
    jwt_token: str = Depends(get_jwt_token)
):
    """Check if user has enough credits for generation"""
    try:
        supabase = get_user_supabase(jwt_token)
        
        # Call the user_has_credits function
        result = supabase.rpc('user_has_credits', {
            'user_uuid': user_id,
            'required_credits': required_credits
        }).execute()
        
        has_credits = result.data if result.data is not None else False
        
        # Get current credit count
        profile_result = supabase.table('user_profiles').select(
            'credits, total_generations'
        ).eq('id', user_id).execute()
        
        profile = profile_result.data[0] if profile_result.data else {}
        
        return {
            "has_credits": has_credits,
            "current_credits": profile.get('credits', 0),
            "total_generations": profile.get('total_generations', 0),
            "required_credits": required_credits
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check credits: {str(e)}")
