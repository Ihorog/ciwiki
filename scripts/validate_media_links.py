#!/usr/bin/env python3
"""Ensure referenced media files exist."""
from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def main() -> None:
    errors = []
    for md_file in DOCS_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        for match in IMAGE_PATTERN.finditer(content):
            link = match.group(1).strip()
            if link.startswith("http://") or link.startswith("https://"):
                continue
            if not (md_file.parent / link).exists():
                errors.append(f"{md_file}: missing media '{link}'")
    if errors:
        print("\n".join(errors))
        sys.exit(1)


if __name__ == "__main__":
    main()
