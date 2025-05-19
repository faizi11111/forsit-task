from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from fastapi import HTTPException
from .. import models, schemas

def get_date_formats(period: schemas.Period):
    formats = {
        schemas.Period.DAILY: ('%Y-%m-%d', '%Y-%m-%d', '+1 day'),
        schemas.Period.WEEKLY: ('%Y-%W', '%Y-%m-%d', 'weekday 0'),
        schemas.Period.MONTHLY: ('%Y-%m', '%Y-%m-01', '+1 month'),
        schemas.Period.ANNUALLY: ('%Y', '%Y-01-01', '+1 year')
    }
    return formats[period]

def get_sales_analysis(
    db: Session,
    period: schemas.Period,
    start_date: datetime = None,
    end_date: datetime = None,
    product_id: int = None,
    category: str = None
):
    query = db.query(models.Sale).join(models.Product)
    
    if start_date:
        query = query.filter(models.Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(models.Sale.sale_date <= end_date)
    if product_id:
        query = query.filter(models.Sale.product_id == product_id)
    if category:
        query = query.filter(models.Product.category == category)
    
    group_fmt, start_fmt, end_mod = get_date_formats(period)
    
    query = query.group_by(
        func.strftime(group_fmt, models.Sale.sale_date)
    ).with_entities(
        func.strftime(start_fmt, models.Sale.sale_date).label('period_start'),
        func.strftime(start_fmt, models.Sale.sale_date, end_mod).label('period_end'),
        func.sum(models.Sale.total_amount).label('total_sales'),
        func.sum(models.Sale.quantity).label('total_quantity'),
        func.count(models.Sale.id).label('number_of_orders')
    ).order_by('period_start')
    
    return query.all()

def get_sales(
    db: Session,
    start_date: datetime = None,
    end_date: datetime = None,
    product_id: int = None,
    category: str = None
):
    query = db.query(models.Sale).join(
        models.Product
    ).options(
        joinedload(models.Sale.product)
    )
    
    if start_date:
        query = query.filter(models.Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(models.Sale.sale_date <= end_date)
    if product_id:
        query = query.filter(models.Sale.product_id == product_id)
    if category:
        query = query.filter(models.Product.category == category)
    
    return query.order_by(models.Sale.sale_date.desc()).all()

def create_sale(db: Session, sale: schemas.SaleCreate):
    product = db.query(models.Product).filter(models.Product.id == sale.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    inventory = db.query(models.Inventory).filter(models.Inventory.product_id == sale.product_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Product inventory not found")
    
    if inventory.quantity < sale.quantity:
        raise HTTPException(
            status_code=400, 
            detail=f"Not enough stock. Available: {inventory.quantity}, Requested: {sale.quantity}"
        )
    
    total_amount = product.price * sale.quantity
    db_sale = models.Sale(
        product_id=sale.product_id,
        quantity=sale.quantity,
        total_amount=total_amount,
        sale_date=datetime.utcnow()
    )
    db.add(db_sale)
    inventory.quantity -= sale.quantity
    
    db.commit()
    db.refresh(db_sale)
    
    return db_sale 