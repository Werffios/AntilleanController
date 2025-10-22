from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class SparePartBase(BaseModel):
    name: str
    part_number: str
    manufacturer: Optional[str] = None
    quantity: int = 0
    unit_cost: Decimal
    location: Optional[str] = None


class SparePartCreate(SparePartBase):
    pass


class SparePartUpdate(BaseModel):
    name: Optional[str] = None
    part_number: Optional[str] = None
    manufacturer: Optional[str] = None
    quantity: Optional[int] = None
    unit_cost: Optional[Decimal] = None
    location: Optional[str] = None


class SparePartResponse(SparePartBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SparePartIdParam(BaseModel):
    id: int

