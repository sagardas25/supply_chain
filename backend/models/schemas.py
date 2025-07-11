from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from enum import Enum


class Store(str, Enum):
    KOLKATA = "Kolkata"
    ASANSOL = "Asansol"
    DURGAPUR = "Durgapur"
    SILIGURI = "Siliguri"
    HOWRAH = "Howrah"


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
    quantity: int = Field(ge=0, description="Quantity cannot be negative")
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
    quantity: int | None = Field(default=None, ge=0, description="Quantity cannot be negative")
    unit: str | None = None
    price: float | None = Field(default=None, gt=0, description="Price must be postive")
    current_stock: int | None = Field(default=None, ge=0, description="Stock cannot be negative")
    min_stock_threshold: int | None = Field(default=None, ge=0)
    max_stock_threshold: int | None = Field(default=None, gt=0)


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


# Stock Alert Schema
class StockAlert(BaseSchema):
    """Schema for stock alerts"""

    item_id: int
    item_name: str
    current_stock: int
    alert_type: AlertType
    details: str


# Inventory Statistics Schema
class InventoryStats(BaseSchema):
    """Schema for inventory statistics"""

    total_items: int
    total_stock: int
    low_stock_items: int
    out_of_stock_items: int


# Forecasting Schemas
class ForecastInputSingleDay(BaseModel):
    item: str
    store: Store
    date: str  # YYYY-MM-DD


class ForecastOutputSingleDay(BaseModel):
    date: str
    store: Store
    item: str
    predicted_units_sold: int


class ForecastInputMonthly(BaseModel):
    store: Store
    year: int
    month: int


class ForecastOutputMonthly(BaseModel):
    item: str
    forecasted_units: int


class ForecastInputDateRange(BaseModel):
    start_date: str  # YYYY-MM-DD
    end_date: str  # YYYY-MM-DD


class ForecastOutputDateRange(BaseModel):
    date: datetime
    store_id: Store
    item_id: str
    predicted_units: float


class ForecastInputSingleDayAllStores(BaseModel):
    item: str
    date: str  # YYYY-MM-DD
