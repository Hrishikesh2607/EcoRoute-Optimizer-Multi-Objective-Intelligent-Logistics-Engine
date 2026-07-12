import pandas as pd
import geopandas as gpd

trips= pd.read_parquet(r"C:\Users\DELL\Desktop\eco-route-optimizer\data\raw\yellow_tripdata_2024-01.parquet")
print(trips.shape)
print(trips.columns.tolist())
print(trips.head())

zones= gpd.read_file(r"C:\Users\DELL\Desktop\eco-route-optimizer\data\raw\taxi_zones.zip")
print(zones.shape)
print(zones.head())