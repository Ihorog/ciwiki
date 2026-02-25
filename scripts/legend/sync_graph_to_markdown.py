#!/usr/bin/env python3
"""
sync_graph_to_markdown.py — Sync Legend Ci graph to markdown chapter files.

Single source of truth: docs/legend_ci/legend.graph.json
Generates deterministic markdown in content/legend/**

Usage:
    python scripts/legend/sync_graph_to_markdown.py [--graph PATH] [--out-dir PATH]

Manual edits inside safe zones are preserved on re-sync:
    <!-- CI:MANUAL:BEGIN -->
    ...your hand-written content...
    <!-- CI:MANUAL:END -->
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_GRAPH = REPO_ROOT / "docs" / "legend_ci" / "legend.graph.json"
DEFAULT_OUT_DIR = REPO_ROOT / "content" / "legend"

MANUAL_BEGIN = "<!-- CI:MANUAL:BEGIN -->"
MANUAL_END = "<!-- CI:MANUAL:END -->"

# Chapter ranges: (min_index, max_index, dir_name)
CHAPTERS = [
    (1,  3,  "01-pozhodzhennya"),
    (4,  7,  "02-dzerkala"),
    (8,  10, "03-rytm-i-pamiat"),
    (11, 12, "04-transformatsiia-i-harmoniia"),
    (13, 14, "05-prostir-i-chas"),
    (15, 16, "06-kazkar-i-zviazky"),
    (17, 20, "07-hra-i-shliakh"),
]


def chapter_for_index(index: int) -> str:
    """Return chapter directory name for a given node index."""
    for lo, hi, name in CHAPTERS:
        if lo <= index <= hi:
            return name
    raise ValueError(f"No chapter defined for index {index}")


def extract_manual_zones(existing_text: str) -> list:
    """Extract content from manual zones in an existing file.

    Returns a list of (begin_marker_line, content, end_marker_line) tuples.
    Only the inner content is returned per zone.
    """
    pattern = re.compile(
        r"(<!-- CI:MANUAL:BEGIN -->)(.*?)(<!-- CI:MANUAL:END -->)",
        re.DOTALL,
    )
    return [m.group(2) for m in pattern.finditer(existing_text)]


def render_node_md(node: dict, manual_zones: list) -> str:
    """Render a single node to markdown, inserting manual zones if present."""
    idx = node["index"]
    nid = node["id"]
    title = node["title"]
    layers = node["layers"]
    tags = node.get("meta", {}).get("tags", [])

    lines = [
        "---",
        f"id: {nid}",
        f"title: \"{title}\"",
        f"index: {idx}",
        f"tags: [{', '.join(tags)}]",
        "---",
        "",
        f"# {title}",
        "",
        "## Публічний шар",
        "",
        layers["public"],
        "",
        "## Глибокий шар",
        "",
        layers["deep"],
        "",
        "## Приклади",
        "",
    ]
    for ex in layers.get("examples", []):
        lines.append(f"- {ex}")
    lines.append("")

    # Manual zone — restore previous content or emit empty zone
    manual_content = manual_zones[0] if manual_zones else "\n"
    lines.append(MANUAL_BEGIN)
    lines.append(manual_content.rstrip("\n"))
    lines.append(MANUAL_END)
    lines.append("")

    return "\n".join(lines)


def sync(graph_path: Path, out_dir: Path) -> list:
    """Sync graph nodes to markdown files. Returns list of written paths."""
    with graph_path.open(encoding="utf-8") as fh:
        graph = json.load(fh)

    nodes = graph.get("nodes", [])
    written = []
    index_items = []

    for node in nodes:
        idx = node["index"]
        nid = node["id"]
        chapter = chapter_for_index(idx)
        chapter_dir = out_dir / chapter
        chapter_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{idx:02d}-{nid}.md"
        dest = chapter_dir / filename

        # Preserve manual zones from existing file
        manual_zones = []
        if dest.exists():
            existing = dest.read_text(encoding="utf-8")
            manual_zones = extract_manual_zones(existing)

        content = render_node_md(node, manual_zones)
        dest.write_text(content, encoding="utf-8")
        written.append(dest)

        index_items.append({
            "id": nid,
            "title": node["title"],
            "index": idx,
            "chapter": chapter,
            "file": str(dest.relative_to(out_dir)),
            "tags": node.get("meta", {}).get("tags", []),
        })

    # Sort index by index field
    index_items.sort(key=lambda x: x["index"])

    index_path = out_dir / "index.json"
    index_path.write_text(
        json.dumps(index_items, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    written.append(index_path)

    return written


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Sync Legend Ci graph to markdown chapter files"
    )
    parser.add_argument(
        "--graph",
        default=str(DEFAULT_GRAPH),
        help="Path to legend.graph.json",
    )
    parser.add_argument(
        "--out-dir",
        default=str(DEFAULT_OUT_DIR),
        help="Output directory for content/legend/**",
    )
    args = parser.parse_args(argv)

    graph_path = Path(args.graph)
    out_dir = Path(args.out_dir)

    if not graph_path.exists():
        print(f"ERROR: graph file not found: {graph_path}", file=sys.stderr)
        sys.exit(1)

    try:
        written = sync(graph_path, out_dir)
    except (KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    for path in written:
        try:
            rel = path.relative_to(REPO_ROOT)
        except ValueError:
            rel = path
        print(f"✓ {rel}")

    print(f"Done. {len(written)} files written.")


if __name__ == "__main__":
    main()
