from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel


class Task(BaseModel):
    id: int
    header: str
    description: str
    done: bool


app = FastAPI()
db = list()


@app.get("/tasks/", response_model=List[Task])
async def get_tasks():
    return db


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    for i in range(len(db)):
        if db[i].id == task_id:
            return db[i]
    raise HTTPException(status_code=404, detail=f'Task with id {task_id} not found')


@app.post("/tasks/", response_model=Task)
async def add_user(task: Task):
    task.id = len(db) + 1
    db.append(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    task.id = task_id
    for i in range(len(db)):
        if db[i].id == task_id:
            db[i] = task
            return task
    raise HTTPException(status_code=404, detail=f'Task with id {task_id} not found')


@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    for i in range(len(db)):
        if db[i].id == task_id:
            task = db[i]
            db.pop(i)
            return task
    raise HTTPException(status_code=404, detail=f'Task with id {task_id} not found')
