from fastapi import APIRouter

from app.api.routes import problems

api_router = APIRouter()
api_router.include_router(problems.router)
