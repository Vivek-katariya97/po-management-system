from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from ..database import get_db
from ..models import PurchaseOrder as PurchaseOrderModel, PurchaseOrderItem as PurchaseOrderItemModel, Product as ProductModel, Vendor as VendorModel
from ..schemas import PurchaseOrder, PurchaseOrderCreateRequest
from ..services.po_service import calculate_total

router = APIRouter(prefix="/purchase-orders", tags=["purchase-orders"])

@router.get("", response_model=List[PurchaseOrder])
def get_purchase_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pos = db.query(PurchaseOrderModel).offset(skip).limit(limit).all()
    return pos

@router.get("/{id}", response_model=PurchaseOrder)
def get_purchase_order(id: int, db: Session = Depends(get_db)):
    po = db.query(PurchaseOrderModel).filter(PurchaseOrderModel.id == id).first()
    if not po:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    return po

@router.post("", response_model=PurchaseOrder)
def create_purchase_order(request: PurchaseOrderCreateRequest, db: Session = Depends(get_db)):
    # Validate vendor
    vendor = db.query(VendorModel).filter(VendorModel.id == request.vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=400, detail="Vendor not found")
        
    items_to_calc = []
    product_dict = {}
    
    # Pre-fetch products to get unit_price
    for item in request.items:
        product = db.query(ProductModel).filter(ProductModel.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=400, detail=f"Product with ID {item.product_id} not found")
        product_dict[item.product_id] = product
        items_to_calc.append({"price": float(product.unit_price), "quantity": item.quantity})
        
    # Calculate 5% tax and totals
    _, _, total_amount = calculate_total(items_to_calc)
    
    # Generate unique PO reference number
    ref_no = f"PO-{uuid.uuid4().hex[:8].upper()}"
    
    # 1. Create Purchase Order header
    db_po = PurchaseOrderModel(
        reference_no=ref_no,
        vendor_id=request.vendor_id,
        total_amount=total_amount,
        status="Pending"
    )
    db.add(db_po)
    db.commit()
    db.refresh(db_po)
    
    # 2. Add Line Items
    for item in request.items:
        db_item = PurchaseOrderItemModel(
            purchase_order_id=db_po.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product_dict[item.product_id].unit_price
        )
        db.add(db_item)
        
    db.commit()
    db.refresh(db_po)
    
    return db_po
