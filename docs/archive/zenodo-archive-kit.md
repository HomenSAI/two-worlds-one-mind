# Kit for archiving the whole book on Zenodo (used for edition 1.1)

Status: **executed on 5 October 2026.** The record of edition 1.1 is Zenodo [10.5281/zenodo.23160031](https://doi.org/10.5281/zenodo.23160031)
(concept DOI 10.5281/zenodo.23160030); files uploaded by hand (option b below) from the assets of the GitHub release
`v1.1`, checksums verified. The existing record 23119816 is the Vision essay and was not touched.
For later editions, create a new *version* of the same record (so the concept DOI stays the same).

Why separately: Zenodo creates a record per upload (or per GitHub release if the repository is
switched on in the owner's Zenodo account). Doing this is an account action by the owner, after
the release exists.

## Metadata to enter (draft)

The machine-readable draft is [zenodo-book-metadata.json](zenodo-book-metadata.json). It is kept
here and **not** as `.zenodo.json` in the repository root, so that nothing happens by accident when a
release is published.

| Field | Value |
|-------|-------|
| Resource type | Publication → Book |
| Title | Two Worlds. One Mind. From code to intent: a short handbook on building where software meets the physical world |
| Authors | Khomenko, Serhii — ORCID 0009-0009-5371-9717 — affiliation as the author prefers (the book uses "HomenS.A Inc." only as a brand name) |
| Language | English (primary); German translation included |
| Version | 1.1 |
| Publication date | the date of the release (to be filled in at publication) |
| License | CC BY 4.0 (text and diagrams) |
| Related identifiers | *is derived from / references*: 10.5281/zenodo.23119816 (the Vision essay, as the source of Chapter 7); *is supplement to*: the GitHub release URL of the same version (after it exists) |
| Contents | PDF English, PDF German, self-contained HTML English and German, `SHA256SUMS`, `manifest.json`, source Markdown and SVG (the source archive of the tag) |

## Steps (owner, after the release is published)

1. Check that the release `v1.1` has the PDF, HTML, `SHA256SUMS` and `manifest.json` attached
   and that the sums match (`sha256sum -c SHA256SUMS`).
2. Either (a) in Zenodo, switch on the GitHub integration for this repository and re-publish the
   release, or (b) upload the files by hand as a new record. In both cases, use the metadata above.
3. Check the new record: title, author, ORCID, version, licence, files, the link to the tag.
4. Only then add the new DOI to `CITATION.bib`, the README and `docs/provenance.md`, and
   describe the integration as working. Keep the Vision DOI labelled as the essay.
