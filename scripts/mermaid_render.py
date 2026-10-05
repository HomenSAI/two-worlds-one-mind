#!/usr/bin/env python3
"""Render Mermaid blocks to SVG with the pinned mermaid-cli (inside the Docker image).

As a script it renders EVERY ```mermaid block of every Markdown file in the repository and fails
if any block does not render or if the English and German books have different numbers of blocks.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from booklib import ROOT, all_markdown_files, mermaid_blocks, BOOK  # noqa: E402

HERE = Path(__file__).resolve().parent
CONFIG = HERE / "mermaid-config.json"
PUPPETEER = HERE / "puppeteer-config.json"
CACHE = ROOT / "dist" / ".mermaid-cache"


def render(code, svg_id, use_cache=True):
    """Return the SVG text for one diagram; raise RuntimeError with mmdc's message on failure."""
    key = hashlib.sha256((code + svg_id + CONFIG.read_text()).encode("utf-8")).hexdigest()[:24]
    CACHE.mkdir(parents=True, exist_ok=True)
    cached = CACHE / f"{key}.svg"
    if use_cache and cached.exists():
        return cached.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as td:
        src, out = Path(td) / "d.mmd", Path(td) / "d.svg"
        src.write_text(code, encoding="utf-8")
        r = subprocess.run(["mmdc", "-i", str(src), "-o", str(out), "-c", str(CONFIG), "-p", str(PUPPETEER),
                            "-I", svg_id, "-q"], capture_output=True, text=True, timeout=120)
        if r.returncode != 0 or not out.exists():
            raise RuntimeError((r.stderr or r.stdout).strip()[-600:])
        svg = out.read_text(encoding="utf-8")
    if "<svg" not in svg or "Syntax error" in svg:
        raise RuntimeError("mermaid produced an error diagram")
    cached.write_text(svg, encoding="utf-8")
    return svg


def main():
    fails, total = [], 0
    counts = {"en": 0, "de": 0}
    for lang, items in BOOK.items():
        for key, rel, kind in items:
            counts[lang] += len(mermaid_blocks((ROOT / rel).read_text(encoding="utf-8")))
    for p in all_markdown_files():
        rel = p.relative_to(ROOT).as_posix()
        for i, code in enumerate(mermaid_blocks(p.read_text(encoding="utf-8")), 1):
            total += 1
            try:
                render(code, f"chk{total}", use_cache=False)
            except Exception as e:  # noqa: BLE001
                fails.append(f"{rel} block {i}: {e}")
    if counts["en"] != counts["de"]:
        fails.append(f"EN has {counts['en']} Mermaid blocks in the book, DE has {counts['de']}")
    if fails:
        print("\n".join(fails))
        print(f"MERMAID: FAIL ({len(fails)} problem(s))")
        return 1
    print(f"MERMAID: OK ({total} blocks rendered in all Markdown files; book blocks EN {counts['en']} = DE {counts['de']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
