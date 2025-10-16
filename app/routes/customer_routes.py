import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Query, Depends

from app.security.jwt_utils import get_current_user

from app.services.customer_service import CustomerService
from app.models.customer_models import CustomerCreate, CustomerUpdate, CustomerResponse


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    dependencies=[Depends(get_current_user)]
)


@router.post(
    path="",
    summary="Create a new customer",
    description="Creates a new customer in the system",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_customer(customer: CustomerCreate):
    try:
        customer_service = CustomerService()
        return await customer_service.create_customer(customer)
    except Exception as e:
        logging.error(f"Error creating customer: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating customer: {str(e)}"
        )


@router.get(
    path="/{customer_id}",
    summary="Get customer by ID",
    description="Retrieves a customer by their ID",
    response_model=CustomerResponse
)
async def get_customer(customer_id: int):
    try:
        customer_service = CustomerService()
        customer = await customer_service.get_customer_by_id(customer_id)

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with ID {customer_id} not found"
            )

        return customer
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving customer: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving customer: {str(e)}"
        )


@router.get(
    path="",
    summary="Get all customers",
    description="Retrieves a paginated list of customers",
    response_model=List[CustomerResponse]
)
async def get_all_customers(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    try:
        customer_service = CustomerService()
        return await customer_service.get_all_customers(limit, offset)
    except Exception as e:
        logging.error(f"Error retrieving customers: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving customers: {str(e)}"
        )


@router.put(
    path="/{customer_id}",
    summary="Update customer",
    description="Updates an existing customer",
    response_model=CustomerResponse
)
async def update_customer(customer_id: int, customer: CustomerUpdate):
    try:
        customer_service = CustomerService()
        updated_customer = await customer_service.update_customer(customer_id, customer)

        if not updated_customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with ID {customer_id} not found"
            )

        return updated_customer
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating customer: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating customer: {str(e)}"
        )


@router.delete(
    path="/{customer_id}",
    summary="Delete customer",
    description="Deletes a customer from the system",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_customer(customer_id: int):
    try:
        customer_service = CustomerService()
        await customer_service.delete_customer(customer_id)
        return None
    except Exception as e:
        logging.error(f"Error deleting customer: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting customer: {str(e)}"
        )

