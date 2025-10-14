from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class BillOfLadingBase(BaseModel):
    shipment_id: int
    bol_number: str
    issue_date: date
    terms_and_conditions: Optional[str] = None
    shipper_details: Optional[str] = None
    consignee_details: Optional[str] = None
    is_hazardous: bool = False


class BillOfLadingCreate(BillOfLadingBase):
    pass


class BillOfLadingUpdate(BaseModel):
    shipment_id: Optional[int] = None
    bol_number: Optional[str] = None
    issue_date: Optional[date] = None
    terms_and_conditions: Optional[str] = None
    shipper_details: Optional[str] = None
    consignee_details: Optional[str] = None
    is_hazardous: Optional[bool] = None


class BillOfLadingResponse(BillOfLadingBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BillOfLadingIdParam(BaseModel):
    id: int

