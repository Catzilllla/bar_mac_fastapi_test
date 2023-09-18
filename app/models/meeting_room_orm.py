# app/models/meeting_room.py

from sqlalchemy import Column, String, Text
from app.core.db_sqlite import Base

class MeetRoomORM(Base):
    # имя должно быть уникальным и не пустым и <100 символов
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    #all_description = Column(Text)
