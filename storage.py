# storage.py
import json
from pathlib import Path
from datetime import datetime
from typing import Any

from models import Task


class JsonTasksRepo:
    def __init__(self, data_file: Path | str = "tasks.json"):
        self.data_file = Path(data_file)

    def _now(self) -> datetime:
        return datetime.now().replace(microsecond=0)

    def _migrate_if_needed(self, data: Any) -> list[dict]:
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
                        "created_at": self._now().isoformat(),
                    }
                )
                next_id += 1
            return out

        # Якщо dict — лишаємо як є
        if all(isinstance(x, dict) for x in data):
            return data

        return []

    def load_tasks(self) -> list[Task]:
        if not self.data_file.exists():
            return []

        try:
            raw = json.loads(self.data_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []

        migrated = self._migrate_if_needed(raw)

        # Нормалізуємо created_at
        norm: list[dict] = []
        for t in migrated:
            created = t.get("created_at")
            if isinstance(created, str):
                created_at = created
            else:
                created_at = self._now().isoformat()

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
            self.save_tasks([Task(**x) for x in norm])

        return [Task(**x) for x in norm]

    def save_tasks(self, tasks: list[Task]) -> None:
        # Рекомендую зробити атомарний запис:
        tmp = self.data_file.with_suffix(self.data_file.suffix + ".tmp")
        tmp.write_text(
            json.dumps(
                [t.model_dump(mode="json") for t in tasks],
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        tmp.replace(self.data_file)

    @staticmethod
    def next_id(tasks: list[Task]) -> int:
        return max((t.id for t in tasks), default=0) + 1

    @staticmethod
    def find_by_id(tasks: list[Task], task_id: int) -> Task | None:
        for t in tasks:
            if t.id == task_id:
                return t
        return None