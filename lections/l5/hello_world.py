from fastapi import FastAPI
# pip install fastapi uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# for data validation you can use
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


# methods must be async
@app.get("/")
async def root():
    logger.info("get request found")
    return {"message": "Hello World"}


@app.post("/items/")
# add item
# get http://127.0.0.1:8000/items/ -> http 405 {"detail":"Method Not Allowed"}
# $ curl -X POST 127.0.0.1:8000/items/ -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"name": "BestSale", "description": "The best of the best", "price": 9.99, "tax": 0.99}'
#   ->{"name":"BestSale","description":"The best of the best","price":9.99,"tax":0.99}
# -H 'accept: application/json' is optional
async def create_item(item: Item):
    logger.info("post request found")
    return item


@app.put("/items/{item_id}")
# change item
# $ curl -X PUT 127.0.0.1:8000/items/42 -H 'Content-Type: application/json' -d '{"name": "new name", "description": "new dsc", "price": 7.99, "tax": 10.01}'
#   -> {"item_id":42,"item":{"name":"new name","description":"new dsc","price":7.99,"tax":10.01}}
# $ curl -X PUT 127.0.0.1:8000/items/42 -H 'Content-Type: application/json' -d '{"name": "new name", "price": 7.99}'
#   -> {"item_id":42,"item":{"name":"new name","description":null,"price":7.99,"tax":null}}
#   watch Item(BaseModel) Optional fields
# $ curl -X PUT 127.0.0.1:8000/items/42 -H 'Content-Type: application/json' -d '{"name": "new name", "tax": 7.99}'
#   -> http 422 {"detail":[{"type":"missing","loc":["body","price"],"msg":"Field required","input":{"name":"new name","tax":7.99},"url":"https://errors.pydantic.dev/2.5/v/missing"}]}
#   struct error description
async def update_item(item_id: int, item: Item):
    logger.info("put request found")
    return {"item_id": item_id, "item": item}


@app.delete("/items/{item_id}")
# delete item
# $ curl -X DELETE 127.0.0.1:8000/items/42 -> {"item_id":42}
async def delete_item(item_id: int):
    logger.info("delete request found")
    return {"item_id": item_id}


@app.get("/items/{item_id}")
# http://127.0.0.1:8000/items/5 -> {"item_id":5,"q":null}
# http://127.0.0.1:8000/items/5?q=abc -> {"item_id":5,"q":"abc"}
# parameter types set in method, not in route
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# use $ uvicorn hello_world:app to run server
# or $ uvicorn lections.l5.hello_world:app to run from parent directory
# :app should match variable in code
# add --reload for dynamic code update
