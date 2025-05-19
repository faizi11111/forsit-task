from sqlalchemy.orm import Session
from fastapi import HTTPException
from .. import models, schemas

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def create_product(db: Session, product: schemas.ProductCreate):
    # Create product
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category
    )
    db.add(db_product)
    db.flush()  # Get the product ID
    
    # Create initial inventory
    inventory = models.Inventory(
        product_id=db_product.id,
        quantity=product.initial_stock
    )
    db.add(inventory)
    
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    db_product = get_product(db, product_id)
    
    for key, value in product.dict().items():
        if key != 'initial_stock':  # Don't update inventory here
            setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"} 