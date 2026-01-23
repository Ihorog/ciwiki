# CiWiki — Центр документації Cimeika

## Огляд

CiWiki є центральним репозиторієм документації та єдиним джерелом правил для всієї екосистеми Cimeika. Всі процеси, стандарти, інструкції та контракти визначаються та підтримуються тут.

## System Node

| Field         | Description                                                                          |
|---------------|--------------------------------------------------------------------------------------|
| Node Role     | Documentation, rules, and the canonical source of truth for all Cimeika nodes.       |
| Inputs        | Change requests (PRs), documentation updates, API traces.                            |
| Outputs       | Canonical instructions, standard contracts/rules, procedural approvals.               |
| Dependencies  | All other nodes depend on ciwiki for system-wide rules and documentation.             |

## Екосистема Cimeika

### Репозиторії

- **ciwiki** (цей репозиторій) — Центральна документація та правила
- **cit** — Основна кодова база проєкту Cimeika
- **cimeika-unified** — Уніфікована інтеграція компонентів
- **citt** — Тестування та інтеграційні тести
- **media** — Медіа ресурси (тільки документація)
- **cit_versel** — Заморожений репозиторій (без змін)

### Документація

#### Основні файли
- [COPILOT_CANON.md](./COPILOT_CANON.md) — Глобальні інструкції для GitHub Copilot
- [SECURITY.md](./SECURITY.md) — Політика безпеки
- [CHANGELOG.md](./CHANGELOG.md) — Історія змін

#### Процеси
- [PR процес](./docs/processes/pr-process.md) — Як створювати та обробляти Pull Request
- [Release процес](./docs/processes/release-process.md) — Процедура випуску релізів
- [Тестування](./docs/processes/testing.md) — Стандарти тестування
- [Управління секретами](./docs/processes/secrets-management.md) — Робота з credentials
- [Конвенції комітів](./docs/processes/commit-conventions.md) — Стандарти для commit messages
- [Master Issue](./docs/processes/master-issue.md) — Робота з master issues

#### Шаблони
- [Шаблон змін](./templates/change-template.md) — Обов'язковий шаблон для покрокових змін
- [PR Template](./.github/pull_request_template.md) — Шаблон Pull Request

#### Політики
- [Copilot Guard](./policies/copilot-guard.md) — Захист від витоку секретів
- [Repository Status](./policies/repository-status.md) — Статус репозиторію

## Швидкий старт

### Для розробників

1. Ознайомтесь з [COPILOT_CANON.md](./COPILOT_CANON.md) — основні правила роботи
2. Прочитайте [PR процес](./docs/processes/pr-process.md) перед створенням PR
3. Використовуйте [шаблон змін](./templates/change-template.md) для всіх змін

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
├── templates/                  # Шаблони для різних процесів
├── policies/                   # Політики та правила
├── .github/                    # GitHub конфігурація
│   ├── workflows/             # CI/CD workflows
│   └── copilot-instructions.md # Copilot інструкції
└── workflows/                  # Додаткові workflow файли
```

## CI/CD

Всі зміни проходять через автоматизовані перевірки:
- Лінтинг коду та документації
- Перевірка безпеки (CodeQL, Secret Scanning)
- Валідація структури документації
- Перевірка MkDocs збірки

Детальніше: [CI/CD документація](./docs/processes/ci-cd.md)

## Внесок змін

1. Створіть feature branch від `main`
2. Зробіть зміни згідно з відповідними process guides
3. Переконайтесь що всі тести проходять
4. Створіть PR використовуючи template
5. Дочекайтесь review та approval
6. Merge після затвердження

**Важливо**: Ніколи не комітьте напряму в `main`. Всі зміни тільки через PR.

## Підтримка

Для питань та проблем:
1. Перевірте відповідну документацію в `/docs/processes/`
2. Створіть issue з детальним описом
3. Використовуйте відповідні labels

## Audit Log

_Last documentation update based on canon: 2026-01-23 — Centralization of Documentation and Processes_.