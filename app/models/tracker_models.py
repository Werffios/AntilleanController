from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TrackerBase(BaseModel):
    tracker_code: str


class TrackerCreate(TrackerBase):
    pass


class TrackerUpdate(BaseModel):
    tracker_code: Optional[str] = None


class TrackerResponse(TrackerBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TrackerIdParam(BaseModel):
    id: int

