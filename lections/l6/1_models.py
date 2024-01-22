from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None  # default value


class User(BaseModel):
    username: str
    full_name: str = None


class Order(BaseModel):
    items: List[Item]
    user: User


class Item2(BaseModel):
    name: str = Field(max_length=10)  # field validators


class User2(BaseModel):
    age: int = Field(default=0)


# for Field options (read doc), some of:
#  alias: str | None = _Unset,
#  gt: float | None = _Unset,
#  ge: float | None = _Unset,
#  lt: float | None = _Unset,
#  le: float | None = _Unset,
#  multiple_of: float | None = _Unset,
#  max_digits: int | None = _Unset,
#  min_length: int | None = _Unset,
#  max_length: int | None = _Unset,

class Item3(BaseModel):
    # ... -> required field
    name: str = Field(..., title="Name", max_length=50)
    price: float = Field(..., title="Price", gt=0, le=100_000)
    description: str = Field(default=None, title="Description", max_length=1000)
    tax: float = Field(0, title="Tax", ge=0, le=10)


class User3(BaseModel):
    username: str = Field(title="Username", max_length=50)
    full_name: str = Field(None, title="Full Name", max_length=100)


###

@app.post("/items/")
async def create_item(item: Item3):
    # on incorrect Item3 values return 422 Unprocessable Entity
    return {"item": item}

