from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.database import InventoryItem, StockTransaction
from models.schemas import InventoryItemCreate 

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
