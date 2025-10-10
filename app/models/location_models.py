from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class LocationType(str, Enum):
    port = "port"
    warehouse = "warehouse"
    customer_facility = "customer_facility"


class LocationBase(BaseModel):
    location_name: str
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    location_type: LocationType


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    location_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    location_type: Optional[LocationType] = None


class LocationResponse(LocationBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LocationIdParam(BaseModel):
    id: int

