# Abilities

**Abilities** — це модульні здатності екосистеми Cimeika, що можуть бути увімкнені у відповідних репозиторіях.

Специфікації abilities зберігаються канонічно у `Ihorog/ciwiki`.  
Consumer repos впроваджують скрипти та workflows на основі цих специфікацій.

## Список abilities

| ID | Назва | Статус | Специфікація |
|----|-------|--------|--------------|
| `audit_supabase` | Audit Supabase | dormant | [README](./audit_supabase/README.md) |

## Як додати нову ability

1. Створіть директорію `docs/abilities/<ability_id>/`.
2. Додайте `README.md` зі специфікацією (призначення, env vars, output contract).
3. Додайте шаблонні файли (скрипт, workflow) як `*.template` з позначкою "read-only reference".
4. Оновіть `manifest.json` — додайте новий модуль зі `status: "dormant"`.
5. Оновіть `SYSTEM_WILL.md` — короткий запис про нову ability.
6. Додайте сторінку в `mkdocs.yml`.

## Конвенції

- **Статус `dormant`**: специфікація готова, runner ще не розгорнутий у consumer repos.
- **Статус `active`**: runner розгорнутий хоча б в одному consumer repo.
- **Шаблонні файли** (`*.template`): read-only reference, не виконувати безпосередньо з ciwiki.
- **Секрети**: ніколи не зберігати у репо; тільки GitHub Actions Secrets.
