from typing import List, Union

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from models.database import get_db, init_db
from models.schemas import (
    InventoryItemCreate,
    InventoryItemResponse,
    UpdateItemSchema,
    StockTransactionCreate,
    StockTransactionResponse,
    InventoryStats,
    ForecastInputSingleDay,
    ForecastOutputSingleDay,
    ForecastInputMonthly,
    ForecastOutputMonthly,
    ForecastInputDateRange,
    ForecastOutputDateRange,
    ForecastInputSingleDayAllStores,
)
from services.inventory import InventoryService
from services.forecasting import ForecastingService

app = FastAPI(
    title="Walmart Supply Chain API",
    description="API for managing Walmart's supply chain inventory",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity, adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize database tables
init_db()

@app.get("/", tags=["Health"])
def read_root():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Supply Chain API is running"}

@app.post("/inventory/", response_model=InventoryItemResponse, tags=["Inventory"])
def create_inventory_item(
    item: InventoryItemCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new inventory item.

    Parameters:
    - item: InventoryItemCreate schema containing item details
    
    Returns:
    - InventoryItemResponse: Created inventory item details
    """
    inventory_service = InventoryService(db)
    return inventory_service.create_item(item)

@app.get("/inventory/{item_id}", response_model=InventoryItemResponse, tags=["Inventory"])
def get_inventory_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Get details of a specific inventory item.

    Parameters:
    - item_id: ID of the inventory item
    
    Returns:
    - InventoryItemResponse: Inventory item details
    
    Raises:
    - HTTPException 404: If item not found
    """
    inventory_service = InventoryService(db)
    return inventory_service.get_item(item_id)

@app.get("/inventory/", response_model=List[InventoryItemResponse], tags=["Inventory"])
def list_inventory_items(
    low_stock: bool = False,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all inventory items with pagination, optionally filtering for low stock items.

    Parameters:
    - low_stock: If True, returns items with stock below their alert threshold (default: False)
    - skip: Number of items to skip (default: 0)
    - limit: Maximum number of items to return (default: 100)
    
    Returns:
    - List[InventoryItemResponse]: List of inventory items
    """
    inventory_service = InventoryService(db)
    if low_stock:
        return inventory_service.get_low_stock_items(skip=skip, limit=limit)
    return inventory_service.list_items(skip=skip, limit=limit)

@app.put("/inventory/{item_id}", response_model=InventoryItemResponse, tags=["Inventory"])
def update_inventory_item(
    item_id: int,
    item: UpdateItemSchema,
    db: Session = Depends(get_db)
):
    """
    Update an existing inventory item.

    Parameters:
    - item_id: ID of the inventory item to update
    - item: UpdateItemSchema containing fields to update
    
    Returns:
    - InventoryItemResponse: Updated inventory item details
    """
    inventory_service = InventoryService(db)
    return inventory_service.update_item(item_id, item)

@app.delete("/inventory/{item_id}", status_code=204, tags=["Inventory"])
def delete_inventory_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an inventory item.

    Parameters:
    - item_id: ID of the inventory item to delete
    
    Returns:
    - HTTP 204 No Content on successful deletion
    """
    inventory_service = InventoryService(db)
    inventory_service.delete_item(item_id)
    return

@app.post("/stock/transaction/", response_model=StockTransactionResponse, tags=["Stock"])
def create_stock_transaction(
    transaction: StockTransactionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new stock transaction (IN/OUT/ADJUSTMENT).

    Parameters:
    - transaction: StockTransactionCreate schema containing transaction details
    
    Returns:
    - StockTransactionResponse: Created transaction details
    
    Raises:
    - HTTPException 404: If referenced item not found
    - HTTPException 400: If transaction would result in negative stock
    """
    inventory_service = InventoryService(db)
    return inventory_service.create_transaction(transaction)

@app.get("/inventory/stats/", response_model=InventoryStats, tags=["Inventory"])
def get_inventory_stats(
    db: Session = Depends(get_db)
):
    """
    Get inventory statistics.
    
    Returns:
    - InventoryStats: Statistics about the inventory
    """
    inventory_service = InventoryService(db)
    return inventory_service.get_inventory_stats()

# Forecasting Endpoints
@app.post("/forecast/single-day", response_model=ForecastOutputSingleDay, tags=["Forecasting"])
def forecast_single_day(
    forecast_input: ForecastInputSingleDay,
):
    """
    Forecasts sales for a single item, in a single store on a specific day.
    """
    forecasting_service = ForecastingService()
    return forecasting_service.forecast_item_store_single_day(
        item=forecast_input.item,
        store=forecast_input.store,
        date_str=forecast_input.date,
    )

@app.post("/forecast/monthly", response_model=List[ForecastOutputMonthly], tags=["Forecasting"])
def forecast_monthly(
    forecast_input: ForecastInputMonthly,
):
    """
    Forecasts monthly sales for all items in a specific store.
    """
    forecasting_service = ForecastingService()
    result_df = forecasting_service.forecast_monthly_demand_for_store(
        store=forecast_input.store,
        year=forecast_input.year,
        month=forecast_input.month,
    )
    return result_df.to_dict(orient="records")


@app.post("/forecast/date-range", response_model=List[ForecastOutputDateRange], tags=["Forecasting"])
def forecast_date_range(
    forecast_input: ForecastInputDateRange,
):
    """
    Forecasts sales for all items and stores over a given date range.
    """
    forecasting_service = ForecastingService()
    result_df = forecasting_service.forecast_date_range(
        start_date=forecast_input.start_date,
        end_date=forecast_input.end_date,
    )
    return result_df.to_dict(orient="records")


@app.post("/forecast/single-day-all-stores", response_model=List[ForecastOutputSingleDay], tags=["Forecasting"])
def forecast_single_day_all_stores(
    forecast_input: ForecastInputSingleDayAllStores,
):
    """
    Forecasts sales for a single item across all stores on a specific day.
    """
    forecasting_service = ForecastingService()
    return forecasting_service.forecast_item_single_day_all_stores(
        item=forecast_input.item,
        date_str=forecast_input.date,
    )


@app.post("/forecast/reload-model", tags=["Forecasting"])
def reload_model():
    """
    Reloads the forecasting model from disk.
    """
    ForecastingService._model = None
    ForecastingService._X_columns = None
    ForecastingService.get_model()
    return {"message": "Forecasting model reloaded successfully"}