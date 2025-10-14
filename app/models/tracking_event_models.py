from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TrackingEventBase(BaseModel):
    shipment_id: int
    location_id: Optional[int] = None
    event_datetime: datetime
    event_type: str
    notes: Optional[str] = None


class TrackingEventCreate(TrackingEventBase):
    pass


class TrackingEventUpdate(BaseModel):
    shipment_id: Optional[int] = None
    location_id: Optional[int] = None
    event_datetime: Optional[datetime] = None
    event_type: Optional[str] = None
    notes: Optional[str] = None


class TrackingEventResponse(TrackingEventBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TrackingEventIdParam(BaseModel):
    id: int

