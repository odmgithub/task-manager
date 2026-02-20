from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
from pathlib import Path

app = FastAPI()

DATA_FILE = Path("tasks.json")


def load_tasks() -> list[str]:
    if not DATA_FILE.exists():
        return []
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def save_tasks(tasks: list[str]) -> None:
    DATA_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


@app.get("/", response_class=HTMLResponse)
def ui():
    # Мінімальний UI в браузері (без окремих файлів)
    return """
<!doctype html>
<html lang="uk">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Task Manager</title>
  <style>
    body{font-family:system-ui,Segoe UI,Arial,sans-serif;max-width:720px;margin:32px auto;padding:0 16px}
    h1{margin:0 0 16px}
    .row{display:flex;gap:8px;margin-bottom:12px}
    input{flex:1;padding:10px;border:1px solid #ccc;border-radius:10px}
    button{padding:10px 12px;border:1px solid #ccc;border-radius:10px;background:#fff;cursor:pointer}
    button:hover{background:#f5f5f5}
    ul{padding:0;list-style:none}
    li{display:flex;align-items:center;gap:8px;padding:10px;border:1px solid #eee;border-radius:12px;margin-bottom:8px}
    .task{flex:1}
    .done{opacity:.7}
    .muted{color:#777;font-size:14px}
  </style>
</head>
<body>
  <h1>Task Manager</h1>
  <div class="row">
    <input id="taskInput" placeholder="Нова задача..." />
    <button id="addBtn">Додати</button>
  </div>
  <div class="muted">Підказка: натисни Enter щоб додати</div>
  <hr style="border:none;border-top:1px solid #eee;margin:16px 0" />
  <ul id="list"></ul>

<script>
const listEl = document.getElementById('list');
const inputEl = document.getElementById('taskInput');
const addBtn = document.getElementById('addBtn');

function escapeHtml(s){
  return s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
}

async function refresh(){
  const res = await fetch('/tasks');
  const data = await res.json();
  listEl.innerHTML = '';
  data.tasks.forEach((t, idx) => {
    const li = document.createElement('li');
    const isDone = t.startsWith('[✓] ');
    li.innerHTML = `
      <span class="task ${isDone ? 'done' : ''}">${escapeHtml(t)}</span>
      <button data-act="done" data-idx="${idx}">✓</button>
      <button data-act="del" data-idx="${idx}">🗑</button>
    `;
    listEl.appendChild(li);
  });
}

async function addTask(){
  const task = inputEl.value.trim();
  if(!task) return;
  await fetch('/tasks', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({task})
  });
  inputEl.value = '';
  await refresh();
}

listEl.addEventListener('click', async (e) => {
  const btn = e.target.closest('button');
  if(!btn) return;
  const idx = Number(btn.dataset.idx);
  const act = btn.dataset.act;
  if(act === 'del'){
    await fetch(`/tasks/${idx}`, {method:'DELETE'});
  } else if(act === 'done'){
    await fetch(`/tasks/${idx}/complete`, {method:'POST'});
  }
  await refresh();
});

addBtn.addEventListener('click', addTask);
inputEl.addEventListener('keydown', (e) => {
  if(e.key === 'Enter') addTask();
});

refresh();
</script>
</body>
</html>
"""


@app.get("/tasks")
def get_tasks():
    return {"tasks": load_tasks()}


@app.post("/tasks")
def add_task(payload: dict):
    task = str(payload.get("task", "")).strip()
    if not task:
        return {"error": "empty task"}
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    return {"tasks": tasks}


@app.delete("/tasks/{idx}")
def delete_task(idx: int):
    tasks = load_tasks()
    if idx < 0 or idx >= len(tasks):
        return {"error": "bad index"}
    tasks.pop(idx)
    save_tasks(tasks)
    return {"tasks": tasks}


@app.post("/tasks/{idx}/complete")
def complete_task(idx: int):
    tasks = load_tasks()
    if idx < 0 or idx >= len(tasks):
        return {"error": "bad index"}
    if not tasks[idx].startswith("[✓] "):
        tasks[idx] = "[✓] " + tasks[idx]
    save_tasks(tasks)
    return {"tasks": tasks}


from fastapi.responses import Response

@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)  # "нема контенту", без помилки