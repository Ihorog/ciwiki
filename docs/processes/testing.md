# Testing Guide

## Загальні принципи

Тестування є обов'язковою частиною розробки в екосистемі Cimeika. Всі зміни коду повинні супроводжуватись відповідними тестами.

## Testing Philosophy

### Testing Pyramid

```
        /\
       /E2E\        ← Мало, але критичні
      /------\
     /Integration\  ← Середня кількість
    /------------\
   /  Unit Tests  \ ← Багато, швидкі
  /________________\
```

- **Unit Tests** (70-80%) — тестують окремі функції/методи
- **Integration Tests** (15-25%) — тестують взаємодію компонентів
- **E2E Tests** (5-10%) — тестують повні user flows

## Test Types

### 1. Unit Tests

**Мета**: Тестувати ізольовані units of code

**Характеристики**:
- Швидкі (< 10ms)
- Ізольовані (без external dependencies)
- Deterministic (завжди той самий результат)
- Focussed (один аспект за раз)

**Приклад**:

```javascript
// utils/math.js
export function add(a, b) {
  return a + b;
}

// utils/math.test.js
import { add } from './math';

describe('add', () => {
  it('should add two positive numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  it('should handle negative numbers', () => {
    expect(add(-2, 3)).toBe(1);
  });

  it('should handle zero', () => {
    expect(add(0, 5)).toBe(5);
  });
});
```

**Коли писати**:
- Для всіх utility functions
- Для business logic
- Для pure functions
- Для класів та методів

### 2. Integration Tests

**Мета**: Тестувати взаємодію між компонентами

**Характеристики**:
- Повільніші ніж unit tests (< 1s)
- Можуть використовувати реальні або mock dependencies
- Тестують взаємодію

**Приклад**:

```javascript
// api/users.integration.test.js
import request from 'supertest';
import app from '../app';
import { db } from '../database';

describe('Users API', () => {
  beforeAll(async () => {
    await db.connect();
  });

  afterAll(async () => {
    await db.disconnect();
  });

  it('should create a new user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        name: 'Test User',
        email: 'test@example.com'
      });

    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty('id');
  });
});
```

**Коли писати**:
- Для API endpoints
- Для database operations
- Для service integrations
- Для workflow tests

### 3. End-to-End (E2E) Tests

**Мета**: Тестувати повні user scenarios

**Характеристики**:
- Найповільніші (seconds to minutes)
- Використовують реальне середовище
- Тестують критичні user flows

**Приклад** (з Playwright):

```javascript
// e2e/login.spec.js
import { test, expect } from '@playwright/test';

test('user can login successfully', async ({ page }) => {
  await page.goto('https://example.com/login');

  await page.fill('input[name="email"]', 'user@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL('https://example.com/dashboard');
  await expect(page.locator('.welcome-message')).toBeVisible();
});
```

**Коли писати**:
- Для критичних user flows
- Для authentication/authorization
- Для payment processes
- Для multi-step workflows

## Test Organization

### Directory Structure

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx      ← Unit test
│   │   └── Button.stories.tsx
│   └── ...
├── services/
│   ├── auth/
│   │   ├── auth.ts
│   │   ├── auth.test.ts         ← Unit test
│   │   └── auth.integration.test.ts ← Integration test
│   └── ...
└── utils/
    ├── validation.ts
    └── validation.test.ts

tests/
├── e2e/
│   ├── login.spec.ts
│   ├── checkout.spec.ts
│   └── ...
├── integration/
│   └── api.test.ts
└── fixtures/
    └── test-data.json
```

### Naming Conventions

- Unit tests: `*.test.ts` або `*.spec.ts`
- Integration tests: `*.integration.test.ts`
- E2E tests: `*.e2e.test.ts` або `*.spec.ts` в `/e2e/`

## Test Writing Guidelines

### AAA Pattern

Arrange, Act, Assert:

```javascript
test('should calculate discount correctly', () => {
  // Arrange - підготовка
  const price = 100;
  const discountPercent = 10;

  // Act - виконання
  const result = calculateDiscount(price, discountPercent);

  // Assert - перевірка
  expect(result).toBe(90);
});
```

### Test Coverage

**Мінімальні вимоги**:
- Overall coverage: >= 80%
- Branch coverage: >= 75%
- Function coverage: >= 85%
- Line coverage: >= 80%

**Перевірка coverage**:

```bash
npm test -- --coverage
```

### What to Test

**DO** test:
- ✅ Public APIs
- ✅ Business logic
- ✅ Edge cases
- ✅ Error handling
- ✅ Critical paths
- ✅ User interactions

**DON'T** test:
- ❌ Third-party libraries
- ❌ Framework internals
- ❌ Trivial getters/setters
- ❌ Generated code

### Test Quality

**Good test characteristics**:
1. **Fast** — швидко виконується
2. **Isolated** — не залежить від інших tests
3. **Repeatable** — детермінований результат
4. **Self-validating** — чіткий pass/fail
5. **Timely** — написаний вчасно (TDD/BDD)

## Mocking

### Коли використовувати mocks

- External API calls
- Database operations (для unit tests)
- Time-dependent functions
- Random number generators
- File system operations

### Приклад mocking

```javascript
// Using Jest
import { fetchUserData } from './api';
import axios from 'axios';

jest.mock('axios');

test('should fetch user data', async () => {
  // Mock axios response
  axios.get.mockResolvedValue({
    data: { id: 1, name: 'Test User' }
  });

  const user = await fetchUserData(1);

  expect(user.name).toBe('Test User');
  expect(axios.get).toHaveBeenCalledWith('/api/users/1');
});
```

## Testing Environments

### Local Development

```bash
# Run all tests
npm test

