import pandas as pd
import numpy as np

FEATURE_COLS= [
    "PULocationID", "DOLocationID",
    "is_rush_hour", "is_weekend",
    "haversine_mi", "lat_diff", "lon_diff",
    "congestion_factor"
]

def test_duration_predictions_are_positive(duration_model, features_df):
    preds= duration_model.predict(features_df[FEATURE_COLS])
    assert (preds > 0).all(), "Model predicted negative or zero duration"

def test_fare_predictions_are_positive(fare_model, features_df):
    preds= fare_model.predict(features_df[FEATURE_COLS])
    assert (preds > 0).all(), "Model predicted negative or zero fare"

def test_duration_predictions_within_reasonable_range(duration_model, features_df):
    preds= duration_model.predict(features_df[FEATURE_COLS])
    assert (preds < 180).all(), "Model predicted unrealistically long duration"

def test_fare_predictions_within_reasonable_range(fare_model, features_df):
    preds= fare_model.predict(features_df[FEATURE_COLS])
    assert (preds < 300).all(), "Model predicted unrealistically high fare"

def test_no_nan_predictions(duration_model, fare_model, features_df):
    duration_preds= duration_model.predict(features_df[FEATURE_COLS])
    fare_preds= fare_model.predict(features_df[FEATURE_COLS])
    assert not np.isnan(duration_preds).any()
    assert not np.isnan(fare_preds).any()

def test_longer_distance_generally_predicts_longer_duration(duration_model, features_df):
    sample= features_df.sample(min(5000, len(features_df)), random_state=42)
    preds= duration_model.predict(sample[FEATURE_COLS])
    correlation= np.corrcoef(sample["haversine_mi"], preds)[0,1]
    assert correlation > 0.3, "Duration predictions don't correlate with distance - possible model issue" 