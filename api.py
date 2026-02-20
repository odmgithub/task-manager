from fastapi import FastAPI
import json
from pathlib import Path

app = FastAPI()

DATA_FILE = Path("tasks.json")


def load_tasks():
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_tasks(tasks):
    DATA_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


@app.get("/")
def root():
    return {"message": "API працює 🔥"}


@app.get("/tasks")
def get_tasks():
    return {"tasks": load_tasks()}


# 👇 НОВЕ
@app.post("/tasks")
def add_task(task: str):
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    return {"message": "додано", "tasks": tasks}