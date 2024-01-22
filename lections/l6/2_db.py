# pip install databases sqlalchemy aiosqlite
from typing import List
import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field

DATABASE_URL = "sqlite:///my_database.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# tables description
users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
)

engine = sqlalchemy.create_engine(DATABASE_URL,
                                  # connector params
                                  connect_args={"check_same_thread": False})
# create tables structure
metadata.create_all(engine)


# models description
class UserIn(BaseModel):
    name: str = Field(max_length=32)
    email: str = Field(max_length=128)
class User(BaseModel):
    id: int
    name: str = Field(max_length=32)
    email: str = Field(max_length=128)


app = FastAPI()


# fire on event:
@app.on_event("startup")
async def startup():
    # just connect, not create structure
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# response_model describes returning object
@app.get('/create_users/{count}', response_model=List[User])
async def create_users(count: int):
    for i in range(count):
        query = users.insert().values(name=f'user{i}', email=f'mail{i}@mail.ru')
        await database.execute(query)
    return {"message": f'{count} users created'}

# response_model describes returning object
@app.post('/users/', response_model=User)
async def create_user(user: UserIn):
    # query = users.insert().values(name=user.name, email=user.email)
    query = users.insert().values(**user.dict())  # SIC deprecated method
    last_record_id = await database.execute(query)  # why i got id here?
    return {**user.dict(), "id": last_record_id}

@app.get('/users/', response_model=List[User])
async def get_users():
    query = users.select()
    return await database.fetch_all(query)

@app.get('/users/{user_id}', response_model=User)
async def get_user(user_id: int):
    query = users.select().where(users.c.id == user_id)  # 'c' is alias to 'columns' ?
    # query = users.select().where(users.columns.id == user_id)
    return await database.fetch_one(query)

@app.put('/users/{user_id}', response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}

@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {"message": "User deleted"}
