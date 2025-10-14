from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class ShipmentItemBase(BaseModel):
    shipment_id: int
    asset_id: int
    description: Optional[str] = None
    weight_kg: Optional[Decimal] = None
    dimensions: Optional[str] = None


class ShipmentItemCreate(ShipmentItemBase):
    pass


class ShipmentItemUpdate(BaseModel):
    shipment_id: Optional[int] = None
    asset_id: Optional[int] = None
    description: Optional[str] = None
    weight_kg: Optional[Decimal] = None
    dimensions: Optional[str] = None


class ShipmentItemResponse(ShipmentItemBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ShipmentItemIdParam(BaseModel):
    id: int

