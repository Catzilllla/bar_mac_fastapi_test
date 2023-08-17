# schemas.py
# все модели здесь и валидация


    # • модель, описывающая переговорки;
    # • модель, описывающая бронирование (какая переговорка забронирована, кем и на какой период времени);
    # • модель пользователей (с разделением ролей на обычных пользователей и админов системы).

import re
from enum import Enum
from typing import Optional, Union

# Для работы с JSON в теле запроса 
# импортируем из pydantic класс BaseModel
from pydantic import BaseModel, Field, validator, root_validator

password_regex = "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"


class EducationLevel(str, Enum):
    SECONDARY = 'Среднее образование'
    SPECIAL = 'Среднее специальное образование'
    HIGHER = 'Высшее образование'


class Person(BaseModel):
    name: str = Field(
        max_length=20, 
        description='Описание имени вводить в любом регистре',
        title='Полное имя'
    )
    surname: Union[str, list[str]] = Field(..., max_length=50)
    age: Optional[int] = Field(None, gt=4, le=99)
    is_staff: bool = Field(False, alias='is-staff')
    education_level: Optional[EducationLevel]
    password: str = Field(..., regex=password_regex)

    class Config:
        title = 'установит в документации кастомное название для класса Person'
        # ограничит длину всех строковых данных в классе Person
        min_anystr_lenght = 2
        schema_extra = {
           'example': {
               'name': 'Eduardo',
               'surname': ['Santos', 'Tavares'],
               'age': 20,
               'is_staff': False,
               'education_level': 'Среднее образование',
               'password': password_regex
           }
        }

    # # В качестве аргумента валидатору передается имя поля, 
    # # которое нужно проверить.
    # @validator('name')
    # # Первый параметр функции-валидатора должен называться строго cls.
    # # Вторым параметром идет проверяемое значение, его можно назвать как угодно.
    # # Декоратор @classmethod ставить нельзя, иначе валидатор не сработает. 
    # def name_cant_be_numeric(cls, value: str):
    #     # Проверяем, не состоит ли строка исключительно из цифр:
    #     if value.isnumeric():
    #         # При ошибке валидации можно выбросить
    #         # ValueError, TypeError или AssertionError.
    #         # В нашем случае подходит ValueError.
    #         # В аргумент передаём сообщение об ошибке.
    #         raise ValueError('Имя не может быть числом')
    #     # Если проверка пройдена, возвращаем значение поля.
    #     return value
    
    # @validator('surname')
    # def surname_cant_be_numeric(cls, value: str):
    #     if value.isnumeric():
    #         raise ValueError('Фамилия не может быть числом')
    #     return value

    @validator('password')
    def password_regex(cls, password: str):
        l, u, p, d = 0, 0, 0, 0
        capitalalphabets="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        smallalphabets="abcdefghijklmnopqrstuvwxyz"
        specialchar=""" ~`!@#$%^&*()_-+={[}]|\:;"'<,>.?/ """
        digits="0123456789"
        if (len(password) >= 8):
            for i in password:
    
                # counting lowercase alphabets
                if (i in smallalphabets):
                    l+=1           
    
                # counting uppercase alphabets
                if (i in capitalalphabets):
                    u+=1           
    
                # counting digits
                if (i in digits):
                    d+=1           
    
                # counting the mentioned special characters
                if(i in specialchar):
                    p+=1       
        if (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(password)):
            return password
        else:
            return ValueError('Пароль не соотвестует требованиям')
    
    # после всех одиночных валидаторов выполняется root_validator
    # kip_on_failure=True: «не выполнять проверку в случае ошибок в предшествующих валидаторах».
    @root_validator(skip_on_failure=True)
    # К названию параметров функции-валидатора нет строгих требований.
    # Первым передается класс, вторым — словарь со значениями всех полей.
    def using_different_languages(cls, values):
        # Объединяем все фамилии в единую строку. 
        # Даже если values['surname'] — это строка, ошибки не будет, 
        # просто все буквы заново объединятся в строку.
        surname = ''.join(values['surname'])
        # Объединяем имя и фамилию в единую строку.
        checked_value = values['name'] + surname
        # Ищем хотя бы одну кириллическую букву в строке
        # и хотя бы одну латинскую букву.
        # Флаг re.IGNORECASE указывает на то, что регистр не важен.
        if (re.search('[а-я]', checked_value, re.IGNORECASE)
                and re.search('[a-z]', checked_value, re.IGNORECASE)):
            raise ValueError(
                'Пожалуйста, не смешивайте русские и латинские буквы'
            )
        # Если проверка пройдена, возвращается словарь со всеми значениями.
        return values 