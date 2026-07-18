from pydantic import BaseModel, Field
from typing import List, Optional

class OptimizeRequest(BaseModel):
    start_node: int
    end_node: int
    weight_time: float = Field(default=0.5, ge=0.0, le=1.0)
    weight_cost: float= Field(default=0.5, ge=0.0, le=1.0)
    avoid_highways: bool= False
    avoid_tolls: bool= False
    user_id: Optional[str]= "anonymous"

class OptimizeResponse(BaseModel):
    route_path: List[int]
    route_coordinates: List[List[float]]
    predicted_duration_min: float
    predicted_fare: float
    weighted_score: float
    generations_run: int

class HealthResponse(BaseModel):
    status: str
    graph_nodes: int
    graph_edges: int
    duration_model_loaded: bool
    fare_model_loaded: bool

class TripHistoryItem(BaseModel):
    id: int
    user_id: str
    start_node: int
    end_node: int
    timestamp: str
    optimized_cost: Optional[float]
    optimized_duration: Optional[float]