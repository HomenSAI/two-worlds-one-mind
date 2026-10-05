# Changelog

All changes to the book are listed here. Each published version is also a Git tag (`v1.0`, `v1.1`,
…) and a GitHub release, so every earlier state stays available with its date. A tag is not a
guarantee of long-term preservation; see the [README](README.md#versions).

Numbering: `1.1, 1.2 …` — edits, new sections, corrections; `2.0` — a new edition (new structure or
a large new part).

**Last published release: [1.1](#11--2026-10-05).** Which edition was written from which version of
the site is in [docs/provenance.md](docs/provenance.md).

## Unreleased

- Two Zenodo records of edition 1.1 are now explained and linked: the book (the one to cite) and the
  Software record of the GitHub release (sources, 10.5281/zenodo.23159950). On the Software record the
  author is now Khomenko, Serhii (ORCID) instead of the account name, and both records point to each
  other. `.zenodo.json` gives later releases the same author and the link to the book.

- The whole book, edition 1.1, is archived on Zenodo as its own record: version DOI
  [10.5281/zenodo.23160031](https://doi.org/10.5281/zenodo.23160031), concept DOI 10.5281/zenodo.23160030 (files: PDF and HTML in English and German,
  `SHA256SUMS`, `manifest.json`, source archive of tag `v1.1`). README, `CITATION.bib`, Notes (EN/DE),
  `docs/citation.md` and `docs/provenance.md` now carry this DOI; the Vision essay keeps its own
  DOIs and label. `scripts/check_meta.py` allows the book's own DOI only on the record of edition 1.1.

## [1.1] — 2026-10-05

Git tag `v1.1`, GitHub release with the PDF and HTML files (English and German), `SHA256SUMS` and
`manifest.json`. No archive record (DOI) existed for the whole book at the time of the release (it was
created the same day, see *Unreleased*). The changes follow the
audit of 5 October 2026; each finding and what was done about it is in
[docs/audit-resolution.md](docs/audit-resolution.md).

### Metadata made after v1.0 (already on `main` before this edition)

- Author ORCID added to `CITATION.cff` and README (commit `7c05fe2`).
- `.gitignore` extended (commit `7c05fe2`).

### Citation, archiving, licence

- `CITATION.cff` removed from active use (its `type: generic` is not valid in CFF 1.2.0 and a
  book is not software); replaced by [CITATION.bib](CITATION.bib) with separate `@book` records for
  the book (1.1 draft, 1.0) and an `@misc` record for the Vision essay; reasons and the option of
  a `preferred-citation` CFF in [docs/citation.md](docs/citation.md). Git history keeps the old file.
- The Zenodo DOI is labelled "Vision essay DOI" everywhere; the unconfirmed promise of automatic
  GitHub–Zenodo synchronisation and "forever" storage is removed; a kit for archiving the whole book
  separately is in [docs/archive/](docs/archive/zenodo-archive-kit.md) (no DOI is claimed).
- `LICENSE` is now the unmodified standard CC BY 4.0 text; scope, the excluded mark, the mark inside
  the robot illustration and the open question about the build scripts are in
  [LICENSING.md](LICENSING.md).

### Text (English)

- Understanding and delegation made consistent: AI reduces manual work, it does not remove the need
  to understand requirements, constraints and verification (audit C01).
- "Once it exists, it can be built" and similar absolutes replaced by tested feasibility; the
  uncertainty diagram now has the outcomes research / change the requirements / stop (C02).
- Physical AI: text errors can have consequences too; a staged approach from requirements to
  controlled use, explicitly not a certification (C03).
- Local AI no longer implies that data stays local; new data-flow checklist in the Field guide (C04).
- EXP-001 is now a protocol with every unknown field marked `PENDING`; the result is labelled
  "author-reported; reproducibility details pending" (C05). Nothing was measured or invented.
- 3D/CAD dates separated into first contact, company switch and so on (C06); achievements, periods
  and personal role versus team stated precisely, "CIS leader" marked as the author's account (C07).
- Notes rewritten with full references; prior uses of "Homo roboticus" identified (C08).
- Vision: facts and hypotheses separated; remote control, robot durability, "the one way",
  the evolution picture and the Voyager/Mars facts corrected in text, diagram and SVG (C09).
- Worked example `examples/order-table` with synthetic data and executed checks (C10).
- Wrong link caption in Field guide section 7 fixed (C11); philosophical management introduced as
  the author's own term and "hardware (non-IT)" replaced by mechanical systems (C12).
- Language fixes (calques, repeated slogans); wellbeing remark phrased as personal experience.
- Author's answers of 5 October 2026 applied to Chapters 1, 3 and 6 (English and German): 2D AutoCAD
  introduced by the author from 2004 (not as the designer) and 3D (SolidWorks, later Inventor) from
  2010, replacing "3D from 2002"; EKVIPTEH team at the peak "up to about 25" (was 26); turnover of
  "up to about $0.9M" given for EKVIPTEH only, for its best years 2012–2013; "CIS leader" for UViS Technologii
  kept as the author's subjective judgement with its stated reason; the author's role at UViS Technologii stated
  as one of the three who started it, de facto founder, oral arrangement without documents, paid a
  salary, no influence on finances.

### Licence decisions (author, 5 October 2026)

- The illustration `line-of-development.svg` may be reproduced under CC BY 4.0 including the mark on
  the robot, if the mark is not separated and no endorsement is suggested.
- Build scripts, workflows and example scripts: MIT licence ([LICENSE-CODE](LICENSE-CODE)); the book
  stays CC BY 4.0.
- No `CITATION.cff`; `CITATION.bib` and the README remain the citation route.

### German edition and tools

- Full German edition `book/de/` (chapters 0–8, Glossary, Notes), `README.de.md`, German
  templates; status in [docs/translation-status.md](docs/translation-status.md).
- Reproducible build of PDF and self-contained HTML in English and German (`./scripts/build.sh`,
  Docker), SHA-256 sums and a manifest; checks (links and anchors, Mermaid, SVG, citation, example,
  Markdown lint) in `scripts/` and `.github/workflows/docs.yml`.
- Added: `CONTRIBUTING.md`, an issue form, `templates/intent-card.md`, `docs/` (audit resolution,
  author questions, GitHub settings, release checklist, provenance, verification report).

## [1.0] — 2026-10-03

First edition. Git tag `v1.0` (commit `8435e7f`).

- Chapters 0–8: Preface, Three worlds, Manifesto, Principles, Physical AI, Lab, Path, Vision,
  Field guide.
- Glossary, Notes and sources.
- Built from the author's own texts and the pages of homensai.com, site version 2.11.
- Chapter 7: the "line of development" picture on a night sky, ending with Homo roboticus as the
  HomenS.A robot (same picture as on the site and in the Zenodo PDF).
- Diagrams as Mermaid (rendered by GitHub).
- License CC BY 4.0, citation file, Zenodo DOI 10.5281/zenodo.23119816 (Vision text).
- "HomenS.A Inc." marked as a brand name, not a legal entity; private, non-commercial project.
