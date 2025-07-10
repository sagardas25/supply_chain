from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.database import InventoryItem, StockTransaction
from models.schemas import InventoryItemCreate, UpdateItemSchema, StockTransactionCreate, StockAlert, InventoryStats
from typing import List

class InventoryService:
    """Service for managing inventory operations."""

    def __init__(self, db: Session):
        self.db = db

    def _get_item_or_404(self, item_id: int):
        """Helper method to get an item or raise 404 if not found."""
        item = self.db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    def _check_unique_walmart_id(self, walmart_item_id: str):
        """Check if the Walmart item ID is unique."""
        existing_item = (
            self.db.query(InventoryItem)
            .filter(InventoryItem.walmart_item_id == walmart_item_id)
            .first()
        )
        if existing_item:
            raise HTTPException(
                status_code=400, detail="Walmart item ID must be unique"
            )

    def create_item(self, item_data: InventoryItemCreate) -> InventoryItem:
        """Create a new inventory item."""
        self._check_unique_walmart_id(item_data.walmart_item_id)

        new_item = InventoryItem(**item_data.model_dump())
        self.db.add(new_item)
        self.db.commit()
        self.db.refresh(new_item)
        return new_item

    def get_item(self, item_id: int) -> InventoryItem:
        """Get an inventory item by ID."""
        return self._get_item_or_404(item_id)

    def list_items(self, skip: int = 0, limit: int = 100) -> List[InventoryItem]:
        """List inventory items with pagination."""
        return self.db.query(InventoryItem).offset(skip).limit(limit).all()

    def update_item(self, item_id: int, item_data: UpdateItemSchema) -> InventoryItem:
        """Update an inventory item."""
        item = self._get_item_or_404(item_id)
        
        # Filter out None values to only update provided fields
        update_data = {
            key: value for key, value in item_data.model_dump().items()
            if value is not None
        }
        
        # If walmart_item_id is being updated, check uniqueness
        if "walmart_item_id" in update_data and update_data["walmart_item_id"] != item.walmart_item_id:
            self._check_unique_walmart_id(update_data["walmart_item_id"])

        for key, value in update_data.items():
            setattr(item, key, value)

        self.db.commit()
        self.db.refresh(item)
        return item

    def delete_item(self, item_id: int):
        """Delete an inventory item."""
        item = self._get_item_or_404(item_id)
        self.db.delete(item)
        self.db.commit()

    def create_transaction(self, transaction_data: StockTransactionCreate) -> StockTransaction:
        """Create a stock transaction and update inventory."""
        item = self._get_item_or_404(transaction_data.item_id)
        
        # Calculate new stock level
        new_stock = item.current_stock
        if transaction_data.transaction_type == "IN":
            new_stock += transaction_data.quantity
        elif transaction_data.transaction_type == "OUT":
            new_stock -= transaction_data.quantity
            if new_stock < 0:
                raise HTTPException(
                    status_code=400,
                    detail="Cannot process transaction: Insufficient stock"
                )
        else:  # ADJUSTMENT
            new_stock = transaction_data.quantity

        # Create transaction record
        transaction = StockTransaction(
            item_id=item.id,
            transaction_type=transaction_data.transaction_type,
            quantity=transaction_data.quantity,
            previous_stock=item.current_stock,
            new_stock=new_stock,
            reason=transaction_data.reason,
            performed_by=transaction_data.performed_by
        )

        self.db.add(transaction)
        item.current_stock = new_stock
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def get_low_stock_items(self, skip: int = 0, limit: int = 100) -> List[InventoryItem]:
        """Get items where current stock is below the minimum threshold."""
        return (
            self.db.query(InventoryItem)
            .filter(InventoryItem.current_stock < InventoryItem.min_stock_threshold)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_inventory_stats(self) -> InventoryStats:
        """Get inventory statistics."""
        total_items = self.db.query(func.count(InventoryItem.id)).scalar()
        total_stock = self.db.query(func.sum(InventoryItem.current_stock)).scalar() or 0
        low_stock_items = (
            self.db.query(func.count(InventoryItem.id))
            .filter(InventoryItem.current_stock < InventoryItem.min_stock_threshold)
            .scalar()
        )
        out_of_stock_items = (
            self.db.query(func.count(InventoryItem.id))
            .filter(InventoryItem.current_stock == 0)
            .scalar()
        )

        return InventoryStats(
            total_items=total_items,
            total_stock=total_stock,
            low_stock_items=low_stock_items,
            out_of_stock_items=out_of_stock_items,
        )
