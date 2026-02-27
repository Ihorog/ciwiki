# Ability: audit_supabase

> **Status**: dormant  
> **Module ID**: `audit_supabase`  
> **Canonical repo**: `Ihorog/ciwiki` (spec only)  
> **Consumer repos**: `Ihorog/cit`, `Ihorog/ci_gitapi`, `Ihorog/cimeika-unified`, `Ihorog/cimeika-backend`, `Ihorog/ci-memory`

---

## Призначення (Purpose)

`audit_supabase` — здатність читати стан бази даних Supabase через `psql` і записувати детерміністичний JSON-артефакт у `audit_out/`.

**Коли активується**:

- Ручний запуск (`workflow_dispatch`) для on-demand аудиту.
- Scheduled trigger (наприклад, раз на добу) для моніторингу стану БД.
- Як pre-step у release pipeline, щоб зафіксувати стан перед деплоєм.
- Після інцидентів — для збереження forensic snapshot.

**Коли НЕ активується**:

- `media` — репо лише для документації, без runtime-доступу до БД.
- Репо без доступу до Supabase (відсутній секрет `SUPABASE_DB_URL`).

---

## Необхідні змінні оточення (Required env vars)

| Змінна | Джерело | Обов'язкова | Опис |
|--------|---------|-------------|------|
| `SUPABASE_DB_URL` | GitHub Secret | ✅ | PostgreSQL connection string (`postgres://user:pass@host:5432/db`). **Ніколи не зберігати в репо.** |
| `OUT_DIR` | Env / workflow input | ✅ | Директорія для запису результатів. Рекомендовано: `audit_out`. |
| `EXECUTED_BY` | Env / workflow context | ✅ | Хто/що запустило аудит: `github-actions`, `termux`, `manual`, тощо. |
| `PROJECT_REF` | Env / workflow input | ✅ | Ідентифікатор проєкту Supabase (або repo slug). Використовується у `meta.project_ref`. |
| `PSQL_TIMEOUT_SEC` | Env / default | ✅ | Таймаут підключення `psql`. За замовчуванням: `30`. |
| `SOFT_FAIL` | Env / default | ✅ | Якщо `1` — помилки підключення не зупиняють workflow (exit 0). За замовчуванням: `1`. |

> **Безпека**: `SUPABASE_DB_URL` зберігається **тільки** у GitHub Actions Secrets відповідного репозиторію.  
> Ніколи не логуйте значення цієї змінної. Ніколи не додавайте її у `.env` файли в репо.

---

## Контракт виводу (Output contract)

Кожен запит записується в окремий файл: `${OUT_DIR}/<query_id>.json`.

### Обов'язкові поля (`meta` + `data`)

```json
{
  "meta": {
    "query_id": "string",
    "executed_at": "ISO-8601 timestamp",
    "executed_by": "string",
    "project_ref": "string",
    "psql_exit_code": 0,
    "duration_ms": 0
  },
  "data": []
}
```

