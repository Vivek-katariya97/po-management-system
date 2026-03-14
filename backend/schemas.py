from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- Vendor Schemas ---
class VendorBase(BaseModel):
    name: str
    contact: str
    rating: Optional[float] = None

class VendorCreate(VendorBase):
    pass

class Vendor(VendorBase):
    id: int

    class Config:
        from_attributes = True

# --- Product Schemas ---
class ProductBase(BaseModel):
    name: str
    sku: str
    unit_price: float
    stock_level: Optional[int] = 0
    category: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

# --- Purchase Order Item Schemas ---
class PurchaseOrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class PurchaseOrderItem(PurchaseOrderItemBase):
    id: int
    purchase_order_id: int
    product: Product

    class Config:
        from_attributes = True

# --- Purchase Order Schemas ---
class PurchaseOrderCreateItem(BaseModel):
    product_id: int
    quantity: int

class PurchaseOrderCreateRequest(BaseModel):
    vendor_id: int
    items: List[PurchaseOrderCreateItem]

class PurchaseOrderBase(BaseModel):
    reference_no: str
    vendor_id: int
    total_amount: float
    status: str
    created_at: datetime

class PurchaseOrder(PurchaseOrderBase):
    id: int
    vendor: Vendor
    items: List[PurchaseOrderItem]

    class Config:
        from_attributes = True
