# core/config.py
from pydantic import BaseSettings


# BaseSettings позволяет считывать переменные из окружения
class mySettings(BaseSettings):
    # app_author: str
    # db_url: str = 'postgres://login:password@127.0.0.1:5432/room_reservation'
    # path: str
    app_title: str = 'Внутренний title в классе'
    description: str
    db_sqlite_url: str
    #db_postgr_url: str

    class Config:
        env_file = '.env'


settings = mySettings()