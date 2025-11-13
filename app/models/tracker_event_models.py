from pydantic import BaseModel, Field
from typing import Optional, Union, Dict, Any
from datetime import datetime


class EventDetails(BaseModel):
    EventType: Optional[str] = None
    ConfidenceLevel: Optional[str] = None


class LocationDetails(BaseModel):
    Latitude: Optional[float] = None
    Longitude: Optional[float] = None
    AccuracyLevel: Optional[str] = None
    LocationName: Optional[str] = None
    Line1: Optional[str] = None
    Area: Optional[str] = None
    Region: Optional[str] = None
    PostalCode: Optional[str] = None
    CountryCode: Optional[str] = None


class TrackerEventBase(BaseModel):
    Alert: Optional[str] = None
    AssetName: Optional[str] = None
    AssetType: Optional[str] = None
    BL: Optional[str] = None
    Booking: Optional[str] = None
    Event: Optional[EventDetails] = None
    EventTime: Optional[datetime] = None
    # Accept both legacy string heartbeat and new object heartbeat payloads
    Heartbeat: Optional[Union[str, Dict[str, Any]]] = None
    Location: Optional[LocationDetails] = None
    ReceiveTime: Optional[datetime] = None
    ReportTime: Optional[datetime] = None
    TrackerId: Optional[str] = None
    TrackerType: Optional[str] = None
    Type: Optional[str] = None


class TrackerEventResponse(TrackerEventBase):
    id: str = Field(alias="_id")

    class Config:
        from_attributes = True
        populate_by_name = True


class TrackerEventCreate(TrackerEventBase):
    pass


class TrackerIdParam(BaseModel):
    tracker_id: str

