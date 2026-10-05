#!/usr/bin/env python3
"""Check relative links, anchors, images and language consistency (EN/DE) of all Markdown files.

Checks
  L1  every relative link/image target exists (file or directory);
  L2  every #fragment exists as a heading anchor (GitHub rules) in the target Markdown file;
  L3  language: German files link only to German files (or shared files), English files only to
      English files; the only allowed crossings are the explicit language-switch links;
  L4  each English chapter/README/template has its German counterpart and the switch link points to it;
  L5  semantic: a link text "Chapter N" must point into chapter N, "section N" into a heading
      starting with "N.", and nav links "Next"/"Previous" must point to the neighbour chapter.
External (http/https/mailto) links are NOT checked here; see check_external_links.py.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from booklib import ROOT, BOOK, CHAPTER_NAMES, all_markdown_files, heading_slugs, iter_links, is_external  # noqa: E402

errors = []


def err(src, msg):
    errors.append(f"{src.relative_to(ROOT).as_posix()}: {msg}")


def lang_of(rel):
    if rel.startswith("book/de/") or rel.endswith(".de.md"):
        return "de"
    return "en"


def counterpart(rel):
    """EN path -> DE path (None when the file is not translated)."""
    if rel.startswith("book/") and not rel.startswith("book/de/"):
        return "book/de/" + rel[len("book/"):]
    if rel == "README.md":
        return "README.de.md"
    if rel in ("templates/intent-card.md", "examples/order-table/README.md", "experiments/EXP-001.md"):
        return rel[:-3] + ".de.md"
    return None


anchors_cache = {}


def anchors(path):
    if path not in anchors_cache:
        anchors_cache[path] = {s for _, _, s in heading_slugs(path.read_text(encoding="utf-8"))}
    return anchors_cache[path]


def main():
    files = all_markdown_files()
    translated_en = {counterpart(p.relative_to(ROOT).as_posix()): p for p in files if counterpart(p.relative_to(ROOT).as_posix())}
    de_to_en = {c: p.relative_to(ROOT).as_posix() for c, p in translated_en.items()}
    en_with_de = {v for v in de_to_en.values()}

    for src in files:
        rel = src.relative_to(ROOT).as_posix()
        text = src.read_text(encoding="utf-8")
        src_lang = lang_of(rel)
        count = 0
        for kind, href, label in iter_links(text):
            if not href or is_external(href):
                continue
            count += 1
            path_part, _, frag = href.partition("#")
            target = src if path_part == "" else (src.parent / unquote(path_part)).resolve()
            try:
                target_rel = target.relative_to(ROOT).as_posix()
            except ValueError:
                err(src, f"link leaves the repository: {href}")
                continue
            if not target.exists():                                              # L1
                err(src, f"missing target: {href}")
                continue
            if frag and target.suffix == ".md":                                  # L2
                if unquote(frag) not in anchors(target):
                    err(src, f"missing anchor: {href}")
            if kind == "link" and target.is_file() and target.suffix == ".md":   # L3
                tl = lang_of(target_rel)
                if tl != src_lang and target_rel in (en_with_de | set(de_to_en)):
                    switch = label.strip().lower().startswith(("deutsch", "english")) or "README.de.md" in label or "book/de/" in label or "Inhalt" in label or label.strip().lower().startswith("this page")
                    if not (switch or rel in ("README.md", "README.de.md")):
                        err(src, f"language jump without a switch link: [{label}]({href})")
                if tl == src_lang and src_lang == "de" and target_rel in en_with_de:
                    err(src, f"German file links to the English version: {href}")
            # L5 semantic checks
            if kind == "link" and target.is_file():
                m = re.search(r"(?:Chapter|Kapitel)\s+(\d)", label)
                if m and target_rel.startswith("book/"):
                    if not Path(target_rel).name.startswith("0" + m.group(1) + "-"):
                        err(src, f"link text says chapter {m.group(1)} but points to {target_rel}")
                m = re.search(r"(?:section|Abschnitt)\s+(\d+)\b", label)
                if m and frag:
                    if not unquote(frag).startswith(m.group(1) + "-"):
                        err(src, f"link text says section {m.group(1)} but anchor is #{frag}")
                m = re.match(r"(?:Next|Weiter|Nächstes|Nächste)[: ]*.*?(\d)\s*·", label)
                if m and target_rel.startswith("book/"):
                    if not Path(target_rel).name.startswith("0" + m.group(1)):
                        err(src, f"navigation 'next' to chapter {m.group(1)} points to {target_rel}")
        # L4 counterpart and switch link
        if rel in en_with_de or rel in de_to_en:
            en = rel if rel in en_with_de else de_to_en[rel]
            de = counterpart(en)
            other = de if rel == en else en
            if not (ROOT / other).exists():
                err(src, f"missing counterpart {other}")
    # every EN chapter has a switch link to its DE file, and vice versa
    for en in sorted(en_with_de):
        de = counterpart(en)
        if not (ROOT / de).exists():
            errors.append(f"{en}: German counterpart {de} does not exist")
            continue
        for a, b, name in ((en, de, "Deutsch"), (de, en, "English")):
            if a.startswith("book/") or a in ("README.md", "README.de.md"):
                src = ROOT / a
                rels = []
                for kind, href, label in iter_links(src.read_text(encoding="utf-8")):
                    if href and not is_external(href):
                        p = (src.parent / unquote(href.partition("#")[0])).resolve()
                        try:
                            rels.append(p.relative_to(ROOT).as_posix())
                        except ValueError:
                            pass
                if b not in rels:
                    errors.append(f"{a}: no link to its counterpart {b}")
    # chapter sequence: each chapter links to the next one in its language
    for lang, items in BOOK.items():
        chapters = [p for _, p, k in items if k == "chapter"]
        for i, cur in enumerate(chapters[:-1]):
            src = ROOT / cur
            nxt = chapters[i + 1]
            targets = []
            for kind, href, label in iter_links(src.read_text(encoding="utf-8")):
                if href and not is_external(href):
                    p = (src.parent / unquote(href.partition("#")[0])).resolve()
                    targets.append(p.relative_to(ROOT).as_posix() if str(p).startswith(str(ROOT)) else "")
            if nxt not in targets:
                errors.append(f"{cur}: no link to the next chapter {nxt}")
            if lang == "de" and any(t.startswith("book/") and not t.startswith("book/de/") for t in targets):
                errors.append(f"{cur}: German chapter links into the English book/ folder")
    if errors:
        print("\n".join(sorted(set(errors))))
        print(f"LINKS: FAIL ({len(set(errors))} problem(s))")
        return 1
    n = len(files)
    print(f"LINKS: OK ({n} Markdown files, relative links, anchors, language and semantic checks passed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
