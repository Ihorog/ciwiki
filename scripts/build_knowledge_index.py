#!/usr/bin/env python3
import sys, os, json, re, io
from pathlib import Path
try:
    import yaml
    HAVE_YAML = True
except Exception:
    HAVE_YAML = False
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT_DIR = (ROOT / "site") if (ROOT / "site").exists() else ROOT
OUT_FILE = OUT_DIR / "knowledge_index.json"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
def warn(*args): print("WARN:", *args, file=sys.stderr)
def read_text(p: Path) -> str:
    with p.open("r", encoding="utf-8", errors="replace") as f: return f.read()
def extract_frontmatter(md_path: Path):
    text = read_text(md_path); m = FRONTMATTER_RE.match(text)
    if not m: return {}
    fm = m.group(1)
    if not HAVE_YAML:
        warn(f"[{md_path}] PyYAML не встановлено — пропускаю фронтматер."); return {}
    try:
        data = yaml.safe_load(fm) or {}
        if not isinstance(data, dict): return {"_frontmatter_raw": data}
        return data
    except Exception as e:
        snippet = fm.strip().splitlines()[:5]
        warn(f"[{md_path}] Некоректний YAML у фронтматері: {e}. Перші рядки: {snippet}")
        return {}
def main():
    if not DOCS.exists():
        print(json.dumps({"error": "docs/ not found"})); sys.exit(0)
    index = []
    for p in DOCS.rglob("*.md"):
        rel = p.relative_to(DOCS).as_posix()
        meta = extract_frontmatter(p)
        item = {"path": rel, "title": meta.get("title") or meta.get("name") or "", "tags": meta.get("tags") if isinstance(meta.get("tags"), list) else []}
        index.append(item)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with io.open(OUT_FILE, "w", encoding="utf-8") as f: json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"Wrote {OUT_FILE} ({len(index)} items)")
if __name__ == "__main__": main()
