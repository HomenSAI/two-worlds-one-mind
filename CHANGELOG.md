# Changelog

All changes to the book are listed here. Each published version is also a Git tag (`v1.0`, `v1.1`,
…) and a GitHub release, so every earlier state stays available with its date. A tag is not a
guarantee of long-term preservation; see the [README](README.md#versions).

Numbering: `1.1, 1.2 …` — edits, new sections, corrections; `2.0` — a new edition (new structure or
a large new part).

**Last published release: [1.0](#10--2026-10-03). The working branch is the draft of 1.1
([Unreleased](#unreleased--edition-11-draft)).** Which edition was written from which version of
the site is in [docs/provenance.md](docs/provenance.md).

## Unreleased — edition 1.1 (draft)

Status: draft / unreleased. No tag, release or archive record exists for 1.1 yet. The changes
follow the audit of 5 October 2026; each finding and what was done about it is in
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
