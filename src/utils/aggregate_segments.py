import pandas as pd
import geopandas as gpd

def build_segment_table(df):
    grouped = df.groupby(
        ["PULocationID", "DOLocationID", "is_rush_hour", "is_weekend"]
    ).agg(
        avg_speed_mph=("avg_speed_mph", "mean"),
        avg_duration_min=("duration_min", "mean"),
        avg_distance_mi=("trip_distance", "mean"),
        avg_fare=("fare_amount", "mean"),
        trip_count=("fare_amount", "count")
    ).reset_index()

    grouped = grouped[grouped["trip_count"] >= 5]

    non_rush = grouped[grouped["is_rush_hour"] == 0]
    baseline = non_rush.groupby(["PULocationID", "DOLocationID"])["avg_speed_mph"].mean()

    grouped = grouped.set_index(["PULocationID", "DOLocationID"])
    grouped["baseline_speed"] = grouped.index.map(baseline)
    grouped = grouped.reset_index()

    grouped["congestion_factor"] = (
        grouped["baseline_speed"] / grouped["avg_speed_mph"]
    ).fillna(1.0)

    return grouped

if __name__ == "__main__":
    df = pd.read_parquet("data/processed/trips_cleaned.parquet")
    seg = build_segment_table(df)
    print(f"Unique segments: {seg.shape[0]:,}")
    print(seg.head(10))
    seg.to_parquet("data/processed/segments.parquet")

    zones = gpd.read_file("/vsizip/data/raw/taxi_zones.zip/taxi_zones/taxi_zones.shp")
    zones["centroid"] = zones.geometry.centroid
    zones = zones.to_crs(epsg=4326) 
    zones["centroid"] = zones["centroid"].to_crs(epsg=4326)
    zones["lon"] = zones.centroid.x
    zones["lat"] = zones.centroid.y

    zone_coords = zones[["LocationID", "lat", "lon"]]
    zone_coords.to_parquet("data/processed/zone_coords.parquet")