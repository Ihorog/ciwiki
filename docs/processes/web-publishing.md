# Web Publishing Process

## Огляд

Документація CiWiki автоматично публікується на GitHub Pages за допомогою MkDocs. Це створює зручний та доступний веб-сайт для всієї документації екосистеми Cimeika.

## Архітектура публікації

### Компоненти

```
┌─────────────────┐
│   Repository    │
│   docs/         │ ← Вихідні файли Markdown
└────────┬────────┘
         │
         v
┌─────────────────┐
│    MkDocs       │
│    Builder      │ ← Генератор статичного сайту
└────────┬────────┘
         │
         v
┌─────────────────┐
│   gh-pages      │
│   branch        │ ← Розгорнутий сайт
└────────┬────────┘
         │
         v
┌─────────────────┐
│  GitHub Pages   │
│ www.cimeika.    │ ← Публічний URL
│  com.ua         │
└─────────────────┘
```

### Основні файли

- **mkdocs.yml** - конфігурація MkDocs
- **docs/** - директорія з документацією
- **.github/workflows/ciwiki-pages.yml** - GitHub Actions workflow для деплою

## GitHub Actions Workflow

### Тригери

Workflow запускається при:

```yaml
on:
  push:
    branches: [ main ]  # При пуші до main
  workflow_dispatch:    # Ручний запуск
```

### Процес деплою

1. **Checkout коду**
   ```yaml
   - uses: actions/checkout@v6
   ```

2. **Налаштування Python**
   ```yaml
   - uses: actions/setup-python@v6
     with:
       python-version: '3.x'
   ```

3. **Встановлення залежностей**
   ```yaml
   - run: pip install mkdocs mkdocs-material
   ```

4. **Копіювання динамічних файлів**
   Workflow копіює файли що часто змінюються:
   - `SECURITY.md` → `docs/SECURITY.md` (оновлюється при кожній збірці)
   
   **Примітка**: Інші файли (COPILOT_CANON.md, Legend-ci/, templates/, policies/, .github/) 
   вже знаходяться в `docs/` і комітяться разом з іншою документацією для простоти підтримки.

5. **Збірка сайту**
   ```yaml
   - run: mkdocs build
   ```
   Генерує статичний сайт у директорії `site/`

6. **Деплой на GitHub Pages**
   ```yaml
   - uses: peaceiris/actions-gh-pages@v4
     with:
       github_token: ${{ secrets.GITHUB_TOKEN }}
       publish_dir: ./site
       publish_branch: gh-pages
   ```

## Структура документації

### Навігація

Структура навігації визначена в `mkdocs.yml`:

```yaml
nav:
  - Головна: index.md
  - Процеси:
    - Огляд: processes/index.md
    - PR Process: processes/pr-process.md
    - ...
  - Легенда Ci:
    - Огляд: Legend-ci/README.md
    - ...
  - Cimeika:
    - Ci:
      - ...
```

### Організація файлів

```
docs/
├── index.md                     # Головна сторінка
├── COPILOT_CANON.md            # Копія з кореня репозиторію
├── SECURITY.md                 # Копіюється при збірці з кореня
├── processes/                  # Процеси та інструкції
│   ├── index.md
│   ├── pr-process.md
│   ├── release-process.md
│   ├── testing.md
│   ├── ci-cd.md
│   ├── web-publishing.md       # Цей файл
│   └── ...
├── Legend-ci/                  # Легенда Ci документація (копія з "Legend ci/")
│   ├── README.md
│   ├── 00-summary.md
│   └── ...
├── Cimeika/                    # Документація проєкту
│   ├── Ci/
│   ├── Казкар/
│   └── ...
├── templates/                  # Шаблони (копія з кореня)
├── policies/                   # Політики (копія з кореня)
└── .github/                    # GitHub конфігурація (копія з кореня)
```

**Примітка про дублікати**: 
- Файли в `docs/Legend-ci/`, `docs/templates/`, `docs/policies/`, `docs/.github/` та `docs/COPILOT_CANON.md` є копіями з кореневої директорії
- `docs/SECURITY.md` автоматично оновлюється при кожній збірці
- Оригінальні файли в `Legend ci/`, `templates/`, `policies/`, `.github/` залишаються джерелом правди
- При оновленні цих файлів потрібно також оновити їх копії в `docs/`

## Локальна розробка

### Попередній перегляд

Для перегляду сайту локально:

```bash
# Встановити MkDocs
pip install mkdocs mkdocs-material

# Запустити dev-сервер
mkdocs serve
```

Сайт буде доступний за адресою: http://127.0.0.1:8000

### Збірка локально

```bash
# Зібрати сайт
mkdocs build

# Сайт буде згенеровано в директорії site/
```

### Валідація

```bash
# Збірка з strict mode (помилка при warnings)
mkdocs build --strict
```

## Конфігурація MkDocs

### Тема

Використовується Material for MkDocs:

```yaml
theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - search.suggest
    - search.highlight
```

### Плагіни

Базові плагіни включені в `mkdocs-material`:
- **search** - повнотекстовий пошук
- **navigation** - покращена навігація

## Управління посиланнями

### Внутрішні посилання

Використовуйте відносні шляхи:

```markdown
# З processes/ci-cd.md до processes/testing.md
[Testing Guide](./testing.md)

# З processes/ до Legend-ci/
[Legend Ci](../Legend-ci/README.md)

# З Cimeika/Ci/ до Legend-ci/
[Definition](../../Legend-ci/01-definition.md)
```

### Посилання на файли поза docs/

Файли з кореня репозиторію копіюються при збірці:
- `SECURITY.md` → `docs/SECURITY.md`
- `COPILOT_CANON.md` → `docs/COPILOT_CANON.md`

Посилання:
```markdown
[Security Policy](../SECURITY.md)
[Copilot Canon](../COPILOT_CANON.md)
```

## GitHub Pages налаштування

### Custom Domain

Домен налаштовано через файл `CNAME`:
```
www.cimeika.com.ua
```

### HTTPS

GitHub Pages автоматично підтримує HTTPS для custom domains.

### Branch

Сайт публікується з гілки `gh-pages`.

## Troubleshooting

### Помилки збірки

**Проблема**: `WARNING - Doc file contains a link to X which is not found`

**Рішення**: Перевірте, чи:
1. Файл існує в `docs/`
2. Шлях правильний (регістр важливий!)
3. Розширення `.md` вказане

**Проблема**: `Aborted with X warnings in strict mode`

**Рішення**: Виправте всі warnings або уберіть `--strict` з команди збірки.

### Деплой не працює

**Проблема**: Workflow запускається, але сайт не оновлюється

**Рішення**:
1. Перевірте статус workflow у GitHub Actions
2. Перевірте, чи гілка `gh-pages` оновилась
3. Перевірте Settings → Pages → Source (має бути `gh-pages`)
4. Очистіть кеш браузера

### Broken links після деплою

**Проблема**: Посилання працюють локально, але не на GitHub Pages

**Рішення**: 
- GitHub Pages case-sensitive, локальна FS може бути ні
- Перевірте регістр імен файлів і посилань

## Workflow конфлікти

### Проблема дублікатів

Якщо є кілька workflows, що намагаються публікувати на GitHub Pages, це створює конфлікти.

**Рішення**: Відключіть зайві workflows:
```bash
mv .github/workflows/duplicate.yml .github/workflows/duplicate.yml.disabled
```

Активний workflow: `ciwiki-pages.yml`

Відключені workflows:
- `docs-pages.yml.disabled` - дублікат
- `pages.yml.disabled` - webpack build (не потрібен)
- `static.yml.disabled` - публікує весь repo (небезпечно)

## Best Practices

### Do's ✅

1. ✅ Пишіть документацію в Markdown
2. ✅ Використовуйте відносні посилання
3. ✅ Тестуйте локально перед commit: `mkdocs serve`
4. ✅ Перевіряйте build warnings
5. ✅ Організуйте файли логічно
6. ✅ Оновлюйте навігацію в `mkdocs.yml`
7. ✅ При оновленні файлів в `Legend ci/`, `templates/`, `policies/` — також оновіть копії в `docs/`

### Don'ts ❌

1. ❌ Не комітьте директорію `site/` (вона генерується)
2. ❌ Не хардкодте абсолютні URL
3. ❌ Не створюйте дублікати workflows
4. ❌ Не пушіть напряму до `gh-pages` branch
5. ❌ Не змінюйте `docs/SECURITY.md` напряму (воно автоматично оновлюється з кореня)
6. ❌ Не використовуйте різні регістри для файлів
7. ❌ Не оновлюйте копії в `docs/` без оновлення оригіналів

## Підтримка копій файлів

### Процес оновлення

Коли оновлюєте файли що існують і в кореневій директорії і в `docs/`:

1. **Оновіть оригінал** в кореневій директорії
   ```bash
   # Приклад: оновлення Legend ci файлу
   vim "Legend ci/README.md"
   ```

2. **Скопіюйте в docs/**
   ```bash
   cp "Legend ci/README.md" docs/Legend-ci/README.md
   ```

3. **Закомітьте обидва**
   ```bash
   git add "Legend ci/README.md" docs/Legend-ci/README.md
   git commit -m "Update Legend ci README"
   ```

### Автоматизація (майбутнє покращення)

Це можна автоматизувати через:
- Pre-commit hook
- GitHub Action
- Makefile команда

**TODO**: Додати автоматичну синхронізацію при коміті

## Моніторинг

### Перевірка деплою

1. Перегляньте Actions: https://github.com/Ihorog/ciwiki/actions
2. Знайдіть останній run "Build & Deploy CiWiki"
3. Перевірте статус (має бути ✅)
4. Відвідайте сайт: https://www.cimeika.com.ua

### Логи

```bash
# Переглянути logs GitHub Actions
# GitHub UI → Actions → Select workflow run → View logs
```

## Додаткові ресурси

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [CI/CD Process](./ci-cd.md)
- [PR Process](./pr-process.md)

## Changelog

- **2026-01-25**: Initial web publishing implementation
  - Copied Legend ci files to docs
  - Fixed broken links
  - Updated workflow to copy all necessary files
  - Disabled conflicting workflows
