from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(
        # same validators as in models
        item_id: int = Path(..., ge=1)):
    return {"item_id": item_id}


@app.get("/items/_{item_id}")
async def read_item2(item_id: int = Path(..., title="The ID", ge=1), q: str = None):
    return {"item_id": item_id}


@app.get("/items/")
#  query manage/validate parameters from requests
#  on invalid request get 422
async def read_items(q: str = Query(None, min_length=3, max_length=50)):
    results = {}
    if q:
        results = {"q": q}
    return results

# for more Field, Query, Path info read Pydantic.Param doc
