from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.api.models import OptimizeRequest, OptimizeResponse
from src.api.dependencies import get_graph
from src.db.connection import get_db, SessionLocal
from src.core.genetic_optimizer import run_ga
import pandas as pd

router= APIRouter()


zone_coords= pd.read_parquet("data/processed/zone_coords.parquet").set_index("LocationID")

@router.post("/v1/optimize", response_model=OptimizeResponse)
def optimize_route(req: OptimizeRequest, db: Session = Depends(get_db)):
    graph= get_graph()

    if req.start_node not in graph.nodes or req.end_node not in graph.nodes:
        raise HTTPException(status_code=404, detail="strat_node or end_node not found in graph")
    
    try:
        raw_best_path, convergence= run_ga(
            start=req.start_node,
            end= req.end_node,
            weight_time=req.weight_time,
            weight_cost= req.weight_cost,
            generations=50,
            pop_size=80
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")
    
    best_path = [int(node.item() if hasattr(node, "item") else node) for node in raw_best_path]
    
    raw_duration = sum(graph[u][v]["duration"] for u, v in zip(best_path[:-1], best_path[1:]))
    raw_fare = sum(graph[u][v]["fare"] for u, v in zip(best_path[:-1], best_path[1:]))
    
    total_duration = float(raw_duration.item() if hasattr(raw_duration, "item") else raw_duration)
    total_fare = float(raw_fare.item() if hasattr(raw_fare, "item") else raw_fare)

    coordinates = [
        [
            float(zone_coords.loc[node, "lat"].item() if hasattr(zone_coords.loc[node, "lat"], "item") else zone_coords.loc[node, "lat"]),
            float(zone_coords.loc[node, "lon"].item() if hasattr(zone_coords.loc[node, "lon"], "item") else zone_coords.loc[node, "lon"])
        ]
        for node in best_path
    ]

    query = text("""
        INSERT INTO trips (user_id, start_node, end_node, weight_time, weight_cost,
                           optimized_cost, optimized_duration, route_path)
        VALUES (:user_id, :start_node, :end_node, :weight_time, :weight_cost,
                :optimized_cost, :optimized_duration, :route_path)
    """)

    db.execute(
        query,
        {
            "user_id": str(req.user_id if req.user_id else "anonymous"),
            "start_node": int(best_path[0]),      
            "end_node": int(best_path[-1]),       
            "weight_time": float(req.weight_time),
            "weight_cost": float(req.weight_cost),
            "optimized_cost": float(total_fare),
            "optimized_duration": float(total_duration),
            "route_path": best_path,              
        }
    )
    db.commit()

    final_score = convergence[-1]
    weighted_score = float(final_score.item() if hasattr(final_score, "item") else final_score)

    return OptimizeResponse(
        route_path=best_path,
        route_coordinates=coordinates,
        predicted_duration_min=total_duration,
        predicted_fare=total_fare,
        weighted_score=weighted_score,
        generations_run=int(len(convergence))
    )