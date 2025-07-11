from ml.loader import load_model
from ml.forecasting import (
    forecast_item_store_single_day as forecast_single,
    forecast_monthly_demand_for_store as forecast_monthly,
    forecast_future as forecast_range,
)
import pandas as pd
from models.schemas import Store


class ForecastingService:
    _model = None
    _X_columns = None
    _stores = [s.value for s in Store]

    @classmethod
    def get_model(cls):
        if cls._model is None or cls._X_columns is None:
            cls._model, cls._X_columns = load_model()
        return cls._model, cls._X_columns

    def __init__(self):
        self.model, self.X_columns = self.get_model()

    def forecast_item_store_single_day(self, item: str, store: Store, date_str: str):
        """
        Forecasts demand for a single item, in a single store on a specific day.
        """
        return forecast_single(self.model, self.X_columns, item, store.value, date_str)

    def forecast_monthly_demand_for_store(self, store: Store, year: int, month: int):
        """
        Forecasts monthly demand for all items in a specific store.
        """
        return forecast_monthly(self.model, self.X_columns, store.value, year, month)

    def forecast_date_range(self, start_date: str, end_date: str):
        """
        Forecasts demand for all items and stores over a date range.
        """
        return forecast_range(self.model, self.X_columns, start_date, end_date)

    def forecast_item_single_day_all_stores(self, item: str, date_str: str):
        """
        Forecasts demand for a single item across all stores on a specific day.
        """
        results = []
        for store in self._stores:
            result = forecast_single(
                self.model, self.X_columns, item, store, date_str
            )
            results.append(result)
        return results
