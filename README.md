<p align="center">
  <img src="assets/logo.svg" alt="HomenS.A Inc. mark: gear and circuit" width="120">
</p>

<h1 align="center">Two Worlds. One Mind.</h1>

<p align="center">
  <b>From code to intent — a short handbook on building where software meets the physical world</b><br>
  Serhii Khomenko · HomenS.A Inc. · English · <a href="README.de.md">Deutsch</a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey.svg" alt="License: CC BY 4.0"></a>
  <a href="https://doi.org/10.5281/zenodo.23119816"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.23119816.svg" alt="Vision essay DOI 10.5281/zenodo.23119816 (the essay only, not the whole book)"></a>
</p>

---

## What this is

A short handbook on **systems thinking, AI-assisted work and the point where machines and software
meet**. It is written from twenty years of designing machines and production lines, and from
today's work with robotics, automation and local AI. Each chapter is one idea in a few pages; the
last chapter turns the ideas into checklists. Chapter 7 is a clearly marked speculative essay.

**Who it is for:** engineers, founders and managers who work with machines, production or
projects — and anyone who wants to work faster with modern tools without losing control.

**What you can apply tomorrow:**

- an [intent card](templates/intent-card.md) to write down what you want and how you will check it;
- a way to decide what to delegate to people or AI, and how to verify the result;
- a [checklist for finding out where your data really goes](book/08-field-guide.md#6-know-where-your-data-goes)
  before using a "local" AI tool;
- a staged outline for testing AI that influences a machine;
- a [worked example](examples/order-table/README.md) with real, runnable checks (on synthetic data).

## Languages

| English | Deutsch |
|---------|---------|
| This page · [Contents](#contents) | [README.de.md](README.de.md) · [Inhalt](README.de.md#inhalt) |
| [book/](book/00-preface.md) | [book/de/](book/de/00-preface.md) |

The German edition is a translation of the edited English text; its review status is in
[docs/translation-status.md](docs/translation-status.md).

## Read and download

- **Read online:** the chapters below, rendered by GitHub.
- **Complete book as one PDF / one self-contained HTML file** (English and German): built by the
  [docs workflow](.github/workflows/docs.yml) or locally with `./scripts/build.sh` (see
  [docs/build.md](docs/build.md)). Until a release is published, the files are available as
  workflow artifacts (Actions → *docs* → a run → Artifacts), not as release downloads.
- **Source:** this repository (Markdown and SVG).

## Status of this version

| | |
|---|---|
| Last published release | [**v1.0**](https://github.com/HomenSAI/two-worlds-one-mind/releases/tag/v1.0), 3 October 2026 (unchanged) |
| This branch | **edition 1.1 — draft, unreleased**: edited text, German edition, examples, build and checks |
| What changed | [CHANGELOG.md](CHANGELOG.md) · how each audit finding was handled: [docs/audit-resolution.md](docs/audit-resolution.md) |
| Which site version the text is based on | [docs/provenance.md](docs/provenance.md) — the book is **not** kept in sync with homensai.com automatically |

## Contents

| # | Chapter | In one line | On the site |
|---|---------|-------------|-------------|
| 0 | [Preface](book/00-preface.md) | Why this book exists | — |
| 1 | [Three worlds](book/01-three-worlds.md) | Imagination, machines and code led here | [Home](https://homensai.com/) |
| 2 | [Manifesto](book/02-manifesto.md) | Imagine wider. Build faster. | [Manifesto](https://homensai.com/manifesto.html) |
| 3 | [Principles](book/03-principles.md) | From programming to philosophical management (the author's own term) | [Concept](https://homensai.com/concept.html) |
| 4 | [Physical AI](book/04-physical-ai.md) | Test what AI can really do in the physical world | [Concept](https://homensai.com/concept.html) |
| 5 | [Lab](book/05-lab.md) | Don't trust it because it's new. Test it. | [Lab](https://homensai.com/lab.html) |
| 6 | [Path](book/06-path.md) | Steel and silicon — always both | [Path](https://homensai.com/path.html) |
| 7 | [Vision](book/07-vision.md) | Life beyond Earth, carried by machines (speculative) | [Vision](https://homensai.com/vision.html) |
| 8 | [Field guide](book/08-field-guide.md) | The method as checklists you can use | — |
| — | [Glossary](book/glossary.md) | Short definitions of the terms used | — |
| — | [Notes and sources](book/notes.md) | Notes, prior uses of terms, references | — |

Read it in order, or jump to the chapter you need — each one stands on its own.

Practical material: [templates/intent-card.md](templates/intent-card.md) ·
[examples/order-table](examples/order-table/README.md) ·
[experiments/EXP-001.md](experiments/EXP-001.md).

## The idea in five lines

1. **We are moving from code to intent.** AI reduces manual work; people still have to understand the requirements, the constraints and how to check the result.
2. **The hardest part is the idea.** Building has become much easier; imagination and judgement are the scarce resource.
3. **Routine goes to machines, verified.** People keep what only people can do: ideas, judgement, responsibility, trust.
4. **Software must meet the physical world.** Robots, CNC machines, sensors — that is where AI is really tested, step by step.
5. **The line of development may continue.** My personal, speculative belief: the next step after *Homo sapiens* — working name *Homo roboticus* — is life carried by machines across worlds.

## Author

**Serhii Khomenko** — Diplom-Systemingenieur, Stuttgart region, Germany.
Twenty years designing machines, production lines and the logic that runs them; today
robotics, automation and local AI.

- Site: <https://homensai.com/>
- ORCID: <https://orcid.org/0009-0009-5371-9717>
- Contact: info@homensai.com

## How to cite

The book and the Vision essay are **two separate works** with separate records. The machine-readable
records are in [CITATION.bib](CITATION.bib).

**The book (edition 1.1 is a draft; until a release exists, cite the repository and the edition):**

> Khomenko, S. (2026). *Two Worlds. One Mind. From code to intent: a short handbook on building
> where software meets the physical world.* Edition 1.1 (draft, unreleased). Self-published.
> <https://github.com/HomenSAI/two-worlds-one-mind>

The published first edition: Khomenko, S. (2026). *Two Worlds. One Mind. …* Edition 1.0.
<https://github.com/HomenSAI/two-worlds-one-mind/releases/tag/v1.0>

**The Vision essay** (the text behind [Chapter 7](book/07-vision.md); a different work) is archived
on Zenodo in English and German:

> Khomenko, S. (2026). *Vision: Life beyond Earth, carried by machines (Homo roboticus).* Zenodo.
> <https://doi.org/10.5281/zenodo.23119816>

That DOI identifies the essay, **not this handbook**. The handbook has no archive record of its own
yet; its published versions are available through GitHub Releases. Why there is no
`CITATION.cff`: [docs/citation.md](docs/citation.md).

## Versions

Every change is listed in [CHANGELOG.md](CHANGELOG.md). Published versions are identified by Git
tags and GitHub Releases (`v1.0`, `v1.1`, …); a tag is not a guarantee of long-term preservation. For
that, use an archive record when one exists (for the handbook none exists yet). Which edition was
written from which version of the site, and which commit: [docs/provenance.md](docs/provenance.md).

## License

Text and diagrams: © 2026 Serhii Khomenko, licensed under
[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE) — you may share and adapt
them, also commercially, as long as you name the author and link to the licence. The name and mark
"HomenS.A Inc." are not covered; details, including the mark in the robot illustration and the
status of the build scripts, are in [LICENSING.md](LICENSING.md).

"HomenS.A Inc." is the author's brand name, not a registered company or legal entity. This is a
private, non-commercial project: nothing here is offered for sale.

## Suggest a correction

Found a factual error, a weak sentence or a translation problem? See
[CONTRIBUTING.md](CONTRIBUTING.md) — there is an issue form for it. Please do not post personal
data.
