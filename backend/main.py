from typing import List, Union

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from models.database import get_db, init_db
from models.schemas import (
    InventoryItemCreate,
    InventoryItemResponse,
    UpdateItemSchema,
    StockTransactionCreate,
    StockTransactionResponse
)
from services.inventory import InventoryService

app = FastAPI(
    title="Walmart Supply Chain API",
    description="API for managing Walmart's supply chain inventory",
    version="1.0.0"
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
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all inventory items with pagination.

    Parameters:
    - skip: Number of items to skip (default: 0)
    - limit: Maximum number of items to return (default: 100)
    
    Returns:
    - List[InventoryItemResponse]: List of inventory items
    """
    inventory_service = InventoryService(db)
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
    
    Raises:
    - HTTPException 404: If item not found
    """
    inventory_service = InventoryService(db)
    return inventory_service.update_item(item_id, item)

@app.post("/inventory/transactions/", response_model=StockTransactionResponse, tags=["Transactions"])
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