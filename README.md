# CiWiki — Центр документації Cimeika

## Огляд

CiWiki є центральним репозіторієм документації та **єдиним джерелом правил** для всієї екосистеми Cimeika.

## System Node

| Field         | Description                                                                          |
|---------------|--------------------------------------------------------------------------------------|
| Node Role     | Documentation, rules, and the canonical source of truth for all Cimeika nodes.       |
| Inputs        | Change requests (PRs), documentation updates, API traces.                            |
| Outputs       | Canonical instructions, standard contracts/rules, procedural approvals.              |
| Dependencies  | All other nodes depend on ciwiki for system-wide rules and documentation.            |

## Екосистема Cimeika

### Репозиторії (актуальний список)

> Всі нижче перелічені репозиторії беруть участь у проекті (виконання / інтеграція):

- **ci_gitapi** — API Authorization & Coordination Gateway
- **ciwiki** (цей репозиторій) — Центральна документація та правила
- **cimeika-unified** — Уніфікована інтеграція компонентів (Vercel)
- **cit** — Основна кодова база / фронтенд (Vercel)
- **cimeika-backend** — Backend (Cloudflare Workers: TypeScript + Hono)
- **ci-memory** — Жива памʼять / контекст екосистеми
- **media** — Медіа ресурси

### Документація

#### Основні файли
- [COPILOT_CANON.md](./COPILOT_CANON.md) — Глобальні інструкції для GitHub Copilot
- [SECURITY.md](./SECURITY.md) — Політика безпеки
- [SECURITY_CHECKLIST.md](./SECURITY_CHECKLIST.md) — Security checklist для розробників
- [CONTRIBUTING.md](./CONTRIBUTING.md) — Гайд для контриб'юторів
- [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) — Кодекс поведінки
- [LICENSE](./LICENSE) — MIT License
- [CHANGELOG.md](./CHANGELOG.md) — Історія змін

#### Ci
- [Ci Core · Production Spec](./docs/ci/production-spec.md) — Канонічна специфікація Ci: FAB, оверлеї, жести, токени, стани

#### Процеси
- [PR процес](./docs/processes/pr-process.md) — Як створювати та обробляти Pull Request
- [Release процес](./docs/processes/release-process.md) — Процедура випуску релізів
- [Тестування](./docs/processes/testing.md) — Стандарти тестування
- [Управління секретами](./docs/processes/secrets-management.md) — Робота з credentials
- [Конвенції комітів](./docs/processes/commit-conventions.md) — Стандарти для commit messages
- [Master Issue](./docs/processes/master-issue.md) — Робота з master issues

#### Шаблони
- [Шаблон змін](./docs/templates/change-template.md) — Обов'язковий шаблон для покрокових змін
- [PR Template](./.github/pull_request_template.md) — Шаблон Pull Request

#### Політики
- [Copilot Guard](./docs/policies/copilot-guard.md) — Захист від витоку секретів
- [Repository Status](./docs/policies/repository-status.md) — Статус репозиторію

## Швидкий старт

### Для розробників

1. Ознайомтесь з [COPILOT_CANON.md](./COPILOT_CANON.md) — основні правила роботи
2. Прочитайте [PR процес](./docs/processes/pr-process.md) перед створенням PR
3. Використовуйте [шаблон змін](./docs/templates/change-template.md) для всіх змін

### Для асистентів (GitHub Copilot)

1. **Обов'язково**: Дотримуйтесь [COPILOT_CANON.md](./COPILOT_CANON.md)
2. Перед будь-якою дією перевірте відповідну документацію в `/docs/processes/`
3. Всі зміни через PR → перевірка → затвердження людиною

## Copilot & Canon Reference

- Global rules: [ciwiki/.github/copilot-instructions.md](https://github.com/Ihorog/ciwiki/blob/main/.github/copilot-instructions.md)
- Canon updated: [ciwiki audit history](https://github.com/Ihorog/ciwiki/commits/main/.github/copilot-instructions.md)
- All functional changes must pass anti-repeat and intent review.

## Структура документації

```
ciwiki/
├── README.md                    # Цей файл - головна сторінка
├── COPILOT_CANON.md            # Глобальні правила Copilot
├── SECURITY.md                 # Політика безпеки
├── docs/                       # Документація MkDocs
│   ├── processes/              # Процеси та інструкції
│   ├── Cimeika/               # Документація проєкту
│   └── index.md               # Головна сторінка документації
├── .github/                    # GitHub конфігурація
│   ├── workflows/             # CI/CD workflows
│   └── copilot-instructions.md # Copilot інструкції
```

## Legend Ci Pipeline

Детальна документація пайплайну: [`legend_registry.yml`](./legend_registry.yml).

Єдине джерело правди: `docs/legend_ci/legend.graph.json`

### Запуск локально

```bash
# Крок 1: синхронізувати граф → markdown-файли
python scripts/legend/sync_graph_to_markdown.py

# Крок 2: побудувати HTML-сторінки та JSON API
python scripts/legend/build_legend.py
```

Результати:
- `content/legend/**` — markdown-файли по главах
- `docs/legend/**` — HTML-сторінки з навігацією
- `api/v1/legend/**` — JSON API

Ручні правки дозволені лише всередині зон:
```
<!-- CI:MANUAL:BEGIN -->
...ваш вміст...
<!-- CI:MANUAL:END -->
```

## CI/CD

Всі зміни проходять через автоматизовані перевірки:
- Лінтинг коду та документації
- Перевірка безпеки (CodeQL, Secret Scanning)
- Валідація структури документації
- Перевірка MkDocs збірки

Детальніше: [CI/CD документація](./docs/processes/ci-cd.md)

## Веб-публікація

Документація автоматично публікується на **GitHub Pages** при кожному push до `main`:

🌐 **Сайт**: [www.cimeika.com.ua](https://www.cimeika.com.ua)

### Технології
- **MkDocs** — генератор статичного сайту
- **Material for MkDocs** — сучасна тема
- **GitHub Actions** — автоматичний деплой

### Локальний перегляд

```bash
# Встановити залежності
pip install mkdocs mkdocs-material

# Запустити dev-сервер
mkdocs serve

# Відкрити http://127.0.0.1:8000
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
- PWA: офлайн-кеш (service worker), Web App Manifest — встановлюється на мобільних

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