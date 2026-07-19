from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from src.api.models import OptimizeRequest
from src.api.dependencies import get_graph
from src.core.genetic_optimizer import run_ga
from src.utils.visualize_route import render_route_map
import pandas as pd

router= APIRouter()
zone_coords= pd.read_parquet("data/processed/zone_coords.parquet").set_index("LocationID")

@router.post("/v1/optimize/map", response_class=HTMLResponse)
def optimize_and_visualize(req: OptimizeRequest):
    graph= get_graph()

    if req.start_node not in graph.nodes or req.end_node not in graph.nodes:
        raise HTTPException(status_code=404, detail="start_node or end_node not found in graph")
    
    raw_best_path, _= run_ga(
        start=req.start_node, end=req.end_node,
        weight_time=req.weight_time, weight_cost=req.weight_cost
    )
    best_path= [int(n.item() if hasattr(n, "item") else n) for n in raw_best_path]

    coordinates= [
        [float(zone_coords.loc[node, "lat"].item() if hasattr(zone_coords.loc[node, "lat"], "item") else zone_coords.loc[node, "lat"]), float(zone_coords.loc[node, "lon"].item() if hasattr(zone_coords.loc[node, "lon"], "item") else zone_coords.loc[node, "lon"])]
        for node in best_path
    ]

    total_duration= sum(graph[u][v]["duration"] for u,v in zip(best_path[:-1], best_path[1:]))
    total_fare= sum(graph[u][v]["fare"] for u,v in zip(best_path[:-1], best_path[1:]))
    
    m= render_route_map(coordinates, int(req.start_node), int(req.end_node), total_duration, total_fare)
    return HTMLResponse(content=m.get_root().render())