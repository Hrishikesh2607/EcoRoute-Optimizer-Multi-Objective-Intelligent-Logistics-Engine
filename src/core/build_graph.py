import pandas as pd
import networkx as nx
import joblib
import pickle

def build_graph():
    seg = pd.read_parquet("data/processed/features.parquet")
    duration_model = joblib.load("models/duration_model.joblib")
    fare_model = joblib.load("models/fare_model.joblib")

    feature_cols= [
        "PULocationID", "DOLocationID",
        "is_rush_hour", "is_weekend",
        "haversine_mi", "lat_diff", "lon_diff",
        "congestion_factor"
    ]

    
    seg["pred_duration"]= duration_model.predict(seg[feature_cols])
    seg["pred_fare"]= fare_model.predict(seg[feature_cols])

    G= nx.DiGraph()

    for _, row in seg.iterrows():
        u,v= row["PULocationID"], row["DOLocationID"]
        if G.has_edge(u,v):
            continue
        G.add_edge(
            u,v,
            duration=row["pred_duration"],
            fare=row["pred_fare"],
            distance=row["haversine_mi"]
        )

    print(f"Graph build: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    with open("data/processed/route_graph.gpickle", "wb") as f:
            pickle.dump(G, f, pickle.HIGHEST_PROTOCOL)
    return G
    
if __name__ == "__main__":
    build_graph()