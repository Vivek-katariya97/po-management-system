from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Vendor as VendorModel
from ..schemas import Vendor, VendorCreate

router = APIRouter(prefix="/vendors", tags=["vendors"])

@router.post("", response_model=Vendor)
def create_vendor(vendor: VendorCreate, db: Session = Depends(get_db)):
    db_vendor = VendorModel(**vendor.model_dump())
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

@router.get("", response_model=List[Vendor])
def get_vendors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vendors = db.query(VendorModel).offset(skip).limit(limit).all()
    return vendors
