# Commit Conventions

## Загальні принципи

Чіткі та структуровані commit messages допомагають:
- 📖 Розуміти історію змін
- 🔍 Знаходити конкретні зміни
- 📝 Генерувати CHANGELOG автоматично
- 🔄 Робити revert безпечно

## Формат Commit Message

### Базова структура

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Приклад

```
feat(auth): add JWT authentication

Implement JWT-based authentication system with refresh tokens.
Uses HS256 algorithm with secret from environment variables.

Closes #123
```

## Type (обов'язковий)

Тип commit вказує на характер змін:

- **feat** — нова функціональність
- **fix** — виправлення bug
- **docs** — зміни в документації
- **style** — форматування, missing semi colons, etc (не впливає на код)
- **refactor** — рефакторинг коду (без нової функціональності або fixes)
- **perf** — покращення performance
- **test** — додавання або виправлення tests
- **build** — зміни в build system або external dependencies
- **ci** — зміни в CI конфігурації та scripts
- **chore** — інші зміни що не модифікують src або test files
- **revert** — revert попереднього commit

### Приклади types

```bash
feat: add user authentication
fix: correct validation error in login form
docs: update API documentation
style: format code with prettier
refactor: extract validation logic to separate module
perf: optimize database queries
test: add unit tests for auth service
build: update webpack configuration
ci: add codecov integration
chore: update dependencies
revert: revert "feat: add user authentication"
```

## Scope (опціональний)

Scope вказує на частину проєкту що змінюється:

**Приклади scope**:
- `auth` — authentication/authorization
- `api` — API endpoints
- `db` — database
- `ui` — user interface
- `config` — configuration
- `deps` — dependencies

```bash
feat(auth): add password reset
fix(api): handle null response
docs(readme): update installation steps
```

**Можна пропустити** якщо зміни стосуються всього проєкту:

```bash
docs: update contributing guidelines
chore: update all dependencies
```

## Subject (обов'язковий)

Коротке описання зміни:

### Правила

1. **Imperative mood** — "add" не "added" чи "adds"
2. **No capitalization** — lowercase first letter
3. **No period** — без крапки в кінці
4. **Max 50 characters** — коротко та ясно

### ✅ Good examples

```
add user authentication
fix memory leak in cache
update installation docs
remove deprecated API
```

### ❌ Bad examples

```
Added user authentication  ❌ (past tense)
Fix Memory Leak           ❌ (capitalized)
update docs.              ❌ (period at end)
This commit updates the documentation for the new API endpoints ❌ (too long)
```

## Body (опціональний)

Детальний опис змін:

### Коли потрібен body

- Складні зміни що потребують пояснення
- Breaking changes
- Архітектурні рішення
- Технічні деталі

### Правила

1. Відокремлений **пустим рядком** від subject
2. **Wrap at 72 characters** для читабельності
3. Пояснює **"що" та "чому"**, не "як"
4. Може містити декілька параграфів

### Приклад

```
feat(auth): implement OAuth2 flow

Add OAuth2 authentication with support for Google and GitHub
providers. Users can now login using their social accounts.

This change improves user experience by reducing friction during
signup process. Implementation follows OAuth2 RFC 6749 standard.

Technical details:
- Using passport.js for OAuth strategies
- Tokens stored in secure HTTP-only cookies
- Added refresh token rotation for security
```

## Footer (опціональний)

Metadata про commit:

### Breaking Changes

Для breaking changes використовуйте `BREAKING CHANGE:`:

```
feat(api): change authentication endpoint

BREAKING CHANGE: Authentication endpoint moved from /auth to /api/v2/auth.
All clients must update their API calls.

Migration guide:
- Update API_URL from `/auth` to `/api/v2/auth`
- Add API version header: `X-API-Version: 2`
```

### Issue References

Link до issues або PR:

```
fix(api): handle timeout errors

Properly handle timeout errors and return 408 status code.

Fixes #123
Closes #456
Related to #789
```

**Keywords**:
- `Fixes #123` — closes issue automatically
- `Closes #123` — closes issue automatically
- `Resolves #123` — closes issue automatically
- `Related to #123` — створює reference (не закриває)

## Спеціальні випадки

### Revert Commits

```
revert: feat(auth): add JWT authentication

This reverts commit 1234567890abcdef.

Reason: JWT implementation caused performance issues in production.
```

### Merge Commits

GitHub автоматично створює merge commits. Якщо робите manual merge:

```
Merge branch 'feature/user-auth' into main

Merged PR #123: Add user authentication
```

### Multiple Changes

**Не робіть це** — розділіть на кілька commits:

```
❌ feat: add login, fix logout, update docs
```

**Робіть окремі commits**:

```
✅ feat(auth): add login functionality
✅ fix(auth): correct logout redirect
✅ docs(auth): update authentication guide
```

## Workflow Examples

### Feature Development

```bash
# Створення нової функціональності
git commit -m "feat(user): add user profile page"
git commit -m "test(user): add tests for profile page"
git commit -m "docs(user): document profile page API"
```

### Bug Fix

```bash
# Simple bug fix
git commit -m "fix(api): handle null user response"

# Complex bug fix з body
git commit -m "fix(api): prevent race condition in user creation

Add mutex lock to prevent concurrent user creation with same email.
This fixes intermittent duplicate user errors in production.

Fixes #456"
```

### Refactoring

