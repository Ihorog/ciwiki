# Release Process

## Загальні принципи

Release process визначає як нові версії коду випускаються в production або публічно доступними. Всі releases проходять через строгу процедуру верифікації.

## Versioning

Використовуємо [Semantic Versioning](https://semver.org/) (SemVer):

```
MAJOR.MINOR.PATCH (наприклад: 2.1.3)
```

- **MAJOR** — breaking changes (несумісні API зміни)
- **MINOR** — нова функціональність (backward compatible)
- **PATCH** — bug fixes (backward compatible)

### Pre-release versions

- **alpha** — `1.0.0-alpha.1` — ранній етап розробки
- **beta** — `1.0.0-beta.1` — feature complete, тестування
- **rc** — `1.0.0-rc.1` — release candidate

## Release Types

### 1. Patch Release (x.x.X)

**Коли**: Bug fixes, маленькі покращення, документація

**Процес**:
```bash
# Створіть hotfix branch від main
git checkout -b hotfix/v1.2.3 main

# Зробіть зміни
# ... fix bugs ...

# Оновіть версію
npm version patch -m "Release v%s"

# Оновіть CHANGELOG.md
# ... додайте зміни ...

# Створіть PR
git push origin hotfix/v1.2.3
```

### 2. Minor Release (x.X.x)

**Коли**: Нова функціональність, покращення, backward compatible

**Процес**:
```bash
# Створіть release branch
git checkout -b release/v1.3.0 develop

# Freeze feature commits, тільки bug fixes
# Оновіть версію
npm version minor -m "Release v%s"

# Оновіть CHANGELOG.md
# Тестування та верифікація

# Створіть PR до main
git push origin release/v1.3.0
```

### 3. Major Release (X.x.x)

**Коли**: Breaking changes, архітектурні зміни

**Процес**:
- Створіть детальний migration guide
- Проведіть extensive testing
- Notify всіх stakeholders заздалегідь
- Створіть backup plan

```bash
git checkout -b release/v2.0.0 develop
npm version major -m "Release v%s"
# ... решта процесу ...
```

## Pre-Release Checklist

### Code Quality

- [ ] Всі tests проходять
- [ ] Code coverage >= 80%
- [ ] Немає критичних security vulnerabilities
- [ ] Linting проходить без warnings
- [ ] Code review completed

### Documentation

- [ ] CHANGELOG.md оновлений
- [ ] README.md актуальний
- [ ] API documentation оновлена
- [ ] Migration guide (для major releases)
- [ ] Release notes підготовлені

### Testing

- [ ] Unit tests проходять
- [ ] Integration tests проходять
- [ ] E2E tests проходять (якщо є)
- [ ] Manual testing завершено
- [ ] Performance testing (для major/minor)

### Infrastructure

- [ ] Build успішний
- [ ] Dependencies оновлені
- [ ] Security audit пройдений
- [ ] Deployment scripts перевірені
- [ ] Rollback procedure documented

## Release Workflow

### 1. Підготовка

```bash
# Переконайтесь що local repo clean
git status

# Переключіться на appropriate branch
git checkout main  # для hotfix
# або
git checkout develop  # для features
git pull origin main
```

### 2. Version Bump

```bash
# Automatic version bump
npm version patch|minor|major -m "Release v%s"

# Або manual в package.json
# Не забудьте commit!
```

### 3. Оновлення CHANGELOG.md

```markdown
## [1.2.3] - 2026-01-23

### Added
- New feature X
- New feature Y

### Changed
- Updated component Z

### Fixed
- Bug fix A (#123)
- Bug fix B (#456)

### Security
- Security patch for vulnerability C
```

### 4. Release PR

Створіть PR з:
- Version bump
- CHANGELOG updates
- Документація updates

**Title**: `Release v1.2.3`

**Description**: Використайте release notes template

### 5. Review & Approval

- Automatic checks повинні пройти
- Мінімум 2 approvals для production releases
- Security team review для major releases

### 6. Merge & Tag

```bash
# Після merge PR
git checkout main
git pull origin main

# Створіть git tag
git tag -a v1.2.3 -m "Release version 1.2.3"
git push origin v1.2.3

# Tag triggers release workflow
```

### 7. GitHub Release

1. Перейдіть на GitHub → Releases
2. Натисніть "Draft a new release"
3. Виберіть tag (v1.2.3)
4. Згенеруйте release notes (або напишіть вручну)
5. Додайте artifacts якщо потрібно
6. Publish release

### 8. Post-Release

```bash
# Merge main назад в develop (якщо використовується)
git checkout develop
git merge main
git push origin develop

# Повідомте команду
# Моніторте production після deployment
```

## CHANGELOG Guidelines

### Формат

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Features in development

## [1.2.3] - 2026-01-23

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security fixes
```

### Категорії

- **Added** — нова функціональність
- **Changed** — зміни в існуючій функціональності
- **Deprecated** — функції що скоро будуть видалені
- **Removed** — видалені функції
- **Fixed** — bug fixes
- **Security** — security patches

## Release Notes Template

```markdown
# Release v1.2.3

## 🎉 Highlights

Brief summary of most important changes.

## 🚀 Features

- Feature A: Description
- Feature B: Description

## 🐛 Bug Fixes

- Fix for issue X (#123)
- Fix for issue Y (#456)

## 📝 Documentation

- Updated guide Z
- New tutorial W

## ⚠️ Breaking Changes

(тільки для major releases)

- Breaking change 1
- Migration steps

## 🔒 Security

- Security patch for CVE-XXXX-YYYY

## 📦 Dependencies

- Updated dependency A to v2.0
- Added dependency B v1.5

## 🙏 Contributors

Thanks to @user1, @user2 for contributions!

## 📚 Full Changelog

[View full changelog](link-to-compare)
```

## Hotfix Process

Для критичних bug fixes в production:

```bash
# 1. Створіть hotfix від main
git checkout -b hotfix/critical-bug main

# 2. Зробіть мінімальний fix
# ... coding ...

# 3. Version bump (patch)
npm version patch

# 4. Створіть PR з label "hotfix"
# 5. Expedited review (скорочений review process)
# 6. Merge і deploy негайно після approval
# 7. Backport до develop
```

## Rollback Procedure

Якщо release містить критичну проблему:

### 1. Immediate Rollback

```bash
# Revert до попередньої версії
git revert <release-commit-sha>
git push origin main

# Або deploy попередній tag
git checkout v1.2.2
# ... deploy ...
```

### 2. Communication

- Повідомте команду про rollback
- Створіть incident report
- Документуйте причину

### 3. Post-Mortem

- Проаналізуйте що пішло не так
- Оновіть release checklist
- Впровадьте додаткові safeguards

## Автоматизація

### GitHub Actions для Releases

Автоматично створює release коли tag pushed:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          draft: false
          prerelease: false
```

## Best Practices

1. **Regular releases** — не накопичуйте зміни
2. **Test thoroughly** — краще late ніж broken
3. **Communicate clearly** — повідомляйте про зміни
4. **Document everything** — CHANGELOG + release notes
5. **Automate when possible** — менше manual steps
6. **Have rollback plan** — завжди

## Security Releases

Для security vulnerabilities:

1. **Private disclosure** — не публічні discussions
2. **Expedited process** — priority review
3. **Security advisory** — GitHub Security Advisory
4. **CVE assignment** — якщо applicable
5. **Coordinated disclosure** — after patch available

## Заборонено

- ❌ Releases без testing
- ❌ Недокументовані breaking changes
- ❌ Пропуск version bump
- ❌ Releases з failed tests
- ❌ Hotfixes без backport

## Контакти

Для питань щодо releases:
- Створіть issue з label "release"
- Консультуйтесь з release manager
- Перевірте цю документацію

## Додаткові ресурси

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Commit Conventions](./commit-conventions.md)
- [Testing Guide](./testing.md)
