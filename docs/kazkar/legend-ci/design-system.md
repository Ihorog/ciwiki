# Дизайн-система Legend CI

> Документ описує візуальну систему та дизайн-токени для інтерактивної веб-реалізації «Легенди ci».

---

## Філософія дизайну

Дизайн «Легенди ci» базується на принципах:

* **Мінімалізм** — форма слідує за змістом
* **Контраст** — світло проти тіні, активне проти потенційного
* **Симетрія** — відображення принципу дуальності у візуалізації
* **Живість** — система дихає, рухається, реагує

> *Дизайн — це не прикраса, а спосіб думати.*

---

## Design Tokens

### Колір (Color)

#### Основна палітра

**Фон та поверхні:**
* `--color-bg`: #0d0d1a — основний фон (глибокий космічний)
* `--color-surface`: #161628 — піднесені поверхні
* `--color-border`: #2a2a4a — межі та роздільники

**Акценти:**
* `--color-accent-1`: #5b8dee — первинний акцент (холодний синій)
* `--color-accent-2`: #a78bfa — вторинний акцент (фіолетовий)
* `--color-accent-3`: #fbbf24 — тритинний акцент (золотий, рідко)

**Текст:**
* `--color-text`: #e2e8f0 — основний текст
* `--color-text-muted`: #94a3b8 — другорядний текст
* `--color-text-dim`: #64748b — приглушений текст

#### Семантичні кольори

**Стани:**
* `--color-active`: #5b8dee — активний елемент
* `--color-visited`: rgba(91, 141, 238, 0.5) — відвіданий
* `--color-resonance`: #a78bfa — резонансний зв'язок

**Шари:**
* `--color-layer-public`: #5b8dee — публічний шар
* `--color-layer-deep`: #8b5cf6 — глибинний шар
* `--color-layer-examples`: #ec4899 — шар прикладів

**Зворотний зв'язок:**
* `--color-success`: #10b981 — успішна дія
* `--color-warning`: #f59e0b — попередження
* `--color-error`: #ef4444 — помилка

#### Градієнти

**Радіальний (для центру Ci):**
```css
--gradient-ci: radial-gradient(
  circle,
  rgba(167, 139, 250, 0.3) 0%,
  rgba(91, 141, 238, 0.2) 50%,
  transparent 100%
);
```

**Лінійний (для переходів):**
```css
--gradient-transition: linear-gradient(
  135deg,
  #5b8dee 0%,
  #a78bfa 100%
);
```

### Типографіка (Typography)

#### Шрифтові сім'ї

* `--font-primary`: 'Inter', system-ui, sans-serif — основний текст
* `--font-display`: 'Plus Jakarta Sans', sans-serif — заголовки
* `--font-mono`: 'JetBrains Mono', monospace — код, дані

#### Розміри шрифтів

**Десктоп:**
* `--font-size-xs`: 0.75rem (12px) — дрібний текст
* `--font-size-sm`: 0.875rem (14px) — другорядний текст
* `--font-size-base`: 1rem (16px) — основний текст
* `--font-size-lg`: 1.125rem (18px) — великий текст
* `--font-size-xl`: 1.25rem (20px) — підзаголовки
* `--font-size-2xl`: 1.5rem (24px) — заголовки H3
* `--font-size-3xl`: 1.875rem (30px) — заголовки H2
* `--font-size-4xl`: 2.25rem (36px) — заголовки H1

**Мобільний (зменшити на 10-15%):**
* Використовувати `clamp()` для адаптивності

#### Вага шрифту

* `--font-weight-light`: 300
* `--font-weight-normal`: 400
* `--font-weight-medium`: 500
* `--font-weight-semibold`: 600
* `--font-weight-bold`: 700

#### Міжрядковий інтервал

* `--line-height-tight`: 1.25 — заголовки
* `--line-height-normal`: 1.5 — основний текст
* `--line-height-relaxed`: 1.75 — довгі тексти

#### Міжлітерний інтервал

* `--letter-spacing-tight`: -0.02em — великі заголовки
* `--letter-spacing-normal`: 0 — основний текст
* `--letter-spacing-wide`: 0.05em — акценти, кнопки

### Відступи (Spacing)

**Система 8px:**

* `--space-1`: 0.25rem (4px)
* `--space-2`: 0.5rem (8px)
* `--space-3`: 0.75rem (12px)
* `--space-4`: 1rem (16px)
* `--space-5`: 1.25rem (20px)
* `--space-6`: 1.5rem (24px)
* `--space-8`: 2rem (32px)
* `--space-10`: 2.5rem (40px)
* `--space-12`: 3rem (48px)
* `--space-16`: 4rem (64px)
* `--space-20`: 5rem (80px)

