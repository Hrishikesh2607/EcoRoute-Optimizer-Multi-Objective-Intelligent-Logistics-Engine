import pandas as pd
import numpy as np

def build_features(seg_path, zone_coords_path):
    seg= pd.read_parquet(seg_path)
    zones= pd.read_parquet(zone_coords_path)

    seg = seg.merge(
        zones.rename(columns={"LocationID": "PULocationID", "lat": "pu_lat", "lon": "pu_lon"}),
        on="PULocationID", how="left"
    )
    seg = seg.merge(
        zones.rename(columns={"LocationID": "DOLocationID", "lat": "do_lat", "lon": "do_lon"}),
        on="DOLocationID", how="left"
    )

    seg= seg.dropna(subset=["pu_lat", "pu_lon", "do_lat", "do_lon"])

    def haversine(lat1, lon1, lat2, lon2):
        R= 3958.8
        lat1, lon1, lat2, lon2= map(np.radians, [lat1, lon1, lat2, lon2])
        dlat= lat2 - lat1
        dlon= lon2 - lon1
        a= np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
        return 2 * R * np.arcsin(np.sqrt(a))
    
    seg["haversine_mi"]= haversine(seg.pu_lat, seg.pu_lon, seg.do_lat, seg.do_lon)

    seg["lat_diff"]= seg["do_lat"] - seg["pu_lat"]
    seg["lon_diff"]= seg["do_lon"] - seg["pu_lon"]

    seg["PULocationID"]= seg["PULocationID"].astype("category")
    seg["DOLocationID"]= seg["DOLocationID"].astype("category")

    return seg

if __name__ == "__main__":
    df= build_features(
        "data/processed/segments.parquet",
        "data/processed/zone_coords.parquet"
    )
    print(f"Feature table shape: {df.shape}")
    print(df.columns.tolist())
    df.to_parquet("data/processed/features.parquet")