#!/usr/bin/env python3
"""
Phase 31 — Build a RAG-ready index of every documentation page.

Walks docs/, guide/, and the i18n trees. For each markdown page, emits one
JSON line containing:

    {
      "doc_id":   "docs/modules/orders.md",
      "locale":   "en",
      "collection": "docs",          // or "guide"
      "url":      "/docs/modules/orders",
      "title":    "orders",
      "summary":  "...",             // from frontmatter
      "topics":   ["orders", "modules", ...],
      "audience": "Backend engineers, QA, PM",
      "headings": ["Key features", "Folder", "Controllers", ...],
      "content":  "<full markdown body, frontmatter stripped>",
      "chunks":   [                   // optional H2-level chunks
        { "heading": "Key features", "text": "..." },
        { "heading": "Folder",       "text": "..." }
      ]
    }

This output is consumer-agnostic — pipe it into:

  - OpenAI's `text-embedding-3-small` / `-large`
  - Anthropic via Voyage AI (`voyage-3`, `voyage-multilingual-2`)
  - sentence-transformers (`paraphrase-multilingual-mpnet-base-v2`)
  - any other embedding endpoint

…and store the result in Pinecone / Weaviate / pgvector / Chroma / etc.

Output: build/rag-index.jsonl (one record per page; ~600 records for current docs)

Usage:
    python3 scripts/build-rag-index.py
    python3 scripts/build-rag-index.py --locale ru
    python3 scripts/build-rag-index.py --collection guide
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "build" / "rag-index.jsonl"


COLLECTIONS = [
    # (source dir, route base, plugin instance id)
    ("docs",  "/docs",  "default"),
    ("guide", "/guide", "guide"),
]

LOCALES = ["en", "ru", "uz"]

# Map plugin instance id to i18n subtree name
I18N_SUBTREE = {
    "default": "docusaurus-plugin-content-docs",
    "guide":   "docusaurus-plugin-content-docs-guide",
}


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and return (meta, body)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    try:
        meta = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError:
        meta = {}
    body = text[end + 4:].lstrip("\n")
    return meta, body


def extract_headings(body: str) -> list[str]:
    """Return all H2/H3/H4 headings in document order."""
    return re.findall(r"^(?:#{2,4})\s+(.+?)\s*$", body, re.MULTILINE)


def split_chunks(body: str) -> list[dict]:
    """Split body into H2 sections. Each chunk is {heading, text}."""
    # Split on H2 headings (## ...)
    parts = re.split(r"^(##\s+.+?)$", body, flags=re.MULTILINE)
    # parts is [preamble, h2_1, text_1, h2_2, text_2, ...]
    chunks = []
    if parts and parts[0].strip():
        chunks.append({"heading": "(intro)", "text": parts[0].strip()})
    for i in range(1, len(parts), 2):
        heading = re.sub(r"^##\s+", "", parts[i]).strip()
        text = parts[i + 1].strip() if i + 1 < len(parts) else ""
        chunks.append({"heading": heading, "text": text})
    return chunks


def file_to_record(
    file_path: Path,
    collection_dir: str,
    route_base: str,
    locale: str,
) -> dict | None:
    """Read a single markdown file and produce one RAG record."""
    try:
        raw = file_path.read_text(encoding="utf-8")
    except OSError:
        return None

    meta, body = parse_frontmatter(raw)

    # Derive the rendered URL from the file path
    # E.g. docs/modules/orders.md -> /docs/modules/orders
    if locale == "en":
        rel = file_path.relative_to(REPO / collection_dir)
    else:
        i18n_root = REPO / "i18n" / locale / I18N_SUBTREE[
            "default" if collection_dir == "docs" else "guide"
        ] / "current"
        rel = file_path.relative_to(i18n_root)

    # Strip .md, then handle index files
    slug = str(rel).removesuffix(".md")
    if slug.endswith("/index"):
        slug = slug.removesuffix("/index")

    # Locale prefix in URL (en is default, no prefix)
    locale_prefix = "" if locale == "en" else f"/{locale}"
    url = f"{locale_prefix}{route_base}/{slug}".rstrip("/")

    record = {
        "doc_id": str(file_path.relative_to(REPO)),
        "locale": locale,
        "collection": "docs" if collection_dir == "docs" else "guide",
        "url": url,
        "title":    meta.get("title", "") if isinstance(meta, dict) else "",
        "summary":  meta.get("summary", "") if isinstance(meta, dict) else "",
        "topics":   meta.get("topics", []) if isinstance(meta, dict) else [],
        "audience": meta.get("audience", "") if isinstance(meta, dict) else "",
        "headings": extract_headings(body),
        "content":  body,
        "chunks":   split_chunks(body),
    }
    return record


def walk(args: argparse.Namespace) -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with OUT.open("w", encoding="utf-8") as out:
        for collection_dir, route_base, plugin_id in COLLECTIONS:
            if args.collection and args.collection != collection_dir:
                continue
            for locale in LOCALES:
                if args.locale and args.locale != locale:
                    continue
                if locale == "en":
                    source = REPO / collection_dir
                else:
                    source = REPO / "i18n" / locale / I18N_SUBTREE[plugin_id] / "current"
                if not source.exists():
                    continue
                for md in source.rglob("*.md"):
                    rec = file_to_record(md, collection_dir, route_base, locale)
                    if not rec:
                        continue
                    out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    total += 1
                    print(f"  {locale}  {rec['url']}", file=sys.stderr)

    print(f"\n{total} records written to {OUT.relative_to(REPO)}", file=sys.stderr)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Build a JSONL index of all docs.")
    ap.add_argument("--locale",     choices=LOCALES, help="Only this locale")
    ap.add_argument("--collection", choices=["docs", "guide"], help="Only this collection")
    args = ap.parse_args()
    return walk(args)


if __name__ == "__main__":
    sys.exit(main())