```bash
git commit -m "refactor(auth): extract validation logic

Move validation from controller to separate validator class.
Improves testability and code organization."
```

### Documentation

```bash
git commit -m "docs(readme): update installation instructions"
git commit -m "docs(api): add examples for authentication endpoints"
```

## Commit Frequency

### Коли комітити

- ✅ Після завершення логічної зміни
- ✅ Коли код компілюється і tests проходять
- ✅ Перед переключенням на іншу задачу
- ✅ В кінці робочого дня (WIP commits)

### Atomic Commits

Кожен commit повинен бути **atomic** — одна логічна зміна:

```bash
# ✅ GOOD - atomic commits
git commit -m "feat(auth): add login form"
git commit -m "feat(auth): add login API endpoint"
git commit -m "test(auth): add login tests"

# ❌ BAD - non-atomic
git commit -m "add complete authentication system with tests and docs"
```

## WIP Commits

Для незавершеної роботи:

```bash
# Save work in progress
git commit -m "wip: implement user profile (incomplete)"

# Continue next day
# ...make changes...

# Squash WIP commits before PR
git rebase -i HEAD~3
# Squash WIP commits into meaningful commit
```

## Commit Hooks

### Pre-commit

Автоматично перевіряє commit message:

```bash
# Install commitlint
npm install --save-dev @commitlint/{cli,config-conventional}

# Configure
echo "module.exports = {extends: ['@commitlint/config-conventional']}" > commitlint.config.js

# Setup hook
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit "$1"'
```

### Pre-commit checks

```bash
# .husky/pre-commit
npm run lint
npm test
```

## Tools

### Commitizen

Interactive tool для створення commits:

```bash
# Install
npm install -g commitizen cz-conventional-changelog

# Use
git cz
```

Output:
```
? Select the type of change: (Use arrow keys)
❯ feat:     A new feature
  fix:      A bug fix
  docs:     Documentation only changes
  style:    Changes that don't affect code meaning
  refactor: A code change that neither fixes a bug nor adds a feature
  perf:     A code change that improves performance
  test:     Adding missing tests
```

### Conventional Changelog

Автоматична генерація CHANGELOG:

```bash
npm install -g conventional-changelog-cli
conventional-changelog -p angular -i CHANGELOG.md -s
```

## Reviewing Commits

### Git Log

```bash
# Readable log
git log --oneline --graph --decorate

# Filter by type
git log --oneline --grep="^feat"
git log --oneline --grep="^fix"

# Show commits for specific file
git log --oneline -- path/to/file

# Show commits by author
git log --author="username"
```

### Finding Changes

```bash
# Find when bug was introduced
git log --grep="fix.*login"

# Find all breaking changes
git log --grep="BREAKING CHANGE"

# Find commits affecting specific feature
git log --grep="feat.*auth"
```

## Ammending Commits

### Last Commit

```bash
# Change last commit message
git commit --amend -m "fix(auth): correct typo in validation"

# Add forgotten files to last commit
git add forgotten-file.js
git commit --amend --no-edit
```

### Multiple Commits (Interactive Rebase)

```bash
# Edit last 3 commits
git rebase -i HEAD~3

# Options:
# pick = keep commit
# reword = keep commit but edit message
# edit = pause to amend commit
# squash = merge into previous commit
# fixup = like squash but discard message
# drop = remove commit
```

**Важливо**: Не rebase commits що вже в main або shared branch!

## Best Practices

### Do's ✅

1. ✅ Write clear, concise messages
2. ✅ Use conventional format
3. ✅ Reference issues
4. ✅ Explain "why" not "what"
5. ✅ Make atomic commits
6. ✅ Test before commit
7. ✅ Proofread messages

### Don'ts ❌

1. ❌ Vague messages ("fix bug", "update code")
2. ❌ Too long subject lines
3. ❌ Mix multiple changes
4. ❌ Commit broken code
5. ❌ Commit secrets or credentials
6. ❌ Use past tense
7. ❌ Skip type prefix

## Examples Library

### Features

```
feat(search): add fuzzy search capability
feat(ui): implement dark mode
feat(api): add pagination to user list
feat(export): support CSV export
```

### Fixes

```
fix(login): prevent double form submission
fix(api): handle timeout gracefully
fix(ui): correct button alignment on mobile
fix(validation): accept international phone numbers
```

### Documentation

```
docs(readme): add quick start guide
docs(api): document error responses
docs(contributing): update PR process
docs(changelog): add version 2.0.0 notes
```

### Performance

```
perf(db): optimize user query with indexes
perf(api): add caching layer
perf(ui): lazy load images
```

### Tests

```
test(auth): add integration tests
test(api): increase coverage to 90%
test(ui): add e2e tests for checkout
```

## Troubleshooting

### Wrong Commit Message

```bash
# Change last commit message
git commit --amend

# Change older commit
git rebase -i HEAD~5  # go back 5 commits
# Change 'pick' to 'reword' for commits to edit
```

### Committed to Wrong Branch

```bash
# Move last commit to another branch
git checkout correct-branch
git cherry-pick wrong-branch
git checkout wrong-branch
git reset --hard HEAD~1
```

## Додаткові ресурси

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit)
- [PR Process](./pr-process.md)
- [Git Best Practices](https://git-scm.com/book/en/v2)

## Питання?

Створіть issue з label "documentation" якщо щось незрозуміло.
