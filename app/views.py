from . import app

from fastapi import APIRouter




api_router = APIRouter(prefix="/antillean/api")







app.include_router(api_router)