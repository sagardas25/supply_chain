# 2_model_training.py
import pandas as pd
import joblib
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from data_creation import preprocess  # ✅ now valid

def train_model(csv_path="historical_sales.csv"):
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'])

    df_processed = preprocess(df)
    X = df_processed.drop(columns=['date', 'units_sold'])
    y = df_processed['units_sold']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = XGBRegressor(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    rmse = mean_squared_error(y_test, predictions, squared=False)
    print(f"✅ XGBoost Model RMSE: {rmse:.2f}")
    joblib.dump(model, "xgb_model.pkl")
    joblib.dump(X.columns.tolist(), "xgb_model_columns.pkl")
    print("✅ Model and column list saved to disk.")
    return model, X.columns.tolist(), df
    

if __name__ == "__main__":
    model, X_cols, df = train_model()

