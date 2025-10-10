from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VoyageBase(BaseModel):
    route_id: int
    vessel_id: int
    departure_datetime: Optional[datetime] = None
    arrival_datetime: Optional[datetime] = None
    status: str = "planned"


class VoyageCreate(VoyageBase):
    pass


class VoyageUpdate(BaseModel):
    route_id: Optional[int] = None
    vessel_id: Optional[int] = None
    departure_datetime: Optional[datetime] = None
    arrival_datetime: Optional[datetime] = None
    status: Optional[str] = None


class VoyageResponse(VoyageBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class VoyageIdParam(BaseModel):
    id: int

