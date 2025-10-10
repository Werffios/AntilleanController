from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from enum import Enum


class Ownership(str, Enum):
    owned = "Owned"
    third_party = "Third-Party"


class AssetStatus(str, Enum):
    empty = "empty"
    full = "full"


class AssetSize(str, Enum):
    twenty_ft = "20ft"
    forty_ft = "40ft"
    forty_five_ft = "45ft"


class AssetCondition(str, Enum):
    operational = "operational"
    non_operational = "non_operational"
    under_maintenance = "under_maintenance"


class AssetCategory(str, Enum):
    excellent = "excellent"
    good = "good"
    bad = "bad"
    very_bad = "very_bad"


class AssetBase(BaseModel):
    asset_code: str
    asset_type_id: Optional[int] = None
    ownership: Ownership
    status: AssetStatus
    size: AssetSize
    condition: AssetCondition
    category: AssetCategory
    manufactured_at: date
    last_maintenance_at: Optional[date] = None
    last_inspection_at: Optional[date] = None
    next_inspection_due_at: Optional[date] = None
    max_payload_kg: int


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    asset_code: Optional[str] = None
    asset_type_id: Optional[int] = None
    ownership: Optional[Ownership] = None
    status: Optional[AssetStatus] = None
    size: Optional[AssetSize] = None
    condition: Optional[AssetCondition] = None
    category: Optional[AssetCategory] = None
    manufactured_at: Optional[date] = None
    last_maintenance_at: Optional[date] = None
    last_inspection_at: Optional[date] = None
    next_inspection_due_at: Optional[date] = None
    max_payload_kg: Optional[int] = None


class AssetResponse(AssetBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AssetIdParam(BaseModel):
    id: int

