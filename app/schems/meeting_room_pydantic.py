from typing import Optional
from pydantic import BaseModel, Field


class MeetingRoomPydanticBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]

# class MeetingRoomCreatePydantic(BaseModel):
#     name: str = Field(max_length=100, nullable=False)
#     description: Optional[str]


class MeetingRoomPydanticCreate(MeetingRoomPydanticBase):
    #преобразуем атрибут name - делаем его обязательным
    name: str = Field(..., min_length=1, max_length=100)
    # descxription уже есть в ьбазовом классе

# модель для response_model=
class MeetingRoomFromDB(MeetingRoomPydanticCreate):
    id: int

    class Config:
        orm_mode = True

