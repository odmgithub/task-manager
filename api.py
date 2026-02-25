# api.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse, Response
from fastapi import Request
from fastapi.responses import JSONResponse

from models import TaskCreate, TaskUpdate, TasksResponse
from deps import get_tasks_service
from services import TasksService
from ui import get_ui_html

from exceptions import TaskNotFound, TaskTextEmpty, TaskError

# Створюємо FastAPI застосунок.
# Цей файл — "web layer": тут тільки HTTP маршрути та перетворення помилок у статус-коди.
app = FastAPI()


# -------------------------
# Global exception handlers
# -------------------------

@app.exception_handler(TaskTextEmpty)
def handle_task_text_empty(request: Request, exc: TaskTextEmpty):
    # 400 — клієнт надіслав невалідні дані
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(TaskNotFound)
def handle_task_not_found(request: Request, exc: TaskNotFound):
    # 404 — ресурс не знайдено
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(TaskError)
def handle_task_error(request: Request, exc: TaskError):
    # 500 — наша доменна помилка, яку не віднесли до 400/404 (запасний варіант)
    return JSONResponse(status_code=500, content={"detail": str(exc)})


@app.get("/favicon.ico")
def favicon():
    """
    Маленький "хак": браузери часто запитують favicon.ico.
    Щоб не засмічувати логи 404 — відповідаємо 204 No Content.
    """
    return Response(status_code=204)


@app.get("/", response_class=HTMLResponse)
def ui():
    """
    Головна сторінка UI.

    Важливо: ми не використовуємо шаблонізатор.
    UI — це просто HTML-рядок (get_ui_html), який повертає бекенд.
    """
    return get_ui_html()


@app.get("/tasks", response_model=TasksResponse)
def get_tasks(svc: TasksService = Depends(get_tasks_service)):
    """
    Отримати список задач.

    svc приходить через DI (Depends):
    FastAPI сам створить JsonTasksRepo -> TasksService.
    """
    return {"tasks": svc.list_tasks()}


@app.post("/tasks", response_model=dict)
def add_task(payload: TaskCreate, svc: TasksService = Depends(get_tasks_service)):
    
    """
    Створити нову задачу.

    TaskCreate валідуюється Pydantic’ом.
    Якщо text порожній — service кидає ValueError -> мапимо на 400.
    """
    # Без try/except: якщо буде TaskTextEmpty — хендлер сам зробить 400
    t = svc.add_task(payload.text)
    return {"task": t}


@app.post("/tasks/{task_id}/toggle", response_model=dict)
def toggle_task(task_id: int, svc: TasksService = Depends(get_tasks_service)):
    """
    Перемкнути done/not done.

    Якщо задача не знайдена — service кидає KeyError -> мапимо на 404.
    """
    t = svc.toggle_task(task_id)
    return {"task": t}


@app.patch("/tasks/{task_id}", response_model=dict)
def update_task(task_id: int, payload: TaskUpdate, svc: TasksService = Depends(get_tasks_service)):
    """
    Оновити текст задачі.
    - ValueError => 400 (невалідний текст)
    - KeyError => 404 (id не знайдено)
    """
    t = svc.update_task(task_id, payload.text)
    return {"task": t}


@app.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int, svc: TasksService = Depends(get_tasks_service)):
    """
    Видалити задачу.
    Якщо id не знайдено -> 404.
    """
    svc.delete_task(task_id)
    return {"ok": True}