from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class VesselBase(BaseModel):
    vessel_name: str
    imo_number: str
    mmsi_number: Optional[str] = None
    call_sign: Optional[str] = None
    ais_transponder_class: Optional[str] = None
    general_vessel_type: Optional[str] = None
    detailed_vessel_type: Optional[str] = None
    service_status: Optional[str] = None
    port_of_registry: Optional[str] = None
    year_built: Optional[int] = None
    dimensions: Optional[str] = None
    design_description: Optional[str] = None
    last_dry_dock_survey: Optional[date] = None
    tonnage_info: Optional[str] = None
    engine_info: Optional[str] = None
    capacity_info: Optional[str] = None


class VesselCreate(VesselBase):
    pass


class VesselUpdate(BaseModel):
    vessel_name: Optional[str] = None
    imo_number: Optional[str] = None
    mmsi_number: Optional[str] = None
    call_sign: Optional[str] = None
    ais_transponder_class: Optional[str] = None
    general_vessel_type: Optional[str] = None
    detailed_vessel_type: Optional[str] = None
    service_status: Optional[str] = None
    port_of_registry: Optional[str] = None
    year_built: Optional[int] = None
    dimensions: Optional[str] = None
    design_description: Optional[str] = None
    last_dry_dock_survey: Optional[date] = None
    tonnage_info: Optional[str] = None
    engine_info: Optional[str] = None
    capacity_info: Optional[str] = None


class VesselResponse(VesselBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class VesselIdParam(BaseModel):
    id: int

