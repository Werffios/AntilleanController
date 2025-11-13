import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Query, Depends

from app.security.jwt_utils import get_current_user
from app.services.maintenance_part_service import MaintenancePartService
from app.models.maintenance_part_models import (
    MaintenancePartCreate,
    MaintenancePartUpdate,
    MaintenancePartResponse,
)


router = APIRouter(
    prefix="/maintenance-parts",
    tags=["Maintenance Parts"],
    dependencies=[Depends(get_current_user)]
)


@router.post(
    path="",
    summary="Create a maintenance part consumption",
    description="Associates a spare part consumption with a maintenance",
    response_model=MaintenancePartResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_maintenance_part(item: MaintenancePartCreate):
    try:
        service = MaintenancePartService()
        return await service.create_maintenance_part(item)
    except Exception as e:
        logging.error(f"Error creating maintenance part: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating maintenance part: {str(e)}"
        )


@router.get(
    path="/maintenance/{maintenance_id}",
    summary="Get parts consumed by maintenance",
    description="Retrieves all maintenance part consumptions for a maintenance",
    response_model=List[MaintenancePartResponse]
)
async def get_by_maintenance(
    maintenance_id: int,
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0)
):
    try:
        service = MaintenancePartService()
        return await service.get_maintenance_parts_by_maintenance(maintenance_id, limit, offset)
    except Exception as e:
        logging.error(f"Error retrieving maintenance parts by maintenance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving maintenance parts by maintenance: {str(e)}"
        )


@router.get(
    path="/spare-part/{spare_part_id}",
    summary="Get maintenance consumptions by spare part",
    description="Retrieves all maintenance part consumptions for a spare part",
    response_model=List[MaintenancePartResponse]
)
async def get_by_spare_part(
    spare_part_id: int,
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0)
):
    try:
        service = MaintenancePartService()
        return await service.get_maintenance_parts_by_spare_part(spare_part_id, limit, offset)
    except Exception as e:
        logging.error(f"Error retrieving maintenance parts by spare part: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving maintenance parts by spare part: {str(e)}"
        )


@router.get(
    path="",
    summary="Get all maintenance part consumptions",
    description="Retrieves all maintenance part consumptions with pagination",
    response_model=List[MaintenancePartResponse]
)
async def get_all(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0)
):
    try:
        service = MaintenancePartService()
        return await service.get_all_maintenance_parts(limit, offset)
    except Exception as e:
        logging.error(f"Error retrieving maintenance parts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving maintenance parts: {str(e)}"
        )


@router.put(
    path="/{maintenance_id}/{spare_part_id}",
    summary="Update a maintenance part consumption",
    description="Updates the quantity used or cost at consumption for a maintenance part",
    response_model=MaintenancePartResponse
)
async def update_maintenance_part(maintenance_id: int, spare_part_id: int, item: MaintenancePartUpdate):
    try:
        service = MaintenancePartService()
        updated = await service.update_maintenance_part(maintenance_id, spare_part_id, item)

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Maintenance part with maintenance_id={maintenance_id} and spare_part_id={spare_part_id} not found"
            )

        return updated
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating maintenance part: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating maintenance part: {str(e)}"
        )


@router.delete(
    path="/{maintenance_id}/{spare_part_id}",
    summary="Delete a maintenance part consumption",
    description="Deletes a maintenance part consumption by maintenance and spare part IDs",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_maintenance_part(maintenance_id: int, spare_part_id: int):
    try:
        service = MaintenancePartService()
        await service.delete_maintenance_part(maintenance_id, spare_part_id)
        return None
    except Exception as e:
        logging.error(f"Error deleting maintenance part: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting maintenance part: {str(e)}"
        )

@router.get(
    path="/{maintenance_id}/{spare_part_id}",
    summary="Get maintenance part by IDs",
    description="Retrieves a maintenance part consumption by maintenance and spare part IDs",
    response_model=MaintenancePartResponse
)
async def get_maintenance_part(maintenance_id: int, spare_part_id: int):
    try:
        service = MaintenancePartService()
        item = await service.get_maintenance_part(maintenance_id, spare_part_id)

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Maintenance part with maintenance_id={maintenance_id} and spare_part_id={spare_part_id} not found"
            )

        return item
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving maintenance part: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving maintenance part: {str(e)}"
        )