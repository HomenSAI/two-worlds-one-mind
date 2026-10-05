# Release checklist for edition 1.1

Status: **prepared, not executed.** The edition is a draft until every step below is done. Merging
to `main`, publishing the release and any archive record need the owner's approval.

## Before the merge

- [ ] Read [author-questions.md](author-questions.md); answer what you can. Nothing blocks the release,
      but open questions stay visible in the text as neutral wording.
- [ ] Read the German edition (or arrange a proof-reader) — [translation-status.md](translation-status.md).
- [ ] The `docs` workflow is green on the pull request (GitHub Actions → *docs*; both jobs `checks`
      and `build`). Download the artifact `book-preview-<sha>` and open the PDFs and HTML files.
- [ ] `sha256sum -c SHA256SUMS` passes for the downloaded artifact.
- [ ] Merge the pull request into `main` (normal merge or squash; do not force-push; do not move `v1.0`).

## Switch the draft to a release (one small commit on `main`)

These places say "draft / unreleased" or avoid a release link until the release exists:

- [ ] `VERSION` stays `1.1`.
- [ ] `README.md` and `README.de.md`: status table ("This branch … draft, unreleased") → "Last published
      release: **v1.1**"; add the links **Download PDF / HTML** to the release assets
      (`https://github.com/HomenSAI/two-worlds-one-mind/releases/tag/v1.1`); remove "Until a release is
      published, the files are available as workflow artifacts".
- [ ] `CITATION.bib`: record `khomenko2026twoworlds` → `edition = {1.1}`, `url` = the release URL, remove
      "Draft: …" from `note`. (`check_meta.py` with `RELEASE_STATE=released` then passes.)
- [ ] `CHANGELOG.md`: rename "Unreleased — edition 1.1 (draft)" to "[1.1] — <date>" and open a new empty
      "Unreleased" section.
- [ ] `docs/provenance.md`: fill in the final commit hash and tag of 1.1.
- [ ] `book/` text needs no change; the title page of the PDF/HTML drops "(draft, unreleased)" when the
      build runs with `RELEASE_STATE=released`.
- [ ] Re-run `RELEASE_STATE=released ./scripts/check.sh` and `RELEASE_STATE=released ./scripts/build.sh`.

## Tag and release

- [ ] Create the annotated tag `v1.1` on the release commit (never move an existing tag).
- [ ] Run the workflow *release-draft* (Actions → release-draft → Run workflow, tag `v1.1`): it builds from the
      tag and creates a **draft** release with the PDFs, HTML files, `SHA256SUMS` and `manifest.json`,
      with the text of [RELEASE_NOTES_1.1.md](RELEASE_NOTES_1.1.md).
- [ ] Open the draft, check the files and the text, then publish it.

## After the release

- [ ] Optional: archive the whole book on Zenodo — [archive kit](archive/zenodo-archive-kit.md). Only then
      add the new DOI to `CITATION.bib`/README.
- [ ] Apply [github-settings.md](github-settings.md): description, website, topics, rulesets (after the
      workflow has run once on `main`). Check that GitHub now shows the licence as CC BY 4.0.
- [ ] Confirm the e-mail of future commits (github-settings.md, section 4).
- [ ] Site recommendation (nothing was changed on homensai.com): add a page or a link block "Read the
      book" with the release link, the two languages and the PDF/HTML downloads; state the book
      version and that the text is not synchronised with the site.
- [ ] Copy the release to Drive/Obsidian as usual.
