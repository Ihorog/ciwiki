# Анімаційні сценарії вузлів

> Документ описує принципи анімації та руху для інтерактивної веб-реалізації «Легенди ci».

---

## Філософія руху

**Мета:** передати сенс через рух. Анімація не прикрашає — вона пояснює.

Кожен вузол легенди має власний характер руху, що відповідає його змісту. Рух стає мовою, через яку абстрактні концепції набувають форми.

> *Рух — це не ефект, а спосіб розповісти те, що не можна сказати словами.*

---

## Загальні принципи руху

### 1. Повільний вхід, чітка фіксація

* Елементи з'являються поступово (ease-in)
* Після досягнення позиції — коротка фіксація
* Це створює відчуття впевненості та стабільності

**Параметри:**
* Duration: 400-600ms
* Easing: cubic-bezier(0.4, 0, 0.2, 1)

### 2. Рух від центру назовні і назад

* Всі анімації починаються від центру (Ci)
* Розгортання — назовні, згортання — назад до центру
* Символізує походження всього з єдиного джерела

**Параметри:**
* Origin point: center
* Expansion radius: 0 → 100%

### 3. Відображення (ліва/права симетрія)

* Дуальні елементи рухаються дзеркально
* Ліва/права симетрія підкреслює принцип дуальності
* Використовується для вузлів, що описують полярності

**Параметри:**
* Transform: scaleX(-1) для дзеркального відображення
* Synchronization: parallel motion

---

## Типові сценарії руху

### 1. Іскра (Spark)

**Концепція:** поява першого імпульсу

**Сценарій:**
1. Поява точки в центрі (0 → 4px, 100ms)
2. Короткий спалах (4px → 16px → 8px, 200ms)
3. Стабілізація (8px, 100ms)

**Код:**
```css
@keyframes spark {
  0% { transform: scale(0); opacity: 0; }
  50% { transform: scale(4); opacity: 1; }
  75% { transform: scale(2); opacity: 0.8; }
  100% { transform: scale(1); opacity: 1; }
}
```

### 2. Ритми (Rhythms)

**Концепція:** пульсація життя

**Сценарій:**
1. Початковий розмір (100%, 0ms)
2. Розширення (110%, 600ms)
3. Стиснення (95%, 600ms)
4. Повернення (100%, 400ms)
5. Цикл повторюється

**Код:**
```css
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  25% { transform: scale(1.1); }
  50% { transform: scale(0.95); }
}
animation: pulse 2s ease-in-out infinite;
```

### 3. Знаки (Signs)

**Концепція:** морфінг символів

**Сценарій:**
1. Початковий символ (форма A)
2. Розмиття (blur 4px, 200ms)
3. Трансформація (форма A → форма B, 400ms)
4. Фокус (blur 0, 200ms)

**Параметри:**
* Path morphing для SVG
* Opacity transition: 1 → 0.3 → 1

### 4. Число (Number)

**Концепція:** зміна ваги

**Сценарій:**
1. Інкремент числа (1 → 2 → 3...)
2. Кожна зміна супроводжується збільшенням font-weight
3. Візуальна вага зростає пропорційно значенню

**Код:**
```css
@keyframes numberWeight {
  0% { font-weight: 300; transform: scale(1); }
  50% { font-weight: 700; transform: scale(1.2); }
  100% { font-weight: 500; transform: scale(1); }
}
```

### 5. Геометрія (Geometry)

**Концепція:** побудова фігури

**Сценарій:**
1. Точка в центрі
2. Поява ліній (stroke-dashoffset анімація)
3. Формування замкненої фігури
4. Заповнення кольором (fill opacity: 0 → 0.3)

**Параметри:**
* SVG path animation
* Duration: 1200ms
* Easing: linear for drawing, ease-in for fill

### 6. Поля (Fields)

**Концепція:** інтерференція хвиль

**Сценарій:**
1. Дві точки-джерела
2. Концентричні кола розходяться від кожної
3. Перетин → змішування кольорів
4. Періодичність: 2s per wave

**Параметри:**
* Multiple radial gradients
* Transform: scale + opacity
* Mix-blend-mode: screen

### 7. Дуальність (Duality)

**Концепція:** дзеркальне розгортання

**Сценарій:**
1. Центральна вісь симетрії
2. Елемент з'являється зліва
3. Одночасно — дзеркальна копія справа
4. Синхронний рух назустріч один одному

**Код:**
```css
.left { animation: slideFromLeft 600ms ease-out; }
.right { animation: slideFromRight 600ms ease-out; }

@keyframes slideFromLeft {
  from { transform: translateX(-100%) scaleX(1); }
  to { transform: translateX(0) scaleX(1); }
}
@keyframes slideFromRight {
  from { transform: translateX(100%) scaleX(-1); }
  to { transform: translateX(0) scaleX(-1); }
}
```

### 8. Людина (Human)

**Концепція:** симетричне зростання форм

**Сценарій:**
1. Центральна лінія (хребет)
2. Симетричне зростання лівої/правої частини
3. Поява деталей (голова, кінцівки)
4. Фіксація форми

