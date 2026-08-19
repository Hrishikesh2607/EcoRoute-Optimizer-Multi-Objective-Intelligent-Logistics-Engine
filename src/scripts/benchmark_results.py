import requests
import random
import networkx as nx
import pickle

from src.api.dependencies import get_graph  

graph = get_graph()
nodes = list(graph.nodes())

results= []
for i in range(10):
    start,end= random.sample(nodes, 2)
    if not nx.has_path(graph, start, end):
        continue
    resp= requests.post("http://localhost:8000/v1/esg-report", json={
        "start_node": start, "end_node": end,
        "weight_time": 0.5, "weight_cost": 0.5
    })
    if resp.status_code == 200:
        results.append(resp.json()["co2_saved_pct"])

print(f"Average CO2 saved: {sum(results)/len(results):.1f}%")
print(f"Range: {min(results):.1f}% to {max(results):.1f}%")