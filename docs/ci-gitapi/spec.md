# CI GitAPI · Специфікація

> **Canonical reference** для всіх вузлів Cimeika, що звертаються до CI GitAPI Gateway.  
> Затверджені зміни вносяться через PR до `ciwiki` main.

---

## 1. Призначення

CI GitAPI є **єдиним шлюзом доступу** до адміністративних функцій Cimeika:

- централізована авторизація всіх міжсервісних запитів
- координація Git-операцій між репозиторіями
- точка управління автоматизацією та workflow
- маршрутизація команд до відповідних модулів

Жоден сервіс екосистеми **не звертається до іншого сервісу безпосередньо** — лише через CI GitAPI.

---

## 2. Gateway Endpoints

### Системні

| Endpoint | Метод | Призначення |
|----------|-------|-------------|
| `/health` | `GET` | Перевірка стану gateway |
| `/v1/status` | `GET` | Статус усіх підключених сервісів |
| `/v1/ecosystem` | `GET` | Карта екосистеми Cimeika |

### Webhooks

| Endpoint | Метод | Призначення |
|----------|-------|-------------|
| `/webhooks` | `POST` | Приймає webhook-події від GitHub та інших джерел |

### Dashboard

| Endpoint | Метод | Призначення |
|----------|-------|-------------|
| `/dashboard` | `GET` | Адміністративний огляд стану системи |

### API v1

| Endpoint | Метод | Призначення |
|----------|-------|-------------|
| `/api/v1` | `GET` | Кореневий endpoint API |
| `/api/v1/automation` | `POST` | Запуск автоматизованих дій (PR, workflow trigger тощо) |
| `/api/v1/automation/pr` | `POST` | Створення Pull Request через automation |

### Git та Logic

| Endpoint | Метод | Призначення |
|----------|-------|-------------|
| `/v1/git/*` | `GET/POST` | Git-операції: читання стану репозиторіїв, тригери |
| `/v1/logic/*` | `POST` | Виконання бізнес-логіки екосистеми |

### Пам'ять та завдання

| Endpoint | Метод | Призначення |
|----------|-------|-------------|
| `/memory/*` | `GET/POST` | Читання та запис до `ci-memory` |
| `/todo` | `GET/POST` | Управління завданнями системи |

---

## 3. Авторизація

Усі запити до CI GitAPI потребують авторизаційного токена.

- Токени зберігаються виключно у **GitHub Secrets** або environment-конфігурації.
- Жодного хардкодування credentials у коді або документації.
- Деталі управління секретами: [Secrets Management](../processes/secrets-management.md).

---

## 4. Автоматизація PR

Ендпоінт `/api/v1/automation/pr` приймає такий payload:

```json
{
  "repo": "Ihorog/cimeika-unified",
  "base": "main",
  "branch": "feature/my-branch",
  "title": "Назва Pull Request",
  "files": [
    {
      "path": "path/to/file.md",
      "action": "create",
      "content": "..."
    }
  ]
}
```

| Поле | Тип | Обов'язкове | Опис |
|------|-----|-------------|------|
| `repo` | string | ✅ | `owner/repo` |
| `base` | string | ✅ | Цільова гілка для merge |
| `branch` | string | ✅ | Гілка з змінами |
| `title` | string | ✅ | Заголовок PR |
| `files` | array | ✅ | Список файлів (action: `create`/`update`/`delete`) |

---

## 5. Моніторинг

CI GitAPI моніторується через ability **Check CI Runs**:

- Workflow: `.github/workflows/check-ci-gitapi-runs.yml`
- Ціль: `Ihorog/ci_gitapi`
- Ліміт: останні 7 runs
- Специфікація: [Check CI Runs](../abilities/check_ci_runs/README.md)

---

## 6. Стани gateway

| Стан | Опис |
|------|------|
| `healthy` | Усі ендпоінти доступні, сервіси підключені |
| `degraded` | Частина сервісів недоступна; core функції працюють |
| `unavailable` | Gateway недоступний; fallback на локальний стан |

Перевірка стану: `GET /health`

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "cit": "ok",
    "cimeika-unified": "ok",
    "cimeika-backend": "ok",
    "ci-memory": "ok"
  }
}
```

---

## 7. Definition of Done

- [ ] `GET /health` повертає коректну відповідь
- [ ] `GET /v1/status` відображає статус усіх сервісів
- [ ] `POST /api/v1/automation/pr` створює PR у цільовому репозиторії
- [ ] Авторизація реалізована через GitHub Secrets
- [ ] Жоден сервіс не взаємодіє з іншим в обхід gateway
- [ ] Check CI Runs workflow активований для моніторингу
- [ ] Audit Supabase здатний підключитися через gateway

---

*Документ є частиною канонічної документації ciwiki. Зміни — через PR → review → merge.*
