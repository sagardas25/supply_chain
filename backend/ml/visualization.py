# 4_visualizations.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_demand_trend(historical_df, future_df, item, store):
    plt.figure(figsize=(10, 5))
    past = historical_df[(historical_df['item_id'] == item) & (historical_df['store_id'] == store)]
    future = future_df[(future_df['item_id'] == item) & (future_df['store_id'] == store)]

    plt.plot(past['date'], past['units_sold'], label='Historical')
    plt.plot(future['date'], future['predicted_units'], '--', label='Forecast')

    plt.title(f"Demand Trend for '{item}' in '{store}'")
    plt.xlabel("Date")
    plt.ylabel("Units Sold")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_heatmap(df):
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.dayofweek
    heatmap_data = df.groupby(['month', 'day_of_week'])['units_sold'].mean().unstack()

    plt.figure(figsize=(8, 6))
    sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu")
    plt.title("Average Units Sold by Month & Day of Week")
    plt.xlabel("Day of Week (0=Mon)")
    plt.ylabel("Month")
    plt.tight_layout()
    plt.show()

def plot_yearly_demand_by_store(df, use_forecast=False):
    value_col = 'predicted_units' if use_forecast else 'units_sold'
    df['month'] = pd.to_datetime(df['date']).dt.month
    grouped = df.groupby(['store_id', 'item_id', 'month'])[value_col].sum().reset_index()

    for store in df['store_id'].unique():
        store_data = grouped[grouped['store_id'] == store]
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=store_data, x='month', y=value_col, hue='item_id', marker='o')
        plt.title(f"Yearly Item-Wise Trend for {store}")
        plt.xticks(range(1, 13), ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
        plt.xlabel("Month")
        plt.ylabel("Units" if not use_forecast else "Forecasted Units")
        plt.legend(title='Item', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