| Поле | Тип | Опис |
|------|-----|------|
| `meta.query_id` | `string` | Унікальний slug запиту (детерміністичний, див. нижче). |
| `meta.executed_at` | `string` | ISO-8601 timestamp запуску. |
| `meta.executed_by` | `string` | Значення `EXECUTED_BY`. |
| `meta.project_ref` | `string` | Значення `PROJECT_REF`. |
| `meta.psql_exit_code` | `integer` | Exit code `psql`. `0` = успіх. |
| `meta.duration_ms` | `integer` | Час виконання запиту в мілісекундах. |
| `data` | `array` | Масив рядків результату (JSON-рядки або об'єкти). |

### Рекомендовані додаткові поля

| Поле | Тип | Опис |
|------|-----|------|
| `meta.sql_sha256` | `string` | SHA-256 хеш SQL-запиту (для audit trail). |
| `meta.data_sha256` | `string` | SHA-256 хеш серіалізованого `data` масиву. |
| `meta.error` | `string \| null` | Повідомлення про помилку (якщо `psql_exit_code != 0`). |
| `meta.db_fingerprint` | `string \| null` | Унікальний ідентифікатор БД (наприклад, `SELECT current_database()`). |

### Приклад валідного артефакту

```json
{
  "meta": {
    "query_id": "list-active-users",
    "executed_at": "2026-02-27T13:00:00Z",
    "executed_by": "github-actions",
    "project_ref": "cit",
    "psql_exit_code": 0,
    "duration_ms": 420,
    "sql_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "data_sha256": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
    "error": null,
    "db_fingerprint": "postgres"
  },
  "data": [
    {"id": 1, "email": "user@example.com", "role": "admin"}
  ]
}
```

---

## Детерміністичний `query_id` (slug)

`query_id` повинен бути:

- **Детерміністичним**: той самий запит завжди дає той самий `query_id`.
- **Slug-форматом**: лише `[a-z0-9-]`, без пробілів та спецсимволів.
- **Зрозумілим**: відображає суть запиту.

**Правила формування**:

1. Взяти назву SQL-файлу або запиту (наприклад, `List Active Users`).
2. Привести до нижнього регістру: `list active users`.
3. Замінити пробіли і `_` на `-`: `list-active-users`.
4. Видалити всі символи, крім `[a-z0-9-]`.

**Приклади**:

| Джерело | `query_id` |
|---------|-----------|
| `list_active_users.sql` | `list-active-users` |
| `check_schema_version` | `check-schema-version` |
| `Count Rows in Orders` | `count-rows-in-orders` |

---

## Сумісність (Termux та CI)

### GitHub Actions (CI)

- Скрипт запускається у `ubuntu-latest` runner.
- `psql` встановлюється через `apt-get install -y postgresql-client`.
- `SUPABASE_DB_URL` передається з GitHub Secrets.
- Таймаут задається через `PGCONNECT_TIMEOUT` env var (дорівнює `PSQL_TIMEOUT_SEC`).
- При `SOFT_FAIL=1` і помилці підключення — workflow продовжується, але `meta.error` заповнюється.

### Termux (Android)

- `psql` встановлюється: `pkg install postgresql`.
- `SUPABASE_DB_URL` встановлюється через `.env` (локально, не в репо) або `export` у терміналі.
- `OUT_DIR` може бути `~/audit_out` або будь-яка доступна директорія.
- Таймаут задається через `PGCONNECT_TIMEOUT` env var.
- Рекомендований запуск:

```bash
export SUPABASE_DB_URL="postgres://..."  # НЕ зберігати в репо
export OUT_DIR="audit_out"
export EXECUTED_BY="termux"
export PROJECT_REF="my-project"
export PSQL_TIMEOUT_SEC=30
export SOFT_FAIL=1

bash abilities/audit_supabase/audit_supabase.sh.template
```

---

## Шаблон скрипта

Дивіться [`audit_supabase.sh.template`](./audit_supabase.sh.template) — шаблон скрипта для адаптації у consumer repos.

> ⚠️ Файл є **шаблоном** (read-only reference). Перед використанням скопіюйте у своє репо та адаптуйте.

---

## Шаблон GitHub Actions workflow

Дивіться [`workflow.template.yml`](./workflow.template.yml) — шаблон workflow для consumer repos.

> ⚠️ Файл є **шаблоном** (read-only reference). Розміщуйте у `.github/workflows/` вашого репо (не в ciwiki).

---

## Rollout plan

| Крок | Репо | Статус |
|------|------|--------|
| 1. Spec документація | `Ihorog/ciwiki` | ✅ Цей PR |
| 2. Runner + workflow | `Ihorog/cit` | 🔲 Наступний PR |
| 3. Runner + workflow | `Ihorog/ci_gitapi` | 🔲 Наступний PR |
| 4. Runner + workflow | `Ihorog/cimeika-unified` | 🔲 Наступний PR |
| 5. Integration expectations | `Ihorog/cimeika-backend` | 🔲 Docs only (TypeScript/Workers) |
| 6. Docs only | `Ihorog/media` | 🔲 Docs only |

---

*Документ підтримується у `Ihorog/ciwiki`. Зміни до контракту — через PR у цей репо.*
