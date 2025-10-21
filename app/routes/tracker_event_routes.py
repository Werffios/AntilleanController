import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Query, Depends

from app.security.jwt_utils import get_current_user

from app.services.tracker_event_service import TrackerEventService
from app.models.tracker_event_models import TrackerEventResponse


router = APIRouter(
    prefix="/tracker-events",
    tags=["Tracker Events"],
    dependencies=[Depends(get_current_user)]
)


@router.get(
    path="",
    summary="Get all tracker events",
    description="Retrieves a paginated list of all tracker events from MongoDB",
    response_model=List[TrackerEventResponse]
)
async def get_all_tracker_events(
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip")
):
    try:
        tracker_event_service = TrackerEventService()
        events = await tracker_event_service.get_all_tracker_events(limit, offset)
        return events
    except Exception as e:
        logging.error(f"Error retrieving tracker events: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tracker events: {str(e)}"
        )


@router.get(
    path="/tracker/{tracker_id}",
    summary="Get tracker events by TrackerId",
    description="Retrieves all tracker events for a specific TrackerId, sorted by EventTime (most recent first)",
    response_model=List[TrackerEventResponse]
)
async def get_tracker_events_by_tracker_id(
    tracker_id: str,
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip")
):
    try:
        tracker_event_service = TrackerEventService()
        events = await tracker_event_service.get_tracker_events_by_tracker_id(tracker_id, limit, offset)

        if not events:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No events found for TrackerId: {tracker_id}"
            )

        return events
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving tracker events by tracker_id: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tracker events: {str(e)}"
        )

@router.get(
    path="/tracker/{tracker_id}/date-range",
    summary="Get tracker events by TrackerId and date range",
    description="Retrieves tracker events for a specific TrackerId within a date range, sorted by EventTime (most recent first)",
    response_model=List[TrackerEventResponse]
)
async def get_tracker_events_by_date_range(
    tracker_id: str,
    start_date: str = Query(None, description="Start date in YYYY-MM-DD format (defaults to today)"),
    end_date: str = Query(None, description="End date in YYYY-MM-DD format (defaults to today)"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip")
):
    try:
        tracker_event_service = TrackerEventService()
        events = await tracker_event_service.get_tracker_events_by_date_range(
            tracker_id, start_date, end_date, limit, offset
        )
        if not events:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No events found for TrackerId: {tracker_id} in the specified date range"
            )
        return events
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving tracker events by date range: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tracker events: {str(e)}"
        )

@router.get(
    path="/event/{event_id}",
    summary="Get tracker event by ID",
    description="Retrieves a specific tracker event by its MongoDB _id",
    response_model=TrackerEventResponse
)
async def get_tracker_event_by_id(event_id: str):
    try:
        tracker_event_service = TrackerEventService()
        event = await tracker_event_service.get_tracker_event_by_id(event_id)

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tracker event with ID {event_id} not found"
            )

        return event
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving tracker event: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tracker event: {str(e)}"
        )


@router.get(
    path="/count/all",
    summary="Count all tracker events",
    description="Returns the total count of tracker events in the database"
)
async def count_all_tracker_events():
    try:
        tracker_event_service = TrackerEventService()
        count = await tracker_event_service.count_tracker_events()
        return {"total_events": count}
    except Exception as e:
        logging.error(f"Error counting tracker events: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error counting tracker events: {str(e)}"
        )


@router.get(
    path="/count/tracker/{tracker_id}",
    summary="Count tracker events by TrackerId",
    description="Returns the count of tracker events for a specific TrackerId"
)
async def count_tracker_events_by_tracker_id(tracker_id: str):
    try:
        tracker_event_service = TrackerEventService()
        count = await tracker_event_service.count_tracker_events_by_tracker_id(tracker_id)
        return {
            "tracker_id": tracker_id,
            "event_count": count
        }
    except Exception as e:
        logging.error(f"Error counting tracker events: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error counting tracker events: {str(e)}"
        )