# Watch mode (re-run on changes)
npm test -- --watch

# Run specific test file
npm test -- path/to/test.ts

# Run with coverage
npm test -- --coverage
```

### CI/CD

Tests автоматично запускаються на CI при:
- Push до будь-якої гілки
- Створенні PR
- Merge до main

**Конфігурація** (`.github/workflows/test.yml`):

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@v3
```

## Test-Driven Development (TDD)

### Red-Green-Refactor Cycle

1. **Red** — напишіть failing test
2. **Green** — напишіть мінімальний код щоб test passed
3. **Refactor** — покращте код, tests залишаються green

```javascript
// 1. RED - напишіть test
test('should validate email format', () => {
  expect(isValidEmail('test@example.com')).toBe(true);
  expect(isValidEmail('invalid-email')).toBe(false);
});

// 2. GREEN - мінімальна реалізація
function isValidEmail(email) {
  return email.includes('@');
}

// 3. REFACTOR - покращення
function isValidEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}
```

## Debugging Tests

### Failed Test Analysis

1. **Read error message** уважно
2. **Check test assumptions** — чи правильні очікування?
3. **Add console.log** для debug output
4. **Run in isolation** — виключіть вплив інших tests
5. **Check test data** — чи правильні fixtures?

### Debug Commands

```bash
# Run single test
npm test -- -t "test name"

# Run with verbose output
npm test -- --verbose

# Debug with Node inspector
node --inspect-brk node_modules/.bin/jest --runInBand

# Run only failed tests
npm test -- --onlyFailures
```

## Performance Testing

### Load Testing

Для API endpoints:

```javascript
import autocannon from 'autocannon';

test('API performance', async () => {
  const result = await autocannon({
    url: 'http://localhost:3000/api/users',
    connections: 10,
    duration: 10
  });

  expect(result.requests.mean).toBeGreaterThan(100); // RPS
  expect(result.latency.p99).toBeLessThan(1000); // ms
});
```

## Flaky Tests

### Avoiding Flakiness

- ❌ Не використовуйте `setTimeout` без причини
- ✅ Використовуйте `waitFor` functions
- ❌ Не покладайтесь на execution order (якщо не explicit)
- ✅ Очищайте state між tests
- ❌ Не використовуйте hardcoded dates
- ✅ Mock time functions

### Fixing Flaky Tests

```javascript
// BAD - flaky
test('should update after delay', () => {
  updateAsync();
  setTimeout(() => {
    expect(getData()).toBe('updated');
  }, 100); // Може бути недостатньо часу
});

// GOOD - stable
test('should update after delay', async () => {
  await updateAsync();
  await waitFor(() => {
    expect(getData()).toBe('updated');
  });
});
```

## Security Testing

### Input Validation

```javascript
test('should reject SQL injection attempts', () => {
  const maliciousInput = "'; DROP TABLE users; --";
  expect(() => {
    queryUser(maliciousInput);
  }).toThrow('Invalid input');
});
```

### Authentication Tests

```javascript
test('should reject unauthorized requests', async () => {
  const response = await request(app)
    .get('/api/admin/users')
    .set('Authorization', 'Bearer invalid-token');

  expect(response.status).toBe(401);
});
```

## Best Practices

### Do's

1. ✅ Пишіть tests для всіх нових features
2. ✅ Тестуйте edge cases та error paths
3. ✅ Використовуйте descriptive test names
4. ✅ Keep tests simple та readable
5. ✅ Isolate tests from each other
6. ✅ Run tests locally перед push
7. ✅ Maintain test coverage

### Don'ts

1. ❌ Не skip tests без причини
2. ❌ Не пишіть flaky tests
3. ❌ Не тестуйте implementation details
4. ❌ Не використовуйте production data
5. ❌ Не ігноруйте failed tests
6. ❌ Не пишіть over-complicated tests

## Test Reporting

### Coverage Reports

Генеруються автоматично при запуску:

```bash
npm test -- --coverage
```

Звіти доступні в:
- Console output
- `coverage/lcov-report/index.html`
- CI/CD (Codecov, Coveralls)

### Test Results

```
Test Suites: 5 passed, 5 total
Tests:       45 passed, 45 total
Snapshots:   0 total
Time:        5.234 s
Coverage:    85.3%
```

## Tools & Frameworks

### JavaScript/TypeScript

- **Jest** — universal test framework
- **Mocha + Chai** — alternative framework
- **Vitest** — fast, modern test runner
- **Playwright** — E2E testing
- **Testing Library** — UI component testing

### CI Integration

- GitHub Actions
- CircleCI
- Travis CI
- Jenkins

## Troubleshooting

### Common Issues

**Tests timeout**:
```javascript
// Збільште timeout
test('long operation', async () => {
  // ...
}, 10000); // 10 seconds
```

**Module not found**:
- Перевірте `jest.config.js` moduleNameMapper
- Встановіть missing dependencies

**Snapshot mismatches**:
```bash
# Update snapshots
npm test -- -u
```

## Continuous Improvement

1. **Review test failures** регулярно
2. **Refactor tests** коли рефакторите код
3. **Monitor coverage trends** — не дозволяйте падати
4. **Share knowledge** — code reviews для tests
5. **Update practices** — документуйте lessons learned

## Додаткові ресурси

- [PR Process](./pr-process.md)
- [Commit Conventions](./commit-conventions.md)
- [CI/CD Guide](./ci-cd.md)
- [Security Policy](../SECURITY.md)

## Питання?

Створіть issue з label "testing" або звертайтесь до testing guild.
