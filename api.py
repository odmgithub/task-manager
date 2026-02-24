# api.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse, Response

from models import TaskCreate, TaskUpdate, TasksResponse
from deps import get_tasks_service
from services import TasksService
from ui import get_ui_html

app = FastAPI()


@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)


@app.get("/", response_class=HTMLResponse)
def ui():
    return get_ui_html()


@app.get("/tasks", response_model=TasksResponse)
def get_tasks(svc: TasksService = Depends(get_tasks_service)):
    return {"tasks": svc.list_tasks()}


@app.post("/tasks", response_model=dict)
def add_task(payload: TaskCreate, svc: TasksService = Depends(get_tasks_service)):
    try:
        t = svc.add_task(payload.text)
        return {"task": t}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/tasks/{task_id}/toggle", response_model=dict)
def toggle_task(task_id: int, svc: TasksService = Depends(get_tasks_service)):
    try:
        t = svc.toggle_task(task_id)
        return {"task": t}
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")


@app.patch("/tasks/{task_id}", response_model=dict)
def update_task(task_id: int, payload: TaskUpdate, svc: TasksService = Depends(get_tasks_service)):
    try:
        t = svc.update_task(task_id, payload.text)
        return {"task": t}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int, svc: TasksService = Depends(get_tasks_service)):
    try:
        svc.delete_task(task_id)
        return {"ok": True}
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")