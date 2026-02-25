# storage_protocol.py
from __future__ import annotations
from typing import Protocol, List, Optional
from models import Task


class TasksRepo(Protocol):
    """
    Контракт (інтерфейс) для будь-якого сховища задач.

    Service layer працює лише з цим інтерфейсом і не знає:
    - JSON це, БД, або ін-меморі список
    """

    def load_tasks(self) -> List[Task]:
        """Повернути всі задачі зі сховища."""
        ...

    def save_tasks(self, tasks: List[Task]) -> None:
        """Зберегти повний список задач у сховище."""
        ...

    def next_id(self, tasks: List[Task]) -> int:
        """Порахувати наступний id на основі поточного списку."""
        ...

    def find_by_id(self, tasks: List[Task], task_id: int) -> Optional[Task]:
        """Знайти задачу за id у вже завантаженому списку."""
        ...