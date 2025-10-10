import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Query

from app.services.route_service import RouteService
from app.models.route_models import RouteCreate, RouteUpdate, RouteResponse


router = APIRouter(
    prefix="/routes",
    tags=["Routes"]
)


@router.post(
    path="",
    summary="Create a new route",
    description="Creates a new route in the system",
    response_model=RouteResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_route(route: RouteCreate):
    try:
        route_service = RouteService()
        return await route_service.create_route(route)
    except Exception as e:
        logging.error(f"Error creating route: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating route: {str(e)}"
        )


@router.get(
    path="/{route_id}",
    summary="Get route by ID",
    description="Retrieves a route by its ID",
    response_model=RouteResponse
)
async def get_route(route_id: int):
    try:
        route_service = RouteService()
        route = await route_service.get_route_by_id(route_id)

        if not route:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Route with ID {route_id} not found"
            )

        return route
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving route: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving route: {str(e)}"
        )


@router.get(
    path="",
    summary="Get all routes",
    description="Retrieves a paginated list of routes",
    response_model=List[RouteResponse]
)
async def get_all_routes(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    try:
        route_service = RouteService()
        return await route_service.get_all_routes(limit, offset)
    except Exception as e:
        logging.error(f"Error retrieving routes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving routes: {str(e)}"
        )


@router.put(
    path="/{route_id}",
    summary="Update route",
    description="Updates an existing route",
    response_model=RouteResponse
)
async def update_route(route_id: int, route: RouteUpdate):
    try:
        route_service = RouteService()
        updated_route = await route_service.update_route(route_id, route)

        if not updated_route:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Route with ID {route_id} not found"
            )

        return updated_route
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating route: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating route: {str(e)}"
        )


@router.delete(
    path="/{route_id}",
    summary="Delete route",
    description="Deletes a route from the system",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_route(route_id: int):
    try:
        route_service = RouteService()
        await route_service.delete_route(route_id)
        return None
    except Exception as e:
        logging.error(f"Error deleting route: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting route: {str(e)}"
        )

