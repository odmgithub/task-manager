# test_services.py
import unittest
from datetime import datetime

from services import TasksService
from in_memory_repo import InMemoryTasksRepo
from models import Task
from exceptions import TaskNotFound, TaskTextEmpty


class TestTasksService(unittest.TestCase):
    def test_add_task_success(self):
        repo = InMemoryTasksRepo()
        svc = TasksService(repo)

        t = svc.add_task("Hello")
        self.assertEqual(t.id, 1)
        self.assertEqual(t.text, "Hello")
        self.assertFalse(t.done)

        tasks = svc.list_tasks()
        self.assertEqual(len(tasks), 1)

    def test_add_task_empty_raises(self):
        repo = InMemoryTasksRepo()
        svc = TasksService(repo)

        with self.assertRaises(TaskTextEmpty):
            svc.add_task("   ")

    def test_toggle_not_found_raises(self):
        repo = InMemoryTasksRepo()
        svc = TasksService(repo)

        with self.assertRaises(TaskNotFound):
            svc.toggle_task(123)

    def test_delete_removes_task(self):
        repo = InMemoryTasksRepo(
            initial=[
                Task(id=1, text="A", done=False, created_at=datetime.now()),
                Task(id=2, text="B", done=False, created_at=datetime.now()),
            ]
        )
        svc = TasksService(repo)

        svc.delete_task(1)
        ids = [t.id for t in svc.list_tasks()]
        self.assertEqual(ids, [2])


if __name__ == "__main__":
    unittest.main()