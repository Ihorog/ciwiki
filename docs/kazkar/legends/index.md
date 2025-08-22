---awk 'BEGIN{p=1} /^---[[:space:]]*$/{c++} c<2 && p{print} c==1 && /^---[[:space:]]*$/{p=0; exit}' docs/kazkar/legends/index.md >/dev/null 2>&1 || true
cat > docs/kazkar/legends/index.md <<'MD'
---
id: kazkar-legends
title: "Легенди"
tags:
  - codex/create-knowledge-index-builder-script
updated: 2025-08-21
summary: "Збірка легенд у Всесвіті Cimeika."
---

# Легенди

(вміст сторінки нижче)
MD

---

# 🧙‍♂️ Легенди

Цей розділ містить легенди, що відкривають глибинні історії Всесвіту Cimeika.
