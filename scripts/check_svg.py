#!/usr/bin/env python3
"""Check SVG files and images: well-formed XML, no scripts or external resources, every image referenced
from Markdown exists, and every file in assets/ is used."""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from booklib import ROOT, all_markdown_files, iter_links, is_external  # noqa: E402

errors = []
SVG_NS = "{http://www.w3.org/2000/svg}"


def main():
    svgs = sorted((ROOT / "assets").glob("*.svg"))
    if not svgs:
        errors.append("no SVG files found in assets/")
    for p in svgs:
        rel = p.relative_to(ROOT).as_posix()
        try:
            tree = ET.parse(p)
        except ET.ParseError as e:
            errors.append(f"{rel}: not well-formed XML: {e}")
            continue
        root = tree.getroot()
        if root.tag != SVG_NS + "svg":
            errors.append(f"{rel}: root element is not svg")
        if "viewBox" not in root.attrib:
            errors.append(f"{rel}: no viewBox")
        if not (root.attrib.get("aria-label") or root.find(SVG_NS + "title") is not None):
            errors.append(f"{rel}: no accessible name (aria-label or title)")
        for el in root.iter():
            tag = el.tag.replace(SVG_NS, "")
            if tag in ("script", "foreignObject"):
                errors.append(f"{rel}: contains <{tag}>")
            for a, v in el.attrib.items():
                if a.lower().startswith("on"):
                    errors.append(f"{rel}: event attribute {a}")
                if a.endswith("href") and is_external(v):
                    errors.append(f"{rel}: external reference {v}")
        raw = p.read_text(encoding="utf-8")
        if re.search(r"url\(\s*['\"]?https?:", raw) or "@import" in raw:
            errors.append(f"{rel}: external resource in CSS")
    used = set()
    n_img = 0
    for md in all_markdown_files():
        for kind, href, label in iter_links(md.read_text(encoding="utf-8")):
            if kind in ("image", "html") and href and not is_external(href) and not href.startswith("#"):
                if re.search(r"\.(svg|png|jpe?g|gif)$", href.partition("#")[0], re.I):
                    n_img += 1
                    t = (md.parent / href.partition("#")[0]).resolve()
                    if not t.exists():
                        errors.append(f"{md.relative_to(ROOT)}: missing image {href}")
                    else:
                        used.add(t)
    for p in svgs:
        if p.resolve() not in used:
            errors.append(f"{p.relative_to(ROOT)}: not referenced from any Markdown file")
    if errors:
        print("\n".join(errors))
        print(f"SVG: FAIL ({len(errors)} problem(s))")
        return 1
    print(f"SVG: OK ({len(svgs)} SVG files well-formed, no scripts/external resources; {n_img} image references resolved)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
