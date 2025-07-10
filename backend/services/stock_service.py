from sqlalchemy.orm import Session
from models.database import StockTransaction, InventoryItem
from models.schemas import StockTransactionCreate, StockTransactionResponse
from typing import List
from fastapi import HTTPException

class StockService:
    def __init__(self, db: Session):
        self.db = db

    def update_stock(self, item_id: int, transaction: StockTransactionCreate) -> StockTransactionResponse:
        item = self.db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        if transaction.type == "OUT" and item.current_stock < transaction.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")

        if transaction.type == "IN":
            item.current_stock += transaction.quantity
        elif transaction.type == "OUT":
            item.current_stock -= transaction.quantity
        elif transaction.type == "ADJUSTMENT":
            item.current_stock = transaction.quantity

        stock_transaction = StockTransaction(
            item_id=item_id,
            type=transaction.type,
            quantity=transaction.quantity
        )

        self.db.add(stock_transaction)
        self.db.commit()
        self.db.refresh(stock_transaction)
        return StockTransactionResponse.from_orm(stock_transaction)

    def get_item_transactions(self, item_id: int) -> List[StockTransactionResponse]:
        transactions = self.db.query(StockTransaction).filter(StockTransaction.item_id == item_id).all()
        return [StockTransactionResponse.from_orm(tx) for tx in transactions]

    def bulk_stock_update(self, updates: List[StockTransactionCreate]) -> List[StockTransactionResponse]:
        responses = []
        for update in updates:
            response = self.update_stock(update.item_id, update)
            responses.append(response)
        return responses

    def get_recent_transactions(self, limit: int) -> List[StockTransactionResponse]:
        transactions = self.db.query(StockTransaction).order_by(StockTransaction.created_at.desc()).limit(limit).all()
        return [StockTransactionResponse.from_orm(tx) for tx in transactions]

    def get_low_stock_items(self, threshold_multiplier: float) -> List[InventoryItem]:
        items = self.db.query(InventoryItem).filter(
            InventoryItem.current_stock <= InventoryItem.min_stock_threshold * threshold_multiplier
        ).all()
        return items
