# GitHub settings: prepared values and instructions

Status: **prepared, not applied.** Changing repository settings is an administrative action for the
owner (account HomenSAI). Nothing here was changed on GitHub by the editor; the state below was read
from the public API on 5 October 2026.

## 1. About (Description, Website, Topics)

| Field | Value to enter |
|-------|----------------|
| Description | `A short handbook on systems thinking, AI-assisted work and the intersection of machines and software, with practical checklists and a clearly marked speculative essay. English and German.` |
| Website | `https://homensai.com/` (the author's site; there is no separate book page yet — see author question 13) |
| Topics | `systems-engineering`, `physical-ai`, `robotics`, `automation`, `technical-writing`, `handbook`, `local-ai` |

Current state: Website empty, no topics.

## 2. Protection of `main` and of published tags

Create these **after** the `docs` workflow has run successfully at least once on GitHub, because a
required check must exist before it can be required. A single maintainer: no required reviewers.

Ruleset 1 — *Protect main* (Settings → Rules → Rulesets → New branch ruleset, target: default branch):

- Restrict deletions: on.
- Block force pushes: on.
- Require status checks to pass: add `checks` and `build` (the job names in `.github/workflows/docs.yml`).
- Require a pull request: **off** (the owner works alone; add it later if others join).

Ruleset 2 — *Protect release tags* (New tag ruleset, target pattern `v*`):

- Restrict deletions: on.
- Restrict updates: on (a published tag such as `v1.0` is never moved).
- Restrict creations: off, so that new release tags can be made.

The same two rulesets as JSON for import are in [rulesets/](rulesets/).

## 3. Licence recognition

`LICENSE` now has the unmodified standard CC BY 4.0 text. After the branch reaches `main`, open the
repository page and check the sidebar: it should say *Creative Commons Attribution 4.0 International*
instead of "Other". The API check: `GET /repos/HomenSAI/two-worlds-one-mind` → `license.spdx_id` is
`CC-BY-4.0`. Not yet checked (the file is not on `main`).

## 4. Authorship of future commits

Checked on the API: the commits `8435e7f` and `7c05fe2` (author email `info@homensai.com`) have no linked
GitHub account (`author: null`), commit `a9ddd6d` is linked to another account. The account HomenSAI has the
numeric id 215283869, so its GitHub noreply address has the form
`215283869+HomenSAI@users.noreply.github.com` (as documented by GitHub; confirm it at Settings →
Emails before using it).

For the commits to show as made by HomenSAI, one of these is needed from the owner:

1. Settings → Emails → add `info@homensai.com` and verify it by the link in the mail; or
2. use the noreply address shown in Settings → Emails as the commit email.

The editor used the name Serhii Khomenko and `info@homensai.com` for the commits of this edition,
by instruction, without touching the global Git configuration. Whether the first option is already
done was not visible to the editor. Old history is not rewritten. The AI co-author line is kept on
purpose; AI involvement is also stated in the Notes. One older commit contains a personal e-mail
address; removing it from published history is a separate, optional task with side effects
(rewriting history) and is not part of this edition.

## 5. Release page

Release notes text: [RELEASE_NOTES_1.1.md](RELEASE_NOTES_1.1.md). Steps: [release-checklist.md](release-checklist.md).
