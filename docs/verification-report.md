# Verification report: edition 1.1 (draft)

What was run, with which tools, what came out, and what was **not** checked. Date: 5 October 2026.
Everything ran inside the pinned Docker image `two-worlds-one-mind-build:1` (see [build.md](build.md)),
started with `./scripts/check.sh` and `./scripts/build.sh` on a clean checkout of the branch.
The runs below were made on commit `f25641a`; the only later change is this report.

## Tool versions

From `dist/manifest.json` of the run: Python 3.11.2, Node v22.11.0, Chromium 154.0.8037.92 (Debian 12),
mermaid-cli 11.4.2, markdown-it-py 3.0.0, markdownlint-cli2 0.15.0 (markdownlint 0.36.1), pypdf 5.1.0,
PyYAML 6.0.2, bibtexparser 1.4.2, poppler-utils (Debian 12) for page images. The workflows use
`actions/checkout` v4.2.2 and `actions/upload-artifact` v4.6.2, pinned by SHA.

## `./scripts/check.sh`: result `CHECKS: ALL PASSED`

| Check | Result |
|-------|--------|
| `check_meta.py` | `META: OK` (3 BibTeX records, version 1.1, state draft; issue form and three workflows parsed; workflow permissions `contents: read`; all actions pinned by SHA) |
| `check_links.py` | `LINKS: OK` (44 Markdown files: relative links, anchors, language separation, counterparts, semantic checks of chapter and section captions) |
| `check_text.py` | `TEXT: OK` (28 forbidden phrases absent, 22 required statements present, EXP-001 fields all PENDING or marked as reported) |
| `check_svg.py` | `SVG: OK` (2 SVG files well-formed, no scripts or external resources, 4 image references resolve) |
| `selftest.py` | `SELFTEST: OK`, 19 injected defects all caught (see below) |
| `mermaid_render.py` | `MERMAID: OK`, 24 blocks rendered (12 English + 12 German); no other Markdown file has a block |
| `examples/order-table/run_example.py` | attempt 1 `FAIL (18 failure(s))`, attempt 2 `PASS (0 failure(s))`, `EXAMPLE OK` |
| `markdownlint-cli2` | 44 files, 0 errors (settings and reasons in `.markdownlint-cli2.jsonc`) |

**Self-test.** A check that cannot fail proves nothing, so `selftest.py` makes a copy of the repository,
injects one defect at a time and expects the right check to fail. The 19 defects include the audit's own:
invalid `type: generic` in a CFF file, the essay DOI in the book record, a draft pointing at a
non-existent release, a "forever" promise, a DOI badge without the essay label, the wrong chapter in a link
caption (C11), a missing anchor, a German file linking into the English folder, an old absolute coming back
(C02), an invented number in EXP-001 (C05), an unpinned action, a workflow with write permission, a script
inside an SVG, a malformed SVG, a broken Mermaid block, and a wrong answer key in the example. All 18 were caught.

## `./scripts/build.sh`: result `BUILD: OK`, `ARTIFACTS: OK`

English: 39 PDF pages, 12 inline diagrams, 14 sections. German: 43 PDF pages, 12 inline diagrams, 14 sections.
`check_artifacts.py` verified for both languages: files present, SHA-256 equal to `SHA256SUMS` and to the
manifest, HTML without `<script>`, `<link>`, `@import` or external resources, every internal `#link` has a
target, the number of inline diagrams equals the number of Mermaid blocks in the sources, every chapter
and appendix title is found in the extractable PDF text. The PDF printer refuses all network requests, so an
external resource would have failed the build. PDF fonts are embedded (Liberation Sans, DejaVu).

## Visual inspection

- **PDF, all pages of both files** (39 + 43 = 82 pages) were looked at as page images (85 dpi, two pages
  per image): title page, table of contents, the start and end of every chapter, every table and every
  diagram. Findings that were fixed: tables with identifiers broken across lines ("EX P-00 1"), an empty
  table header row, wide diagrams too small to read (spacing reduced; the staged diagram made vertical),
  checklists shown as "[ ]" text (now check boxes), over-long lines in the intent-card text blocks, a label of
  the robot illustration cut off at the edge and a note overlapping the picture. After those fixes the pages
  with changes were looked at again (intent cards, tables with identifiers, uncertainty and staged
  diagrams); page counts did not change.
- **HTML** was opened in a browser pane at 375 px (mobile) and 1280 px (desktop) width, English and
  German: no page-level horizontal overflow; wide tables scroll inside their own frame on the phone; all
  internal links resolve; the 12 diagrams are inline SVG. A screenshot of the German page at desktop
  width timed out, so desktop was checked by measurement only (page width, table widths).
- The robot illustration is a picture with small labels; on a phone its labels are too small to read. This
  is a property of the original image and was not redesigned.

## External facts checked on 5 October 2026

Zenodo API (record 23119816: title, DOIs, files, licence; no record for the book), GitHub API (releases,
tags, default branch, topics, licence detection, commits' linked accounts), NASA pages (Mars delay 3 to
22 minutes, Voyager 1 dates, one light-day on 18 November 2026), the Falls 2018 article and the
bibliographic records of the 2017/2019/2023 "Homo roboticus" books, the Einstein interview (date and
title), the CC BY 4.0 legal text (identical to the copy in `LICENSE`). `check_external_links.py` was run by hand over all 23 unique external URLs of the Markdown files: 22 OK, 1 FORBIDDEN (the DOI link of the Falls article: the publisher refuses automatic access with HTTP 403; the DOI itself was confirmed in a web search), no broken link.

## Not verified, and why

- The *docs* workflow ran on GitHub: the first run failed (shell scripts not executable, fixed in commit
  `f6286cd`), the second run is green in both jobs and produced the preview artifact. The *external-links* and
  *release-draft* workflows have not been run.
- GitHub's recognition of `LICENSE`, the issue form's rendering, branch protection and the Release page can
  only be seen on GitHub after the merge, and the settings need the owner's account.
- The German text has not been reviewed by a native speaker or by the author; the check is structural.
- The statements about the author's career are the author's own and were not verified; see
  [author-questions.md](author-questions.md).
- PDFs are not byte-reproducible (creation date); the text and checks are.
