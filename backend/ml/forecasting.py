
import pandas as pd
import numpy as np

def align_columns(input_df, reference_columns):
    for col in reference_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    return input_df[reference_columns]

def forecast_future(model, X_columns, start_date, end_date):
    future_dates = pd.date_range(start=start_date, end=end_date)
    cities = ['Kolkata', 'Asansol', 'Durgapur', 'Siliguri', 'Howrah']
    items = ['Rice', 'Wheat', 'Sugar', 'Salt', 'Oil', 'Milk', 'Potato', 'Onion', 'Dal', 'Atta']

    future_data = []
    for date in future_dates:
        for store in cities:
            for item in items:
                temp = np.random.normal(30, 5)
                is_holiday = int(date.weekday() == 6)
                future_data.append({
                    'date': date,
                    'store_id': store,
                    'item_id': item,
                    'temperature': temp,
                    'is_holiday': is_holiday,
                    'day_of_week': date.weekday(),
                    'month': date.month
                })

    df = pd.DataFrame(future_data)
    df_encoded = pd.get_dummies(df, columns=['store_id', 'item_id'])
    df_encoded = align_columns(df_encoded, X_columns)
    df['predicted_units'] = model.predict(df_encoded)
    return df

def forecast_item_store_single_day(model, X_columns, item, store, date_str):
    date = pd.to_datetime(date_str)
    temp = np.random.normal(30, 5)
    is_holiday = int(date.weekday() == 6)

    df = pd.DataFrame([{
        'date': date,
        'store_id': store,
        'item_id': item,
        'temperature': temp,
        'is_holiday': is_holiday,
        'day_of_week': date.weekday(),
        'month': date.month
    }])

    df_encoded = pd.get_dummies(df, columns=['store_id', 'item_id'])
    df_encoded = align_columns(df_encoded, X_columns)
    prediction = model.predict(df_encoded)[0]

    return {
        'date': date_str,
        'store': store,
        'item': item,
        'predicted_units_sold': round(prediction)
    }

def forecast_monthly_demand_for_store(model, X_columns, store, year, month):
    start_date = pd.to_datetime(f"{year}-{month:02d}-01")
    end_date = start_date + pd.offsets.MonthEnd(0)
    dates = pd.date_range(start=start_date, end=end_date)
    items = ['Rice', 'Wheat', 'Sugar', 'Salt', 'Oil', 'Milk', 'Potato', 'Onion', 'Dal', 'Atta']

    data = []
    for date in dates:
        for item in items:
            temp = np.random.normal(30, 5)
            is_holiday = int(date.weekday() == 6)
            data.append({
                'date': date,
                'store_id': store,
                'item_id': item,
                'temperature': temp,
                'is_holiday': is_holiday,
                'day_of_week': date.weekday(),
                'month': date.month
            })

    df = pd.DataFrame(data)
    df_encoded = pd.get_dummies(df, columns=['store_id', 'item_id'])
    df_encoded = align_columns(df_encoded, X_columns)
    df['predicted_units'] = model.predict(df_encoded)

    total = df.groupby('item_id')['predicted_units'].sum().round().astype(int).reset_index()
    return total.rename(columns={'item_id': 'item', 'predicted_units': 'forecasted_units'})
