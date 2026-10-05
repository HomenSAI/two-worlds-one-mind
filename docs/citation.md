# Citation: decisions

## Why there is no `CITATION.cff`

The earlier `CITATION.cff` had `type: generic` at the top level. In the official CFF 1.2.0 schema
the top-level `type` can only be `software` or `dataset` (the validator reports
`'generic' is not one of ['dataset', 'software']`). Changing it to `software` just to satisfy the
validator would be wrong in substance: the main work is a book. The same file also put the DOI of
the Vision essay into the metadata of the whole book.

**Decision:** the file is no longer active. The records are in [`CITATION.bib`](../CITATION.bib)
(BibTeX, `@book` for the book and its editions, `@misc` for the Vision essay) and in the README
section "How to cite". Git history keeps the old file.

## Option: a CFF with `preferred-citation`

If you want GitHub's "Cite this repository" button, a CFF file is the only format GitHub turns
into APA/BibTeX. The correct form would be a file whose top level only describes the repository
(`type: dataset` or `software`, with an honest title) and whose `preferred-citation` has
`type: book` for the handbook. That makes the repository's own description say "software" or
"dataset" for a book, which is a compromise, and the button's output cannot be checked before the
file is on the default branch. This is left as a decision for the author
(see [author-questions.md](author-questions.md), question 8). If it is adopted, the validator in
`scripts/` should be extended to check that file against the CFF 1.2.0 schema.

## The two works

| | Handbook | Vision essay |
|---|----------|--------------|
| Title | Two Worlds. One Mind. From code to intent | Vision: Life beyond Earth, carried by machines (Homo roboticus) |
| Identifier | Git tag / release URL; no DOI | Zenodo version DOI 10.5281/zenodo.23119816, concept DOI 10.5281/zenodo.23119815 |
| Archive | none yet | Zenodo record 23119816: two PDFs (English, German) |

Checked on 5 October 2026 against the public Zenodo API: record 23119816, title as above,
published 2026-10-03, version 1.0, licence CC BY 4.0, files `Khomenko_Vision_en.pdf` and
`Khomenko_Vision_de.pdf`.

## Checks

`scripts/check_citation.py` verifies that `CITATION.bib` parses, that the required fields exist,
that no book record carries a Zenodo DOI of the essay, that the book record's edition matches the
`VERSION` file, and that a draft record has no release URL.
