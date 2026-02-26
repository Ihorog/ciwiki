# SYSTEM_WILL — Архітектура CiWiki / Cimeika

## Огляд

CiWiki — єдиний статичний сайт, що є публічним шаром (outer) і містить внутрішній світ Legend CI (inner). Сайт будується через MkDocs (Material theme) і деплоїться на GitHub Pages за адресою `https://www.cimeika.com.ua/`.

## Два шари

| Шар | Назва | Шлях | Видимість |
|-----|-------|------|-----------|
| Outer | CiWiki | `/` | Публічний |
| Inner | Legend CI | `/legend/` | Внутрішній (no public indexing) |

**Outer (CiWiki)** — документація, процеси, концепції Cimeika. Доступний для всіх.

**Inner (Legend CI)** — жива космологія Cimeika: 20 вузлів + центр Ci, організованих у шари (public / deep / examples). Позначений в UI як `[internal]`. Контент доступний статично, але не рекламується.

## Структура проєкту

```
ciwiki/
├── docs/                        # Усі джерела MkDocs
│   ├── index.md                 # Головна сторінка (outer)
│   ├── legend/                  # Inner world — Legend CI
│   │   ├── index.md             # Landing page для /legend/
│   │   ├── legend_map.html      # Автономна HTML-карта вузлів
│   │   └── <node>/index.html    # Сторінки вузлів (20 штук)
│   ├── legend_ci/               # Дані Legend CI (JSON, Markdown)
│   │   ├── legend.graph.json    # Source-of-truth граф
│   │   └── legend.nodes.md      # Згенерований список вузлів
│   ├── kazkar/legend-ci/        # Наративні розділи (7 актів)
│   └── ...                      # Інші розділи (ci, podija, тощо)
├── scripts/legend/              # Скрипти для Legend CI
├── manifest.json                # Organism manifest
├── mkdocs.yml                   # Конфігурація MkDocs
├── CNAME                        # Кастомний домен
└── .github/workflows/
    └── pages.yml                # GitHub Pages deployment workflow
```

## Навігація (глобальна)

```
[ Головна ] [ Ci ] [ ПоДія ] [ Казкар ] [ Legend CI ] [ ... ]
```

- **Головна** → `/` — стартова сторінка CiWiki
- **Legend CI** → `/legend/` — inner world

## Деплой

### GitHub Pages (автоматичний)

Workflow: `.github/workflows/pages.yml`

Тригер: `push` до гілки `main` або `workflow_dispatch`.

Кроки:
1. Checkout коду
2. Встановлення Python + MkDocs Material
3. Копіювання `SECURITY.md` → `docs/`
4. Побудова Legend CI HTML через `python scripts/legend/build_legend.py`
5. `mkdocs build` → `site/`
6. Копіювання `api/` → `site/api/`
7. Копіювання `CNAME` → `site/CNAME`
8. `actions/configure-pages` + `actions/upload-pages-artifact` + `actions/deploy-pages`

### Локальний запуск (Termux / Ubuntu)

```bash
# Встановити залежності
pip install mkdocs mkdocs-material

# Підготувати динамічні файли
cp SECURITY.md docs/
python scripts/legend/build_legend.py

# Запустити dev-сервер
mkdocs serve

# Відкрити http://127.0.0.1:8000
```

Збірка у папку `site/`:

```bash
mkdocs build
```

## Як додати нові сторінки

### У зовнішній шар (CiWiki)

1. Створіть `docs/<section>/your-page.md`
2. Додайте запис у `nav:` в `mkdocs.yml`

### У внутрішній шар (Legend CI)

1. Наративні тексти: `docs/kazkar/legend-ci/`
2. Нові вузли: оновіть `docs/legend_ci/legend.graph.json`, потім `python scripts/legend/render.py`
3. Лендінг: `docs/legend/index.md`

## Manifest

Organism manifest знаходиться у `manifest.json` (корінь репозиторію). Він декларує шари, навігаційні корені та метадані збірки/деплою.

## Безпека

- Сайт є повністю статичним (GitHub Pages, без серверних компонентів).
- Секрети зберігаються лише в GitHub Secrets, не в коді.
- `docs/SECURITY.md` генерується з кореневого `SECURITY.md` під час збірки.
