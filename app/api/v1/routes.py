from fastapi import APIRouter

from app.api.v1 import bot
from . import candidates, jobs

api_router = APIRouter()
api_router.include_router(candidates.router)
api_router.include_router(bot.router)
api_router.include_router(jobs.router)
