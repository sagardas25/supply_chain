from sqlalchemy import create_engine, Column, Integer, DateTime, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone


class DatabaseConfig:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./inventory.db"
    CONNECT_ARGS = {"check_same_thread": False}


engine = create_engine(
    DatabaseConfig.SQLALCHEMY_DATABASE_URL, connect_args=DatabaseConfig.CONNECT_ARGS
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )


class InventoryItem(BaseModel):
    __tablename__ = "inventory_items"

    walmart_item_id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String)
    category = Column(String, index=True)
    quantity = Column(Integer, default=0)
    unit = Column(String, default="pieces")
    price = Column(Float, default=0.0)
    current_stock = Column(Integer, default=0)
    min_stock_threshold = Column(Integer, default=10)
    max_stock_threshold = Column(Integer, default=10_00)


class StockTransaction(BaseModel):
    __tablename__ = "stock_transactions"

    item_id = Column(Integer, index=True)
    transaction_type = Column(String)  # "IN", "OUT", "ADJUSTMENT"
    quantity = Column(Integer)
    previous_stock = Column(Integer)
    new_stock = Column(Integer)
    reason = Column(String)
    performed_by = Column(String)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
