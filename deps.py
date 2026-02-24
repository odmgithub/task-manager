# deps.py
from fastapi import Depends
from config import settings
from storage import JsonTasksRepo
from services import TasksService

def get_repo() -> JsonTasksRepo:
    return JsonTasksRepo(settings.tasks_path)

def get_tasks_service(repo=Depends(get_repo)) -> TasksService:
    return TasksService(repo)