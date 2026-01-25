# Secrets Management Guide

## Загальні принципи

Secrets (паролі, API keys, tokens, certificates) **НІКОЛИ** не повинні бути в коді або документації. Це критична вимога безпеки.

## Що таке Secret?

Secret — це будь-яка конфіденційна інформація:

- 🔑 API keys (OpenAI, AWS, etc.)
- 🔒 Паролі
- 🎫 Access tokens
- 📜 Certificates та private keys
- 🔐 Database connection strings з credentials
- 🗝️ Encryption keys
- 📧 Email credentials
- 💳 Payment gateway credentials

## Заборонено

### ❌ НЕ РОБІТЬ ЦЕ:

```javascript
// ❌ BAD - hardcoded secret
const apiKey = 'sk-1234567890abcdefghijklmnop';

// ❌ BAD - secret в коментарі
// My OpenAI key: sk-1234567890abcdefghijklmnop

// ❌ BAD - secret в commit message
git commit -m "Added API key sk-1234567890abcdefghijklmnop"
```

```yaml
# ❌ BAD - secret в конфігурації
database:
  host: db.example.com
  username: admin
  password: SuperSecret123!
```

```markdown
<!-- ❌ BAD - secret в документації -->
To use the API, use this key: hf_abcdefghijklmnopqrstuvwxyz
```

## Дозволено

### ✅ РОБІТЬ ТАК:

```javascript
// ✅ GOOD - використання змінних середовища
const apiKey = process.env.OPENAI_API_KEY;

// ✅ GOOD - перевірка наявності
if (!apiKey) {
  throw new Error('OPENAI_API_KEY environment variable is required');
}
```

```yaml
# ✅ GOOD - placeholder в документації
database:
  host: db.example.com
  username: ${DB_USERNAME}
  password: ${DB_PASSWORD}
```

```markdown
<!-- ✅ GOOD - placeholder в документації -->
To use the API, set your key in environment:
```bash
export OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```
```

## Environment Variables

### Local Development

#### .env файл (НІКОЛИ не комітити)

```bash
# .env (додайте в .gitignore!)
OPENAI_API_KEY=sk-your-actual-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/db
JWT_SECRET=your-jwt-secret
```

#### .env.example (можна комітити)

```bash
# .env.example - template для розробників
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
DATABASE_URL=postgresql://username:password@localhost:5432/database
JWT_SECRET=YOUR_JWT_SECRET
```

#### Завантаження .env

```javascript
// Використовуйте dotenv
require('dotenv').config();

// Або в ES modules
import 'dotenv/config';

// Доступ до змінних
const apiKey = process.env.OPENAI_API_KEY;
```

### .gitignore

**ОБОВ'ЯЗКОВО** додайте в `.gitignore`:

```gitignore
# Secrets
.env
.env.local
.env.*.local
*.key
*.pem
*.pfx
*.p12

# IDE
.vscode/settings.json
.idea/

# OS
.DS_Store
Thumbs.db
```

## GitHub Secrets

### Додавання Secrets

1. Перейдіть на GitHub: Repository → Settings → Secrets and variables → Actions
2. Натисніть "New repository secret"
3. Введіть:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: `sk-your-actual-key`
4. Save

### Використання в GitHub Actions

```yaml
name: CI

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: npm test
```

### Types of Secrets

- **Repository secrets** — доступні в одному репозиторії
- **Organization secrets** — доступні в усіх репозиторіях організації
- **Environment secrets** — specific до environment (production, staging)

## Secret Rotation

### Коли міняти secrets

- 🔄 Регулярно (кожні 90 днів)
- 🚨 При підозрі на компрометацію
- 👤 Коли працівник покидає команду
- 📦 Після публічного leak
- 🔒 Після security incident

### Процес ротації

1. **Генеруйте новий secret**
2. **Оновіть в GitHub Secrets**
3. **Оновіть локально** (інформуйте команду)
4. **Верифікуйте** що все працює з новим secret
5. **Видаліть старий secret** (після grace period)
6. **Документуйте** ротацію

## Secret Scanning

### Автоматичне сканування

GitHub автоматично сканує на patterns:

- OpenAI keys: `sk-[A-Za-z0-9]{20,}`
- HuggingFace tokens: `hf_[A-Za-z0-9]{20,}`
- AWS keys: `AKIA[0-9A-Z]{16}`
- Generic secrets: довгі рядки з високою ентропією

### Copilot Guard

Політика [Copilot Guard](../policies/copilot-guard.md) блокує:

1. Реальні API keys в коді/документації
2. Tokens у будь-якому форматі
3. Masked secrets (більше 32 зірочок)

### Якщо виявлено secret

**Негайні дії**:

1. 🚨 **STOP** — не комітьте
2. 🔄 **Змініть secret** негайно
3. 🧹 **Очистіть git history** (якщо вже закомітили)
4. 📝 **Документуйте incident**
5. 🔒 **Review processes** — як це сталося?

### Очистка git history

