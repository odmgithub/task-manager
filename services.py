# services.py
from __future__ import annotations

from datetime import datetime
from typing import List

from models import Task
from storage import JsonTasksRepo


class TasksService:
    def __init__(self, repo: JsonTasksRepo):
        self.repo = repo

    def list_tasks(self) -> List[Task]:
        tasks = self.repo.load_tasks()
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)

    def add_task(self, text: str) -> Task:
        text = (text or "").strip()
        if not text:
            raise ValueError("Task text is empty")

        tasks = self.repo.load_tasks()
        task = Task(
            id=self.repo.next_id(tasks),
            text=text,
            done=False,
            created_at=datetime.now().replace(microsecond=0),
        )
        tasks.append(task)
        self.repo.save_tasks(tasks)
        return task

    def toggle_task(self, task_id: int) -> Task:
        tasks = self.repo.load_tasks()
        task = self.repo.find_by_id(tasks, task_id)
        if not task:
            raise KeyError("Task not found")

        task.done = not task.done
        self.repo.save_tasks(tasks)
        return task

    def update_task(self, task_id: int, text: str) -> Task:
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
        tasks = self.repo.load_tasks()
        new_tasks = [t for t in tasks if t.id != task_id]
        if len(new_tasks) == len(tasks):
            raise KeyError("Task not found")
        self.repo.save_tasks(new_tasks)