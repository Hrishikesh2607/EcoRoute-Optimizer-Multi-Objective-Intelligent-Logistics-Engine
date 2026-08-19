from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from src.api.dependencies import get_graph
from src.core.genetic_optimizer import run_ga_scenario

router = APIRouter()

class WhatIfRequest(BaseModel):
    start_node: int
    end_node: int
    weight_time: float = Field(default=0.5, ge=0.0, le=1.0)
    weight_cost: float = Field(default=0.5, ge=0.0, le=1.0)
    fuel_price_increase_pct: float = Field(default=50.0, description="e.g., 50 means fuel prices up 50%")

@router.post("/v1/whatif")
def whatif_scenario(req: WhatIfRequest):
    graph = get_graph()

    if req.start_node not in graph.nodes or req.end_node not in graph.nodes:
        raise HTTPException(status_code=404, detail="start_node or end_node not found in graph")

    fuel_multiplier = 1.0 + (req.fuel_price_increase_pct / 100.0)

    baseline_path = run_ga_scenario(
        req.start_node, req.end_node, req.weight_time, req.weight_cost,
        fuel_multiplier=1.0, generations=40, pop_size=60
    )
    scenario_path = run_ga_scenario(
        req.start_node, req.end_node, req.weight_time, req.weight_cost,
        fuel_multiplier=fuel_multiplier, generations=40, pop_size=60
    )

    def path_totals(path):
        duration = sum(graph[u][v]["duration"] for u, v in zip(path[:-1], path[1:]))
        fare = sum(graph[u][v]["fare"] for u, v in zip(path[:-1], path[1:]))
        return {"duration_min": round(duration, 2), "fare": round(fare, 2)}

    route_changed = list(baseline_path) != list(scenario_path)

    return {
        "baseline_route": baseline_path,
        "baseline_totals": path_totals(baseline_path),
        "scenario_route": scenario_path,
        "scenario_totals": path_totals(scenario_path),
        "fuel_price_increase_pct": req.fuel_price_increase_pct,
        "route_changed": route_changed
    }