# run_forecasting.py

import joblib
import pandas as pd
from forecasting import (
    forecast_future,
    forecast_item_store_single_day,
    forecast_monthly_demand_for_store
)

# ✅ Step 1: Load saved model and columns
model = joblib.load("xgb_model.pkl")
X_columns = joblib.load("xgb_model_columns.pkl")

print("✅ Loaded saved model and feature columns.\n")

# ✅ Step 2: Forecast full future date range (all items, all stores)
print("🔮 Forecasting for January 2025 (All Items, All Stores)...")
future_df = forecast_future(model, X_columns, "2025-01-01", "2025-01-31")
print(future_df.head(10))

# ✅ Step 3: Forecast for a single day & item across all stores
print("\n📆 Forecast for 'Rice' on 2025-02-14 (All Stores):")
item = "Rice"
date = "2025-02-14"
stores = ['Kolkata', 'Asansol', 'Durgapur', 'Siliguri', 'Howrah']

for store in stores:
    result = forecast_item_store_single_day(model, X_columns, item=item, store=store, date_str=date)
    print(f"{result['store']:10s} | {result['item']:6s} | {result['date']} | Predicted Units Sold: {result['predicted_units_sold']}")

# ✅ Step 4: Monthly item-wise forecast for a store
print("\n📦 Monthly Forecast for 'Durgapur' in Feb 2025:")
monthly_durgapur = forecast_monthly_demand_for_store(model, X_columns, store="Durgapur", year=2025, month=2)
print(monthly_durgapur)

print("\n📦 Monthly Forecast for 'Kolkata' in July 2025:")
monthly_kolkata = forecast_monthly_demand_for_store(model, X_columns, store="Kolkata", year=2025, month=7)
print(monthly_kolkata)
