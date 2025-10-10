from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AssetTypeBase(BaseModel):
    type_name: str


class AssetTypeCreate(AssetTypeBase):
    pass


class AssetTypeUpdate(BaseModel):
    type_name: Optional[str] = None


class AssetTypeResponse(AssetTypeBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AssetTypeIdParam(BaseModel):
    id: int

