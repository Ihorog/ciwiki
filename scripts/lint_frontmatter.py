#!/usr/bin/env python3
"""Validate front matter of markdown files."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - handled in CI
    raise SystemExit("PyYAML is required to run this script") from exc

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
REQUIRED_KEYS = {"id", "title", "summary", "updated"}


def check_file(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return "missing front matter"
    try:
        _, fm, _ = text.split("---\n", 2)
    except ValueError:
        return "malformed front matter"
    data = yaml.safe_load(fm) or {}
    missing = [key for key in REQUIRED_KEYS if not data.get(key)]
    if missing:
        return f"missing keys: {', '.join(missing)}"
    return None


def main() -> None:
    errors = []
    for md_file in DOCS_DIR.rglob("*.md"):
        error = check_file(md_file)
        if error:
            errors.append(f"{md_file}: {error}")
    if errors:
        print("\n".join(errors))
        sys.exit(1)


if __name__ == "__main__":
    main()
