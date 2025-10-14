import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Query
from app.services.user_service import UserService
from app.models.user_models import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    try:
        user_service = UserService()
        return await user_service.create_user(user)
    except Exception as e:
        logging.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    try:
        user_service = UserService()
        user = await user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Todo: Aquí irían los endpoints para GET (all), PUT y DELETE, siguiendo el patrón de las otras rutas.