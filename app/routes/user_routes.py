import logging
from fastapi import APIRouter, HTTPException, status, Depends
from app.services.user_service import UserService
from app.models.user_models import UserCreate, UserResponse
from app.security.jwt_utils import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get(
    path="/me",
    response_model=UserResponse
)
async def get_me(
        current_user: UserResponse = Depends(get_current_user)
):
    return current_user

# Todo: Aquí irían los endpoints para GET (all), PUT y DELETE, siguiendo el patrón de las otras rutas.