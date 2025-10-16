import logging
from fastapi import APIRouter, HTTPException, status
from app.models.auth_models import RegisterRequest, LoginRequest, AuthResponse
from app.security.jwt_utils import create_access_token
from app.services.user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(req: RegisterRequest):
    try:
        service = UserService()
        user = await service.register_from_encrypted(req)
        token = create_access_token(user.id)
        return AuthResponse(access_token=token, user=user)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error(f"Error en registro: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno")


@router.post("/login", response_model=AuthResponse)
async def login(req: LoginRequest):
    try:
        service = UserService()
        user = await service.authenticate_from_encrypted(req)
        if not user:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        token = create_access_token(user.id)
        return AuthResponse(access_token=token, user=user)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error en login: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno")
