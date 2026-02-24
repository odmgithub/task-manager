Purpose
-------
This file orients AI coding agents to the Task Manager repository: its architecture, data flows, runtime commands, and project-specific conventions. Use it to make safe, minimal edits and to implement features that integrate with the existing design.

**Big Picture**
- **API + UI:** `api.py` exposes a FastAPI app and serves the single-page UI from `ui.py` (route `/`). The UI talks to the HTTP API endpoints under `/tasks`.
- **Business layer:** `services.py` contains all domain logic (add/toggle/update/delete/get). Prefer extending or calling `services.py` for feature work rather than re-implementing logic elsewhere.
- **Storage:** `storage.py` is the canonical persistence layer. It reads/writes `tasks.json`, performs migrations (old string-list format → dicts), normalizes `created_at`, and exposes helpers: `load_tasks()`, `save_tasks()`, `next_id()`, `find_by_id()`.
- **Models:** `models.py` uses Pydantic models (`Task`, `TaskCreate`, `TaskUpdate`, `TasksResponse`). The rest of the code expects Pydantic v2 usage (see `Task.model_dump(mode="json")` in `storage.py`).
- **CLI variants:** There are two CLI entrypoints: `main.py` (a simple, older menu operating on list[str]) and `cli.py` (modern CLI that uses `services.py` and `Task` objects). For backend work prefer `cli.py` and `services.py`.

**Data flow & formats**
- UI -> `api.py` -> `services.py` -> `storage.py` -> `tasks.json`.
- `tasks.json` canonical format: list of objects with keys `id` (int), `text` (str), `done` (bool), `created_at` (ISO str). Example element: `{ "id": 3, "text": "Buy milk", "done": false, "created_at": "2026-02-20T18:27:22" }`.
- Migration: `storage._migrate_if_needed` accepts legacy list-of-strings like `"[✓] done task"` and will rewrite the file to the canonical dict format. Be cautious when editing `storage.py` — changes may rewrite `tasks.json` during load.

**Error & control patterns**
- `services.py` uses exceptions to signal problems: `ValueError` for invalid input, `KeyError` for missing tasks. `api.py` maps these to HTTP errors (400/404). Follow this pattern when adding service-layer checks.
- IDs are assigned by `storage.next_id(tasks)` as `max(ids)+1` — avoid creating code that relies on external ID generation.

**Runtime / dev commands**
- Install runtime deps (if adding/working on the API/UI):

```bash
pip install fastapi uvicorn pydantic
```

- Run the web server (serves UI + API):

```bash
uvicorn api:app --reload --port 8000
```

- Run the modern CLI (uses services + models):

```bash
python cli.py
```

- `main.py` is legacy/simple and uses a different internal format (list[str]); avoid changing it for API work.

**Integration points & HTTP contract**
- GET `/tasks` -> `{ "tasks": [Task...] }` where each `Task` contains `id,text,done,created_at`.
- POST `/tasks` body `{ "text": "..." }` -> returns `{ "task": Task }` (400 if text empty).
- POST `/tasks/{id}/toggle` -> toggles `done` (404 if not found).
- PATCH `/tasks/{id}` body `{ "text": "..." }` -> updates text (400/404 on errors).
- DELETE `/tasks/{id}` -> deletes (404 if not found).

**Editing guidance / examples**
- Prefer adding new logic in `services.py` and only touch `storage.py` when persistence changes are required.
- When adding fields to `Task`, update `models.py` and ensure `storage.save_tasks` serializes with `model_dump(mode="json")` to keep compatibility.
- Example: call `add_task_service("hello")` from tests or `cli.py` to create a `Task` object; it returns a Pydantic `Task` instance.

If anything in this summary is unclear or you want more examples (e.g., sample API requests/responses, unit-test guidance, or migration details), tell me which area to expand and I'll iterate.
