from fastapi import APIRouter, HTTPException
import networkx as nx
from src.api.models import OptimizeRequest
from src.api.dependencies import get_graph
from src.core.genetic_optimizer import run_ga
from src.core.esg_calculator import generate_esg_report

router = APIRouter()

@router.post("/v1/esg-report")
def esg_report(req: OptimizeRequest):
    graph = get_graph()

    if req.start_node not in graph.nodes or req.end_node not in graph.nodes:
        raise HTTPException(status_code=404, detail="start_node or end_node not found in graph")

    ga_path, _ = run_ga(
        start=req.start_node, end=req.end_node,
        weight_time=req.weight_time, weight_cost=req.weight_cost
    )

    try:
        baseline_path = nx.shortest_path(graph, req.start_node, req.end_node, weight="duration")
    except nx.NetworkXNoPath:
        raise HTTPException(status_code=404, detail="No baseline path exists between these nodes")

    report = generate_esg_report(graph, ga_path, baseline_path)
    report["ga_route"] = ga_path
    report["baseline_route"] = baseline_path

    return report