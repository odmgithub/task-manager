# models.py
from datetime import datetime
from pydantic import BaseModel, Field


class Task(BaseModel):
    """
    Основна модель задачі (domain model).

    Важливо:
    - Pydantic автоматично валідує типи та парсить datetime з ISO-рядка.
    - Цю модель використовують і storage, і service, і API.
    """
    id: int
    text: str
    done: bool = False
    created_at: datetime


class TaskCreate(BaseModel):
    """
    DTO (data transfer object) для створення задачі через API.
    Тут ми задаємо валідацію: 1..200 символів.
    """
    text: str = Field(min_length=1, max_length=200)


class TaskUpdate(BaseModel):
    """
    DTO для оновлення задачі (PATCH).
    Та ж валідація, що і при створенні.
    """
    text: str = Field(min_length=1, max_length=200)


class TasksResponse(BaseModel):
    """
    Формат відповіді GET /tasks.

    Чому не просто list[Task]:
    - UI вже очікує обʼєкт { "tasks": [...] }
    - легко додати метадані (total, done_count) не ламаючи клієнтів
    """
    tasks: list[Task]