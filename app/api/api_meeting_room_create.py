# app/api/api_meeting_room_create.py

from fastapi import APIRouter, HTTPException
from app.crud.crud_meeting_room import create_meeting_room, get_id_room_byname, n_test
from app.schems.meeting_room_pydantic import MeetingRoomPydanticCreate, MeetingRoomFromDB

router = APIRouter()


@router.post(
        '/meeting_room_create/',
        #указыыаем схему ответа
        response_model=MeetingRoomFromDB,
        response_model_exclude_none=True,
)
async def create_new_meeting_room(
    meeting_room: MeetingRoomPydanticCreate,
):
    room_id = await get_id_room_byname(meeting_room.name)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует',
        )

    new_room = await create_meeting_room(meeting_room)
    return new_room

# @router.post('/test/')
# async def test_room(input_test: MeetingRoomPydanticCreate):
#     buff_test = await n_test(input_test)
#     return buff_test
