#!/usr/bin/env python3
"""Build the complete book (English and German) as one self-contained HTML file and one PDF each.

Run inside the Docker image (see scripts/build.sh). Output goes to dist/:
  two-worlds-one-mind_<version>_<lang>.html   self-contained: no CDN, no scripts, diagrams pre-rendered
  two-worlds-one-mind_<version>_<lang>.pdf
  SHA256SUMS, manifest.json

Environment: BUILD_COMMIT (source commit), RELEASE_STATE (draft|released), SOURCE_DATE_EPOCH (optional).
"""
import base64
import datetime
import hashlib
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from booklib import ROOT, BOOK, TEXT, REPO_URL, md_parser, plain_text, slugify, is_external  # noqa: E402
import mermaid_render  # noqa: E402

DIST = ROOT / "dist"
VERSION = (ROOT / "VERSION").read_text().strip()
STATE = os.environ.get("RELEASE_STATE", "draft")
COMMIT = os.environ.get("BUILD_COMMIT", "unknown")
if os.environ.get("SOURCE_DATE_EPOCH"):
    NOW = datetime.datetime.fromtimestamp(int(os.environ["SOURCE_DATE_EPOCH"]), datetime.timezone.utc)
else:
    NOW = datetime.datetime.now(datetime.timezone.utc)
FILE_STEM = f"two-worlds-one-mind_{VERSION}"
NAV_LINK_TEXTS = ("contents", "inhalt", "deutsch", "english")

CSS = r"""
:root { --ink:#1b2430; --muted:#5b6775; --line:#cfd6de; --accent:#0e6f7a; --gold:#b07d12; --bg:#ffffff; --soft:#f4f6f8; }
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin:0; background:var(--bg); color:var(--ink);
  font-family:"Liberation Sans","DejaVu Sans",Arial,Helvetica,sans-serif; font-size:16px; line-height:1.55; }
main { max-width: 46rem; margin: 0 auto; padding: 1.2rem 1rem 4rem; }
h1,h2,h3 { line-height:1.25; color:#0f1a26; }
h1 { font-size:1.9rem; margin:2.2rem 0 .8rem; border-bottom:2px solid var(--accent); padding-bottom:.3rem; }
h2 { font-size:1.35rem; margin:1.8rem 0 .6rem; }
h3 { font-size:1.1rem; margin:1.4rem 0 .4rem; }
p, li { overflow-wrap:break-word; }
a { color:var(--accent); }
blockquote { margin:1rem 0; padding:.2rem 1rem; border-left:4px solid var(--gold); background:var(--soft); color:#2b3846; }
code, pre { font-family:"DejaVu Sans Mono","Liberation Mono",monospace; font-size:.88em; }
code { background:var(--soft); padding:.05em .3em; border-radius:3px; }
pre { background:var(--soft); border:1px solid var(--line); padding:.7rem .9rem; white-space:pre-wrap; overflow-wrap:anywhere; border-radius:4px; }
pre code { background:none; padding:0; }
.table-wrap { overflow-x:auto; margin:1rem 0; }
table { border-collapse:collapse; width:100%; font-size:.92em; }
th, td { border:1px solid var(--line); padding:.35rem .5rem; vertical-align:top; text-align:left; overflow-wrap:break-word; }
th { background:var(--soft); }
figure.diagram { margin:1.2rem 0; text-align:center; }
figure.diagram svg { max-width:100%; height:auto; }
img { max-width:100%; height:auto; }
hr { border:0; border-top:1px solid var(--line); margin:1.5rem 0; }
.titlepage { text-align:center; padding:2.5rem 0 2rem; border-bottom:1px solid var(--line); margin-bottom:1.5rem; }
.titlepage img { width:110px; height:auto; }
.titlepage h1 { border:0; font-size:2.6rem; margin:1rem 0 .3rem; }
.titlepage .sub { font-size:1.15rem; color:var(--muted); margin:0 0 1.2rem; }
.titlepage .meta { font-size:.9rem; color:var(--muted); }
td.nw { white-space:nowrap; }
li.task { list-style:none; padding-left:1.4em; text-indent:-1.4em; }
nav.toc ol { list-style:none; padding-left:0; }
nav.toc ol ol { padding-left:1.2rem; font-size:.92em; }
nav.toc li { margin:.15rem 0; }
nav.toc > ol > li { margin:.5rem 0 .1rem; font-weight:bold; }
nav.toc > ol > li > ol > li { font-weight:normal; }
section.chapter { margin-top:2rem; }
@media (max-width:600px) { body { font-size:15px; } h1 { font-size:1.5rem; } .titlepage h1 { font-size:2rem; } }
@media print {
  @page { size:A4; margin:18mm 16mm 20mm 16mm; }
  body { font-size:10.5pt; line-height:1.45; }
  main { max-width:none; padding:0; }
  .titlepage { border:0; padding-top:30mm; page-break-after:always; break-after:page; }
  nav.toc { break-after:page; }
  section.chapter { break-before:page; margin-top:0; }
  h1 { margin-top:0; font-size:20pt; }
  h2, h3 { break-after:avoid; }
  .table-wrap { overflow:visible; }
  table { font-size:8.8pt; }
  tr, figure.diagram, pre, blockquote { break-inside:avoid; }
  a { color:inherit; text-decoration:none; }
  figure.diagram svg { max-height:215mm; }
}
"""


