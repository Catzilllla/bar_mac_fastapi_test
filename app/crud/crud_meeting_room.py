# app/crud/crud_meeting_room.py
from typing import Optional
from sqlalchemy import select

from app.core.db_sqlite import AsyncSessionLocal
from app.schems.meeting_room_pydantic import MeetingRoomPydanticCreate
from app.models.meeting_room_orm import MeetRoomORM


async def create_meeting_room(
        new_room: MeetingRoomPydanticCreate
) -> MeetRoomORM:
    # конвертируем pydantic модель в словарь
    new_room_data = new_room.dict()

    # создаем объект ОРМ модели MeetingRoomORM
    # распаковываем словарь
    db_room = MeetRoomORM(**new_room_data)

    # создаем асинхронную сессию через контекстный менеджер
    async with AsyncSessionLocal() as session:
        # добавляе созданный объект в сессию
        # записываем изменения в БД
        # обновляем объект db_room: считываем из БД получаем id
        session.add(db_room)
        await session.commit()
        await session.refresh(db_room)

    return db_room

async def get_id_room_byname(room_name: str) -> Optional[int]:
    async with AsyncSessionLocal() as session:
        db_room_id = await session.execute(
            select(MeetRoomORM.id).where(MeetRoomORM.name == room_name)
        )
        db_room_id = db_room_id.scalars().first()
    return db_room_id

async def n_test(
        new_room: MeetingRoomPydanticCreate
) -> MeetRoomORM:
    tbuffer = new_room.dict()
    # print(new_room)
    # print(tbuffer)
    db_test = MeetRoomORM(**tbuffer)
    # print(db_test)

    async with AsyncSessionLocal() as open_session:
        open_session.add(db_test)
        await open_session.commit()
        await open_session.refresh(db_test)
    return db_test
