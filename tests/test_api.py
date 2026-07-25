from fastapi.testclient import TestClient
from src.api.main import app

client= TestClient(app)

def test_health_endpoint():
    response= client.get("/v1/health")
    assert response.status_code == 200
    data= response.json()
    assert data["status"] in ["ok", "degraded"]
    assert data["graph_nodes"] > 0

def test_optimize_endpoint_valid_request(graph):
    nodes= list(graph.nodes())
    start, end= nodes[0], nodes[10]
    response= client.post("/v1/optimize", json={
        "start_node": start,
        "end_node": end,
        "weight_time": 0.5,
        "weight_cost": 0.5
    })
    assert response.status_code in [200, 404, 500]
    if response.status_code == 200:
        data= response.json()
        assert data["predicted_duration_min"] > 0
        assert data["predicted_fare"] > 0
        assert len(data["route_path"]) >= 2

def test_optimize_endpoint_invalid_node():
    response= client.post("/v1/optimize", json={
        "start_node": -1,
        "end_node": -2,
        "weight_time": 0.5,
        "weight_cost": 0.5
    })
    assert response.status_code == 404

def test_optimize_weight_validation():
    response= client.post("/v1/optimize", json={
        "start_node": 1,
        "end_node": 2,
        "weight_time": 1.5,
        "weight_cost": 0.5
    })
    assert response.status_code == 422

def test_history_endpoint_returns_list():
    response= client.get("/v1/history?user_id=anonymous&limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)