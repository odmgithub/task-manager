from datetime import datetime
from typing import List

from models import Task
from storage import load_tasks, save_tasks, next_id, find_by_id


def get_tasks_service() -> List[Task]:
    tasks = load_tasks()
    return sorted(tasks, key=lambda t: t.created_at, reverse=True)


def add_task_service(text: str) -> Task:
    text = (text or "").strip()
    if not text:
        raise ValueError("Task text is empty")

    tasks = load_tasks()
    task = Task(
        id=next_id(tasks),
        text=text,
        done=False,
        created_at=datetime.now().replace(microsecond=0),
    )
    tasks.append(task)
    save_tasks(tasks)
    return task


def toggle_task_service(task_id: int) -> Task:
    tasks = load_tasks()
    task = find_by_id(tasks, task_id)
    if not task:
        raise KeyError("Task not found")

    task.done = not task.done
    save_tasks(tasks)
    return task


def update_task_service(task_id: int, text: str) -> Task:
    text = (text or "").strip()
    if not text:
        raise ValueError("Task text is empty")

    tasks = load_tasks()
    task = find_by_id(tasks, task_id)
    if not task:
        raise KeyError("Task not found")

    task.text = text
    save_tasks(tasks)
    return task


def delete_task_service(task_id: int) -> None:
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t.id != task_id]
    if len(new_tasks) == len(tasks):
        raise KeyError("Task not found")
    save_tasks(new_tasks)