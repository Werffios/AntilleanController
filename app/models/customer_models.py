from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class CustomerBase(BaseModel):
    full_name: str
    identification_number: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    full_name: Optional[str] = None
    identification_number: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None


class CustomerResponse(CustomerBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CustomerIdParam(BaseModel):
    id: int

