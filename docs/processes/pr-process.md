# Pull Request Process

## Загальні принципи

Pull Request (PR) є основним механізмом внесення змін у будь-який репозиторій екосистеми Cimeika. Всі зміни **обов'язково** проходять через PR процес.

## Вимоги до PR

### Обов'язкові елементи

Кожен PR **ПОВИНЕН** містити:

1. **Що змінилось** (What changed)
   - Чіткий опис змін у коді
   - Список змінених файлів з коментарями

2. **Чому змінилось** (Why)
   - Посилання на issue або опис проблеми
   - Root cause аналіз
   - Обґрунтування рішення

3. **Як верифіковано** (How it was verified)
   - Які тести пройдено
   - Результати мануальної перевірки
   - Screenshots для UI змін

4. **Оцінка ризиків** (Risk assessment)
   - Потенційні проблеми
   - Вплив на існуючий функціонал
   - Backward compatibility

5. **План відкату** (Rollback plan)
   - Як повернути зміни якщо щось піде не так
   - Які дії потрібні для rollback

### PR Template

Використовуйте [PR template](./.github/pull_request_template.md) який автоматично додається при створенні PR.

## Процес створення PR

### 1. Підготовка

```bash
# Переконайтесь що ви на останній версії main
git checkout main
git pull origin main

# Створіть feature branch
git checkout -b feature/your-feature-name
# або
git checkout -b fix/issue-description
```

### 2. Внесення змін

- Робіть atomic commits (одна логічна зміна = один commit)
- Використовуйте [commit conventions](./commit-conventions.md)
- Тестуйте зміни локально перед commit

### 3. Перевірка перед створенням PR

```bash
# Перевірте статус
git status

# Переглянте зміни
git diff

# Запустіть локальні тести
npm test  # або відповідна команда для вашого проєкту

# Запустіть лінтери
npm run lint  # якщо доступно
```

### 4. Створення PR

```bash
# Push вашої гілки
git push origin feature/your-feature-name
```

Після push:
1. Перейдіть на GitHub
2. Натисніть "Compare & pull request"
3. Заповніть всі секції PR template
4. Додайте відповідні labels
5. Призначте reviewers (якщо потрібно)
6. Створіть PR

## Review Process

### Для автора PR

1. **Відповідайте на коментарі** оперативно
2. **Робіть зміни** в тій же гілці
3. **Push додаткові commits** до тієї ж гілки
4. **Позначайте conversations as resolved** після виправлення

### Для reviewer

1. **Перевіряйте код** на відповідність стандартам
2. **Тестуйте зміни** локально якщо потрібно
3. **Залишайте конструктивні коментарі**
4. **Approve** тільки якщо всі вимоги виконані

## Автоматичні перевірки

Кожен PR автоматично проходить через:

- **Linting** — перевірка стилю коду
- **Tests** — виконання всіх тестів
- **Security checks** — CodeQL та secret scanning
- **Build** — перевірка що проєкт збирається
- **Documentation** — валідація документації

PR можна мерджити **тільки** якщо всі перевірки пройшли успішно (✅).

## Merge Process

### Коли можна мерджити

PR готовий до merge коли:

- ✅ Всі автоматичні перевірки пройдені
- ✅ Отримано необхідні approvals
- ✅ Всі conversations resolved
- ✅ Немає merge conflicts
- ✅ Branch актуальний з main

### Типи merge

**Використовуйте "Squash and merge"** для більшості PR:
- Об'єднує всі commits в один
- Зберігає чисту історію main branch
- Легше робити revert якщо потрібно

**"Create a merge commit"** тільки для:
- Release branches
- Важливих milestone PR

**Ніколи не використовуйте "Rebase and merge"** — це ускладнює rollback.

### Після merge

1. Видаліть feature branch (автоматично або вручну)
2. Перевірте що main branch актуальний
3. Моніторте CI/CD для main branch
4. Якщо виникли проблеми — виконайте rollback

## Anti-repeat правило для PR

Якщо ви створюєте подібні PR неодноразово:

1. **STOP** — це сигнал проблеми
2. **Автоматизуйте** повторюваний процес
3. **Документуйте** автоматизацію
4. **Оновіть** процес щоб уникнути повторів

## Common Issues

### Merge conflicts

```bash
# Оновіть вашу гілку з main
git checkout main
git pull origin main
git checkout your-branch
git merge main

# Вирішіть конфлікти
# Після вирішення:
git add .
git commit -m "Resolve merge conflicts"
git push
```

### Failed CI checks

1. Переглянте логи failed checks
2. Виправте проблеми локально
3. Push виправлення
4. Дочекайтесь повторного запуску checks

### Неактуальний branch

```bash
# Синхронізуйте з main
git checkout your-branch
git fetch origin
git rebase origin/main
git push --force-with-lease
```

## Best Practices

1. **Робіть маленькі PR** — легше review, менше ризику
2. **Одна зміна = один PR** — не змішуйте різні функції
3. **Опис з першого разу** — не змушуйте reviewers гадати
4. **Тестуйте локально** — не покладайтесь тільки на CI
5. **Будьте responsive** — швидко відповідайте на feedback
6. **Draft PR для WIP** — використовуйте draft для незавершених змін

## Заборонено

- ❌ Прямі commits в main
- ❌ Force push до shared branches (крім випадку rebase після review)
- ❌ Merge власного PR без review (крім trivial docs)
- ❌ Ігнорування failed checks
- ❌ Secrets або credentials в коді

## Приклад гарного PR

**Title**: `feat: Add user authentication with JWT`

**Description**:
```
## Summary
**What changed:** Implemented JWT-based authentication for user login

**Why:** Required for secure API access (#123)

## Scope
- **Repo:** cit
- **Component:** auth
- **Files:** src/auth/jwt.ts, src/middleware/auth.ts

## Acceptance Checklist
- [x] Anti-repeat: Reusable auth middleware created
- [x] No-docs-secrets: Using environment variables
- [x] Tests/Checks: All tests pass, 95% coverage
- [x] Rollback: Can revert to API key auth
- [x] Builds/runs
- [x] No breaking API changes
- [x] Minimal diff / focused PR

## Notes
**Risks:** Users need to re-authenticate after deployment

**Rollback:** Revert this PR and redeploy previous version
```

## Додаткові ресурси

- [Commit Conventions](./commit-conventions.md)
- [Testing Guide](./testing.md)
- [Security Policy](../../SECURITY.md)
- [COPILOT_CANON.md](../../COPILOT_CANON.md)
