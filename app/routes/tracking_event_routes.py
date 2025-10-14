import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Query

from app.services.tracking_event_service import TrackingEventService
from app.models.tracking_event_models import TrackingEventCreate, TrackingEventUpdate, TrackingEventResponse


router = APIRouter(
    prefix="/tracking-events",
    tags=["Tracking Events"]
)


@router.post(
    path="",
    summary="Create a new tracking event",
    description="Creates a new tracking event in the system",
    response_model=TrackingEventResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_tracking_event(tracking_event: TrackingEventCreate):
    try:
        tracking_event_service = TrackingEventService()
        return await tracking_event_service.create_tracking_event(tracking_event)
    except Exception as e:
        logging.error(f"Error creating tracking event: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating tracking event: {str(e)}"
        )


@router.get(
    path="/{tracking_event_id}",
    summary="Get tracking event by ID",
    description="Retrieves a tracking event by its ID",
    response_model=TrackingEventResponse
)
async def get_tracking_event(tracking_event_id: int):
    try:
        tracking_event_service = TrackingEventService()
        tracking_event = await tracking_event_service.get_tracking_event_by_id(tracking_event_id)

        if not tracking_event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tracking event with ID {tracking_event_id} not found"
            )

        return tracking_event
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving tracking event: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tracking event: {str(e)}"
        )


@router.get(
    path="/shipment/{shipment_id}",
    summary="Get tracking events by shipment",
    description="Retrieves all tracking events for a specific shipment",
    response_model=List[TrackingEventResponse]
)
async def get_tracking_events_by_shipment(shipment_id: int):
    try:
        tracking_event_service = TrackingEventService()
        return await tracking_event_service.get_tracking_events_by_shipment(shipment_id)
    except Exception as e:
        logging.error(f"Error retrieving tracking events: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tracking events: {str(e)}"
        )


@router.get(
    path="",
    summary="Get all tracking events",
    description="Retrieves all tracking events with pagination",
    response_model=List[TrackingEventResponse]
)
async def get_all_tracking_events(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0)
):
    try:
        tracking_event_service = TrackingEventService()
        return await tracking_event_service.get_all_tracking_events(limit, offset)
    except Exception as e:
        logging.error(f"Error retrieving tracking events: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tracking events: {str(e)}"
        )


@router.put(
    path="/{tracking_event_id}",
    summary="Update tracking event",
    description="Updates an existing tracking event",
    response_model=TrackingEventResponse
)
async def update_tracking_event(tracking_event_id: int, tracking_event: TrackingEventUpdate):
    try:
        tracking_event_service = TrackingEventService()
        updated_event = await tracking_event_service.update_tracking_event(tracking_event_id, tracking_event)

        if not updated_event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tracking event with ID {tracking_event_id} not found"
            )

        return updated_event
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating tracking event: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating tracking event: {str(e)}"
        )


@router.delete(
    path="/{tracking_event_id}",
    summary="Delete tracking event",
    description="Deletes a tracking event by ID",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_tracking_event(tracking_event_id: int):
    try:
        tracking_event_service = TrackingEventService()
        await tracking_event_service.delete_tracking_event(tracking_event_id)
    except Exception as e:
        logging.error(f"Error deleting tracking event: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting tracking event: {str(e)}"
        )
