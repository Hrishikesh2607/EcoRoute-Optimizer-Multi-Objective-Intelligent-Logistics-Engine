from fastapi import APIRouter
from src.api.models import HealthResponse
from src.api.dependencies import get_graph, get_duration_model, get_fare_model

router= APIRouter()

@router.get("/v1/health", response_model=HealthResponse)
def health_check():
    graph= get_graph()
    duration_ok= True
    fare_ok= True
    try:
        get_duration_model()
    except Exception:
        duration_ok= False
    try:
        get_fare_model()
    except Exception:
        fare_ok= False

    return HealthResponse(
        status="ok" if duration_ok and fare_ok else "degraded",
        graph_nodes=graph.number_of_nodes(),
        graph_edges= graph.number_of_edges(),
        duration_model_loaded=duration_ok,
        fare_model_loaded=fare_ok
    )