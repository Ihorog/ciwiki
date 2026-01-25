# Налаштування GitHub Pages для CiWiki

## Статус системи

✅ **Автоматична публікація налаштована та працює**

- **Workflow**: `.github/workflows/ciwiki-pages.yml` - активний
- **Гілка деплою**: `gh-pages` - автоматично оновлюється
- **Останній деплой**: Успішний (перевірте [Actions](https://github.com/Ihorog/ciwiki/actions))
- **Домен**: `www.cimeika.com.ua` (налаштовано через CNAME)

## Як працює публікація

### 1. Процес автоматичного деплою

```
Push to main → GitHub Actions → MkDocs Build → Deploy to gh-pages → GitHub Pages
```

При кожному `push` до гілки `main`:

1. **GitHub Actions** запускає workflow `ciwiki-pages.yml`
2. **MkDocs** будує статичний сайт з файлів у `docs/`
3. **peaceiris/actions-gh-pages** деплоїть сайт до гілки `gh-pages`
4. **GitHub Pages** публікує контент з гілки `gh-pages`

### 2. Необхідні налаштування в GitHub

⚠️ **ВАЖЛИВО**: Потрібно налаштувати GitHub Pages вручну (один раз)

#### Крок 1: Відкрийте налаштування репозиторію

1. Перейдіть до репозиторію: https://github.com/Ihorog/ciwiki
2. Клікніть на вкладку **Settings** (Налаштування)
3. У лівому меню знайдіть розділ **Pages** (у секції "Code and automation")

#### Крок 2: Налаштуйте джерело публікації

У розділі **"Build and deployment"**:

1. **Source** (Джерело): Виберіть **"Deploy from a branch"**
2. **Branch** (Гілка): 
   - Виберіть `gh-pages`
   - Директорія: `/ (root)`
3. Натисніть **Save**

#### Крок 3: Налаштуйте Custom Domain (опційно, якщо використовується)

У розділі **"Custom domain"**:

1. Введіть: `www.cimeika.com.ua`
2. Натисніть **Save**
3. Дочекайтесь DNS check (може зайняти кілька хвилин)
4. Увімкніть **"Enforce HTTPS"** після успішної перевірки DNS

#### Крок 4: Перевірка

Після налаштування ви побачите зелене повідомлення:

```
✅ Your site is live at https://www.cimeika.com.ua
```

або (без custom domain):

```
✅ Your site is live at https://ihorog.github.io/ciwiki/
```

## Структура проєкту

### Вихідні файли документації

```
ciwiki/
├── docs/                          # Джерело документації
│   ├── index.md                   # Головна сторінка
│   ├── processes/                 # Документація процесів
│   ├── Legend-ci/                 # Легенда Ci
│   ├── Cimeika/                   # Документація проєкту
│   └── ...
├── mkdocs.yml                     # Конфігурація MkDocs
├── CNAME                          # Custom domain
└── .github/workflows/
    └── ciwiki-pages.yml          # Workflow для деплою
```

### Зібраний сайт (гілка gh-pages)

```
gh-pages/
├── index.html                     # Головна сторінка сайту
├── .nojekyll                      # Вимикає Jekyll на GitHub Pages
├── processes/                     # Статичні HTML файли
├── assets/                        # CSS, JS, images
└── ...                            # Інші згенеровані файли
```

## Перевірка статусу деплою

### Через GitHub Actions

1. Перейдіть до: https://github.com/Ihorog/ciwiki/actions
2. Знайдіть останній run **"Build & Deploy CiWiki"**
3. Перевірте статус:
   - ✅ зелена галочка = успішно
   - ❌ червоний хрестик = помилка (перегляньте логи)

### Через гілку gh-pages

1. Перейдіть до: https://github.com/Ihorog/ciwiki/tree/gh-pages
2. Перевірте:
   - Наявність `index.html`
   - Наявність `.nojekyll`
   - Дату останнього коміту (має бути недавня)

### Через веб-сайт

1. Відкрийте: https://www.cimeika.com.ua (або https://ihorog.github.io/ciwiki/)
2. Перевірте, що контент відображається правильно
3. Перевірте навігацію та посилання

## Troubleshooting

### Проблема: Сайт не відображається (404)

**Можливі причини та рішення:**

1. **GitHub Pages не налаштований**
   - Перейдіть до Settings → Pages
   - Переконайтеся, що Source = `gh-pages` branch, `/ (root)` folder
   
2. **Гілка gh-pages порожня або не існує**
   - Перевірте: https://github.com/Ihorog/ciwiki/tree/gh-pages
   - Якщо порожня: запустіть workflow вручну (Actions → Build & Deploy CiWiki → Run workflow)

3. **DNS не налаштований для custom domain**
   - Перевірте DNS записи вашого домену
   - Має бути CNAME запис: `www.cimeika.com.ua` → `ihorog.github.io`

### Проблема: Сайт застарілий (не оновлюється)

**Рішення:**

1. Перевірте, чи запустився workflow після останнього push:
   - Actions → Build & Deploy CiWiki → перевірте timestamp
   
2. Очистіть кеш браузера:
   - Ctrl+Shift+R (Windows/Linux)
   - Cmd+Shift+R (Mac)

3. Перевірте, чи був успішним останній деплой:
   - Actions → перегляньте логи останнього run

### Проблема: Workflow падає з помилкою

**Найпоширеніші помилки:**

1. **"File not found: SECURITY.md"**
   ```bash
   # Перевірте наявність файлу
   ls -la SECURITY.md
   ```

2. **"Failed to build documentation"**
   ```bash
   # Перевірте локально
   pip install mkdocs mkdocs-material
   mkdocs build --strict
   ```
   
3. **"Permission denied"**
   - Перевірте налаштування Actions: Settings → Actions → General
   - Переконайтеся, що "Read and write permissions" увімкнено

## Локальний перегляд

Для тестування перед пушем:

```bash
# Встановлення залежностей
pip install mkdocs mkdocs-material

# Запуск dev-сервера
mkdocs serve

# Відкрити http://127.0.0.1:8000
```

## Додаткова інформація

### Час оновлення

- **Збірка**: ~20-30 секунд
- **Деплой до gh-pages**: ~5-10 секунд
- **Публікація на GitHub Pages**: ~1-2 хвилини
- **DNS propagation** (для custom domain): ~5-10 хвилин (перший раз)

### Корисні посилання

- **Документація**: [Web Publishing Process](./processes/web-publishing.md)
- **Workflow конфігурація**: [ciwiki-pages.yml](https://github.com/Ihorog/ciwiki/blob/main/.github/workflows/ciwiki-pages.yml)
- **MkDocs конфігурація**: [mkdocs.yml](https://github.com/Ihorog/ciwiki/blob/main/mkdocs.yml)
- **GitHub Pages Docs**: https://docs.github.com/en/pages

## Контакти та підтримка

Якщо виникли проблеми:

1. Перевірте [Web Publishing Process](./processes/web-publishing.md)
2. Перегляньте логи в [GitHub Actions](https://github.com/Ihorog/ciwiki/actions)
3. Створіть issue з детальним описом проблеми

---

**Останнє оновлення**: 2026-01-25  
**Статус**: ✅ Активний та працює
