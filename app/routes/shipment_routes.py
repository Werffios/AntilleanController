import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Query

from app.services.shipment_service import ShipmentService
from app.models.shipment_models import ShipmentCreate, ShipmentUpdate, ShipmentResponse


router = APIRouter(
    prefix="/shipments",
    tags=["Shipments"]
)


@router.post(
    path="",
    summary="Create a new shipment",
    description="Creates a new shipment in the system",
    response_model=ShipmentResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_shipment(shipment: ShipmentCreate):
    try:
        shipment_service = ShipmentService()
        return await shipment_service.create_shipment(shipment)
    except Exception as e:
        logging.error(f"Error creating shipment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating shipment: {str(e)}"
        )


@router.get(
    path="/{shipment_id}",
    summary="Get shipment by ID",
    description="Retrieves a shipment by its ID",
    response_model=ShipmentResponse
)
async def get_shipment(shipment_id: int):
    try:
        shipment_service = ShipmentService()
        shipment = await shipment_service.get_shipment_by_id(shipment_id)

        if not shipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shipment with ID {shipment_id} not found"
            )

        return shipment
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving shipment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving shipment: {str(e)}"
        )


@router.get(
    path="/tracking/{tracking_code}",
    summary="Get shipment by tracking code",
    description="Retrieves a shipment by its tracking code",
    response_model=ShipmentResponse
)
async def get_shipment_by_tracking(tracking_code: str):
    try:
        shipment_service = ShipmentService()
        shipment = await shipment_service.get_shipment_by_tracking_code(tracking_code)

        if not shipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shipment with tracking code {tracking_code} not found"
            )

        return shipment
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving shipment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving shipment: {str(e)}"
        )


@router.get(
    path="/customer/{customer_id}",
    summary="Get shipments by customer",
    description="Retrieves all shipments for a specific customer",
    response_model=List[ShipmentResponse]
)
async def get_shipments_by_customer(customer_id: int):
    try:
        shipment_service = ShipmentService()
        return await shipment_service.get_shipments_by_customer(customer_id)
    except Exception as e:
        logging.error(f"Error retrieving shipments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving shipments: {str(e)}"
        )


@router.get(
    path="",
    summary="Get all shipments",
    description="Retrieves a paginated list of shipments",
    response_model=List[ShipmentResponse]
)
async def get_all_shipments(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    try:
        shipment_service = ShipmentService()
        return await shipment_service.get_all_shipments(limit, offset)
    except Exception as e:
        logging.error(f"Error retrieving shipments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving shipments: {str(e)}"
        )


@router.put(
    path="/{shipment_id}",
    summary="Update shipment",
    description="Updates an existing shipment",
    response_model=ShipmentResponse
)
async def update_shipment(shipment_id: int, shipment: ShipmentUpdate):
    try:
        shipment_service = ShipmentService()
        updated_shipment = await shipment_service.update_shipment(shipment_id, shipment)

        if not updated_shipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shipment with ID {shipment_id} not found"
            )

        return updated_shipment
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating shipment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating shipment: {str(e)}"
        )


@router.delete(
    path="/{shipment_id}",
    summary="Delete shipment",
    description="Deletes a shipment from the system",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_shipment(shipment_id: int):
    try:
        shipment_service = ShipmentService()
        await shipment_service.delete_shipment(shipment_id)
        return None
    except Exception as e:
        logging.error(f"Error deleting shipment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting shipment: {str(e)}"
        )

