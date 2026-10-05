#!/usr/bin/env python3
"""Check the built artifacts in dist/ (run after build.py).

A1  both languages have a PDF and an HTML file; SHA256SUMS matches the files; manifest is complete;
A2  the HTML files are self-contained: no <script>, no http(s) src/href to load resources, no <link>,
    no @import, all diagrams are inline <svg>, no foreignObject-free requirement;
A3  every internal #link in the HTML has a target id;
A4  the number of inline diagrams equals the number of Mermaid blocks in the source chapters;
A5  every chapter and appendix appears as a section; the PDF has a plausible page count, embedded text
    (extractable), and the expected chapter titles on its pages.
"""
import hashlib
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from booklib import ROOT, BOOK, mermaid_blocks  # noqa: E402

DIST = ROOT / "dist"
errors = []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.hrefs, self.scripts, self.links, self.ext, self.svgs, self.sections = set(), [], 0, 0, [], 0, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "script":
            self.scripts += 1
        if tag == "link":
            self.links += 1
        if tag == "svg":
            self.svgs += 1
        if tag == "section" and "chapter" in (a.get("class") or ""):
            self.sections += 1
        for k in ("src", "href", "poster", "data"):
            v = a.get(k)
            if v is None:
                continue
            if k == "href" and v.startswith("#"):
                self.hrefs.append(v[1:])
            elif re.match(r"^https?:", v) and k != "href":
                self.ext.append(v)
            elif k == "src" and not v.startswith("data:"):
                self.ext.append(v)


def pdf_info(path):
    from pypdf import PdfReader
    r = PdfReader(str(path))
    texts = [(pg.extract_text() or "") for pg in r.pages]
    return len(r.pages), texts


def main():
    manifest = json.loads((DIST / "manifest.json").read_text(encoding="utf-8"))
    version = (ROOT / "VERSION").read_text().strip()
    if manifest.get("version") != version:
        errors.append("manifest version differs from VERSION")
    sums = {}
    for line in (DIST / "SHA256SUMS").read_text().splitlines():
        h, name = line.split("  ", 1)
        sums[name] = h
    summary = []
    for lang, items in BOOK.items():
        stem = f"two-worlds-one-mind_{version}_{lang}"
        for ext in ("html", "pdf"):
            f = DIST / f"{stem}.{ext}"
            if not f.exists() or f.stat().st_size < 10_000:
                errors.append(f"{f.name}: missing or too small")
                continue
            if sums.get(f.name) != hashlib.sha256(f.read_bytes()).hexdigest():
                errors.append(f"{f.name}: SHA-256 does not match SHA256SUMS")
            if f.name not in [x["name"] for x in manifest["files"]]:
                errors.append(f"{f.name}: not in manifest")
        h = (DIST / f"{stem}.html").read_text(encoding="utf-8")
        p = P()
        p.feed(h)
        if p.scripts or p.links:
            errors.append(f"{stem}.html: contains <script> or <link>")
        if p.ext:
            errors.append(f"{stem}.html: external resources: {p.ext[:3]}")
        if "@import" in h:
            errors.append(f"{stem}.html: @import")
        missing = sorted({x for x in p.hrefs if x not in p.ids})
        if missing:
            errors.append(f"{stem}.html: internal links without target: {missing[:5]}")
        expected = sum(len(mermaid_blocks((ROOT / rel).read_text(encoding='utf-8'))) for _, rel, _ in items)
        # inline SVGs: one per diagram (the robot illustration is an <img>, not inline)
        if p.svgs != expected:
            errors.append(f"{stem}.html: {p.svgs} inline diagrams, expected {expected}")
        if p.sections != len(items):
            errors.append(f"{stem}.html: {p.sections} sections, expected {len(items)}")
        pages, texts = pdf_info(DIST / f"{stem}.pdf")
        if pages < 25:
            errors.append(f"{stem}.pdf: only {pages} pages")
        joined = "\n".join(texts)
        for key, rel, kind in items:
            title = (ROOT / rel).read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
            probe = re.sub(r"\s+", " ", title)[:25]
            if probe not in re.sub(r"\s+", " ", joined):
                errors.append(f"{stem}.pdf: title of {rel} not found in the PDF text: {probe!r}")
        summary.append(f"{lang}: {pages} PDF pages, {p.svgs} inline diagrams, {p.sections} sections")
    if errors:
        print("\n".join(errors))
        print(f"ARTIFACTS: FAIL ({len(errors)} problem(s))")
        return 1
    print("ARTIFACTS: OK (" + "; ".join(summary) + ")")
    return 0


if __name__ == "__main__":
    sys.exit(main())
