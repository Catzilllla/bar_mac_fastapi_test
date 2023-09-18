# здесь происходит магия
# при миграции модели MeetRoom alembic каким-то образом цепляет метаданные
# для базовой модели Base.
# Это необходимо для правильной работы с миграциями

""" Импорты класса Base и всех моделей для Alembic """
from app.core.db_sqlite import Base
from app.models.meeting_room_orm import MeetRoomORM

