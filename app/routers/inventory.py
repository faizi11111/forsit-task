from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas
from ..database import get_db
from ..services import inventory_service

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"]
)

@router.get("/low-stock", response_model=List[schemas.Inventory])
def get_low_stock(threshold: int = 10, db: Session = Depends(get_db)):
    return inventory_service.get_low_stock(db, threshold)

@router.get("/{product_id}", response_model=schemas.Inventory)
def get_stock(product_id: int, db: Session = Depends(get_db)):
    return inventory_service.get_stock(db, product_id)

@router.post("/{product_id}/add-stock", response_model=schemas.Inventory)
def add_stock(product_id: int, stock_update: schemas.StockUpdate, db: Session = Depends(get_db)):
    return inventory_service.add_stock(db, product_id, stock_update.quantity) 