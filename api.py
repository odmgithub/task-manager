from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response

from models import TaskCreate, TaskUpdate, TasksResponse, Task
from services import (
    get_tasks_service,
    add_task_service,
    toggle_task_service,
    update_task_service,
    delete_task_service,
)
from ui import get_ui_html

app = FastAPI()


@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)


@app.get("/", response_class=HTMLResponse)
def ui():
    return get_ui_html()


from models import TasksResponse, Task   # ← якщо ще немає імпорту

@app.get("/tasks", response_model=TasksResponse)
def get_tasks():
    tasks = get_tasks_service()
    return {"tasks": tasks}


@app.post("/tasks", response_model=dict)
def add_task(payload: TaskCreate):
    try:
        t = add_task_service(payload.text)
        return {"task": t}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/tasks/{task_id}/toggle", response_model=dict)
def toggle_task(task_id: int):
    try:
        t = toggle_task_service(task_id)
        return {"task": t}
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")


@app.patch("/tasks/{task_id}", response_model=dict)
def update_task(task_id: int, payload: TaskUpdate):
    try:
        t = update_task_service(task_id, payload.text)
        return {"task": t}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int):
    try:
        delete_task_service(task_id)
        return {"ok": True}
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")