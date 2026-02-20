from pydantic import BaseModel, Field
from datetime import datetime


class Task(BaseModel):
    id: int
    text: str
    done: bool = False
    created_at: datetime


class TaskCreate(BaseModel):
    text: str = Field(min_length=1, max_length=200)


from pydantic import BaseModel
from typing import List

class TasksResponse(BaseModel):
    tasks: list[Task]

class TaskUpdate(BaseModel):
    text: str = Field(min_length=1, max_length=200)