import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Query, Depends

from app.security.jwt_utils import get_current_user
from app.services.spare_part_service import SparePartService
from app.models.spare_part_models import SparePartCreate, SparePartUpdate, SparePartResponse


router = APIRouter(
    prefix="/spare-parts",
    tags=["Spare Parts"],
    dependencies=[Depends(get_current_user)]
)


@router.post(
    path="",
    summary="Create a new spare part",
    description="Creates a new spare part in the system",
    response_model=SparePartResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_spare_part(part: SparePartCreate):
    try:
        service = SparePartService()
        return await service.create_spare_part(part)
    except Exception as e:
        logging.error(f"Error creating spare part: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating spare part: {str(e)}"
        )


@router.get(
    path="/{part_id}",
    summary="Get spare part by ID",
    description="Retrieves a spare part by its ID",
    response_model=SparePartResponse
)
async def get_spare_part(part_id: int):
    try:
        service = SparePartService()
        part = await service.get_spare_part_by_id(part_id)

        if not part:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Spare part with ID {part_id} not found"
            )

        return part
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving spare part: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving spare part: {str(e)}"
        )


@router.get(
    path="",
    summary="Get all spare parts",
    description="Retrieves all spare parts with pagination",
    response_model=List[SparePartResponse]
)
async def get_all_spare_parts(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0)
):
    try:
        service = SparePartService()
        return await service.get_all_spare_parts(limit, offset)
    except Exception as e:
        logging.error(f"Error retrieving spare parts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving spare parts: {str(e)}"
        )


@router.put(
    path="/{part_id}",
    summary="Update spare part",
    description="Updates an existing spare part",
    response_model=SparePartResponse
)
async def update_spare_part(part_id: int, part: SparePartUpdate):
    try:
        service = SparePartService()
        updated = await service.update_spare_part(part_id, part)

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Spare part with ID {part_id} not found"
            )

        return updated
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating spare part: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating spare part: {str(e)}"
        )


@router.delete(
    path="/{part_id}",
    summary="Delete spare part",
    description="Deletes a spare part by ID",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_spare_part(part_id: int):
    try:
        service = SparePartService()
        await service.delete_spare_part(part_id)
        return None
    except Exception as e:
        logging.error(f"Error deleting spare part: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting spare part: {str(e)}"
        )

