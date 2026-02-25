#!/usr/bin/env python3
"""
render.py — Legend Ci graph renderer and validator.

Usage:
    python scripts/legend/render.py [--graph PATH] [--schema PATH] [--out-dir PATH]

Generates:
    docs/legend_ci/legend.nodes.md   — human-readable per-node summaries
    docs/legend_ci/legend.map.mmd    — Mermaid graph
    docs/legend_ci/legend.search.json — flat index for PWA search

Validates:
    - legend.graph.json against SCHEMA.legend.graph.json
    - unique node ids
    - edges reference existing node ids
    - required fields
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_GRAPH = REPO_ROOT / "docs" / "legend_ci" / "legend.graph.json"
DEFAULT_SCHEMA = REPO_ROOT / "docs" / "legend_ci" / "SCHEMA.legend.graph.json"
DEFAULT_OUT_DIR = REPO_ROOT / "docs" / "legend_ci"


# ---------------------------------------------------------------------------
# Schema validation (pure-stdlib, no jsonschema dependency required)
# ---------------------------------------------------------------------------

def _validate_required(obj: dict, fields: list, path: str) -> list:
    errors = []
    for f in fields:
        if f not in obj:
            errors.append(f"Missing required field '{f}' at {path}")
    return errors


def validate(graph: dict, schema_path: Path) -> list:
    """Return list of validation error strings (empty = valid), including JSON schema validation using schema_path."""
    errors = []

    # JSON schema validation (external, from provided schema_path)
    try:
        from jsonschema import Draft7Validator
        try:
            with schema_path.open("r", encoding="utf-8") as f:
                schema = json.load(f)
        except OSError as exc:
            errors.append(f"Unable to read schema file '{schema_path}': {exc}")
            return errors
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON schema in '{schema_path}': {exc}")
            return errors
        validator = Draft7Validator(schema)
        schema_errors = [
            f"Schema validation error at '{'/'.join(map(str, e.path)) or 'root'}': {e.message}"
            for e in validator.iter_errors(graph)
        ]
        if schema_errors:
            return schema_errors
    except ImportError:
        pass  # jsonschema not installed; fall back to built-in checks below

    # Basic structure
    errors += _validate_required(graph, ["version", "center", "nodes", "edges"], "root")
    if errors:
        return errors  # stop early; further checks would cascade

    # Center node
    center = graph["center"]
    errors += _validate_required(center, ["id", "title"], "center")

    # Nodes
    nodes = graph.get("nodes", [])
    seen_ids: set = set()
    seen_ids.add(center.get("id", ""))

    for i, node in enumerate(nodes):
        path = f"nodes[{i}]"
        errors += _validate_required(node, ["id", "title", "layers"], path)
        nid = node.get("id", "")
        if nid in seen_ids:
            errors.append(f"Duplicate node id '{nid}' at {path}")
        seen_ids.add(nid)

        layers = node.get("layers", {})
        errors += _validate_required(layers, ["public", "deep", "examples"], f"{path}.layers")
        if "examples" in layers and not isinstance(layers["examples"], list):
            errors.append(f"'{path}.layers.examples' must be an array")

    # Edges
    for j, edge in enumerate(graph.get("edges", [])):
        path = f"edges[{j}]"
        errors += _validate_required(edge, ["from", "to", "type"], path)
        for endpoint in ("from", "to"):
            ref = edge.get(endpoint)
            if not isinstance(ref, str):
                errors.append(f"Edge '{endpoint}' must be a string at {path}")
            elif not ref.strip():
                errors.append(f"Edge '{endpoint}' must be a non-empty string at {path}")
            elif ref not in seen_ids:
                errors.append(f"Edge '{endpoint}' references unknown node id '{ref}' at {path}")

    return errors


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------

def generate_nodes_md(graph: dict) -> str:
    lines = [
        "# Legend Ci — Огляд вузлів\n",
        "> Згенеровано автоматично з `legend.graph.json`. Не редагуйте вручну.\n",
    ]
    center = graph["center"]
    lines.append(f"\n## ⭕ Центр: {center['title']}\n")
    if "summary" in center:
        lines.append(f"{center['summary']}\n")

    for node in graph["nodes"]:
        idx = node.get("index", "?")
        title = node["title"]
        layers = node["layers"]
        lines.append(f"\n---\n\n## [{idx}] {title}\n")
        lines.append(f"**Публічний шар (метафора):** {layers['public']}\n\n")
        lines.append(f"**Глибокий шар (наукове):** {layers['deep']}\n\n")
        examples = layers.get("examples", [])
        if examples:
            lines.append("**Приклади:**\n")
            for ex in examples:
                lines.append(f"- {ex}\n")
        meta = node.get("meta", {})
        tags = meta.get("tags", [])
        if tags:
            lines.append(f"\n*Теги: {', '.join(f'#{t}' for t in tags)}*\n")

    return "".join(lines)


def generate_mermaid(graph: dict) -> str:
    lines = ["graph LR\n"]
    center_id = graph["center"]["id"]
    center_title = graph["center"]["title"]
    lines.append(f'    {center_id}(("{center_title}"))\n')

    for node in graph["nodes"]:
        nid = node["id"]
        title = node["title"].replace('"', "'")
        lines.append(f'    {nid}["{title}"]\n')

    for edge in graph["edges"]:
        frm = edge["from"]
        to = edge["to"]
        label = edge.get("label", "")
        bidir = edge.get("bidirectional", False)
        arrow = "<-->" if bidir else "-->"
        if label:
            safe_label = label.replace('"', "'")
            lines.append(f'    {frm} {arrow}|"{safe_label}"| {to}\n')
        else:
            lines.append(f'    {frm} {arrow} {to}\n')

    return "".join(lines)


def generate_search_json(graph: dict) -> list:
    index = []
    center = graph["center"]
    index.append({
        "id": center["id"],
        "title": center["title"],
        "text": center.get("summary", ""),
        "tags": [],
        "type": "center",
    })
    for node in graph["nodes"]:
        layers = node["layers"]
        text = " ".join([
            layers.get("public", ""),
            layers.get("deep", ""),
            " ".join(layers.get("examples", [])),
        ]).strip()
        index.append({
            "id": node["id"],
            "title": node["title"],
            "index": node.get("index"),
            "text": text,
            "tags": node.get("meta", {}).get("tags", []),
            "type": "node",
        })
    return index


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate and render Legend Ci graph")
    parser.add_argument("--graph", default=str(DEFAULT_GRAPH), help="Path to legend.graph.json")
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA), help="Path to schema file")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="Output directory")
    args = parser.parse_args(argv)

    graph_path = Path(args.graph)
    schema_path = Path(args.schema)
    out_dir = Path(args.out_dir)

    # Load graph
    if not graph_path.exists():
        print(f"ERROR: graph file not found: {graph_path}", file=sys.stderr)
        sys.exit(1)
    with graph_path.open(encoding="utf-8") as fh:
        graph = json.load(fh)

    # Validate
    errors = validate(graph, schema_path)
    if errors:
        print("Validation FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    print(f"✓ legend.graph.json is valid ({len(graph['nodes'])} nodes, {len(graph['edges'])} edges)")

    # Generate outputs
    out_dir.mkdir(parents=True, exist_ok=True)

    nodes_md = generate_nodes_md(graph)
    nodes_md_path = out_dir / "legend.nodes.md"
    nodes_md_path.write_text(nodes_md, encoding="utf-8")
    try:
        print(f"✓ Generated {nodes_md_path.relative_to(REPO_ROOT)}")
    except ValueError:
        print(f"✓ Generated {nodes_md_path}")

    mmd = generate_mermaid(graph)
    mmd_path = out_dir / "legend.map.mmd"
    mmd_path.write_text(mmd, encoding="utf-8")
    try:
        print(f"✓ Generated {mmd_path.relative_to(REPO_ROOT)}")
    except ValueError:
        print(f"✓ Generated {mmd_path}")

    search = generate_search_json(graph)
    search_path = out_dir / "legend.search.json"
    search_path.write_text(json.dumps(search, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        print(f"✓ Generated {search_path.relative_to(REPO_ROOT)}")
    except ValueError:
        print(f"✓ Generated {search_path}")

    print("Done.")


if __name__ == "__main__":
    main()
