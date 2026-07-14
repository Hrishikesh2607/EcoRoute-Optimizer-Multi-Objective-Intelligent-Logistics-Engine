import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

def train_duration_model():
    df= pd.read_parquet("data/processed/features.parquet")

    feature_cols= [
        "PULocationID", "DOLocationID",
        "is_rush_hour", "is_weekend",
        "haversine_mi", "lat_diff", "lon_diff",
        "congestion_factor"
    ]
    target_col= "avg_duration_min"

    X= df[feature_cols]
    y= df[target_col]

    X_train, X_test, y_train, y_test= train_test_split(
        X,y, test_size=0.3, random_state=42
    )

    model= xgb.XGBRegressor(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        enable_categorical=True,
        random_state=42
    )

    model.fit(X_train, y_train)

    preds= model.predict(X_test)
    mae= mean_absolute_error(y_test, preds)
    r2= r2_score(y_test, preds)

    print(f"MAE: {mae:.2f} minutes")
    print(f"R²: {r2:.3f}")

    importance= pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=False)
    print("\nFeature importances:")
    print(importance)

    joblib.dump(model, "models/duration_model.joblib")
    return model, mae, r2

def train_fare_model():
    df= pd.read_parquet("data/processed/features.parquet")

    feature_cols= [
        "PULocationID", "DOLocationID",
        "is_rush_hour", "is_weekend",
        "haversine_mi", "lat_diff", "lon_diff",
        "congestion_factor"
    ]
    target_col= "avg_fare"

    X= df[feature_cols]
    y= df[target_col]

    X_train, X_test, y_train, y_test= train_test_split(
        X,y, test_size=0.3, random_state=42
    )

    model= xgb.XGBRegressor(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        enable_categorical=True,
        random_state=42
    )

    model.fit(X_train, y_train)

    preds= model.predict(X_test)
    mae= mean_absolute_error(y_test, preds)
    r2= r2_score(y_test, preds)

    print(f"MAE: {mae:.2f} minutes")
    print(f"R²: {r2:.3f}")

    importance= pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=False)
    print("\nFeature importances:")
    print(importance)

    joblib.dump(model, "models/fare_model.joblib")
    return model, mae, r2

def check():
    model = joblib.load("models/duration_model.joblib")
    df= pd.read_parquet("data/processed/features.parquet")

    feature_cols= [
        "PULocationID", "DOLocationID",
        "is_rush_hour", "is_weekend",
        "haversine_mi", "lat_diff", "lon_diff",
        "congestion_factor"
    ]
    target_col= "avg_duration_min"

    X= df[feature_cols]
    y= df[target_col]

    X_train, X_test, y_train, y_test= train_test_split(
        X,y, test_size=0.3, random_state=42
    )
    sample = X_test.iloc[[0]]
    print("Predicted:", model.predict(sample))
    print("Actual:", y_test.iloc[0])

if __name__ == "__main__":
    train_duration_model()
    train_fare_model()
    check()