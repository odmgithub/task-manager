from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
import json
from pathlib import Path
from datetime import datetime

app = FastAPI()

DATA_FILE = Path("tasks.json")


def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def migrate_if_needed(data):
    """
    Підтримка старого формату: ["task 1", "[✓] task 2"]
    -> нового: [{"id":..., "text":..., "done":..., "created_at":...}]
    """
    if not isinstance(data, list):
        return []

    # Якщо список рядків — це старий формат
    if all(isinstance(x, str) for x in data):
        tasks = []
        next_id = 1
        for s in data:
            done = s.startswith("[✓] ")
            text = s[4:] if done else s
            tasks.append(
                {
                    "id": next_id,
                    "text": text,
                    "done": done,
                    "created_at": now_iso(),
                }
            )
            next_id += 1
        return tasks

    # Якщо список об’єктів — залишаємо
    if all(isinstance(x, dict) for x in data):
        return data

    return []


def load_tasks() -> list[dict]:
    if not DATA_FILE.exists():
        return []

    try:
        raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

    tasks = migrate_if_needed(raw)

    # Якщо була міграція — збережемо одразу в новому форматі
    if raw != tasks:
        save_tasks(tasks)

    return tasks


def save_tasks(tasks: list[dict]) -> None:
    DATA_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def next_task_id(tasks: list[dict]) -> int:
    if not tasks:
        return 1
    return max(int(t.get("id", 0)) for t in tasks) + 1


def find_by_id(tasks: list[dict], task_id: int):
    for t in tasks:
        if int(t.get("id", -1)) == task_id:
            return t
    return None


@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)


@app.get("/", response_class=HTMLResponse)
def ui():
    return """
<!doctype html>
<html lang="uk">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Task Manager</title>
  <style>
    body{font-family:system-ui,Segoe UI,Arial,sans-serif;max-width:820px;margin:32px auto;padding:0 16px}
    h1{margin:0 0 16px}
    .row{display:flex;gap:8px;margin-bottom:12px}
    input{flex:1;padding:10px;border:1px solid #ccc;border-radius:10px}
    button{padding:10px 12px;border:1px solid #ccc;border-radius:10px;background:#fff;cursor:pointer}
    button:hover{background:#f5f5f5}
    .toolbar{display:flex;gap:8px;align-items:center;margin:12px 0}
    .chip{padding:6px 10px;border-radius:999px;border:1px solid #ddd;background:#fff;cursor:pointer}
    .chip.active{border-color:#999}
    ul{padding:0;list-style:none}
    li{display:flex;align-items:center;gap:10px;padding:10px;border:1px solid #eee;border-radius:12px;margin-bottom:8px}
    .task{flex:1}
    .done{opacity:.65;text-decoration:line-through}
    .meta{color:#777;font-size:12px}
  </style>
</head>
<body>
  <h1>Task Manager</h1>

  <div class="row">
    <input id="taskInput" placeholder="Нова задача..." />
    <button id="addBtn">Додати</button>
  </div>

  <div class="toolbar">
    <button class="chip active" data-filter="all">Всі</button>
    <button class="chip" data-filter="active">Активні</button>
    <button class="chip" data-filter="done">Виконані</button>
    <span id="count" class="meta"></span>
  </div>

  <ul id="list"></ul>

<script>
const listEl = document.getElementById('list');
const inputEl = document.getElementById('taskInput');
const addBtn = document.getElementById('addBtn');
const countEl = document.getElementById('count');
let filter = 'all';

function escapeHtml(s){
  return String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
}

function setActiveChip(){
  document.querySelectorAll('.chip').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.filter === filter);
  });
}

async function refresh(){
  const res = await fetch('/tasks');
  const data = await res.json();
  const tasks = data.tasks || [];

  // лічильник
  const doneCount = tasks.filter(t => t.done).length;
  countEl.textContent = `${tasks.length} задач • ${doneCount} виконано`;

  // фільтр
  const visible = tasks.filter(t => {
    if(filter === 'active') return !t.done;
    if(filter === 'done') return t.done;
    return true;
  });

  listEl.innerHTML = '';
  visible.forEach((t) => {
    const li = document.createElement('li');
    li.innerHTML = `
      <span class="task ${t.done ? 'done' : ''}">${escapeHtml(t.text)}</span>
      <span class="meta">${escapeHtml(t.created_at || '')}</span>
      <button data-act="toggle" data-id="${t.id}">✓</button>
      <button data-act="del" data-id="${t.id}">🗑</button>
    `;
    listEl.appendChild(li);
  });
}

async function addTask(){
  const text = inputEl.value.trim();
  if(!text) return;

  await fetch('/tasks', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({text})
  });

  inputEl.value = '';
  await refresh();
}

listEl.addEventListener('click', async (e) => {
  const btn = e.target.closest('button');
  if(!btn) return;
  const id = Number(btn.dataset.id);
  const act = btn.dataset.act;

  if(act === 'del'){
    await fetch(`/tasks/${id}`, {method:'DELETE'});
  } else if(act === 'toggle'){
    await fetch(`/tasks/${id}/toggle`, {method:'POST'});
  }
  await refresh();
});

document.querySelectorAll('.chip').forEach(btn => {
  btn.addEventListener('click', async () => {
    filter = btn.dataset.filter;
    setActiveChip();
    await refresh();
  });
});

addBtn.addEventListener('click', addTask);
inputEl.addEventListener('keydown', (e) => { if(e.key === 'Enter') addTask(); });

setActiveChip();
refresh();
</script>
</body>
</html>
"""


@app.get("/tasks")
def get_tasks():
    # Сортуємо: спочатку нові
    tasks = load_tasks()
    tasks_sorted = sorted(tasks, key=lambda t: t.get("created_at", ""), reverse=True)
    return {"tasks": tasks_sorted}


@app.post("/tasks")
def add_task(payload: dict):
    text = str(payload.get("text", "")).strip()
    if not text:
        return {"error": "empty text"}

    tasks = load_tasks()
    task = {
        "id": next_task_id(tasks),
        "text": text,
        "done": False,
        "created_at": now_iso(),
    }
    tasks.append(task)
    save_tasks(tasks)
    return {"task": task}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = load_tasks()
    before = len(tasks)
    tasks = [t for t in tasks if int(t.get("id", -1)) != task_id]

    if len(tasks) == before:
        return {"error": "not found"}

    save_tasks(tasks)
    return {"ok": True}


@app.post("/tasks/{task_id}/toggle")
def toggle_task(task_id: int):
    tasks = load_tasks()
    t = find_by_id(tasks, task_id)
    if not t:
        return {"error": "not found"}

    t["done"] = not bool(t.get("done", False))
    save_tasks(tasks)
    return {"task": t}