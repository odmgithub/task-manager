import json
from pathlib import Path
from datetime import datetime
from typing import Any
from models import Task

DATA_FILE = Path("tasks.json")


def _now() -> datetime:
    return datetime.now().replace(microsecond=0)


def _migrate_if_needed(data: Any) -> list[dict]:
    """
    Підтримка старих форматів:
    1) ["task", "[✓] done task"]
    2) список dict (старий/новий)
    -> повертаємо список dict нового формату
    """
    if not isinstance(data, list):
        return []

    # Старий формат: список рядків
    if all(isinstance(x, str) for x in data):
        out = []
        next_id = 1
        for s in data:
            done = s.startswith("[✓] ")
            text = s[4:] if done else s
            out.append(
                {
                    "id": next_id,
                    "text": text,
                    "done": done,
                    "created_at": _now().isoformat(),
                }
            )
            next_id += 1
        return out

    # Якщо dict — лишаємо як є
    if all(isinstance(x, dict) for x in data):
        return data

    return []


def load_tasks() -> list[Task]:
    if not DATA_FILE.exists():
        return []

    try:
        raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

    migrated = _migrate_if_needed(raw)

    # Нормалізуємо created_at в ISO якщо там datetime/щось інше
    norm = []
    for t in migrated:
        created = t.get("created_at")
        if isinstance(created, str):
            created_at = created
        else:
            created_at = _now().isoformat()

        norm.append(
            {
                "id": int(t.get("id", 0)),
                "text": str(t.get("text", "")),
                "done": bool(t.get("done", False)),
                "created_at": created_at,
            }
        )

    # якщо була міграція/нормалізація — збережемо
    if raw != norm:
        save_tasks([Task(**x) for x in norm])

    return [Task(**x) for x in norm]


def save_tasks(tasks: list[Task]) -> None:
    DATA_FILE.write_text(
        json.dumps([t.model_dump(mode="json") for t in tasks], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def next_id(tasks: list[Task]) -> int:
    return (max((t.id for t in tasks), default=0) + 1)


def find_by_id(tasks: list[Task], task_id: int) -> Task | None:
    for t in tasks:
        if t.id == task_id:
            return t
    return None