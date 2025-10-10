import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Query

from app.services.voyage_service import VoyageService
from app.models.voyage_models import VoyageCreate, VoyageUpdate, VoyageResponse


router = APIRouter(
    prefix="/voyages",
    tags=["Voyages"]
)


@router.post(
    path="",
    summary="Create a new voyage",
    description="Creates a new voyage in the system",
    response_model=VoyageResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_voyage(voyage: VoyageCreate):
    try:
        voyage_service = VoyageService()
        return await voyage_service.create_voyage(voyage)
    except Exception as e:
        logging.error(f"Error creating voyage: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating voyage: {str(e)}"
        )


@router.get(
    path="/{voyage_id}",
    summary="Get voyage by ID",
    description="Retrieves a voyage by its ID",
    response_model=VoyageResponse
)
async def get_voyage(voyage_id: int):
    try:
        voyage_service = VoyageService()
        voyage = await voyage_service.get_voyage_by_id(voyage_id)

        if not voyage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Voyage with ID {voyage_id} not found"
            )

        return voyage
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving voyage: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving voyage: {str(e)}"
        )


@router.get(
    path="/vessel/{vessel_id}",
    summary="Get voyages by vessel",
    description="Retrieves all voyages for a specific vessel",
    response_model=List[VoyageResponse]
)
async def get_voyages_by_vessel(vessel_id: int):
    try:
        voyage_service = VoyageService()
        return await voyage_service.get_voyages_by_vessel(vessel_id)
    except Exception as e:
        logging.error(f"Error retrieving voyages: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving voyages: {str(e)}"
        )


@router.get(
    path="",
    summary="Get all voyages",
    description="Retrieves a paginated list of voyages",
    response_model=List[VoyageResponse]
)
async def get_all_voyages(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    try:
        voyage_service = VoyageService()
        return await voyage_service.get_all_voyages(limit, offset)
    except Exception as e:
        logging.error(f"Error retrieving voyages: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving voyages: {str(e)}"
        )


@router.put(
    path="/{voyage_id}",
    summary="Update voyage",
    description="Updates an existing voyage",
    response_model=VoyageResponse
)
async def update_voyage(voyage_id: int, voyage: VoyageUpdate):
    try:
        voyage_service = VoyageService()
        updated_voyage = await voyage_service.update_voyage(voyage_id, voyage)

        if not updated_voyage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Voyage with ID {voyage_id} not found"
            )

        return updated_voyage
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating voyage: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating voyage: {str(e)}"
        )


@router.delete(
    path="/{voyage_id}",
    summary="Delete voyage",
    description="Deletes a voyage from the system",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_voyage(voyage_id: int):
    try:
        voyage_service = VoyageService()
        await voyage_service.delete_voyage(voyage_id)
        return None
    except Exception as e:
        logging.error(f"Error deleting voyage: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting voyage: {str(e)}"
        )