### Радіуси (Border Radius)

* `--radius-sm`: 4px — дрібні елементи
* `--radius-md`: 8px — стандартні картки
* `--radius-lg`: 12px — великі панелі
* `--radius-xl`: 16px — модальні вікна
* `--radius-full`: 9999px — кругові елементи

### Тіні (Shadows)

**Глибини:**

* `--shadow-xs`: 0 1px 2px rgba(0, 0, 0, 0.05) — мінімальна
* `--shadow-sm`: 0 2px 4px rgba(0, 0, 0, 0.1) — дрібна
* `--shadow-md`: 0 4px 8px rgba(0, 0, 0, 0.15) — середня
* `--shadow-lg`: 0 8px 16px rgba(0, 0, 0, 0.2) — велика
* `--shadow-xl`: 0 16px 32px rgba(0, 0, 0, 0.25) — дуже велика

**Світіння (glow):**

* `--glow-primary`: 0 0 20px rgba(91, 141, 238, 0.5)
* `--glow-secondary`: 0 0 24px rgba(167, 139, 250, 0.5)
* `--glow-active`: 0 0 36px rgba(91, 141, 238, 0.7)

---

## Компоненти

### Node (Вузол)

**Варіанти стану:**

#### Idle (Спокійний)

```css
.node-idle {
  width: var(--node-size, 56px);
  height: var(--node-size, 56px);
  border: 2px solid var(--color-border);
  background: var(--color-surface);
  border-radius: var(--radius-full);
  box-shadow: var(--shadow-sm);
  transition: all 200ms ease;
}
```

#### Active (Активний)

```css
.node-active {
  border-color: var(--color-accent-1);
  background: linear-gradient(135deg, var(--color-accent-1), var(--color-accent-2));
  box-shadow: var(--glow-active);
  transform: scale(1.1);
}
```

#### Visited (Відвіданий)

```css
.node-visited {
  border-color: var(--color-visited);
  opacity: 0.7;
}
```

### Center Node (Центральний вузол Ci)

```css
.node-center {
  width: var(--center-size, 72px);
  height: var(--center-size, 72px);
  background: var(--color-accent-2);
  background-image: var(--gradient-ci);
  border-radius: var(--radius-full);
  box-shadow: var(--glow-secondary);
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-xl);
  animation: pulse 3s ease-in-out infinite;
}
```

### Ring (Кільце глибини)

**Три рівні:**

```css
.ring-overview {
  stroke: var(--color-border);
  stroke-width: 1px;
  fill: none;
  opacity: 0.3;
}

.ring-immersion {
  stroke: var(--color-accent-1);
  stroke-width: 2px;
  fill: none;
  opacity: 0.5;
}

.ring-integration {
  stroke: var(--color-accent-2);
  stroke-width: 2px;
  fill: none;
  opacity: 0.7;
}
```

### Edge (Ребро графу)

```css
.edge {
  stroke: var(--color-border);
  stroke-width: 1px;
  opacity: 0.3;
  transition: all 300ms ease;
}

.edge-active {
  stroke: var(--color-accent-1);
  stroke-width: 2px;
  opacity: 1;
  stroke-dasharray: 5 3;
  animation: dash 1s linear infinite;
}

@keyframes dash {
  to { stroke-dashoffset: -8; }
}
```

### Tooltip (Підказка)

```css
.tooltip {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-3) var(--space-4);
  box-shadow: var(--shadow-lg);
  font-size: var(--font-size-sm);
  max-width: 240px;
  z-index: 1000;
}

.tooltip-arrow {
  width: 8px;
  height: 8px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  transform: rotate(45deg);
}
```

### Legend Card (Картка вузла)

```css
.legend-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  box-shadow: var(--shadow-md);
  max-width: 600px;
}

.legend-card-header {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}

.legend-card-title {
  font-family: var(--font-display);
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
}

.legend-card-index {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  font-weight: var(--font-weight-medium);
}
```

### Layer Tabs (Вкладки шарів)

```css
.layer-tabs {
  display: flex;
  gap: var(--space-2);
  border-bottom: 1px solid var(--color-border);
}

.layer-tab {
  padding: var(--space-3) var(--space-4);
  background: transparent;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  transition: all 200ms ease;
  border-bottom: 2px solid transparent;
}

.layer-tab-active {
  color: var(--color-accent-1);
  border-bottom-color: var(--color-accent-1);
}

.layer-tab:hover:not(.layer-tab-active) {
  color: var(--color-text);
}
```

