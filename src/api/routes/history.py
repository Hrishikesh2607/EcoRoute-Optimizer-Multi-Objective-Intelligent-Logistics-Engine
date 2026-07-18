from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from src.api.models import TripHistoryItem
from src.db.connection import get_db

router= APIRouter()

@router.get("/v1/history", response_model=List[TripHistoryItem])
def get_history(user_id: str= Query(default="anonymous"), limit: int=20, db: Session= Depends(get_db)):
    query = text("""
        SELECT id, user_id, start_node, end_node, 
               NOW()::text as timestamp, 
               optimized_cost, optimized_duration
        FROM trips
        WHERE user_id = :user_id
        ORDER BY id DESC
        LIMIT :limit
    """)
    result = db.execute(query, {"user_id": user_id, "limit": limit})
    rows = result.fetchall()
    return [
        TripHistoryItem(
            id=r[0], user_id=r[1], start_node=r[2], end_node=r[3],
            timestamp=r[4], optimized_cost=float(r[5]), optimized_duration=float(r[6])
        ) for r in rows
    ]