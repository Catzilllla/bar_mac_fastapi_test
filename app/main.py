# main.py
from app.schems.schemas import Person
from app.core.config import settings
from fastapi import FastAPI, Form, UploadFile, File

app = FastAPI(title=settings.app_title, description=settings.description)


# Меняем метод GET на POST, указываем статичный адрес.
@app.post('/hello')
# Вместо множества параметра теперь будет только один - person, 
# в качестве аннотации указываем класс Person.
def greetings(person: Person) -> dict[str, str]:
    if isinstance(person.surname, list):
        surnames = ' '.join(person.surname)
    else:
        surnames = person.surname
    result = ' '.join([person.name, surnames])
    result = result.title()
    if person.age is not None:
        result += ', ' + str(person.age)
    if person.education_level is not None:
        result += ', ' + person.education_level.lower()
    if person.is_staff:
        result += ', сотрудник'
    return {'Hello': result}

@app.post('/login')
def login_form(
    username: str = Form(..., description='Описание username'),
    password: str = Form(..., description='Описание password'),
    somefile: UploadFile = File(...)
):
    file_content = somefile.file.read().splitlines()
    return {'username': username,
            'somefile': file_content
    }
