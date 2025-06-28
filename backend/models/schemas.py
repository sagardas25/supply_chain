from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from enum import Enum


class TransactionType(str, Enum):
    IN = "IN"
    OUT = "OUT"
    ADJUSTMENT = "ADJUSTMENT"


class AlertType(str, Enum):
    LOW_STOCK = "LOW_STOCK"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    OVERSTOCK = "OVERSTOCK"


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


class BaseItemSchema(BaseSchema):
    """Base schema for inventory items."""

    walmart_item_id: str
    name: str
    brand: str | None = None
    category: str
    quantity: int
    unit: str = "pieces"
    price: float = Field(gt=0, description="Price must be postive")
    current_stock: int = Field(ge=0, description="Stock cannot be negative")
    min_stock_threshold: int = Field(ge=0, default=10)
    max_stock_threshold: int = Field(gt=0, default=1000)


# Inventory Item Schemas


class InventoryItemCreate(BaseItemSchema):
    """Schema for creating inventory items"""

    pass


class UpdateItemSchema(BaseItemSchema):
    """Schema for updating inventory items"""

    walmart_item_id: str | None = None
    name: str | None = None
    brand: str | None = None
    category: str | None = None
    quantity: int | None = None
    unit: str | None = None
    price: float | None = None
    current_stock: int | None = None
    min_stock_threshold: int | None = None
    max_stock_threshold: int | None = None


class InventoryItemResponse(BaseItemSchema):
    """Schema for returning inventory responses"""

    id: int
    created_at: datetime
    updated_at: datetime


# Transaction Schemas


class StockTransactionCreate(BaseSchema):
    """Schema for stock transactions"""

    item_id: int
    transaction_type: TransactionType
    quantity: int = Field(gt=0, description="Quantity must be positive")
    reason: str | None = None
    performed_by: str | None = None

    @field_validator("quantity")
    def validate_quantity(cls, v, values):
        transaction_type = values.get("transaction_type")
        if transaction_type in [TransactionType.IN, TransactionType.OUT] and v <= 0:
            raise ValueError("Quantity must be positive")
        return v


class StockTransactionResponse(BaseSchema):
    id: int
    item_id: int
    transaction_type: TransactionType
    quantity: int
    previous_stock: int
    new_stock: int
    reason: str | None = None
    performed_by: str | None = None
    timestamp: datetime
