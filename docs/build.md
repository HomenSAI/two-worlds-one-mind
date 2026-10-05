# Building and checking the book

One command, from a clean checkout, with Docker as the only requirement (no Python, Node or Chrome
needed on your computer):

```bash
./scripts/build.sh      # builds dist/: PDF + self-contained HTML, English and German, then checks them
./scripts/check.sh      # all checks that need no build
```

On Windows use Git Bash (or WSL). The first run builds the image `two-worlds-one-mind-build:1` from the
[Dockerfile](../Dockerfile), which takes a few minutes; later runs are fast. The container sees only this
repository, mounted at `/work`, and no network is needed for the build itself.

## What is produced (in `dist/`, not committed)

| File | Content |
|------|---------|
| `two-worlds-one-mind_<version>_en.pdf` / `_de.pdf` | the whole book: title page, table of contents, chapters 0–8, Glossary, Notes, three appendices; page numbers; bookmarks |
| `two-worlds-one-mind_<version>_en.html` / `_de.html` | the same as one self-contained file: no scripts, no external resources; diagrams are pre-rendered inline SVG; the robot illustration and the logo are embedded |
| `SHA256SUMS` | SHA-256 of the four files above (`sha256sum -c SHA256SUMS`) |
| `manifest.json` | version, state (draft/released), languages, source commit, build time, tool versions, files with sizes and hashes |

An EPUB is not built: the pre-rendered diagrams and wide tables could not be made to read well in
the common e-readers within this edition, and a poor EPUB would be worse than none.

## Pipeline

1. `scripts/build.py` reads the Markdown (markdown-it-py, CommonMark + tables), numbers the headings with
   GitHub-style anchors prefixed by the chapter, removes the page-to-page navigation lines, rewrites links
   between chapters into internal links, embeds images, and renders every Mermaid block to SVG with the
   pinned `mermaid-cli`.
2. It writes the standalone HTML, then `scripts/render_pdf.js` prints it to PDF with headless Chromium.
   Chromium is run with network access refused; any attempt to load an external resource fails the build.
3. Links from the books to files that are not part of the books (for example `docs/provenance.md`) become
   links to the repository on GitHub (`main`).
4. `scripts/check_artifacts.py` checks the result (see below).

## Checks

| Script | What it checks |
|--------|----------------|
| `check_meta.py` | `CITATION.bib` (parse, fields, book and essay kept apart, no DOI for the book), `VERSION` matches README, CHANGELOG and the citation; no "forever" or sync promises; the DOI badge is labelled; no invalid `CITATION.cff` |
| `check_links.py` | all relative links, images and `#anchors` in all Markdown files, EN and DE; the language switch; German files link only to German files; each English chapter has its German counterpart; semantic checks (a link text "Chapter 3" must lead into chapter 3, "section 6" into a heading numbered 6, "Next" must lead to the next chapter) |
| `check_svg.py` | the SVG files in `assets/` are well-formed XML, with no scripts, event handlers or external resources; every image used in Markdown exists |
| `mermaid_render.py` | renders **every** Mermaid block in all Markdown files; fails on any error; EN and DE must have the same number of book diagrams |
| `examples/order-table/run_example.py` | runs the worked example: attempt 1 must fail its acceptance check, attempt 2 must pass |
| `markdownlint-cli2` | Markdown style; settings in `.markdownlint-cli2.jsonc` with the reason for each disabled rule |
| `check_artifacts.py` | after a build: files exist, SHA-256 and manifest agree, HTML is self-contained, internal links resolve, the number of inline diagrams equals the number of Mermaid blocks, PDF has text and every chapter title |
| `check_external_links.py` | run separately (monthly, or by hand): external links, with 404 told apart from 429, timeouts and refusals |

None of these replaces reading the pages: the PDFs and the HTML were also inspected visually; see the
[verification report](verification-report.md).

## Settings and pinned versions

- Base image `node:22.11.0-bookworm-slim`; Chromium and fonts from the Debian packages of that release
  (the exact versions are written to `manifest.json` at every build, because Debian package versions
  move with security updates and are not pinned in the Dockerfile).
- Python packages: `tools/requirements.txt` (exact versions). Node packages: `tools/package.json` with the
  lock file `tools/package-lock.json` (`npm ci`).
- The GitHub workflows use the two official actions pinned by commit SHA (`actions/checkout` v4.2.2,
  `actions/upload-artifact` v4.6.2) and have `contents: read` only. `release.yml` is manual, has write
  permission only for creating a **draft** release, and publishing it stays a human click.
- Builds are not byte-identical: the PDF contains a creation date. The text and the checks are stable.

## Licence of the build tools

The scripts are not part of the CC BY text. See [LICENSING.md](../LICENSING.md): no licence chosen yet; MIT is proposed.