```bash
# УВАГА: Це переписує історію!
# Використовуйте BFG Repo-Cleaner
git clone --mirror https://github.com/user/repo.git
bfg --replace-text passwords.txt repo.git
cd repo.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

**Важливо**: Навіть після очистки, вважайте secret compromised і змініть його!

## Secrets в різних середовищах

### Development

```bash
# Local .env file
NODE_ENV=development
API_KEY=YOUR_DEV_API_KEY
DATABASE_URL=postgresql://localhost:5432/myapp_dev
```

### Staging

```yaml
# GitHub Actions з environment secrets
jobs:
  deploy-staging:
    environment: staging
    steps:
      - name: Deploy
        env:
          API_KEY: ${{ secrets.STAGING_API_KEY }}
```

### Production

```yaml
# GitHub Actions з production secrets
jobs:
  deploy-production:
    environment: production
    needs: approval  # Вимагає manual approval
    steps:
      - name: Deploy
        env:
          API_KEY: ${{ secrets.PRODUCTION_API_KEY }}
```

## Best Practices

### Do's ✅

1. ✅ Використовуйте environment variables
2. ✅ Додайте `.env` в `.gitignore`
3. ✅ Створюйте `.env.example` template
4. ✅ Ротуйте secrets регулярно
5. ✅ Використовуйте GitHub Secrets для CI/CD
6. ✅ Різні secrets для різних environments
7. ✅ Логуйте access до secrets (audit trail)
8. ✅ Використовуйте secret management tools (Vault, AWS Secrets Manager)
9. ✅ Encrypt secrets at rest
10. ✅ Minimum viable access (principle of least privilege)

### Don'ts ❌

1. ❌ Hardcode secrets в коді
2. ❌ Комітьте `.env` файли
3. ❌ Share secrets через Slack/Email
4. ❌ Use same secret у різних environments
5. ❌ Логуйте secrets (навіть в debug mode)
6. ❌ Store secrets в version control
7. ❌ Use default/example secrets in production
8. ❌ Share production secrets widely
9. ❌ Залишайте secrets в code comments
10. ❌ Use weak secrets (короткі, прості паролі)

## Генерація сильних secrets

### Паролі

```bash
# Генерація strong password (32 chars)
openssl rand -base64 32

# Або
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

### API Keys

```bash
# UUID v4
uuidgen

# Або custom format
node -e "console.log('sk-' + require('crypto').randomBytes(32).toString('base64'))"
```

### JWT Secrets

```bash
# Minimum 256 bits для HMAC
openssl rand -base64 32
```

## Secrets Management Tools

### Рекомендовані інструменти

- **GitHub Secrets** — для CI/CD
- **AWS Secrets Manager** — для AWS infrastructure
- **HashiCorp Vault** — enterprise solution
- **Azure Key Vault** — для Azure
- **Google Secret Manager** — для GCP
- **1Password** — для команд
- **Doppler** — unified secrets management

### Приклад з AWS Secrets Manager

```javascript
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';

async function getSecret(secretName) {
  const client = new SecretsManagerClient({ region: 'us-east-1' });

  try {
    const response = await client.send(
      new GetSecretValueCommand({ SecretId: secretName })
    );
    return JSON.parse(response.SecretString);
  } catch (error) {
    console.error('Error retrieving secret:', error);
    throw error;
  }
}

// Використання
const dbCredentials = await getSecret('prod/database/credentials');
```

## Audit та Compliance

### Logging

```javascript
// LOG secret access (але НЕ сам secret!)
logger.info('API key accessed', {
  user: currentUser,
  timestamp: new Date(),
  secretName: 'OPENAI_API_KEY',
  // ❌ НЕ логуйте: secretValue: actualKey
});
```

### Regular Audits

Checklist для security audits:

- [ ] Всі secrets в environment variables або secret manager?
- [ ] `.env` в `.gitignore`?
- [ ] Немає secrets в git history?
- [ ] Secrets ротуються регулярно?
- [ ] Різні secrets для різних environments?
- [ ] Access control налаштований правильно?
- [ ] Audit logging працює?
- [ ] Team знає practices?

## Incident Response

### Якщо secret leaked

1. **Hour 0** — виявлення leak
   - Alert security team
   - Assess scope

2. **Hour 0-1** — containment
   - Revoke compromised secret
   - Generate new secret
   - Deploy new secret

3. **Hour 1-24** — remediation
   - Remove secret з git history
   - Scan для інших leaks
   - Update documentation

4. **Day 1-7** — post-mortem
   - Root cause analysis
   - Process improvements
   - Team training

### Reporting

Internal: Створіть security incident report

External: Якщо customer data compromised:
- Notify affected parties
- Follow legal requirements
- Update security advisory

## Додаткові ресурси

- [SECURITY.md](../SECURITY.md) — Security Policy
- [Copilot Guard](../policies/copilot-guard.md) — Secret Detection Rules
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)

## Контакти

Security issues: Дивіться [SECURITY.md](../SECURITY.md) для reporting instructions.
