from sqlalchemy.orm import Session
from fastapi import HTTPException
from .. import models, schemas

def get_low_stock(db: Session, threshold: int = 10):
    return db.query(models.Inventory).join(
        models.Product
    ).filter(
        models.Inventory.quantity < threshold
    ).all()

def get_stock(db: Session, product_id: int):
    inventory = db.query(models.Inventory).filter(
        models.Inventory.product_id == product_id
    ).first()
    
    if not inventory:
        raise HTTPException(status_code=404, detail="Product not found in inventory")
    
    return inventory

def add_stock(db: Session, product_id: int, quantity: int):
    inventory = db.query(models.Inventory).filter(
        models.Inventory.product_id == product_id
    ).first()
    
    if not inventory:
        raise HTTPException(status_code=404, detail="Product not found in inventory")
    
    inventory.quantity += quantity
    db.commit()
    db.refresh(inventory)
    
    return inventory 