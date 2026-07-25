import pytest
import networkx as nx
import joblib
import pandas as pd
import pickle
from dotenv import load_dotenv

load_dotenv() 

@pytest.fixture(scope="session")
def graph():
    return pickle.load(open("data/processed/route_graph.gpickle", "rb"))

@pytest.fixture(scope="session")
def duration_model():
    return joblib.load("models/duration_model.joblib")

@pytest.fixture(scope="session")
def fare_model():
    return joblib.load("models/fare_model.joblib")

@pytest.fixture(scope="session")
def features_df():
    return pd.read_parquet("data/processed/features.parquet")