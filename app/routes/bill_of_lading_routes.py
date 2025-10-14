import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Query

from app.services.bill_of_lading_service import BillOfLadingService
from app.models.bill_of_lading_models import BillOfLadingCreate, BillOfLadingUpdate, BillOfLadingResponse


router = APIRouter(
    prefix="/bills-of-lading",
    tags=["Bills of Lading"]
)


@router.post(
    path="",
    summary="Create a new bill of lading",
    description="Creates a new bill of lading in the system",
    response_model=BillOfLadingResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_bill_of_lading(bill: BillOfLadingCreate):
    try:
        bill_service = BillOfLadingService()
        return await bill_service.create_bill_of_lading(bill)
    except Exception as e:
        logging.error(f"Error creating bill of lading: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating bill of lading: {str(e)}"
        )


@router.get(
    path="/{bill_id}",
    summary="Get bill of lading by ID",
    description="Retrieves a bill of lading by its ID",
    response_model=BillOfLadingResponse
)
async def get_bill_of_lading(bill_id: int):
    try:
        bill_service = BillOfLadingService()
        bill = await bill_service.get_bill_of_lading_by_id(bill_id)

        if not bill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bill of lading with ID {bill_id} not found"
            )

        return bill
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving bill of lading: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving bill of lading: {str(e)}"
        )


@router.get(
    path="/bol-number/{bol_number}",
    summary="Get bill of lading by BOL number",
    description="Retrieves a bill of lading by its BOL number",
    response_model=BillOfLadingResponse
)
async def get_bill_of_lading_by_number(bol_number: str):
    try:
        bill_service = BillOfLadingService()
        bill = await bill_service.get_bill_of_lading_by_bol_number(bol_number)

        if not bill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bill of lading with BOL number {bol_number} not found"
            )

        return bill
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving bill of lading: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving bill of lading: {str(e)}"
        )


@router.get(
    path="/shipment/{shipment_id}",
    summary="Get bill of lading by shipment",
    description="Retrieves a bill of lading for a specific shipment",
    response_model=BillOfLadingResponse
)
async def get_bill_of_lading_by_shipment(shipment_id: int):
    try:
        bill_service = BillOfLadingService()
        bill = await bill_service.get_bill_of_lading_by_shipment(shipment_id)

        if not bill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bill of lading for shipment {shipment_id} not found"
            )

        return bill
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving bill of lading: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving bill of lading: {str(e)}"
        )


@router.get(
    path="",
    summary="Get all bills of lading",
    description="Retrieves all bills of lading with pagination",
    response_model=List[BillOfLadingResponse]
)
async def get_all_bills_of_lading(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0)
):
    try:
        bill_service = BillOfLadingService()
        return await bill_service.get_all_bills_of_lading(limit, offset)
    except Exception as e:
        logging.error(f"Error retrieving bills of lading: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving bills of lading: {str(e)}"
        )


@router.put(
    path="/{bill_id}",
    summary="Update bill of lading",
    description="Updates an existing bill of lading",
    response_model=BillOfLadingResponse
)
async def update_bill_of_lading(bill_id: int, bill: BillOfLadingUpdate):
    try:
        bill_service = BillOfLadingService()
        updated_bill = await bill_service.update_bill_of_lading(bill_id, bill)

        if not updated_bill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bill of lading with ID {bill_id} not found"
            )

        return updated_bill
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating bill of lading: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating bill of lading: {str(e)}"
        )


@router.delete(
    path="/{bill_id}",
    summary="Delete bill of lading",
    description="Deletes a bill of lading by ID",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_bill_of_lading(bill_id: int):
    try:
        bill_service = BillOfLadingService()
        await bill_service.delete_bill_of_lading(bill_id)
    except Exception as e:
        logging.error(f"Error deleting bill of lading: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting bill of lading: {str(e)}"
        )
