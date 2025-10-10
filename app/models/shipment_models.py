from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class ShipmentBase(BaseModel):
    tracking_code: str
    customer_id: int
    voyage_id: Optional[int] = None
    origin_location_id: int
    destination_location_id: int
    creation_datetime: datetime
    declared_value: Optional[Decimal] = None
    current_status: str = "created"


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentUpdate(BaseModel):
    tracking_code: Optional[str] = None
    customer_id: Optional[int] = None
    voyage_id: Optional[int] = None
    origin_location_id: Optional[int] = None
    destination_location_id: Optional[int] = None
    creation_datetime: Optional[datetime] = None
    declared_value: Optional[Decimal] = None
    current_status: Optional[str] = None


class ShipmentResponse(ShipmentBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ShipmentIdParam(BaseModel):
    id: int

