import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Query

from app.services.shipment_item_service import ShipmentItemService
from app.models.shipment_item_models import ShipmentItemCreate, ShipmentItemUpdate, ShipmentItemResponse


router = APIRouter(
    prefix="/shipment-items",
    tags=["Shipment Items"]
)


@router.post(
    path="",
    summary="Create a new shipment item",
    description="Creates a new shipment item in the system",
    response_model=ShipmentItemResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_shipment_item(item: ShipmentItemCreate):
    try:
        item_service = ShipmentItemService()
        return await item_service.create_shipment_item(item)
    except Exception as e:
        logging.error(f"Error creating shipment item: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating shipment item: {str(e)}"
        )


@router.get(
    path="/{item_id}",
    summary="Get shipment item by ID",
    description="Retrieves a shipment item by its ID",
    response_model=ShipmentItemResponse
)
async def get_shipment_item(item_id: int):
    try:
        item_service = ShipmentItemService()
        item = await item_service.get_shipment_item_by_id(item_id)

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shipment item with ID {item_id} not found"
            )

        return item
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving shipment item: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving shipment item: {str(e)}"
        )


@router.get(
    path="/shipment/{shipment_id}",
    summary="Get shipment items by shipment",
    description="Retrieves all items for a specific shipment",
    response_model=List[ShipmentItemResponse]
)
async def get_shipment_items_by_shipment(shipment_id: int):
    try:
        item_service = ShipmentItemService()
        return await item_service.get_shipment_items_by_shipment(shipment_id)
    except Exception as e:
        logging.error(f"Error retrieving shipment items: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving shipment items: {str(e)}"
        )


@router.get(
    path="/asset/{asset_id}",
    summary="Get shipment items by asset",
    description="Retrieves all shipment items for a specific asset",
    response_model=List[ShipmentItemResponse]
)
async def get_shipment_items_by_asset(asset_id: int):
    try:
        item_service = ShipmentItemService()
        return await item_service.get_shipment_items_by_asset(asset_id)
    except Exception as e:
        logging.error(f"Error retrieving shipment items: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving shipment items: {str(e)}"
        )


@router.get(
    path="",
    summary="Get all shipment items",
    description="Retrieves all shipment items with pagination",
    response_model=List[ShipmentItemResponse]
)
async def get_all_shipment_items(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0)
):
    try:
        item_service = ShipmentItemService()
        return await item_service.get_all_shipment_items(limit, offset)
    except Exception as e:
        logging.error(f"Error retrieving shipment items: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving shipment items: {str(e)}"
        )


@router.put(
    path="/{item_id}",
    summary="Update shipment item",
    description="Updates an existing shipment item",
    response_model=ShipmentItemResponse
)
async def update_shipment_item(item_id: int, item: ShipmentItemUpdate):
    try:
        item_service = ShipmentItemService()
        updated_item = await item_service.update_shipment_item(item_id, item)

        if not updated_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shipment item with ID {item_id} not found"
            )

        return updated_item
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating shipment item: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating shipment item: {str(e)}"
        )


@router.delete(
    path="/{item_id}",
    summary="Delete shipment item",
    description="Deletes a shipment item by ID",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_shipment_item(item_id: int):
    try:
        item_service = ShipmentItemService()
        await item_service.delete_shipment_item(item_id)
    except Exception as e:
        logging.error(f"Error deleting shipment item: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting shipment item: {str(e)}"
        )