**Параметри:**
* SVG group animation
* Stagger delay: 100ms per element
* Final scale: 1.0

### 9. Мережа (Network)

**Концепція:** активація вузлів і зв'язків

**Сценарій:**
1. Вузли з'являються послідовно (stagger)
2. Після появи вузлів — з'являються ребра
3. Клік на вузол → підсвічуються зв'язки
4. Імпульси біжать по ребрах

**Параметри:**
* Stagger delay: 80ms per node
* Edge animation: stroke-dashoffset
* Pulse speed: 1000ms per edge

### 10. Час (Time)

**Концепція:** циклічний таймлайн

**Сценарій:**
1. Коло як циферблат
2. Маркер обертається (360deg)
3. Події з'являються на колі в момент їх "часу"
4. Повний цикл: 12s (символічна година)

**Код:**
```css
@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.marker {
  animation: rotate 12s linear infinite;
  transform-origin: center;
}
```

---

## Motion Design Tokens

**Швидкості:**

* `--motion-instant`: 100ms — миттєві зміни
* `--motion-fast`: 200ms — швидкі переходи
* `--motion-normal`: 400ms — стандартні анімації
* `--motion-slow`: 600ms — повільні трансформації
* `--motion-glacial`: 1200ms — епічні розгортання

**Easing функції:**

* `--ease-standard`: cubic-bezier(0.4, 0, 0.2, 1)
* `--ease-decelerate`: cubic-bezier(0, 0, 0.2, 1)
* `--ease-accelerate`: cubic-bezier(0.4, 0, 1, 1)
* `--ease-bounce`: cubic-bezier(0.68, -0.55, 0.265, 1.55)

**Затримки (stagger):**

* `--stagger-xs`: 50ms
* `--stagger-sm`: 80ms
* `--stagger-md`: 120ms
* `--stagger-lg`: 200ms

---

## Анімації станів

### Hover (Наведення)

**Ефект:** м'яке збільшення + світіння

**Параметри:**
* Scale: 1.0 → 1.05
* Box-shadow: 0 → 12px blur
* Duration: 200ms
* Easing: ease-out

### Active (Активний)

**Ефект:** пульсація + підсвічування

**Параметри:**
* Pulse animation (див. Ритми)
* Glow intensity: 0.5 → 1.0
* Duration: infinite

### Visited (Відвіданий)

**Ефект:** зміна прозорості + слід

**Параметри:**
* Opacity: 1.0 → 0.7
* Trail effect (fade-out gradient)
* Persist: session

---

## Переходи між вузлами

### Лінійний перехід

**Анімація:**
1. Fade out поточного вузла (300ms)
2. Slide in наступного вузла з правої сторони (400ms)

**Код:**
```css
.exit { animation: fadeOut 300ms ease-out; }
.enter { animation: slideInRight 400ms ease-out; }
```

### Радіальний перехід

**Анімація:**
1. Zoom in на вибраний вузол (500ms)
2. Інші вузли fade out (300ms)
3. Деталі вузла fade in (400ms)

### Резонансний перехід

**Анімація:**
1. Імпульс від поточного вузла
2. Хвиля розповсюджується до рекомендованих вузлів
3. Підсвічування резонансних зв'язків
4. Користувач обирає напрямок

---

## Мікроанімації

### Loading (Завантаження)

**Візуалізація:** пульсуючі кола

**Сценарій:**
* Три кола з затримкою 120ms
* Scale: 0.8 → 1.2 → 0.8
* Opacity: 0.3 → 1.0 → 0.3

### Success (Успіх)

**Візуалізація:** галочка з'являється

**Сценарій:**
* Checkmark path drawing (300ms)
* Green glow pulse (200ms)
* Scale bounce effect

### Error (Помилка)

**Візуалізація:** хрестик + червоне світло

**Сценарій:**
* X mark drawing (200ms)
* Red pulse (300ms)
* Shake animation (100ms)

---

## Accessibility (Доступність)

### Повага до налаштувань користувача

**Перевірка prefers-reduced-motion:**

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Альтернативи для анімацій

* Fade замість slide
* Instant замість animated
* Skip animations button

---

## Продуктивність

**Оптимізація:**

* Використовувати `transform` та `opacity` (GPU-accelerated)
* Уникати `width`, `height`, `top`, `left` в анімаціях
* `will-change` для складних анімацій
* RequestAnimationFrame для JS-анімацій

**Ліміти:**

* Максимум 5 одночасних анімацій
* FPS target: 60
* Budget per frame: 16ms

---

## Статус реалізації

* ✅ Концептуальні сценарії
* ✅ Motion design tokens
* 🔧 CSS/SCSS бібліотека
* 🔧 Прототип в Figma/Rive
* 🔧 Повна реалізація

---

## Посилання

* [Повна модель легенди](model.md)
* [Інтерактивна навігація та UX](interactive-ux.md)
* [Дизайн-система](design-system.md)
* [Material Motion Guidelines](https://material.io/design/motion/)
