# services.py
from __future__ import annotations

from datetime import datetime
from typing import List

from models import Task
from storage import JsonTasksRepo
from exceptions import TaskNotFound, TaskTextEmpty


class TasksService:
    """
    Бізнес-логіка для задач.

    Важлива ідея:
    - Service НЕ знає нічого про FastAPI / HTTP
    - Service НЕ знає, що це JSON-файл
    Він працює тільки з repo (сховищем), яке вміє load/save.

    Завдяки цьому:
    - API і CLI можуть використовувати один і той самий сервіс
    - сховище можна замінити (JSON -> SQLite) без переписування логіки
    """
    """
    Бізнес-логіка задач.

    Тепер service залежить НЕ від JsonTasksRepo,
    а від абстракції TasksRepo (Protocol).
    """

    def __init__(self, repo: JsonTasksRepo):
        # repo — це об’єкт, який відповідає за доступ до даних (storage layer)
        self.repo = repo

    def list_tasks(self) -> List[Task]:
        """
        Повертає всі задачі, відсортовані за часом створення (нові зверху).
        """
        tasks = self.repo.load_tasks()  # читаємо дані з repo (JSON/БД — неважливо)
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)

    def add_task(self, text: str) -> Task:
        """
        Створює нову задачу.
        - валідує text (щоб не зберігати порожні задачі)
        - генерує id
        - ставить created_at
        - зберігає оновлений список
        """
        # 1) Валідація/нормалізація введення
        text = (text or "").strip()
        if not text:
            raise TaskTextEmpty("Task text is empty")

        # 2) Читаємо поточний стан
        tasks = self.repo.load_tasks()

        # 3) Створюємо об’єкт Task (Pydantic model)
        task = Task(
            id=self.repo.next_id(tasks),                  # наступний ID
            text=text,
            done=False,
            created_at=datetime.now().replace(microsecond=0),  # чистіше в UI
        )

        # 4) Змінюємо стан в пам’яті і зберігаємо
        tasks.append(task)
        self.repo.save_tasks(tasks)

        return task

    def toggle_task(self, task_id: int) -> Task:
        """
        Перемикає done <-> not done для задачі.

        Якщо задачі з таким id нема — кидаємо KeyError,
        а вже API шар вирішує, що це буде HTTP 404.
        """
        tasks = self.repo.load_tasks()

        # шукаємо задачу у списку
        task = self.repo.find_by_id(tasks, task_id)
        if not task:
            raise TaskNotFound(f"Task {task_id} not found")

        # змінюємо стан
        task.done = not task.done

        # зберігаємо весь список назад
        self.repo.save_tasks(tasks)
        return task

    def update_task(self, task_id: int, text: str) -> Task:
        """
        Оновлює текст задачі.

        Важливо:
        - знову робимо валідацію (порожній текст не дозволяємо)
        - знаходимо задачу
        - міняємо тільки одне поле
        """
        text = (text or "").strip()
        if not text:
            raise ValueError("Task text is empty")

        tasks = self.repo.load_tasks()
        task = self.repo.find_by_id(tasks, task_id)
        if not task:
            raise KeyError("Task not found")

        task.text = text
        self.repo.save_tasks(tasks)
        return task

    def delete_task(self, task_id: int) -> None:
        """
        Видаляє задачу за id.

        Трюк:
        - фільтруємо список
        - якщо довжина не змінилась — значить нічого не видалили => 404
        """
        tasks = self.repo.load_tasks()

        new_tasks = [t for t in tasks if t.id != task_id]

        # Якщо нічого не видалилось — id не існує
        if len(new_tasks) == len(tasks):
            raise KeyError("Task not found")

        self.repo.save_tasks(new_tasks)