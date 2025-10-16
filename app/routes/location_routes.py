import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Query, Depends

from app.security.jwt_utils import get_current_user

from app.services.location_service import LocationService
from app.models.location_models import LocationCreate, LocationUpdate, LocationResponse


router = APIRouter(
    prefix="/locations",
    tags=["Locations"],
    dependencies=[Depends(get_current_user)]
)


@router.post(
    path="",
    summary="Create a new location",
    description="Creates a new location in the system",
    response_model=LocationResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_location(location: LocationCreate):
    try:
        location_service = LocationService()
        return await location_service.create_location(location)
    except Exception as e:
        logging.error(f"Error creating location: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating location: {str(e)}"
        )


@router.get(
    path="/{location_id}",
    summary="Get location by ID",
    description="Retrieves a location by its ID",
    response_model=LocationResponse
)
async def get_location(location_id: int):
    try:
        location_service = LocationService()
        location = await location_service.get_location_by_id(location_id)

        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Location with ID {location_id} not found"
            )

        return location
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving location: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving location: {str(e)}"
        )


@router.get(
    path="",
    summary="Get all locations",
    description="Retrieves a paginated list of locations",
    response_model=List[LocationResponse]
)
async def get_all_locations(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    try:
        location_service = LocationService()
        return await location_service.get_all_locations(limit, offset)
    except Exception as e:
        logging.error(f"Error retrieving locations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving locations: {str(e)}"
        )


@router.put(
    path="/{location_id}",
    summary="Update location",
    description="Updates an existing location",
    response_model=LocationResponse
)
async def update_location(location_id: int, location: LocationUpdate):
    try:
        location_service = LocationService()
        updated_location = await location_service.update_location(location_id, location)

        if not updated_location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Location with ID {location_id} not found"
            )

        return updated_location
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating location: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating location: {str(e)}"
        )


@router.delete(
    path="/{location_id}",
    summary="Delete location",
    description="Deletes a location from the system",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_location(location_id: int):
    try:
        location_service = LocationService()
        await location_service.delete_location(location_id)
        return None
    except Exception as e:
        logging.error(f"Error deleting location: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting location: {str(e)}"
        )

