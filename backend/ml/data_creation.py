# 1_data_creation.py
import pandas as pd
import numpy as np

def generate_data(start_date, end_date):
    dates = pd.date_range(start_date, end_date)
    cities = ['Kolkata', 'Asansol', 'Durgapur', 'Siliguri', 'Howrah']
    items = ['Rice', 'Wheat', 'Sugar', 'Salt', 'Oil', 'Milk', 'Potato', 'Onion', 'Dal', 'Atta']

    data = []
    for date in dates:
        for city in cities:
            for item in items:
                base = np.random.randint(50, 200)
                temp = np.random.normal(28, 5)
                is_holiday = int(date.weekday() == 6)
                variation = np.random.normal(1.0, 0.1)
                units_sold = int(base * variation * (1.2 if is_holiday else 1.0))
                data.append({
                    'date': date,
                    'store_id': city,
                    'item_id': item,
                    'temperature': round(temp, 2),
                    'is_holiday': is_holiday,
                    'units_sold': units_sold
                })

    df = pd.DataFrame(data)
    df.to_csv("historical_sales.csv", index=False)
    return df

def preprocess(df):
    df = df.copy()
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    df = pd.get_dummies(df, columns=['store_id', 'item_id'])
    return df

if __name__ == "__main__":
    df = generate_data("2024-10-01", "2024-12-31")
    df['date'] = pd.to_datetime(df['date'])  # Ensure date column is datetime
    print("✅ Dataset created and saved to 'historical_sales.csv'")
