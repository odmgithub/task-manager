# models.py
from datetime import datetime
from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int
    text: str
    done: bool = False
    created_at: datetime


class TaskCreate(BaseModel):
    text: str = Field(min_length=1, max_length=200)


class TaskUpdate(BaseModel):
    text: str = Field(min_length=1, max_length=200)


class TasksResponse(BaseModel):
    tasks: list[Task]