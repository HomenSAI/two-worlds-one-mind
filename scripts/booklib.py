"""Shared helpers for building and checking the book (standard library + markdown-it-py)."""
import os
import re
from pathlib import Path

from markdown_it import MarkdownIt

ROOT = Path(os.environ.get("BOOK_ROOT") or Path(__file__).resolve().parents[1]).resolve()
REPO_URL = "https://github.com/HomenSAI/two-worlds-one-mind"

CHAPTER_NAMES = [
    "00-preface", "01-three-worlds", "02-manifesto", "03-principles", "04-physical-ai",
    "05-lab", "06-path", "07-vision", "08-field-guide", "glossary", "notes",
]

# language -> list of (key, path relative to ROOT, kind)
BOOK = {
    "en": (
        [(n, f"book/{n}.md", "chapter") for n in CHAPTER_NAMES]
        + [("appx-intent-card", "templates/intent-card.md", "appendix"),
           ("appx-example", "examples/order-table/README.md", "appendix"),
           ("appx-exp001", "experiments/EXP-001.md", "appendix")]
    ),
    "de": (
        [(n, f"book/de/{n}.md", "chapter") for n in CHAPTER_NAMES]
        + [("appx-intent-card", "templates/intent-card.de.md", "appendix"),
           ("appx-example", "examples/order-table/README.de.md", "appendix"),
           ("appx-exp001", "experiments/EXP-001.de.md", "appendix")]
    ),
}

README = {"en": "README.md", "de": "README.de.md"}

TEXT = {
    "en": {"toc": "Contents", "subtitle": "From code to intent — a short handbook on building where software meets the physical world",
           "edition": "Edition", "draft": "draft, unreleased", "built": "Built", "commit": "Source commit",
           "license": "Licence: CC BY 4.0 (text and diagrams); the name and mark \"HomenS.A Inc.\" are not licensed. Details: LICENSING.md in the repository.",
           "appx": "Appendices", "lang": "en", "title": "Two Worlds. One Mind."},
    "de": {"toc": "Inhalt", "subtitle": "Vom Code zur Absicht — ein kurzes Handbuch über das Bauen dort, wo Software auf die physische Welt trifft",
           "edition": "Ausgabe", "draft": "Entwurf, unveröffentlicht", "built": "Erstellt", "commit": "Quell-Commit",
           "license": "Lizenz: CC BY 4.0 (Text und Diagramme); Name und Zeichen „HomenS.A Inc.“ sind nicht lizenziert. Einzelheiten: LICENSING.md im Repository.",
           "appx": "Anhänge", "lang": "de", "title": "Zwei Welten. Ein Geist."},
}


def md_parser():
    return MarkdownIt("commonmark", {"html": True}).enable("table")


def plain_text(inline_token):
    out = []
    for ch in inline_token.children or []:
        if ch.type in ("text", "code_inline"):
            out.append(ch.content)
        elif ch.type in ("softbreak", "hardbreak"):
            out.append(" ")
    return "".join(out)


def slugify(text):
    """GitHub-style heading anchor."""
    s = text.strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)
    return s.replace(" ", "-")


def heading_slugs(md_text):
    """Return the list of (level, text, slug) with GitHub's duplicate suffixes."""
    toks = md_parser().parse(md_text)
    seen, out = {}, []
    for i, t in enumerate(toks):
        if t.type == "heading_open":
            text = plain_text(toks[i + 1])
            base = slugify(text)
            n = seen.get(base, 0)
            seen[base] = n + 1
            out.append((int(t.tag[1]), text, base if n == 0 else f"{base}-{n}"))
    return out


def iter_links(md_text):
    """Yield (kind, target, text) for links, images and raw-HTML src/href attributes."""
    toks = md_parser().parse(md_text)

    def walk(tokens):
        for t in tokens:
            if t.type == "inline":
                kids = t.children or []
                i = 0
                while i < len(kids):
                    c = kids[i]
                    if c.type == "link_open":
                        href = c.attrGet("href")
                        j, label = i + 1, []
                        while j < len(kids) and kids[j].type != "link_close":
                            label.append(kids[j].content if kids[j].type in ("text", "code_inline") else "")
                            j += 1
                        yield ("link", href, "".join(label))
                    elif c.type == "image":
                        yield ("image", c.attrGet("src"), c.content)
                    elif c.type == "html_inline":
                        for m in re.finditer(r'(?:src|href)="([^"]+)"', c.content):
                            yield ("html", m.group(1), "")
                    i += 1
            elif t.type == "html_block":
                for m in re.finditer(r'(?:src|href)="([^"]+)"', t.content):
                    yield ("html", m.group(1), "")
    yield from walk(toks)


def mermaid_blocks(md_text):
    return [t.content for t in md_parser().parse(md_text) if t.type == "fence" and t.info.strip() == "mermaid"]


def all_markdown_files():
    skip = {".git", "node_modules", "dist", "tools"}
    out = []
    for p in sorted(ROOT.rglob("*.md")):
        if any(part in skip for part in p.relative_to(ROOT).parts):
            continue
        out.append(p)
    return out


def is_external(href):
    return re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", href) is not None
