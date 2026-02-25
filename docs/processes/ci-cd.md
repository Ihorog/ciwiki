# CI/CD Documentation

## Огляд

CI/CD (Continuous Integration / Continuous Deployment) автоматизує процес тестування, збірки та деплою коду в екосистемі Cimeika.

## Принципи

1. **Automation First** — автоматизуємо все що можливо
2. **Fast Feedback** — швидкі результати для розробників
3. **Quality Gates** — зупиняємо bad code до production
4. **Reproducible Builds** — однаковий результат кожен раз
5. **Security by Default** — security checks на кожному етапі

## CI/CD Pipeline

### Workflow Triggers

Pipeline запускається при:

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  release:
    types: [published]
```

### Pipeline Stages

```
┌─────────────┐
│   Trigger   │
└──────┬──────┘
       │
       v
┌─────────────┐
│  Checkout   │ ← Clone repository
└──────┬──────┘
       │
       v
┌─────────────┐
│   Setup     │ ← Install dependencies
└──────┬──────┘
       │
       v
┌─────────────┐
│    Lint     │ ← Code quality checks
└──────┬──────┘
       │
       v
┌─────────────┐
│    Build    │ ← Compile/bundle
└──────┬──────┘
       │
       v
┌─────────────┐
│    Test     │ ← Run tests
└──────┬──────┘
       │
       v
┌─────────────┐
│  Security   │ ← Security scans
└──────┬──────┘
       │
       v
┌─────────────┐
│   Deploy    │ ← Deploy (if main/release)
└──────┬──────┘
       │
       v
┌─────────────┐
│   Verify    │ ← Post-deploy checks
└─────────────┘
```

## GitHub Actions Workflows

### Main CI Workflow

`.github/workflows/ci.yml`:

```yaml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@v3

  build:
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v3
        with:
          name: build
          path: dist/

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run CodeQL
        uses: github/codeql-action/analyze@v2
```

### Documentation Build

`.github/workflows/docs.yml`:

```yaml
name: Documentation

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'mkdocs.yml'

jobs:
  build-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - run: pip install mkdocs-material
      - run: mkdocs build --strict
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

## Quality Gates

### Обов'язкові перевірки

Для merge до main **ВСІ** мають пройти:

- ✅ Linting (no errors)
- ✅ Tests (100% passing)
- ✅ Coverage (>= 80%)
- ✅ Build successful
- ✅ Security scan (no critical/high)
- ✅ Code review approved

### Status Checks

```
Required status checks:
  ✓ lint
  ✓ test
  ✓ build
  ✓ security
  ✓ code-review
```

## Branch Protection

### Main Branch Rules

```yaml
Branch Protection Rules for 'main':
  ☑ Require pull request before merging
  ☑ Require approvals: 1
  ☑ Dismiss stale reviews
  ☑ Require review from Code Owners
  ☑ Require status checks to pass
  ☑ Require branches to be up to date
  ☑ Require conversation resolution
  ☐ Require signed commits (optional)
  ☑ Include administrators
  ☐ Allow force pushes: Never
  ☐ Allow deletions: Never
```

## Caching Strategies

### Node Modules Cache

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### Build Cache

```yaml
- uses: actions/cache@v3
  with:
    path: dist
    key: build-${{ github.sha }}
```

## Secrets Management

### GitHub Secrets

Налаштовані secrets:

- `NPM_TOKEN` — для publish packages
- `DEPLOY_KEY` — для deployment
- `CODECOV_TOKEN` — для coverage reporting
- `SLACK_WEBHOOK` — для notifications

### Використання

```yaml
- name: Deploy
  env:
    DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
  run: ./deploy.sh
```

## Continuous Deployment

### Staging Environment

Auto-deploy на staging при merge до `develop`:

```yaml
name: Deploy to Staging

on:
  push:
    branches: [develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v3
      - name: Deploy
        run: ./deploy-staging.sh
```

### Production Environment

Deploy на production при release:

```yaml
name: Deploy to Production

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://cimeika.com
    steps:
      - uses: actions/checkout@v3
      - name: Deploy
        run: ./deploy-production.sh
```

## Notifications

### Slack Integration

```yaml
- name: Notify Slack
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Email Notifications

GitHub автоматично відправляє email при:
- Pipeline failure
- Successful deployment
- Security alerts

## Monitoring & Observability

### Pipeline Metrics

Track:
- Build duration
- Success/failure rate
- Time to deploy
- Test coverage trends

### Dashboards

- GitHub Actions dashboard
- codecov.io для coverage
- Dependabot для dependencies

## Troubleshooting

### Common Issues

**Build fails on CI but works locally**:
- Check Node/Python versions match
- Clear cache and retry
- Check environment variables

**Tests timeout**:
- Increase timeout in workflow
- Optimize slow tests
- Use test sharding

**Deployment fails**:
- Check deployment logs
- Verify secrets configured
- Check environment status

### Debug Mode

Enable debug logging:

```yaml
- name: Debug Step
  run: |
    echo "::debug::Debug message"
  env:
    ACTIONS_STEP_DEBUG: true
```

## Best Practices

### Do's ✅

1. ✅ Keep workflows DRY (reusable workflows)
2. ✅ Use caching for dependencies
3. ✅ Run jobs in parallel when possible
4. ✅ Fail fast on errors
5. ✅ Use matrix builds для multiple versions
6. ✅ Monitor pipeline performance
7. ✅ Keep secrets secure

### Don'ts ❌

1. ❌ Hardcode secrets in workflows
2. ❌ Skip tests для "quick fixes"
3. ❌ Deploy without testing
4. ❌ Ignore failed pipelines
5. ❌ Run unnecessary jobs
6. ❌ Store artifacts indefinitely

## Documentation Validation

### MkDocs Build Check

Автоматична перевірка документації:

```yaml
name: Validate Documentation

on:
  pull_request:
    paths:
      - 'docs/**'
      - 'mkdocs.yml'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install MkDocs
        run: pip install mkdocs-material

      - name: Validate MkDocs Config
        run: mkdocs build --strict

      - name: Check Broken Links
        run: |
          pip install linkchecker
          mkdocs build
          linkchecker site/
```

### Documentation Linting

```yaml
- name: Lint Markdown
  run: |
    npm install -g markdownlint-cli
    markdownlint 'docs/**/*.md'
```

## Додаткові ресурси

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Testing Guide](./testing.md)
- [Release Process](./release-process.md)
- [Security Policy](../SECURITY.md)
