from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List
from pydantic import BaseModel
from hashlib import sha256
import pandas as pd

"""
Задание №3
📌 Создать API для добавления нового пользователя в базу данных. Приложение
должно иметь возможность принимать POST запросы с данными нового
пользователя и сохранять их в базу данных.
* вместо БД использовать внутренний словарь
📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
📌 Создайте класс User с полями id, name, email и password.
📌 Создайте список users для хранения пользователей.
📌 Создайте маршрут для добавления нового пользователя (метод POST).
📌 Реализуйте валидацию данных запроса и ответа.
Задание №4
Создайте маршрут для обновления информации о пользователе (метод PUT).
Задание №5
Создайте маршрут для удаления информации о пользователе (метод DELETE).
Задание №6
📌 Создать веб-страницу для отображения списка пользователей. Приложение
должно использовать шаблонизатор Jinja для динамического формирования HTML
страницы.
"""


class User(BaseModel):
    id: int
    name: str
    email: Optional[str]
    password: str


app = FastAPI()
templates = Jinja2Templates(directory="./templates")
db = list()


@app.get("/", response_model=List[User])
async def list_users():
    return db


@app.get("/users/", response_class=HTMLResponse)
async def fancy_list_users():
    # data = pd.DataFrame(db)
    data = pd.DataFrame([vars(user) for user in db])
    return data.to_html()


@app.post("/", response_model=User)
async def add_user(user: User):
    user.id = len(db) + 1
    user.password = sha256(user.password.encode("utf-8")).hexdigest()
    db.append(user)
    return user


@app.put("/{user_id}", response_model=User)
async def add_user(user_id: int, user: User):
    # if user_id-1 < len(db):
    user.id = user_id
    user.password = sha256(user.password.encode("utf-8")).hexdigest()
    db[user_id-1] = user
    return user


@app.delete("/{user_id}", response_model=User)
async def add_user(user_id: int, user: User):
    db.pop(user_id - 1)  # SIC change user_id afterward is incorrect because of possible relations to ID
    for user in db[user_id:]:
        user.id = user_id
        user_id += 1
    return user


@app.get("/users_html/", response_class=HTMLResponse)
async def users_html(request: Request):
    return templates.TemplateResponse("users.html",
                                      {"request": request,
                                       "usersTable": pd.DataFrame([vars(user) for user in db]).to_html()})
