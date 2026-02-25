/**
 * Cimeika To-Do — vanilla JS PWA
 * Storage key: cimeika_todo_v1
 */

'use strict';

const STORAGE_KEY = 'cimeika_todo_v1';

// ── State ────────────────────────────────────────────────────────────────────
let tasks  = load();
let filter = 'all';

// ── DOM refs ─────────────────────────────────────────────────────────────────
const form          = document.getElementById('add-form');
const newTaskInput  = document.getElementById('new-task');
const taskList      = document.getElementById('task-list');
const filterBtns    = document.querySelectorAll('.filter-btn');
const tasksLeftEl   = document.getElementById('tasks-left');
const exportBtn     = document.getElementById('export-btn');
const importInput   = document.getElementById('import-input');
const clearBtn      = document.getElementById('clear-completed');

// ── Storage helpers ───────────────────────────────────────────────────────────
function load() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  } catch {
    return [];
  }
}

function save() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
}

// ── Task helpers ──────────────────────────────────────────────────────────────
function createTask(text) {
  return { id: Date.now().toString(36) + Math.random().toString(36).slice(2), text, done: false };
}

function filtered() {
  if (filter === 'active')    return tasks.filter(t => !t.done);
  if (filter === 'completed') return tasks.filter(t =>  t.done);
  return tasks;
}

// ── Render ────────────────────────────────────────────────────────────────────
function render() {
  const visible = filtered();
  taskList.innerHTML = '';

  visible.forEach(task => {
    const li = document.createElement('li');
    li.className = 'task-item' + (task.done ? ' done' : '');
    li.dataset.id = task.id;
    li.setAttribute('role', 'listitem');

    const cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.className = 'task-checkbox';
    cb.checked = task.done;
    cb.setAttribute('aria-label', task.done ? 'Позначити як незавершене' : 'Позначити як завершене');
    cb.addEventListener('change', () => toggleTask(task.id));

    const span = document.createElement('span');
    span.className = 'task-text';
    span.textContent = task.text;

    const del = document.createElement('button');
    del.className = 'delete-btn';
    del.textContent = '✕';
    del.setAttribute('aria-label', 'Видалити завдання');
    del.addEventListener('click', () => deleteTask(task.id));

    li.append(cb, span, del);
    taskList.appendChild(li);
  });

  // Footer counter
  const activeCount = tasks.filter(t => !t.done).length;
  tasksLeftEl.textContent = `${activeCount} залишилось`;
}

// ── Actions ───────────────────────────────────────────────────────────────────
function addTask(text) {
  text = text.trim();
  if (!text) return;
  tasks.unshift(createTask(text));
  save();
  render();
}

function toggleTask(id) {
  const t = tasks.find(t => t.id === id);
  if (t) { t.done = !t.done; save(); render(); }
}

function deleteTask(id) {
  tasks = tasks.filter(t => t.id !== id);
  save();
  render();
}

function clearCompleted() {
  tasks = tasks.filter(t => !t.done);
  save();
  render();
}

// ── Export / Import ───────────────────────────────────────────────────────────
function exportJSON() {
  const blob = new Blob([JSON.stringify({ version: 1, tasks }, null, 2)], { type: 'application/json' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href     = url;
  a.download = 'cimeika-todo.json';
  a.click();
  URL.revokeObjectURL(url);
}

function importJSON(file) {
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    try {
      const data = JSON.parse(e.target.result);
      const imported = Array.isArray(data.tasks) ? data.tasks : (Array.isArray(data) ? data : null);
      if (!imported) throw new Error('Невірний формат');
      // Merge: keep existing, add new by id
      const existingIds = new Set(tasks.map(t => t.id));
      const newTasks    = imported.filter(t => t.id && t.text !== undefined && !existingIds.has(t.id));
      tasks = [...tasks, ...newTasks];
      save();
      render();
    } catch (err) {
      alert('Помилка імпорту: ' + err.message);
    }
  };
  reader.readAsText(file);
}

// ── Event listeners ───────────────────────────────────────────────────────────
form.addEventListener('submit', e => {
  e.preventDefault();
  addTask(newTaskInput.value);
  newTaskInput.value = '';
});

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filter = btn.dataset.filter;
    filterBtns.forEach(b => b.classList.toggle('active', b === btn));
    render();
  });
});

exportBtn.addEventListener('click', exportJSON);
importInput.addEventListener('change', e => { importJSON(e.target.files[0]); e.target.value = ''; });
clearBtn.addEventListener('click', clearCompleted);

// ── Service Worker registration ───────────────────────────────────────────────
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').catch(err => {
      console.warn('SW registration failed:', err);
    });
  });
}

// ── Initial render ────────────────────────────────────────────────────────────
render();
