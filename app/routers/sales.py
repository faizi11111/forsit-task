from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from .. import schemas
from ..database import get_db
from ..services import sales_service

router = APIRouter(
    prefix="/sales",
    tags=["sales"]
)

@router.get("/analysis", response_model=List[schemas.PeriodSales])
def analyze_sales(
    period: schemas.Period,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    product_id: Optional[int] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return sales_service.get_sales_analysis(
        db=db,
        period=period,
        start_date=start_date,
        end_date=end_date,
        product_id=product_id,
        category=category
    )

@router.get("/", response_model=List[schemas.Sale])
def get_sales(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    product_id: Optional[int] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return sales_service.get_sales(
        db=db,
        start_date=start_date,
        end_date=end_date,
        product_id=product_id,
        category=category
    )

@router.post("/", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    return sales_service.create_sale(db=db, sale=sale) 