import networkx as nx
import joblib
from functools import lru_cache
import pickle

GRAPH_PATH= "data/processed/route_graph.gpickle"
DURATION_MODEL_PATH = "models/duration_model.joblib"
FARE_MODEL_PATH = "models/fare_model.joblib"

@lru_cache()
def get_graph():
    return pickle.load(open(GRAPH_PATH, "rb"))

@lru_cache()
def get_duration_model():
    return joblib.load(DURATION_MODEL_PATH)

@lru_cache()
def get_fare_model():
    return joblib.load(FARE_MODEL_PATH)