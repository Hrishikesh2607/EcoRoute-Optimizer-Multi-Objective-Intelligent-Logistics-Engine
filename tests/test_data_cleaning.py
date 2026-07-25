import pandas as pd
from src.utils.clean_data import load_and_clean

def test_no_negative_duration():
    df= load_and_clean("data/raw/yellow_tripdata_2024-01.parquet")
    assert (df["duration_min"] >0).all()

def test_no_negative_distances():
    df= load_and_clean("data/raw/yellow_tripdata_2024-01.parquet")
    assert (df["trip_distance"] > 0).all()

def test_no_zero_distance_travel():
    df= load_and_clean("data/raw/yellow_tripdata_2024-01.parquet")
    assert (df["PULocationID"] != df["DOLocationID"]).all()

def test_speed_within_physical_bounds():
    df= load_and_clean("data/raw/yellow_tripdata_2024-01.parquet")
    assert (df["avg_speed_mph"] > 0).all()
    assert (df["avg_speed_mph"] < 80).all()

def test_retains_reasonable_row_fraction():
    raw= pd.read_parquet("data/raw/yellow_tripdata_2024-01.parquet")
    cleaned= load_and_clean("data/raw/yellow_tripdata_2024-01.parquet")
    retention_rate= len(cleaned) / len(raw)
    assert retention_rate > 0.85