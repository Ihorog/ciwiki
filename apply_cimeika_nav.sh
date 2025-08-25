#!/usr/bin/env bash
set -euo pipefail

BRANCH_NAME="content/cimeika-7-sections"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
DOCS_DIR="$REPO_ROOT/docs"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "❌ Не git-репозиторій. Запустіть у корені локального клону." >&2; exit 1
fi

if [ ! -f "$REPO_ROOT/mkdocs.yml" ]; then
  echo "❌ mkdocs.yml не знайдено у $REPO_ROOT" >&2; exit 1
fi

if [ -n "$(git status --porcelain)" ]; then
  echo "⚠️  Є незакомічені зміни. Зробіть commit або stash перед запуском."; exit 1
fi

git fetch --all -q
if git rev-parse --verify "$BRANCH_NAME" >/dev/null 2>&1; then
  git checkout "$BRANCH_NAME"
else
  git checkout -b "$BRANCH_NAME"
fi

mkdir -p "$DOCS_DIR"/{{ci,podija,kazkar,nastrij,malya,gallery,calendar}}
for s in ci podija kazkar nastrij malya gallery calendar; do
  if [ ! -f "$DOCS_DIR/$s/index.md" ]; then
    cat > "$DOCS_DIR/$s/index.md" <<EOF
# ${s^}
(Заглушка сторінки. Контент буде додано.)
EOF
    echo "✓ Створено $DOCS_DIR/$s/index.md"
  fi
done

LEG_DIR="$DOCS_DIR/kazkar/legend-ci"
miss=0
for f in index.md 01-source.md 02-division.md 03-matter-mirror.md 04-mind-mirror.md 05-dance-of-opposites.md 06-bridges.md 07-manifest-ci.md; do
  if [ ! -f "$LEG_DIR/$f" ]; then
    echo "⚠️  Відсутній файл легенди: $LEG_DIR/$f"; miss=1
  fi
done

ts="$(date +%Y%m%d-%H%M%S)"
cp "$REPO_ROOT/mkdocs.yml" "$REPO_ROOT/mkdocs.yml.bak-$ts"
echo "✓ Бекап mkdocs.yml → mkdocs.yml.bak-$ts"

cat > "$REPO_ROOT/mkdocs.yml" <<'YAML'
site_name: Cimeika

theme:
  name: material
  language: uk

plugins:
  - search

nav:
  - Ci: ci/index.md
  - ПоДія: podija/index.md
  - Казкар:
      - kazkar/index.md
      - Легенда CI:
          - Огляд: kazkar/legend-ci/index.md
          - "[1] Першоджерело": kazkar/legend-ci/01-source.md
          - "[2] Перший поділ": kazkar/legend-ci/02-division.md
          - "[3] Дзеркало матерії": kazkar/legend-ci/03-matter-mirror.md
          - "[4] Дзеркало свідомості": kazkar/legend-ci/04-mind-mirror.md
          - "[5] Танець протилежностей": kazkar/legend-ci/05-dance-of-opposites.md
          - "[6] Мости єдності": kazkar/legend-ci/06-bridges.md
          - "[7] Прояв CI": kazkar/legend-ci/07-manifest-ci.md
      - Інтерактив:
          - Legend CI (SPA): _assets/legend/legend_ci_single.html
          - Legends Portal: _assets/legend/legend_ci_portal.html
      - Legacy:
          - legend_ci.html: _assets/legend/legend_ci.html
          - legends_ci.html: _assets/legend/legends_ci.html
  - Настрій: nastrij/index.md
  - Маля: malya/index.md
  - Галерея: gallery/index.md
  - Календар: calendar/index.md
YAML

echo "✓ Оновлено mkdocs.yml (7 розділів + 'Легенда CI')"

git add -A
git commit -m "feat(nav): 7 розділів Cimeika + повний розділ 'Легенда CI' у Казкарі"
git push -u origin "$BRANCH_NAME"

echo
echo "✅ Готово. Відкрийте Pull Request з гілки: $BRANCH_NAME"
if [ "$miss" -eq 1 ]; then
  echo "ℹ️  Деякі файли легенди відсутні. Додайте їх у docs/kazkar/legend-ci/ перед збіркою."
fi
