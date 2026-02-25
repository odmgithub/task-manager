# in_memory_repo.py
from __future__ import annotations
from typing import List, Optional
from models import Task


class InMemoryTasksRepo:
    """
    Просте сховище в памʼяті.

    Для тестів це ідеально:
    - ніяких файлів
    - ніякого JSON
    - все швидко і детерміновано
    """

    def __init__(self, initial: List[Task] | None = None):
        self._tasks: List[Task] = list(initial or [])

    def load_tasks(self) -> List[Task]:
        # Повертаємо копію, щоб зовнішній код випадково не ламав стан напряму
        return list(self._tasks)

    def save_tasks(self, tasks: List[Task]) -> None:
        # Замінюємо весь стан (як у JSON repo)
        self._tasks = list(tasks)

    @staticmethod
    def next_id(tasks: List[Task]) -> int:
        return max((t.id for t in tasks), default=0) + 1

    @staticmethod
    def find_by_id(tasks: List[Task], task_id: int) -> Optional[Task]:
        for t in tasks:
            if t.id == task_id:
                return t
        return None