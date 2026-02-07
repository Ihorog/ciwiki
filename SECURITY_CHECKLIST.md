# Security Checklist для CiWiki

Цей checklist допомагає забезпечити дотримання стандартів безпеки в екосистемі Cimeika.

## 📋 Зміст

- [Pre-Commit Security](#pre-commit-security)
- [Code Review Security](#code-review-security)
- [Deployment Security](#deployment-security)
- [Dependency Security](#dependency-security)
- [Documentation Security](#documentation-security)

---

## 🔒 Pre-Commit Security

### Перед кожним commit:

- [ ] **Немає секретів в коді**
  - Перевірте на наявність API keys, passwords, tokens
  - Використовуйте `.env` файли (додані в `.gitignore`)
  - Використовуйте GitHub Secrets для CI/CD

- [ ] **Немає sensitive даних в документації**
  - Немає внутрішніх URL або IP адрес
  - Немає конфіденційної інформації про інфраструктуру
  - Дотримання [Copilot Guard Policy](./docs/policies/copilot-guard.md)

- [ ] **Валідація введення**
  - Всі user inputs валідовані
  - Використовується sanitization де потрібно
  - Параметризовані queries для баз даних

- [ ] **Безпечні залежності**
  ```bash
  # Перевірка npm залежностей
  npm audit
  
  # Перевірка Python залежностей
  pip-audit
  # або
  safety check
  ```

### Інструменти для автоматизації:

```bash
# Git hooks для перевірки секретів
# Додайте в .git/hooks/pre-commit

#!/bin/bash
# Перевірка на наявність потенційних секретів
if git diff --cached | grep -E "(password|secret|key|token|api_key)" -i; then
    echo "⚠️  Можливо виявлено секрет! Перевірте код перед commit."
    exit 1
fi
```

---

## 👁️ Code Review Security

### Що перевіряти під час review:

#### Аутентифікація та Авторизація
- [ ] Перевірка прав доступу реалізована
- [ ] Сесії захищені (HttpOnly, Secure cookies)
- [ ] JWT токени правильно валідовані
- [ ] Principle of Least Privilege дотримується

#### Інжекції
- [ ] SQL injection захист (parameterized queries)
- [ ] XSS захист (escaped output)
- [ ] Command injection захист
- [ ] Path traversal захист

#### Sensitive Data
- [ ] Паролі хешовані (bcrypt, Argon2)
- [ ] Sensitive data не логується
- [ ] PII (Personally Identifiable Information) захищена
- [ ] Шифрування для sensitive даних at rest

#### Error Handling
- [ ] Не розкриває внутрішню інформацію
- [ ] Безпечні error messages для користувачів
- [ ] Детальні логи тільки для адміністраторів

---

## 🚀 Deployment Security

### Before Deployment Checklist:

#### Dependencies
- [ ] `npm audit` пройдено без критичних вразливостей
- [ ] `pip-audit` або `safety check` пройдено
- [ ] Dependabot alerts розглянуті
- [ ] Всі залежності оновлені до безпечних версій

#### Configuration
- [ ] Всі secrets в GitHub Secrets або environment variables
- [ ] Production mode увімкнено
- [ ] Debug mode вимкнено
- [ ] Secure headers налаштовані
  ```
  Strict-Transport-Security
  X-Content-Type-Options
  X-Frame-Options
  Content-Security-Policy
  ```

#### HTTPS/TLS
- [ ] HTTPS увімкнено всюди
- [ ] Valid SSL/TLS сертифікати
- [ ] TLS 1.2+ мінімум
- [ ] Redirect HTTP → HTTPS

#### Monitoring
- [ ] Логування налаштовано
- [ ] Security events моніторяться
- [ ] Alerts налаштовані для suspicious activity

---

## 📦 Dependency Security

### Regular Maintenance:

#### Weekly:
```bash
# Перевірка вразливостей npm
npm audit

# Автоматичне виправлення non-breaking
npm audit fix

# Перевірка Python залежностей
pip-audit

# Перевірка GitHub Actions
# (Dependabot автоматично створює PRs)
```

#### Monthly:
- [ ] Review всіх Dependabot PRs
- [ ] Оновлення major versions (з тестуванням)
- [ ] Видалення unused dependencies
- [ ] Audit третьосторонніх сервісів

### Dependabot Configuration

Вже налаштовано в `.github/dependabot.yml`:
- ✅ npm dependencies
- ✅ pip dependencies  
- ✅ GitHub Actions
- ✅ Weekly security updates

### Security Advisories

GitHub автоматично сканує:
- ✅ Known vulnerabilities (CVEs)
- ✅ Secret scanning
- ✅ CodeQL analysis

Перевіряйте:
- **Security tab** в GitHub
- **Dependabot alerts**
- **Security advisories**

---

## 📖 Documentation Security

### Що НЕ включати в документацію:

#### ❌ НІКОЛИ не документуйте:
- API keys, passwords, tokens
- Private SSH keys
- Database credentials
- Internal IP addresses (production)
- Internal system architecture details
- Vulnerability details до патчу

#### ✅ Безпечно документувати:
- Загальні архітектурні підходи
- Публічні API endpoints
- Environment variable names (не values!)
- Приклади з placeholder даними
- Security best practices

### Example Template для Docs:

```markdown
## Configuration

Set the following environment variables:

- `API_KEY` - Your API key (get from dashboard)
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Application secret (generate with `openssl rand -hex 32`)

### ❌ Неправильно:
API_KEY=sk_live_abc123xyz789

### ✅ Правильно:
API_KEY=your_api_key_here
```

---

## 🛡️ Copilot Guard Policy

Дотримуйтесь [Copilot Guard Policy](./docs/policies/copilot-guard.md):

### Правила для AI Agents:

1. **Ніколи не генерувати**:
   - Реальні credentials
   - Production secrets
   - Private keys
   - Real database URLs

2. **Завжди використовувати placeholders**:
   ```
   API_KEY=your_api_key_here
   DATABASE_URL=postgresql://user:password@localhost/db
   SECRET=your-secret-here
   ```

3. **Перевіряти before commit**:
   - Regex scan for secrets
   - Manual review sensitive files
   - Test with dummy data

---

## 🔐 Security Testing

### Automated Testing:

```bash
# CodeQL Analysis (автоматично в CI)
# Перевіряє на:
# - SQL injection
# - XSS vulnerabilities
# - Command injection
# - Path traversal
# - і інше

# Secret Scanning (автоматично в GitHub)
# Виявляє leaked credentials
```

### Manual Testing:

#### Checklist для Manual Security Review:
- [ ] Authentication bypass tests
- [ ] Authorization tests (різні ролі)
- [ ] Input validation tests (boundary values)
- [ ] Error handling tests
- [ ] Session management tests
- [ ] CSRF protection tests

---

## 📊 Security Metrics

### Track and Monitor:

1. **Time to Patch**
   - Critical: < 24 hours
   - High: < 7 days
   - Medium: < 30 days

2. **Vulnerability Count**
   - Target: 0 critical, 0 high
   - Monitor Dependabot dashboard

3. **Security Training**
   - All team members trained
   - Annual refreshers

4. **Audit Frequency**
   - Code reviews: Every PR
   - Dependency audits: Weekly
   - Infrastructure review: Quarterly
   - Penetration testing: Annually

---

## 🚨 Incident Response

### If Security Breach Detected:

#### Immediate (Hour 0):
1. **Contain**
   - Disable compromised accounts
   - Block suspicious IPs
   - Isolate affected systems

2. **Preserve Evidence**
   - Don't delete logs
   - Snapshot affected systems
   - Document timeline

3. **Notify**
   - Security team immediately
   - Follow [SECURITY.md](./SECURITY.md) protocol

#### Short-term (Hours 1-24):
1. **Assess Impact**
   - What data was accessed?
   - What systems affected?
   - Who is impacted?

2. **Root Cause Analysis**
   - How did breach occur?
   - What vulnerability exploited?

3. **Begin Remediation**
   - Patch vulnerability
   - Reset credentials
   - Update access controls

#### Long-term (Days 1-30):
1. **Complete Remediation**
   - All systems patched
   - All affected users notified
   - Monitoring enhanced

2. **Post-Mortem**
   - Document incident
   - Lessons learned
   - Update procedures

3. **Prevention**
   - Update security measures
   - Improve detection
   - Train team

---

## ✅ Quick Reference

### Daily:
- [ ] Review security alerts
- [ ] Monitor logs for anomalies

### Weekly:
- [ ] `npm audit` & `pip-audit`
- [ ] Review Dependabot PRs
- [ ] Check security tab

### Monthly:
- [ ] Update dependencies
- [ ] Review access controls
- [ ] Security training reminder

### Quarterly:
- [ ] Infrastructure security review
- [ ] Update SECURITY.md
- [ ] Penetration testing prep

### Annually:
- [ ] Comprehensive security audit
- [ ] Penetration testing
- [ ] Policy review and update

---

## 📚 Resources

### Internal:
- [SECURITY.md](./SECURITY.md) - Security Policy
- [Copilot Guard](./docs/policies/copilot-guard.md) - AI Safety
- [Secrets Management](./docs/processes/secrets-management.md) - Credential handling

### External:
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [npm Security Best Practices](https://docs.npmjs.com/security-best-practices)
- [Python Security Guide](https://python.readthedocs.io/en/latest/library/security_warnings.html)

---

## 🎯 Remember

> **Security is everyone's responsibility**

- 🔒 Never commit secrets
- 🛡️ Always validate input
- 📊 Keep dependencies updated
- 👁️ Monitor for anomalies
- 🚨 Report issues immediately

**Last Updated**: 2026-02-01  
**Next Review**: 2026-05-01
