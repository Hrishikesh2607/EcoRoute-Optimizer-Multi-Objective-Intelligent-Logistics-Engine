import pandas as pd

def load_and_clean(path):
    df= pd.read_parquet(path)

    cols= [
        "tpep_pickup_datetime", "tpep_dropoff_datetime",
        "PULocationID", "DOLocationID",
        "trip_distance", "fare_amount", "total_amount",
        "passenger_count"
    ]
    df = df[cols].copy()

    df["duration_min"] = (
        df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
    ).dt.total_seconds() / 60

    df= df[
        (df["trip_distance"] > 0) & (df["trip_distance"] < 100) &
        (df["duration_min"] > 0) & (df["duration_min"] < 180) &
        (df["fare_amount"] > 0) & (df["fare_amount"] < 500) &
        (df["PULocationID"] != df["DOLocationID"])
    ]

    df["avg_speed_mph"]= df["trip_distance"] / (df["duration_min"] / 60)
    df= df[df["avg_speed_mph"] < 80]

    df["hour"]= df["tpep_pickup_datetime"].dt.hour
    df["day_of_week"]= df["tpep_pickup_datetime"].dt.dayofweek
    df["is_weekend"]= df["day_of_week"].isin([5,6]).astype(int)
    df["is_rush_hour"]= df["hour"].isin([7, 8, 9, 16, 17, 18, 19]).astype(int)

    return df

if __name__ == "__main__":
    df = load_and_clean("data/raw/yellow_tripdata_2024-01.parquet")
    print(f"Rows after cleaning: {len(df):,}")
    print(df.describe())
    df.to_parquet("data/processed/trips_cleaned.parquet")