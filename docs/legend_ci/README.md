# Legend Ci — Дані та автоматизація

> **Єдине джерело істини:** `docs/legend_ci/legend.graph.json`

Цей каталог містить **канонічну модель даних** Legend Ci. Усі описові документи у `docs/kazkar/legend-ci/` та майбутній PWA-інтерфейс живляться саме звідси.

---

## Структура каталогу

| Файл | Статус | Призначення |
|------|--------|-------------|
| `legend.graph.json` | ✍️ ручне | Єдине джерело істини: 20 вузлів + центр Ci, ребра, шари |
| `SCHEMA.legend.graph.json` | ✍️ ручне | JSON Schema для валідації графу |
| `legend.nodes.md` | ⚙️ генерується | Людиночитабельний огляд кожного вузла |
| `legend.map.mmd` | ⚙️ генерується | Mermaid-граф усіх зв'язків |
| `legend.search.json` | ⚙️ генерується | Плаский індекс для PWA-пошуку |

---

## Архітектура графу

```
center: Ci
  └── 20 nodes (index 1–20)
        └── layers: public / deep / examples
edges: linear | resonance | contrast | emergence | return
meta: layout_hint, animation, hex_facets (Ci-1 … Ci-7)
```

Перші 7 вузлів (індекси 1–7) відповідають 7 розділам `docs/kazkar/legend-ci/`:

| Вузол | ID | Файл |
|-------|----|------|
| Першоджерело | `pershodzherelo` | `01-source.md` |
| Перший поділ | `pershyi_podil` | `02-division.md` |
| Дзеркало матерії | `dzerkalo_materii` | `03-matter-mirror.md` |
| Дзеркало свідомості | `dzerkalo_svidomosti` | `04-mind-mirror.md` |
| Танець протилежностей | `tanets_protylezhnostei` | `05-dance-of-opposites.md` |
| Мости єдності | `mosti_yednosti` | `06-bridges.md` |
| Прояв CI | `proyav_ci` | `07-manifest-ci.md` |

---

## Як додати або змінити вузол

1. Відкрий `legend.graph.json`
2. Знайди потрібний вузол у масиві `nodes` (за `id`)
3. Відредагуй поля `layers.public`, `layers.deep`, `layers.examples`
4. **Не змінюй `id`** — він є ключем у ребрах (`edges`)
5. Запусти валідацію та рендер:
   ```bash
   python scripts/legend/render.py
   ```
6. Закомітуй зміни, включаючи згенеровані файли

## Як додати новий вузол

1. Додай новий об'єкт у масив `nodes` з унікальним `id` (snake_case, лише `[a-z0-9_-]`)
2. Вкажи обов'язкові поля: `id`, `title`, `layers` (з `public`, `deep`, `examples`)
3. За потреби додай ребра у масив `edges` (перевір, що `from`/`to` посилаються на існуючі `id`)
4. Запусти `python scripts/legend/render.py` — валідація покаже помилки

## Запуск генератора (локально / Termux)

```bash
# Встановлення (одноразово)
pip install jsonschema   # рекомендовано: вмикає повну валідацію за JSON Schema; без нього — лише базові перевірки

# Запуск
cd /шлях/до/репозиторію
python scripts/legend/render.py

# Кастомні шляхи
python scripts/legend/render.py \
  --graph docs/legend_ci/legend.graph.json \
  --schema docs/legend_ci/SCHEMA.legend.graph.json \
  --out-dir docs/legend_ci
```

## CI-перевірка

Кожен push автоматично запускає `.github/workflows/legend-ci-validate.yml`, який:
- Валідує `legend.graph.json` проти схеми
- Перевіряє унікальність ID вузлів
- Перевіряє, що всі ребра посилаються на існуючі вузли
- Запускає `render.py` (детерміновано)

---

*Читай також: [Казкар → Легенда CI](../kazkar/legend-ci/index.md)*
