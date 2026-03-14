from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Product as ProductModel
from ..schemas import Product, ProductCreate

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.sku == product.sku).first()
    if db_product:
        raise HTTPException(status_code=400, detail="SKU already registered")
    
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("", response_model=List[Product])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(ProductModel).offset(skip).limit(limit).all()
    return products
