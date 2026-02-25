#!/usr/bin/env python3
"""
build_legend.py — Build HTML pages and JSON API from Legend Ci markdown files.

Reads generated markdown from content/legend/** (produced by sync_graph_to_markdown.py).
Parses frontmatter, sorts nodes by index, and produces:
  - docs/legend/{id}/index.html        per-node HTML page (with prev/next navigation)
  - api/v1/legend/index.json           full index JSON
  - api/v1/legend/{id}.json            per-node JSON

Usage:
    python scripts/legend/build_legend.py [--content-dir PATH] [--docs-dir PATH] [--api-dir PATH]

stdlib-only; no external dependencies required.
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CONTENT_DIR = REPO_ROOT / "content" / "legend"
DEFAULT_DOCS_DIR = REPO_ROOT / "docs" / "legend"
DEFAULT_API_DIR = REPO_ROOT / "api" / "v1" / "legend"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


# ---------------------------------------------------------------------------
# Frontmatter parser (stdlib YAML-lite for simple key: value pairs)
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple:
    """Return (frontmatter_dict, body_text).

    Supports simple scalar values and inline arrays: [a, b, c].
    """
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text

    raw = m.group(1)
    body = text[m.end():]
    fm = {}

    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()

        # Inline list: [a, b, c]
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1]
            fm[key] = [v.strip() for v in inner.split(",") if v.strip()]
        else:
            # Strip surrounding quotes
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            # Try int
            try:
                fm[key] = int(value)
            except ValueError:
                fm[key] = value

    return fm, body


# ---------------------------------------------------------------------------
# Minimal Markdown → HTML converter (stdlib-only)
# ---------------------------------------------------------------------------

def md_to_html(text: str) -> str:
    """Convert a small subset of Markdown to HTML (headings, bullets, paragraphs)."""
    lines = text.split("\n")
    out = []
    in_ul = False

    for line in lines:
        # Strip manual-zone markers from rendered HTML
        if line.strip() in ("<!-- CI:MANUAL:BEGIN -->", "<!-- CI:MANUAL:END -->"):
            continue

        # ATX headings
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            level = len(m.group(1))
            out.append(f"<h{level}>{html.escape(m.group(2))}</h{level}>")
            continue

        # Unordered list item
        m = re.match(r"^[-*]\s+(.*)", line)
        if m:
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{html.escape(m.group(1))}</li>")
            continue

        if in_ul:
            out.append("</ul>")
            in_ul = False

        stripped = line.strip()
        if stripped:
            out.append(f"<p>{html.escape(stripped)}</p>")

    if in_ul:
        out.append("</ul>")

    return "\n".join(out)


# ---------------------------------------------------------------------------
# HTML page template
# ---------------------------------------------------------------------------

def render_html_page(node_data: dict, prev_node: dict, next_node: dict, body_html: str) -> str:
    title = html.escape(node_data.get("title", "Legend"))
    index = node_data.get("index", "")
    tags = node_data.get("tags", [])
    tags_html = " ".join(f'<span class="tag">#{html.escape(t)}</span>' for t in tags)

    prev_link = ""
    if prev_node:
        prev_id = prev_node["id"]
        prev_title = html.escape(prev_node["title"])
        prev_link = f'<a href="../../{html.escape(prev_id)}/" class="nav-prev">← {prev_title}</a>'

    next_link = ""
    if next_node:
        next_id = next_node["id"]
        next_title = html.escape(next_node["title"])
        next_link = f'<a href="../../{html.escape(next_id)}/" class="nav-next">{next_title} →</a>'

    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Legend Ci</title>
<style>
  body {{ font-family: sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; }}
  nav.breadcrumb {{ margin-bottom: 1rem; font-size: 0.9rem; }}
  .tags {{ margin: 0.5rem 0; }}
  .tag {{ background: #eee; border-radius: 3px; padding: 2px 6px; margin-right: 4px; font-size: 0.8rem; }}
  .nav-bar {{ display: flex; justify-content: space-between; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #eee; }}
  a {{ color: #0066cc; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<nav class="breadcrumb"><a href="../../">Legend Ci</a> › {index}. {title}</nav>
<h1>{title}</h1>
<div class="tags">{tags_html}</div>
{body_html}
<nav class="nav-bar">
  <div>{prev_link}</div>
  <div>{next_link}</div>
</nav>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Index HTML page
# ---------------------------------------------------------------------------

def render_index_html(nodes: list) -> str:
    items_html = "\n".join(
        f'<li><a href="{html.escape(n["id"])}/">{n["index"]}. {html.escape(n["title"])}</a></li>'
        for n in nodes
    )
    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Legend Ci</title>
<style>
  body {{ font-family: sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; }}
  ul {{ list-style: none; padding: 0; }}
  li {{ margin: 0.5rem 0; }}
  a {{ color: #0066cc; text-decoration: none; font-size: 1.1rem; }}
  a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<h1>Legend Ci</h1>
<ul>
{items_html}
</ul>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def load_nodes(content_dir: Path) -> list:
    """Load all node markdown files from content/legend/**/*.md, sorted by index."""
    nodes = []
    for md_file in content_dir.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if "id" not in fm or "index" not in fm:
            continue  # skip files without expected frontmatter
        nodes.append({"fm": fm, "body": body, "path": md_file})

    nodes.sort(key=lambda x: x["fm"]["index"])
    return nodes


def build(content_dir: Path, docs_dir: Path, api_dir: Path) -> None:
    nodes = load_nodes(content_dir)
    if not nodes:
        print("WARNING: no node markdown files found", file=sys.stderr)

    api_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    index_entries = []

    for i, node in enumerate(nodes):
        fm = node["fm"]
        body = node["body"]
        nid = fm["id"]
        prev_fm = nodes[i - 1]["fm"] if i > 0 else None
        next_fm = nodes[i + 1]["fm"] if i < len(nodes) - 1 else None

        body_html = md_to_html(body)
        page_html = render_html_page(fm, prev_fm, next_fm, body_html)

        # docs/legend/{id}/index.html
        page_dir = docs_dir / nid
        page_dir.mkdir(parents=True, exist_ok=True)
        page_path = page_dir / "index.html"
        page_path.write_text(page_html, encoding="utf-8")
        try:
            print(f"✓ {page_path.relative_to(REPO_ROOT)}")
        except ValueError:
            print(f"✓ {page_path}")

        # api/v1/legend/{id}.json
        api_node = {
            "id": nid,
            "title": fm.get("title", ""),
            "index": fm.get("index"),
            "tags": fm.get("tags", []),
            "layers": {
                "public": _extract_section(body, "Публічний шар"),
                "deep": _extract_section(body, "Глибокий шар"),
            },
        }
        node_api_path = api_dir / f"{nid}.json"
        node_api_path.write_text(
            json.dumps(api_node, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        try:
            print(f"✓ {node_api_path.relative_to(REPO_ROOT)}")
        except ValueError:
            print(f"✓ {node_api_path}")

        index_entries.append({
            "id": nid,
            "title": fm.get("title", ""),
            "index": fm.get("index"),
            "tags": fm.get("tags", []),
            "url": f"/legend/{nid}/",
        })

    # api/v1/legend/index.json
    api_index_path = api_dir / "index.json"
    api_index_path.write_text(
        json.dumps(index_entries, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    try:
        print(f"✓ {api_index_path.relative_to(REPO_ROOT)}")
    except ValueError:
        print(f"✓ {api_index_path}")

    # docs/legend/index.html
    docs_index_path = docs_dir / "index.html"
    docs_index_path.write_text(
        render_index_html([e for e in index_entries]), encoding="utf-8"
    )
    try:
        print(f"✓ {docs_index_path.relative_to(REPO_ROOT)}")
    except ValueError:
        print(f"✓ {docs_index_path}")

    print(f"Done. {len(nodes)} nodes processed.")


def _extract_section(body: str, heading: str) -> str:
    """Extract the first paragraph after a ## heading."""
    pattern = re.compile(
        r"##\s+" + re.escape(heading) + r"\s*\n+(.*?)(?:\n##|\Z)", re.DOTALL
    )
    m = pattern.search(body)
    if not m:
        return ""
    return m.group(1).strip()


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Build HTML pages and JSON API from Legend Ci markdown"
    )
    parser.add_argument(
        "--content-dir",
        default=str(DEFAULT_CONTENT_DIR),
        help="Directory containing generated markdown (content/legend)",
    )
    parser.add_argument(
        "--docs-dir",
        default=str(DEFAULT_DOCS_DIR),
        help="Output directory for HTML pages (docs/legend)",
    )
    parser.add_argument(
        "--api-dir",
        default=str(DEFAULT_API_DIR),
        help="Output directory for API JSON (api/v1/legend)",
    )
    args = parser.parse_args(argv)

    content_dir = Path(args.content_dir)
    docs_dir = Path(args.docs_dir)
    api_dir = Path(args.api_dir)

    if not content_dir.exists():
        print(f"ERROR: content dir not found: {content_dir}", file=sys.stderr)
        sys.exit(1)

    build(content_dir, docs_dir, api_dir)


if __name__ == "__main__":
    main()
