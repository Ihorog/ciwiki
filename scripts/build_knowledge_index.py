#!/usr/bin/env python3
"""Build knowledge index from docs front matter."""
from __future__ import annotations

import json
from pathlib import Path
import datetime as dt

try:
    import yaml
except ImportError as exc:  # pragma: no cover - handled in CI
    raise SystemExit("PyYAML is required to run this script") from exc

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
OUTPUT_FILE = Path(__file__).resolve().parent.parent / "knowledge.index.json"


def extract_frontmatter(path: Path) -> dict | None:
    """Extract YAML front matter from a markdown file."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    try:
        _, fm, _ = text.split("---\n", 2)
    except ValueError:
        return None
    data = yaml.safe_load(fm) or {}
    # Ensure all values are JSON-serialisable
    for key, value in list(data.items()):
        if isinstance(value, dt.date):
            data[key] = value.isoformat()
    data["path"] = str(path.relative_to(DOCS_DIR))
    return data


def main() -> None:
    entries = []
    for md_file in DOCS_DIR.rglob("*.md"):
        meta = extract_frontmatter(md_file)
        if meta:
            entries.append(meta)
    OUTPUT_FILE.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