def file_b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(Path(path).read_bytes()).decode("ascii")


def mime_for(path):
    ext = Path(path).suffix.lower()
    return {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}[ext]


class Doc:
    """One language edition: parse all chapters, collect ids, rewrite links, render HTML."""

    def __init__(self, lang):
        self.lang = lang
        self.items = BOOK[lang]
        self.by_path = {(ROOT / rel).resolve(): key for key, rel, _ in self.items}
        self.md = md_parser()
        self.diagram_no = 0
        self.diagrams = 0
        self.toc = []   # (key, title, [(id, text)])

    # -- link handling
    def rewrite_href(self, href, src_path):
        if not href or is_external(href):
            return href
        path_part, _, frag = href.partition("#")
        frag = unquote(frag)
        if path_part == "":
            return f"#{self.cur_key}-{frag}" if frag else "#"
        target = (src_path.parent / unquote(path_part)).resolve()
        key = self.by_path.get(target)
        if key:
            return f"#{key}-{frag}" if frag else f"#{key}"
        rel = target.relative_to(ROOT).as_posix()
        # the other language's files and repository files: link to the repository (default branch)
        kind = "tree" if target.is_dir() else "blob"
        return f"{REPO_URL}/{kind}/main/{rel}" + (f"#{frag}" if frag else "")

    def embed_img(self, src, src_path):
        target = (src_path.parent / unquote(src)).resolve()
        return file_b64(target, mime_for(target))

    # -- rendering
    def render_chapter(self, key, rel, kind):
        src_path = ROOT / rel
        self.cur_key = key
        tokens = self.md.parse(src_path.read_text(encoding="utf-8"))
        tokens = self.strip_nav(tokens)
        seen, out, h2 = {}, [], []
        title = key
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if t.type == "heading_open":
                text = plain_text(tokens[i + 1])
                if t.tag == "h1":
                    hid, title = key, text
                else:
                    base = slugify(text)
                    n = seen.get(base, 0)
                    seen[base] = n + 1
                    hid = f"{key}-{base}" + (f"-{n}" if n else "")
                    if t.tag == "h2":
                        h2.append((hid, text))
                t.attrSet("id", hid)
            if t.type == "inline":
                for c in t.children or []:
                    if c.type == "link_open":
                        c.attrSet("href", self.rewrite_href(c.attrGet("href"), src_path))
                    elif c.type == "image":
                        c.attrSet("src", self.embed_img(c.attrGet("src"), src_path))
                    elif c.type == "html_inline":
                        c.content = self.rewrite_html(c.content, src_path)
            if t.type == "html_block":
                t.content = self.rewrite_html(t.content, src_path)
            if t.type == "fence" and t.info.strip() == "mermaid":
                self.diagram_no += 1
                svg = mermaid_render.render(t.content, f"d{self.lang}{self.diagram_no}")
                svg = re.sub(r"^<\?xml[^>]*>\s*", "", svg)
                t.type, t.tag = "html_block", ""
                t.content = f'<figure class="diagram" role="img" aria-label="Diagram {self.diagram_no}">{svg}</figure>\n'
                self.diagrams += 1
            i += 1
        body = self.md.renderer.render(tokens, self.md.options, {})
        body = re.sub(r"<thead>\s*<tr>\s*(<th[^>]*></th>\s*)+</tr>\s*</thead>\s*", "", body)  # tables with an empty header row
        body = body.replace("<li>[ ] ", '<li class="task">☐ ')
        body = re.sub(r"<td>([^<\s]{1,12})</td>", r'<td class="nw">\1</td>', body)  # short IDs such as P-01 stay on one line
        body = re.sub(r"<table>", '<div class="table-wrap"><table>', body)
        body = body.replace("</table>", "</table></div>")
        self.toc.append((key, title, h2, kind))
        return f'<section class="chapter" id="sec-{key}">\n{body}</section>\n'

    def rewrite_html(self, content, src_path):
        def img(m):
            return f'src="{self.embed_img(m.group(1), src_path)}"'
        content = re.sub(r'src="([^"]+)"', lambda m: img(m) if not is_external(m.group(1)) else m.group(0), content)
        content = re.sub(r'href="([^"]+)"', lambda m: f'href="{self.rewrite_href(m.group(1), src_path)}"', content)
        return content

    def strip_nav(self, tokens):
        """Remove the navigation paragraphs (Contents / language switch / prev-next) and rules at the ends."""
        out, i = [], 0
        first_h1_seen = False
        while i < len(tokens):
            t = tokens[i]
            if t.type == "paragraph_open" and tokens[i + 1].type == "inline":
                kids = tokens[i + 1].children or []
                if kids and kids[0].type == "link_open":
                    label = "".join(c.content for c in kids[1:3] if c.type == "text").strip().lower()
                    if label.startswith(NAV_LINK_TEXTS):
                        i += 3
                        continue
            out.append(t)
            i += 1
        while out and out[-1].type == "hr":
            out.pop()
        # drop an hr right after the title block (line under nav)
        for j, t in enumerate(out):
            if t.type == "hr" and j <= 12 and all(x.type != "hr" for x in out[:j]):
                prev = [x for x in out[:j] if x.type == "heading_open"]
                if len(prev) == 1:
                    out.pop(j)
                break
        return out


