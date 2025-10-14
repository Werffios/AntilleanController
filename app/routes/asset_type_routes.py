import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Query

from app.services.asset_type_service import AssetTypeService
from app.models.asset_type_models import AssetTypeCreate, AssetTypeUpdate, AssetTypeResponse


router = APIRouter(
    prefix="/asset-types",
    tags=["Asset Types"]
)


@router.post(
    path="",
    summary="Create a new asset type",
    description="Creates a new asset type in the system",
    response_model=AssetTypeResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_asset_type(asset_type: AssetTypeCreate):
    try:
        asset_type_service = AssetTypeService()
        return await asset_type_service.create_asset_type(asset_type)
    except Exception as e:
        logging.error(f"Error creating asset type: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating asset type: {str(e)}"
        )


@router.get(
    path="/{asset_type_id}",
    summary="Get asset type by ID",
    description="Retrieves an asset type by its ID",
    response_model=AssetTypeResponse
)
async def get_asset_type(asset_type_id: int):
    try:
        asset_type_service = AssetTypeService()
        asset_type = await asset_type_service.get_asset_type_by_id(asset_type_id)

        if not asset_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asset type with ID {asset_type_id} not found"
            )

        return asset_type
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving asset type: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving asset type: {str(e)}"
        )


@router.get(
    path="",
    summary="Get all asset types",
    description="Retrieves all asset types with pagination",
    response_model=List[AssetTypeResponse]
)
async def get_all_asset_types(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0)
):
    try:
        asset_type_service = AssetTypeService()
        return await asset_type_service.get_all_asset_types(limit, offset)
    except Exception as e:
        logging.error(f"Error retrieving asset types: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving asset types: {str(e)}"
        )


@router.put(
    path="/{asset_type_id}",
    summary="Update asset type",
    description="Updates an existing asset type",
    response_model=AssetTypeResponse
)
async def update_asset_type(asset_type_id: int, asset_type: AssetTypeUpdate):
    try:
        asset_type_service = AssetTypeService()
        updated_asset_type = await asset_type_service.update_asset_type(asset_type_id, asset_type)

        if not updated_asset_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asset type with ID {asset_type_id} not found"
            )

        return updated_asset_type
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating asset type: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating asset type: {str(e)}"
        )


@router.delete(
    path="/{asset_type_id}",
    summary="Delete asset type",
    description="Deletes an asset type by ID",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_asset_type(asset_type_id: int):
    try:
        asset_type_service = AssetTypeService()
        await asset_type_service.delete_asset_type(asset_type_id)
    except Exception as e:
        logging.error(f"Error deleting asset type: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting asset type: {str(e)}"
        )
