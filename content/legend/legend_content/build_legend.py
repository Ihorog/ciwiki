#!/usr/bin/env python3
"""
Simple converter for Legend Ci content.

This script reads all markdown files in the current directory with frontmatter,
parses the YAML frontmatter, and generates a static HTML index and per-chapter HTML pages.
It is a minimal example and can be extended to support templates and navigation.

Usage:
    python build_legend.py

Requires: pyyaml, markdown
"""
import os
import yaml
import markdown

# Directory containing markdown files
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SOURCE_DIR, "public")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load all markdown files
chapters = []
for filename in sorted(os.listdir(SOURCE_DIR)):
    if filename.endswith(".md"):
        path = os.path.join(SOURCE_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if content.startswith("---"):
            # split frontmatter
            parts = content.split("---", 2)
            frontmatter = yaml.safe_load(parts[1])
            body = parts[2].strip()
        else:
            frontmatter = {}
            body = content
        # convert markdown to html
        html_body = markdown.markdown(body, extensions=['markdown.extensions.tables','markdown.extensions.fenced_code'])
        chapters.append((frontmatter, html_body, filename))
        # write individual html
        html_filename = f"{frontmatter.get('id', filename[:-3])}.html"
        with open(os.path.join(OUTPUT_DIR, html_filename), "w", encoding="utf-8") as out:
            out.write(f"<html><head><meta charset='utf-8'><title>{frontmatter.get('title','Legend')}</title></head><body>")
            out.write(f"<h1>{frontmatter.get('title','Legend')}</h1>")
            out.write(html_body)
            out.write("</body></html>")

# Create index.html
with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as idx:
    idx.write("<html><head><meta charset='utf-8'><title>Legend Ci</title></head><body>")
    idx.write("<h1>Legend Ci</h1><ul>")
    for fm, _html, _fn in chapters:
        idx.write(f"<li><a href='{fm.get('id', _fn[:-3])}.html'>{fm.get('title','Untitled')}</a></li>")
    idx.write("</ul></body></html>")
