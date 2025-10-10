from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RouteBase(BaseModel):
    origin_location_id: int
    destination_location_id: int


class RouteCreate(RouteBase):
    pass


class RouteUpdate(BaseModel):
    origin_location_id: Optional[int] = None
    destination_location_id: Optional[int] = None


class RouteResponse(RouteBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RouteIdParam(BaseModel):
    id: int

