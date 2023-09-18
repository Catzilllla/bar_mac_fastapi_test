# app/main.py

from fastapi import FastAPI
from app.api.api_meeting_room_create import router
from app.core.config import settings


app = FastAPI(title=settings.app_title, description=settings.description)

app.include_router(router)
