from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from decimal import Decimal
from enum import Enum


class MaintenanceType(str, Enum):
    preventive = "preventive"
    corrective = "corrective"
    inspection = "inspection"
    emergency = "emergency"
    upgrade = "upgrade"


class MaintenanceStatus(str, Enum):
    scheduled = "scheduled"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"
    on_hold = "on_hold"


class MaintenanceBase(BaseModel):
    asset_id: int
    maintenance_type: MaintenanceType
    status: MaintenanceStatus = MaintenanceStatus.scheduled
    description: str
    service_provider: Optional[str] = None
    cost: Optional[Decimal] = None
    scheduled_at: Optional[date] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class MaintenanceCreate(MaintenanceBase):
    pass


class MaintenanceUpdate(BaseModel):
    asset_id: Optional[int] = None
    maintenance_type: Optional[MaintenanceType] = None
    status: Optional[MaintenanceStatus] = None
    description: Optional[str] = None
    service_provider: Optional[str] = None
    cost: Optional[Decimal] = None
    scheduled_at: Optional[date] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class MaintenanceResponse(MaintenanceBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MaintenanceIdParam(BaseModel):
    id: int
