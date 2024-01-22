from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="./templates")


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
# auto type validation
# $ curl 127.0.0.1:8000/items/abc
#   -> 422 {"detail":[{"type":"int_parsing","loc":["path","item_id"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"abc","url":"https://errors.pydantic.dev/2.5/v/int_parsing"}]}
# $ curl 127.0.0.1:8000/items/123?q=123
#   -> {"item_id":123,"q":"123"}
async def read_item(item_id: int, q: str = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.get("/items/{item_id}/orders/{order_id}")
async def read_data(item_id: int, order_id: int):
    # do something
    return {"item_id": item_id, "order_id": order_id}


@app.get("/items/")
# $ curl 127.0.0.1:8000/items/?limit=25
#   -> {"skip":0,"limit":25}
# $ curl "127.0.0.1:8000/items/?limit=25&skip=5"
#   -> {"skip":5,"limit":25}
async def skip_limit(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


@app.get("/html/", response_class=HTMLResponse)
# $ curl "127.0.0.1:8000/html/" -I ->"HEAD /html/ HTTP/1.1" 405 Method Not Allowed
# but classic get request works correctly
async def read_html():
    return "<h1>Hello World</h1>"


@app.get("/message")
async def read_message():
    message = {"message": "Hello world"}
    return JSONResponse(content=message, status_code=200)


@app.get("/{name}")
async def read_item(request: Request, name: str):
    print(request)
    return templates.TemplateResponse("item.html", {"request": request, "name": name})

# autodoc
# see localhost:8000/docs
# or localhost:8000/redoc

# can modify docs schemas
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="custom title",
        version="1.0.0",
        description="this is custom openapi schema",
        routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi