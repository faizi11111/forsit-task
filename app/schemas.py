from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category: str

class ProductCreate(ProductBase):
    initial_stock: Optional[int] = 0

class InventoryBase(BaseModel):
    quantity: int

class Inventory(InventoryBase):
    id: int
    product_id: int
    last_updated: datetime
    
    class Config:
        from_attributes = True

class Product(ProductBase):
    id: int
    inventory: list[Inventory] = []
    
    class Config:
        from_attributes = True

class StockUpdate(BaseModel):
    quantity: int

class SaleCreate(BaseModel):
    product_id: int
    quantity: int

class Sale(BaseModel):
    id: int
    product_id: int
    quantity: int
    total_amount: float
    sale_date: datetime
    
    class Config:
        from_attributes = True

class SalesFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    product_id: Optional[int] = None
    category: Optional[str] = None

class Period(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ANNUALLY = "annually"

class PeriodSales(BaseModel):
    period_start: datetime
    period_end: datetime
    total_sales: float
    total_quantity: int
    number_of_orders: int

    class Config:
        from_attributes = True 