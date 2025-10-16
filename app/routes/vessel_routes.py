import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Query, Depends

from app.security.jwt_utils import get_current_user

from app.services.vessel_service import VesselService
from app.models.vessel_models import VesselCreate, VesselUpdate, VesselResponse


router = APIRouter(
    prefix="/vessels",
    tags=["Vessels"],
    dependencies=[Depends(get_current_user)]
)


@router.post(
    path="",
    summary="Create a new vessel",
    description="Creates a new vessel in the system",
    response_model=VesselResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_vessel(vessel: VesselCreate):
    try:
        vessel_service = VesselService()
        return await vessel_service.create_vessel(vessel)
    except Exception as e:
        logging.error(f"Error creating vessel: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating vessel: {str(e)}"
        )


@router.get(
    path="/{vessel_id}",
    summary="Get vessel by ID",
    description="Retrieves a vessel by its ID",
    response_model=VesselResponse
)
async def get_vessel(vessel_id: int):
    try:
        vessel_service = VesselService()
        vessel = await vessel_service.get_vessel_by_id(vessel_id)

        if not vessel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vessel with ID {vessel_id} not found"
            )

        return vessel
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving vessel: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving vessel: {str(e)}"
        )


@router.get(
    path="",
    summary="Get all vessels",
    description="Retrieves a paginated list of vessels",
    response_model=List[VesselResponse]
)
async def get_all_vessels(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    try:
        vessel_service = VesselService()
        return await vessel_service.get_all_vessels(limit, offset)
    except Exception as e:
        logging.error(f"Error retrieving vessels: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving vessels: {str(e)}"
        )


@router.put(
    path="/{vessel_id}",
    summary="Update vessel",
    description="Updates an existing vessel",
    response_model=VesselResponse
)
async def update_vessel(vessel_id: int, vessel: VesselUpdate):
    try:
        vessel_service = VesselService()
        updated_vessel = await vessel_service.update_vessel(vessel_id, vessel)

        if not updated_vessel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vessel with ID {vessel_id} not found"
            )

        return updated_vessel
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating vessel: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating vessel: {str(e)}"
        )


@router.delete(
    path="/{vessel_id}",
    summary="Delete vessel",
    description="Deletes a vessel from the system",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_vessel(vessel_id: int):
    try:
        vessel_service = VesselService()
        await vessel_service.delete_vessel(vessel_id)
        return None
    except Exception as e:
        logging.error(f"Error deleting vessel: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting vessel: {str(e)}"
        )

