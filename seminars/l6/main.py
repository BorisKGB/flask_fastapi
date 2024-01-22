"""
Задание пред семинара, но реализовать БД

Задание №3
📌 Создать API для добавления нового пользователя в базу данных. Приложение
должно иметь возможность принимать POST запросы с данными нового
пользователя и сохранять их в базу данных.
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

import databases
import sqlalchemy
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import List
from hashlib import sha256
import pandas as pd


DATABASE_URL = "sqlite:///my_database.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(64)),
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)


class UserIn(BaseModel):
    name: str = Field(..., max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(..., min_length=5, max_length=64)


class User(BaseModel):
    id: int
    name: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(min_length=5, max_length=64)


app = FastAPI()
templates = Jinja2Templates(directory="./templates")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/", response_model=List[User])
async def list_users():
    return await database.fetch_all(users.select())


@app.get("/{user_id}", response_model=User)
async def list_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.get("/users/", response_class=HTMLResponse)
async def fancy_list_users():
    all_users = await database.fetch_all(users.select())
    # data = pd.DataFrame([user for user in all_users])
    data = pd.DataFrame(all_users)
    return data.to_html()


@app.post('/users/', response_model=User)
async def create_user(user: UserIn):
    hex_password = sha256(user.password.encode("utf-8")).hexdigest()
    query = users.insert().values(
        name=user.name, email=user.email,
        password=hex_password)
    last_record_id = await database.execute(query)
    return User(name=user.name, email=user.email,
                password=hex_password, id=last_record_id)  # is it correct?


@app.put('/users/{user_id}', response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    hex_password = sha256(new_user.password.encode("utf-8")).hexdigest()
    query = users.update().where(users.c.id == user_id).values(name=new_user.name, email=new_user.email,
                                                               password=hex_password)
    await database.execute(query)
    return {"name": new_user.name, "email": new_user.email,
            "password": hex_password, "id": user_id}  # is it correct?


@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {"message": "User deleted"}


@app.get("/users_html/", response_class=HTMLResponse)
async def users_html(request: Request):
    all_users = await database.fetch_all(users.select())
    data = pd.DataFrame(all_users)
    return templates.TemplateResponse("users.html",
                                      {"request": request,
                                       "usersTable": data.to_html()})
