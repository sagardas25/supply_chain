

import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from forecasting import (
    forecast_future,
    forecast_item_store_single_day,
    forecast_monthly_demand_for_store
)

# Load model and columns
model = joblib.load("xgb_model.pkl")
X_columns = joblib.load("xgb_model_columns.pkl")

st.set_page_config(page_title="Demand Forecasting App", layout="wide")
st.title("🛒 Store & Item Demand Forecasting")
st.markdown("Built with XGBoost and Streamlit")

# Tabs
tabs = st.tabs(["📆 Monthly Forecast", "🛍️ Item Forecast (Single Day)", "🏪 Store+Item Forecast (One Day)", "📦 Monthly Demand Summary"])

# 📆 Tab 1: Forecast for future date range
with tabs[0]:
    st.subheader("Forecast for Future Date Range (All Stores, All Items)")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", pd.to_datetime("2025-01-01"))
    with col2:
        end_date = st.date_input("End Date", pd.to_datetime("2025-01-31"))

    if start_date > end_date:
        st.warning("Start date must be before end date.")
    else:
        if st.button("🔮 Forecast Full Range"):
            future_df = forecast_future(model, X_columns, start_date, end_date)
            st.dataframe(future_df.head(20))

            st.success("Forecast complete! Showing top results.")
            # Optional: heatmap by item and date
            fig, ax = plt.subplots(figsize=(12, 4))
            daily_total = future_df.groupby('date')['predicted_units'].sum()
            daily_total.plot(ax=ax)
            ax.set_title("📈 Total Predicted Units Over Time")
            st.pyplot(fig)

# 🛍️ Tab 2: Forecast for a single item across all stores
with tabs[1]:
    st.subheader("Forecast One Item Across All Stores on a Given Date")
    item = st.selectbox("Select Item", ['Rice', 'Wheat', 'Sugar', 'Salt', 'Oil', 'Milk', 'Potato', 'Onion', 'Dal', 'Atta'], key="item_select")
    date_str = st.date_input("Select Date", pd.to_datetime("2025-02-14"))

    if st.button("🔍 Forecast All Stores for Selected Item"):
        stores = ['Kolkata', 'Asansol', 'Durgapur', 'Siliguri', 'Howrah']
        results = []
        for store in stores:
            res = forecast_item_store_single_day(model, X_columns, item=item, store=store, date_str=str(date_str))
            results.append(res)
        st.dataframe(pd.DataFrame(results))

# 🏪 Tab 3: Forecast a single item + store + date
with tabs[2]:
    st.subheader("Forecast for One Store, One Item, One Day")
    store = st.selectbox("Select Store", ['Kolkata', 'Asansol', 'Durgapur', 'Siliguri', 'Howrah'])
    item = st.selectbox("Select Item", ['Rice', 'Wheat', 'Sugar', 'Salt', 'Oil', 'Milk', 'Potato', 'Onion', 'Dal', 'Atta'])
    date = st.date_input("Select Date for Store+Item", pd.to_datetime("2025-02-14"))

    if st.button("🎯 Forecast Specific Store+Item"):
        result = forecast_item_store_single_day(model, X_columns, item=item, store=store, date_str=str(date))
        st.json(result)

# 📦 Tab 4: Forecast monthly demand for all items in a store
with tabs[3]:
    st.subheader("Monthly Demand Forecast Summary for Store")
    store = st.selectbox("Store", ['Kolkata', 'Asansol', 'Durgapur', 'Siliguri', 'Howrah'], key="summary_store")
    year = st.number_input("Year", min_value=2024, max_value=2030, value=2025)
    month = st.number_input("Month (1-12)", min_value=1, max_value=12, value=2)

    if st.button("📦 Forecast Monthly Demand"):
        monthly = forecast_monthly_demand_for_store(model, X_columns, store=store, year=year, month=month)
        st.dataframe(monthly)

        # Optional chart
        fig, ax = plt.subplots()
        sns.barplot(data=monthly, x='item', y='forecasted_units', ax=ax)
        ax.set_title(f"Forecasted Units Sold in {store} - {year}-{month:02d}")
        ax.set_ylabel("Units")
        ax.set_xlabel("Item")
        plt.xticks(rotation=45)
        st.pyplot(fig)
