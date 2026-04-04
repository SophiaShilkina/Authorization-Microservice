from fastapi import APIRouter
from .v1 import auth

api_v1_router = APIRouter(tags=['API v1'], prefix='/api/v1')

api_v1_router.include_router(auth.router, tags=['Auth'], prefix='/auth')

current_router = api_v1_router
