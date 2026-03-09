# Ability: check_ci_runs

> **Status**: active  
> **Module ID**: `check_ci_runs`  
> **Canonical repo**: `Ihorog/ciwiki` (spec only)  
> **Primary consumer**: `Ihorog/ci_gitapi`  
> **Other consumers**: будь-який репозиторій екосистеми Cimeika з GitHub Actions

---

## Призначення (Purpose)

`check_ci_runs` — здатність отримувати та перевіряти останні N виконань GitHub Actions у заданому репозиторії і виводити зведений звіт у GitHub Actions Job Summary.

**Коли активується**:

- Ручний запуск (`workflow_dispatch`) для on-demand перевірки стану pipeline.
- Scheduled trigger (наприклад, щогодини або раз на добу) для регулярного моніторингу.
- Як credentials-free health check після деплою або інциденту.
- Під час перегляду статусу екосистеми (звіт про останні 7 виконань).

**Коли НЕ активується**:

- `media` — репозиторій лише для документації, без CI pipeline.
- Репозиторії без GitHub Actions workflows.

---

## Необхідні змінні оточення (Required env vars)

| Змінна | Джерело | Обов'язкова | Опис |
|--------|---------|-------------|------|
| `GH_TOKEN` | GitHub Secret або `${{ secrets.GITHUB_TOKEN }}` | ✅ | Токен для доступу до GitHub API. Для перевірки іншого репо потрібен `repo:read` scope або PAT. |
| `TARGET_REPO` | Env / workflow input | ✅ | Репозиторій для перевірки у форматі `owner/repo` (напр. `Ihorog/ci_gitapi`). |
| `RUN_LIMIT` | Env / workflow input | ✅ | Кількість останніх запусків для перевірки. За замовчуванням: `7`. |
| `WORKFLOW_FILE` | Env / workflow input | ні | Назва конкретного workflow-файлу для фільтрації (напр. `ci.yml`). Якщо не задано — перевіряються всі workflows. |

> **Безпека**: якщо `TARGET_REPO` є приватним репозиторієм в іншій організації, потрібен PAT з відповідними правами.  
> Ніколи не логуйте значення `GH_TOKEN`.

---

## Контракт виводу (Output contract)

Результат виводиться у:
1. **GitHub Actions Job Summary** — таблиця з останніми N запусками.
2. **Stdout** — JSON-масив запусків для машинного читання.
3. **Артефакт** (опційно) — `ci_runs_report.json` з повними даними.

### Структура JSON-звіту

```json
{
  "meta": {
    "target_repo": "Ihorog/ci_gitapi",
    "checked_at": "ISO-8601 timestamp",
    "executed_by": "github-actions",
    "run_limit": 7,
    "workflow_filter": null
  },
  "summary": {
    "total": 7,
    "success": 5,
    "failure": 1,
    "cancelled": 0,
    "in_progress": 1
  },
  "runs": [
    {
      "run_id": 12345678,
      "workflow_name": "CI",
      "status": "completed",
      "conclusion": "success",
      "branch": "main",
      "commit_sha": "abc1234",
      "commit_message": "fix: update endpoint",
      "created_at": "ISO-8601",
      "updated_at": "ISO-8601",
      "html_url": "https://github.com/Ihorog/ci_gitapi/actions/runs/12345678"
    }
  ]
}
```

| Поле | Тип | Опис |
|------|-----|------|
| `meta.target_repo` | `string` | Репозиторій, який перевірявся. |
| `meta.checked_at` | `string` | ISO-8601 timestamp перевірки. |
| `meta.run_limit` | `integer` | Кількість запитаних запусків. |
| `summary.total` | `integer` | Загальна кількість запусків у звіті. |
| `summary.success` | `integer` | Успішні (`conclusion: success`). |
| `summary.failure` | `integer` | Невдалі (`conclusion: failure`). |
| `runs[].run_id` | `integer` | GitHub Actions run ID. |
| `runs[].status` | `string` | `queued` / `in_progress` / `completed`. |
| `runs[].conclusion` | `string \| null` | `success` / `failure` / `cancelled` / `skipped` / `null` (якщо ще виконується). |

---

## Крок впровадження у consumer repo

1. Скопіюйте `workflow.template.yml` до `.github/workflows/check-ci-runs.yml` у цільовому репо.
2. Встановіть секрет `CI_READ_TOKEN` (PAT з `repo:read`) якщо перевіряєте **інший** приватний репозиторій.
3. За потреби скопіюйте `check_ci_runs.sh.template` до `scripts/check_ci_runs.sh`.
4. Запустіть workflow вручну через GitHub UI або `gh workflow run`.

---

## Стан впровадження

| Репозиторій | Статус впровадження |
|-------------|---------------------|
| `Ihorog/ciwiki` | ✅ Workflow для ci_gitapi додано |
| `Ihorog/ci_gitapi` | 🔲 Наступний крок |
| `Ihorog/cit` | 🔲 |
| `Ihorog/cimeika-unified` | 🔲 |
