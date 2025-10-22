from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class MaintenancePartBase(BaseModel):
    maintenance_id: int
    spare_part_id: int
    quantity_used: int
    cost_at_consumption: Decimal


class MaintenancePartCreate(MaintenancePartBase):
    pass


class MaintenancePartUpdate(BaseModel):
    quantity_used: Optional[int] = None
    cost_at_consumption: Optional[Decimal] = None


class MaintenancePartResponse(MaintenancePartBase):
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

