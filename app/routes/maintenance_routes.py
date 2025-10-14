import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Query

from app.services.maintenance_service import MaintenanceService
from app.models.maintenance_models import MaintenanceCreate, MaintenanceUpdate, MaintenanceResponse


router = APIRouter(
    prefix="/maintenances",
    tags=["Maintenances"]
)


@router.post(
    path="",
    summary="Create a new maintenance",
    description="Creates a new maintenance record in the system",
    response_model=MaintenanceResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_maintenance(maintenance: MaintenanceCreate):
    try:
        maintenance_service = MaintenanceService()
        return await maintenance_service.create_maintenance(maintenance)
    except Exception as e:
        logging.error(f"Error creating maintenance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating maintenance: {str(e)}"
        )


@router.get(
    path="/{maintenance_id}",
    summary="Get maintenance by ID",
    description="Retrieves a maintenance record by its ID",
    response_model=MaintenanceResponse
)
async def get_maintenance(maintenance_id: int):
    try:
        maintenance_service = MaintenanceService()
        maintenance = await maintenance_service.get_maintenance_by_id(maintenance_id)

        if not maintenance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Maintenance with ID {maintenance_id} not found"
            )

        return maintenance
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving maintenance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving maintenance: {str(e)}"
        )


@router.get(
    path="/asset/{asset_id}",
    summary="Get maintenances by asset",
    description="Retrieves all maintenance records for a specific asset",
    response_model=List[MaintenanceResponse]
)
async def get_maintenances_by_asset(asset_id: int):
    try:
        maintenance_service = MaintenanceService()
        return await maintenance_service.get_maintenances_by_asset(asset_id)
    except Exception as e:
        logging.error(f"Error retrieving maintenances: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving maintenances: {str(e)}"
        )


@router.get(
    path="/status/{status}",
    summary="Get maintenances by status",
    description="Retrieves all maintenance records with a specific status",
    response_model=List[MaintenanceResponse]
)
async def get_maintenances_by_status(status: str):
    try:
        maintenance_service = MaintenanceService()
        return await maintenance_service.get_maintenances_by_status(status)
    except Exception as e:
        logging.error(f"Error retrieving maintenances by status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving maintenances by status: {str(e)}"
        )


@router.get(
    path="/type/{maintenance_type}",
    summary="Get maintenances by type",
    description="Retrieves all maintenance records of a specific type",
    response_model=List[MaintenanceResponse]
)
async def get_maintenances_by_type(maintenance_type: str):
    try:
        maintenance_service = MaintenanceService()
        return await maintenance_service.get_maintenances_by_type(maintenance_type)
    except Exception as e:
        logging.error(f"Error retrieving maintenances by type: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving maintenances by type: {str(e)}"
        )


@router.get(
    path="",
    summary="Get all maintenances",
    description="Retrieves a paginated list of maintenance records",
    response_model=List[MaintenanceResponse]
)
async def get_all_maintenances(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    try:
        maintenance_service = MaintenanceService()
        return await maintenance_service.get_all_maintenances(limit, offset)
    except Exception as e:
        logging.error(f"Error retrieving maintenances: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving maintenances: {str(e)}"
        )


@router.put(
    path="/{maintenance_id}",
    summary="Update maintenance",
    description="Updates an existing maintenance record",
    response_model=MaintenanceResponse
)
async def update_maintenance(maintenance_id: int, maintenance: MaintenanceUpdate):
    try:
        maintenance_service = MaintenanceService()
        updated_maintenance = await maintenance_service.update_maintenance(maintenance_id, maintenance)

        if not updated_maintenance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Maintenance with ID {maintenance_id} not found"
            )

        return updated_maintenance
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating maintenance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating maintenance: {str(e)}"
        )


@router.delete(
    path="/{maintenance_id}",
    summary="Delete maintenance",
    description="Deletes a maintenance record from the system",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_maintenance(maintenance_id: int):
    try:
        maintenance_service = MaintenanceService()
        await maintenance_service.delete_maintenance(maintenance_id)
        return None
    except Exception as e:
        logging.error(f"Error deleting maintenance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting maintenance: {str(e)}"
        )

