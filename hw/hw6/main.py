from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import starlette.status as status
from models import User, Product, Order
from db import database, users, products, orders


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def main_page():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # reload=True not implemented ->
    # WARNING:  You must pass the application as an import string to enable 'reload' or 'workers'.
