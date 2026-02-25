# deps.py
from fastapi import Depends
from config import settings
from storage import JsonTasksRepo
from services import TasksService
from storage_protocol import TasksRepo


def get_repo() -> TasksRepo:
        # Повертаємо конкретну реалізацію, але назовні — як TasksRepo
    """
    Dependency provider для repo.

    FastAPI буде викликати цю функцію, коли потрібно отримати доступ до сховища.
    Перевага: шлях до файлу береться з settings, а не хардкодиться у 10 місцях.
    """
    return JsonTasksRepo(settings.tasks_path)


def get_tasks_service(repo: TasksRepo = Depends(get_repo)) -> TasksService:
    """
    Dependency provider для сервісу.

    Тут "склеюються" шари:
    - repo (storage layer)
    - service (business logic layer)

    Роутери в api.py не створюють об’єкти вручну,
    а просто "просять" TasksService через Depends.
    """
    return TasksService(repo)