def build_lang(lang, logo_b64):
    tx = TEXT[lang]
    doc = Doc(lang)
    sections = [doc.render_chapter(k, rel, kind) for k, rel, kind in doc.items]
    # table of contents
    def li(key, title, h2):
        sub = "".join(f'<li><a href="#{i}">{html.escape(t)}</a></li>' for i, t in h2)
        return f'<li><a href="#{key}">{html.escape(title)}</a>' + (f"<ol>{sub}</ol>" if sub else "") + "</li>"
    chapters = "".join(li(k, t, h) for k, t, h, kind in doc.toc if kind == "chapter")
    appendices = "".join(li(k, t, []) for k, t, h, kind in doc.toc if kind == "appendix")
    toc = (f'<nav class="toc" aria-label="{tx["toc"]}"><h2 id="toc">{tx["toc"]}</h2><ol>{chapters}</ol>'
           f'<h3>{tx["appx"]}</h3><ol>{appendices}</ol></nav>')
    state = tx["draft"] if STATE == "draft" else ""
    edition = f'{tx["edition"]} {VERSION}' + (f" ({state})" if state else "")
    title_page = f"""<header class="titlepage">
<img src="{logo_b64}" alt="HomenS.A Inc. mark: gear and circuit">
<h1>{html.escape(tx['title'])}</h1>
<p class="sub">{html.escape(tx['subtitle'])}</p>
<p><strong>Serhii Khomenko</strong></p>
<p class="meta">{html.escape(edition)} · {tx['built']} {NOW.strftime('%Y-%m-%d')} · {tx['commit']} {html.escape(COMMIT[:12])}</p>
<p class="meta">{html.escape(tx['license'])}</p>
</header>"""
    page = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(tx['title'])} — {html.escape(edition)}</title>
<meta name="author" content="Serhii Khomenko">
<style>{CSS}</style>
</head>
<body>
<main>
{title_page}
{toc}
{''.join(sections)}
</main>
</body>
</html>
"""
    out_html = DIST / f"{FILE_STEM}_{lang}.html"
    out_html.write_text(page, encoding="utf-8", newline="\n")
    footer = (f'<div style="font-size:8px;width:100%;text-align:center;color:#666;">'
              f'{html.escape(tx["title"])} · {html.escape(edition)} · <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
    out_pdf = DIST / f"{FILE_STEM}_{lang}.pdf"
    subprocess.run(["node", str(Path(__file__).resolve().parent / "render_pdf.js"), str(out_html), str(out_pdf), footer],
                   check=True)
    return out_html, out_pdf, doc.diagrams


def sha256(p):
    h = hashlib.sha256()
    h.update(Path(p).read_bytes())
    return h.hexdigest()


def tool_versions():
    def run(cmd):
        try:
            return subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout.strip().splitlines()[0]
        except Exception:  # noqa: BLE001
            return "unknown"
    import markdown_it
    return {"python": sys.version.split()[0], "node": run(["node", "--version"]),
            "chromium": run(["chromium", "--version"]), "mermaid-cli": run(["mmdc", "--version"]),
            "markdown-it-py": markdown_it.__version__, "pdfinfo": run(["pdfinfo", "-v"]) if False else ""}


def main():
    DIST.mkdir(exist_ok=True)
    for f in DIST.glob("two-worlds-one-mind_*"):
        f.unlink()
    logo = file_b64(ROOT / "assets" / "logo.svg", "image/svg+xml")
    files, diagrams = [], {}
    for lang in BOOK:
        h, p, n = build_lang(lang, logo)
        files += [h, p]
        diagrams[lang] = n
    sums = [f"{sha256(f)}  {f.name}" for f in files]
    (DIST / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8", newline="\n")
    manifest = {
        "title": "Two Worlds. One Mind.", "version": VERSION, "state": STATE,
        "languages": list(BOOK), "source_commit": COMMIT,
        "build_time_utc": NOW.strftime("%Y-%m-%dT%H:%M:%SZ"), "tools": tool_versions(),
        "mermaid_diagrams_rendered": diagrams,
        "files": [{"name": f.name, "bytes": f.stat().st_size, "sha256": sha256(f)} for f in files],
        "note": "SHA256SUMS covers the HTML and PDF files. PDF files contain a creation date, so a rebuild "
                "gives the same text but not byte-identical PDFs unless SOURCE_DATE_EPOCH is also honoured by the PDF tool.",
    }
    (DIST / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print("BUILD: OK", ", ".join(f.name for f in files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
