import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Query

from app.services.tracker_service import TrackerService
from app.models.tracker_models import TrackerCreate, TrackerUpdate, TrackerResponse


router = APIRouter(
    prefix="/trackers",
    tags=["Trackers"]
)


@router.post(
    path="",
    summary="Create a new tracker",
    description="Creates a new tracker in the system",
    response_model=TrackerResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_tracker(tracker: TrackerCreate):
    try:
        tracker_service = TrackerService()
        return await tracker_service.create_tracker(tracker)
    except Exception as e:
        logging.error(f"Error creating tracker: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating tracker: {str(e)}"
        )


@router.get(
    path="/{tracker_id}",
    summary="Get tracker by ID",
    description="Retrieves a tracker by its ID",
    response_model=TrackerResponse
)
async def get_tracker(tracker_id: int):
    try:
        tracker_service = TrackerService()
        tracker = await tracker_service.get_tracker_by_id(tracker_id)

        if not tracker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tracker with ID {tracker_id} not found"
            )

        return tracker
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving tracker: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tracker: {str(e)}"
        )


@router.get(
    path="/code/{tracker_code}",
    summary="Get tracker by code",
    description="Retrieves a tracker by its code",
    response_model=TrackerResponse
)
async def get_tracker_by_code(tracker_code: str):
    try:
        tracker_service = TrackerService()
        tracker = await tracker_service.get_tracker_by_code(tracker_code)

        if not tracker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tracker with code {tracker_code} not found"
            )

        return tracker
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving tracker: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tracker: {str(e)}"
        )


@router.get(
    path="",
    summary="Get all trackers",
    description="Retrieves all trackers with pagination",
    response_model=List[TrackerResponse]
)
async def get_all_trackers(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0)
):
    try:
        tracker_service = TrackerService()
        return await tracker_service.get_all_trackers(limit, offset)
    except Exception as e:
        logging.error(f"Error retrieving trackers: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving trackers: {str(e)}"
        )


@router.put(
    path="/{tracker_id}",
    summary="Update tracker",
    description="Updates an existing tracker",
    response_model=TrackerResponse
)
async def update_tracker(tracker_id: int, tracker: TrackerUpdate):
    try:
        tracker_service = TrackerService()
        updated_tracker = await tracker_service.update_tracker(tracker_id, tracker)

        if not updated_tracker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tracker with ID {tracker_id} not found"
            )

        return updated_tracker
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating tracker: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating tracker: {str(e)}"
        )


@router.delete(
    path="/{tracker_id}",
    summary="Delete tracker",
    description="Deletes a tracker by ID",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_tracker(tracker_id: int):
    try:
        tracker_service = TrackerService()
        await tracker_service.delete_tracker(tracker_id)
    except Exception as e:
        logging.error(f"Error deleting tracker: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting tracker: {str(e)}"
        )
