# forecast_main.py
from data_creation import generate_data
from model_training import train_model
from forecasting import forecast_future, forecast_item_store_single_day
from visualization import plot_demand_trend, plot_yearly_demand_by_store

# Generate + Train
generate_data("2024-10-01", "2024-12-31")
model, X_columns, df = train_model()

# Forecast
future_df = forecast_future(model, X_columns, "2025-01-01", "2025-01-31")

# Plots
plot_demand_trend(df, future_df, item='Oil', store='Kolkata')
plot_yearly_demand_by_store(df, use_forecast=False)
plot_yearly_demand_by_store(future_df, use_forecast=True)
