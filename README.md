# Cimeika Nav Pack

Призначення: застосувати 7 розділів головного меню і повну структуру «Легенда CI» у розділі Казкар.

## Вміст
- `mkdocs.yml` — готова конфігурація навігації.
- `apply_cimeika_nav.sh` — Git Bash-скрипт, що створює гілку, додає заглушки і замінює mkdocs.yml.

## Як використати (Windows, Git Bash)
```bash
cd /c/Users/simei/ciwiki
# Розпакуйте архів сюди (у корінь репозиторію)
chmod +x ./apply_cimeika_nav.sh
./apply_cimeika_nav.sh
```
Потім створіть Pull Request з гілки `content/cimeika-7-sections`.

---

## ✅ To-Do PWA (`docs/todo/`)

Мінімальний PWA-застосунок «Список справ» — без залежностей (vanilla JS/HTML/CSS).

### Функції
- Додавання, виконання та видалення завдань
- Фільтри: Усі / Активні / Виконані
- Дані зберігаються у `localStorage` під ключем `cimeika_todo_v1`
- Експорт / імпорт JSON (для резервного копіювання)
- PWA: офлайн-кеш (service worker), Web App Manifest — встановлюється на мобільному

### Як запустити локально (Termux / будь-яка ОС)
```bash
# Python 3 (stdlib, без pip)
python3 -m http.server 8000 --directory docs/todo

# Або Node.js
npx serve docs/todo
```
Відкрийте `http://localhost:8000` у браузері.

### Як працює сховище
| Ключ | Значення |
|------|---------|
| `cimeika_todo_v1` | JSON-масив завдань: `[{id, text, done}, …]` |

Версія ключа (`v1`) дозволяє безпечно змінювати схему у майбутньому без конфліктів.

### Розгортання на Vercel
Сайт будується командою `mkdocs build` → папка `site/`.  
To-Do app автоматично потрапляє до `site/todo/` і доступна за адресою `/todo/`.
