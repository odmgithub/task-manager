def get_ui_html() -> str:
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
    /* --- UI polish --- */
:root {
  --bg: #ffffff;
  --text: #111827;
  --muted: #6b7280;
  --line: #e5e7eb;
  --card: #f9fafb;
  --shadow: 0 10px 30px rgba(17, 24, 39, 0.08);
  --shadow2: 0 12px 24px rgba(17, 24, 39, 0.12);
  --radius: 16px;
  --radius2: 12px;
  --trans: 160ms ease;
}

body {
  background: radial-gradient(1200px 700px at 30% -10%, rgba(99,102,241,0.08), transparent 60%),
              radial-gradient(900px 600px at 90% 10%, rgba(16,185,129,0.08), transparent 55%),
              var(--bg);
}

.container, .wrap, main {
  /* якщо у тебе інша обгортка — ок, це не зламає */
}

.card, .panel {
  background: rgba(255,255,255,0.85);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  backdrop-filter: blur(6px);
}

h1 {
  letter-spacing: -0.02em;
}

/* input + button */
input[type="text"], .input {
  transition: box-shadow var(--trans), border-color var(--trans), transform var(--trans);
}

input[type="text"]:focus, .input:focus {
  outline: none;
  border-color: rgba(99, 102, 241, 0.55);
  box-shadow: 0 0 0 4px rgba(99,102,241,0.15);
  transform: translateY(-1px);
}

button, .btn {
  transition: transform var(--trans), box-shadow var(--trans), opacity var(--trans);
}

button:hover, .btn:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow2);
}

button:active, .btn:active {
  transform: translateY(0px);
  box-shadow: var(--shadow);
}

button[disabled], .btn[disabled] {
  opacity: 0.55;
  cursor: not-allowed;
  box-shadow: none;
}

/* tasks list */
.task-row, li {
  border: 1px solid var(--line);
  border-radius: var(--radius2);
  background: rgba(255,255,255,0.7);
  transition: transform var(--trans), box-shadow var(--trans), border-color var(--trans);
}

.task-row:hover, li:hover {
  transform: translateY(-1px);
  border-color: rgba(99, 102, 241, 0.25);
  box-shadow: 0 10px 24px rgba(17, 24, 39, 0.08);
}

.task.done, .done {
  opacity: 0.55;
  text-decoration-thickness: 2px;
}

.chips button, .chips .chip {
  transition: background var(--trans), color var(--trans), border-color var(--trans), transform var(--trans);
}

.chips button:hover, .chips .chip:hover {
  transform: translateY(-1px);
}

.chips .active, .chips button.active {
  border-color: rgba(99, 102, 241, 0.5);
  background: rgba(99, 102, 241, 0.08);
}

/* subtle appear animation */
@keyframes popIn {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}
.task-row, li {
  animation: popIn 160ms ease;
}

/* toast */
.toast {
  position: fixed;
  right: 18px;
  bottom: 18px;
  background: rgba(17,24,39,0.92);
  color: white;
  padding: 10px 12px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.22);
  display: flex;
  align-items: center;
  gap: 10px;
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 180ms ease, transform 180ms ease;
  z-index: 9999;
  font-size: 14px;
}

.toast.show {
  opacity: 1;
  transform: translateY(0);
}

.toast .dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: #22c55e;
}

.toast.error .dot {
  background: #ef4444;
}
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

function showToast(message, isError = false) {
  let toast = document.querySelector('.toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span class="dot"></span><span class="msg"></span>`;
    document.body.appendChild(toast);
  }

  toast.classList.toggle('error', isError);
  toast.querySelector('.msg').textContent = message;

  // show
  requestAnimationFrame(() => toast.classList.add('show'));

  // hide
  clearTimeout(toast._t);
  toast._t = setTimeout(() => toast.classList.remove('show'), 1400);
}

async function withDisabled(btn, fn) {
  const old = btn.textContent;
  btn.disabled = true;
  btn.textContent = '...';
  try {
    return await fn();
  } finally {
    btn.disabled = false;
    btn.textContent = old;
  }
}



async function refresh(){
  const res = await fetch('/tasks');
  const data = await res.json();
  const tasks = data.tasks || [];

  const doneCount = tasks.filter(t => t.done).length;
  countEl.textContent = `${tasks.length} задач • ${doneCount} виконано`;

  const visible = tasks.filter(t => {
    if(filter === 'active') return !t.done;
    if(filter === 'done') return t.done;
    return true;
  });

  listEl.innerHTML = '';
  visible.forEach((t) => {
    const li = document.createElement('li');
    li.innerHTML = `
      <span class="task ${t.done ? 'done' : ''}" data-id="${t.id}">
       ${escapeHtml(t.text)}
      </span>
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

  await withDisabled(addBtn, async () => {

    const res = await fetch('/tasks', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ text })
    });

    if(!res.ok){
      showToast('Не вдалося додати 😕', true);
      return;
    }

    showToast('Додано ✅');
    inputEl.value = '';
    await refresh();
  });
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

listEl.addEventListener('dblclick', async (e) => {
  const taskEl = e.target.closest('.task');
  if (!taskEl) return;

  const id = Number(taskEl.dataset.id);
  const oldText = taskEl.textContent.trim();
  const newText = prompt('Редагувати задачу:', oldText);

  if (newText === null) return;            // Cancel
  if (!newText.trim()) return;             // порожнє не приймаємо

  await fetch(`/tasks/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: newText.trim() })
  });

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