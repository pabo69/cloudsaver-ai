#!/usr/bin/env python3
"""
FastAPI server for CloudSaver
"""
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Import our modules
from auth import get_user, supabase
from database import SessionLocal, CostRecord
from sqlalchemy import func

app = FastAPI(title="CloudSaver API")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to verify authentication
def verify_token(authorization: Optional[str] = Header(None)):
    """Verify JWT token from header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="No authorization header")
    
    # Extract token (format: "Bearer TOKEN")
    try:
        token = authorization.split(" ")[1]
    except:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    # Verify with Supabase
    user = get_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user

# Routes
@app.get("/")
def root():
    """Health check"""
    return {"status": "ok", "message": "CloudSaver API is running"}

@app.get("/api/costs")
def get_costs(
    db = Depends(get_db),
    current_user = Depends(verify_token)
):
    """
    Get cost data (protected endpoint)
    """
    # Query database
    costs = db.query(CostRecord).order_by(CostRecord.date.desc()).limit(100).all()
    
    # Convert to dict
    results = [
        {
            "date": cost.date.isoformat(),
            "service": cost.service,
            "cost": cost.cost
        }
        for cost in costs
    ]
    
    return {
        "user": current_user.user.email,
        "count": len(results),
        "costs": results
    }

@app.get("/api/summary")
def get_summary(
    db = Depends(get_db),
    current_user = Depends(verify_token)
):
    """
    Get cost summary by service
    """
    # Group by service and sum
    results = db.query(
        CostRecord.service,
        func.sum(CostRecord.cost).label('total_cost')
    ).group_by(CostRecord.service).all()
    
    summary = [
        {"service": service, "total_cost": float(total)}
        for service, total in results
    ]
    
    # Sort by cost
    summary.sort(key=lambda x: x['total_cost'], reverse=True)
    
    return {
        "user": current_user.user.email,
        "services": summary
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting server on http://localhost:8000")
    print("Docs at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)