### Back-to-Center Button (Кнопка повернення)

```css
.back-to-center {
  position: fixed;
  bottom: var(--space-6);
  right: var(--space-6);
  width: 48px;
  height: 48px;
  background: var(--color-accent-2);
  border: none;
  border-radius: var(--radius-full);
  box-shadow: var(--shadow-lg);
  cursor: pointer;
  transition: all 200ms ease;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: var(--font-size-xl);
}

.back-to-center:hover {
  transform: scale(1.1);
  box-shadow: var(--glow-secondary);
}
```

---

## Layout (Компонування)

### Radial Map (Радіальна карта)

**Структура:**

```css
.radial-container {
  position: relative;
  width: 520px;
  height: 520px;
  margin: auto;
}

.node-positioned {
  position: absolute;
  /* Position calculated via JS:
     x = centerX + radius * cos(angle)
     y = centerY + radius * sin(angle)
  */
  transform: translate(-50%, -50%);
}
```

**Параметри розміщення:**
* Центр: (260px, 260px)
* Радіус: 200px
* Кут між вузлами: 360° / 20 = 18°

### Grid System (Сіткова система)

**Для списків та галерей:**

```css
.grid-nodes {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: var(--space-4);
  padding: var(--space-6);
}
```

### Responsive Breakpoints (Точки перелому)

* `--breakpoint-sm`: 640px — мобільні пристрої
* `--breakpoint-md`: 768px — планшети
* `--breakpoint-lg`: 1024px — десктопи
* `--breakpoint-xl`: 1280px — великі екрани

```css
@media (max-width: 768px) {
  .radial-container {
    width: 100%;
    height: 80vh;
    max-width: 400px;
  }

  .node-btn {
    --node-size: 42px;
  }

  .node-center {
    --center-size: 56px;
  }
}
```

---

## Accessibility (Доступність)

### Focus States (Стани фокусу)

```css
.node-btn:focus-visible {
  outline: 2px solid var(--color-accent-1);
  outline-offset: 4px;
}

/* Приховати outline при кліку мишею */
.node-btn:focus:not(:focus-visible) {
  outline: none;
}
```

### High Contrast Mode (Режим високого контрасту)

```css
@media (prefers-contrast: high) {
  :root {
    --color-bg: #000;
    --color-text: #fff;
    --color-border: #fff;
    --color-accent-1: #00aaff;
  }
}
```

### Dark/Light Mode Toggle

За замовчуванням — темна тема. Світла тема — опційно:

```css
[data-theme="light"] {
  --color-bg: #f8fafc;
  --color-surface: #ffffff;
  --color-text: #1e293b;
  --color-text-muted: #64748b;
  --color-border: #e2e8f0;
}
```

---

## Figma Структура

### Фрейми (Frames)

1. **Cover / Entry** — титульний екран
2. **Map (Radial)** — головна карта
3. **Node View** — детальний вигляд вузла
4. **Layer View** — перемикач шарів
5. **Settings** — налаштування

### Компоненти (Components)

* Node / Idle
* Node / Active
* Node / Visited
* Node / Hover
* Center Node
* Ring / Overview
* Ring / Immersion
* Ring / Integration
* Tooltip
* Legend Card
* Layer Tab
* Back-to-Center Button

### Варіанти (Variants)

**Node:**
* State: idle | active | visited | hover
* Size: small (42px) | medium (56px) | large (72px)

**Layer Tab:**
* Layer: public | deep | examples
* State: inactive | active

---

## Ілюстрації та іконографія

### Стиль ілюстрацій

* **Геометричні форми** — чіткі лінії, мінімалізм
* **Градієнти** — м'які переходи кольорів
* **Символізм** — абстрактні форми замість реалістичних зображень

### Іконки

**Бібліотека:** Lucide Icons (або Heroicons)

**Основні іконки:**
* `circle` — вузол
* `activity` — активність
* `layers` — шари
* `compass` — навігація
* `home` — повернення до центру
* `book-open` — читання
* `grid` — галерея
* `zap` — резонанс

---

## Статус реалізації

* ✅ Design tokens визначені
* ✅ Компоненти описані
* 🔧 Figma файл у розробці
* 🔧 CSS/SCSS бібліотека
* 🔧 React/Vue компоненти

---

## Посилання

* [Повна модель легенди](model.md)
* [Інтерактивна навігація та UX](interactive-ux.md)
* [Анімаційні сценарії](animation.md)
* [Ci Production Spec](../../ci/production-spec.md)
* [Material Design Color System](https://material.io/design/color/)
