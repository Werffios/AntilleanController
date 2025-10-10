import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Query

from app.services.asset_service import AssetService
from app.models.asset_models import AssetCreate, AssetUpdate, AssetResponse


router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)


@router.post(
    path="",
    summary="Create a new asset",
    description="Creates a new asset in the system",
    response_model=AssetResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_asset(asset: AssetCreate):
    try:
        asset_service = AssetService()
        return await asset_service.create_asset(asset)
    except Exception as e:
        logging.error(f"Error creating asset: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating asset: {str(e)}"
        )


@router.get(
    path="/{asset_id}",
    summary="Get asset by ID",
    description="Retrieves an asset by its ID",
    response_model=AssetResponse
)
async def get_asset(asset_id: int):
    try:
        asset_service = AssetService()
        asset = await asset_service.get_asset_by_id(asset_id)

        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asset with ID {asset_id} not found"
            )

        return asset
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving asset: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving asset: {str(e)}"
        )


@router.get(
    path="",
    summary="Get all assets",
    description="Retrieves a paginated list of assets",
    response_model=List[AssetResponse]
)
async def get_all_assets(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    try:
        asset_service = AssetService()
        return await asset_service.get_all_assets(limit, offset)
    except Exception as e:
        logging.error(f"Error retrieving assets: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving assets: {str(e)}"
        )


@router.put(
    path="/{asset_id}",
    summary="Update asset",
    description="Updates an existing asset",
    response_model=AssetResponse
)
async def update_asset(asset_id: int, asset: AssetUpdate):
    try:
        asset_service = AssetService()
        updated_asset = await asset_service.update_asset(asset_id, asset)

        if not updated_asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asset with ID {asset_id} not found"
            )

        return updated_asset
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating asset: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating asset: {str(e)}"
        )


@router.delete(
    path="/{asset_id}",
    summary="Delete asset",
    description="Deletes an asset from the system",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_asset(asset_id: int):
    try:
        asset_service = AssetService()
        await asset_service.delete_asset(asset_id)
        return None
    except Exception as e:
        logging.error(f"Error deleting asset: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting asset: {str(e)}"
        )

