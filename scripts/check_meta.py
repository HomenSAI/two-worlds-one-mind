#!/usr/bin/env python3
"""Check citation metadata and version consistency.

M1  CITATION.bib parses; every entry has author, title, year, url or doi;
M2  the book records never carry the Zenodo DOI of the Vision essay (10.5281/zenodo.23119815/6);
M3  the Vision record exists and carries exactly the version DOI;
M4  the draft book record matches VERSION and has no release URL while the version is unreleased;
M5  README (EN/DE), CHANGELOG and CITATION.bib name the same edition as the VERSION file;
M6  no unconfirmed promises: no "forever" storage claim, no claim that GitHub and Zenodo sync
    automatically, the DOI badge is labelled as the essay;
M7  no CITATION.cff with the invalid root type remains active;
M8  published tag URLs: README does not link to a release of the current (unreleased) version.
Default is RELEASE_STATE=released (the state of main). Set RELEASE_STATE=draft on a draft branch of the next
edition to apply the draft-specific rules (M4, M8).
"""
import os
import re
import sys
from pathlib import Path

import bibtexparser
import yaml

ROOT = Path(os.environ.get("BOOK_ROOT") or Path(__file__).resolve().parents[1]).resolve()
errors = []


def err(msg):
    errors.append(msg)


def main():
    version = (ROOT / "VERSION").read_text().strip()
    released = os.environ.get("RELEASE_STATE", "released") == "released"
    bib = bibtexparser.loads((ROOT / "CITATION.bib").read_text(encoding="utf-8"))
    entries = {e["ID"]: e for e in bib.entries}
    if not entries:
        err("CITATION.bib has no entries")
    for k, e in entries.items():                                                     # M1
        for f in ("author", "title", "year"):
            if f not in e:
                err(f"CITATION.bib {k}: missing {f}")
        if "url" not in e and "doi" not in e:
            err(f"CITATION.bib {k}: needs url or doi")
    essay_ids = ("23119816", "23119815")
    for k, e in entries.items():                                                     # M2
        if e["ENTRYTYPE"] == "book":
            blob = " ".join(str(v) for v in e.values())
            if any(i in blob for i in essay_ids):
                err(f"CITATION.bib {k}: a book record carries a Zenodo DOI of the Vision essay")
            if "doi" in e and not (k == "khomenko2026twoworlds" and e["doi"] == "10.5281/zenodo.23160031"):
                err(f"CITATION.bib {k}: only the record of edition 1.1 may carry the book's own DOI (10.5281/zenodo.23160031)")
    v = entries.get("khomenko2026vision")                                            # M3
    if not v or v.get("doi") != "10.5281/zenodo.23119816" or v["ENTRYTYPE"] != "misc":
        err("CITATION.bib: the Vision essay record is missing or wrong (must be @misc with doi 10.5281/zenodo.23119816)")
    cur = entries.get("khomenko2026twoworlds")                                       # M4
    if not cur or not cur.get("edition", "").startswith(version):
        err(f"CITATION.bib: khomenko2026twoworlds edition does not start with VERSION {version}")
    elif not released:
        if "draft" not in cur["edition"].lower():
            err("CITATION.bib: draft edition must say draft")
        if "/releases/tag/v" + version in cur.get("url", ""):
            err("CITATION.bib: the draft record points to a release URL that does not exist yet")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")                         # M5, M6, M8
    readme_de = (ROOT / "README.de.md").read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if not released:
        for name, text, needle in (("README.md", readme, f"edition {version}"), ("README.de.md", readme_de, f"Ausgabe {version}")):
            if needle not in text:
                err(f"{name}: does not mention '{needle}'")
        if f"edition {version} (draft)" not in changelog:
            err(f"CHANGELOG.md: no 'edition {version} (draft)' section")
        for name, text in (("README.md", readme), ("README.de.md", readme_de)):
            if f"/releases/tag/v{version}" in text:
                err(f"{name}: links to a release of the unreleased version {version}")
    for name, text in (("README.md", readme), ("README.de.md", readme_de)):
        low = text.lower()
        if "forever" in low or "für immer" in low:
            err(f"{name}: unconfirmed long-term-storage promise")
        if re.search(r"updated together|every new version here gets a matching", low):
            err(f"{name}: unconfirmed GitHub/Zenodo synchronisation promise")
        if "badge/DOI" in text and not re.search(r"alt=\"[^\"]*(Vision essay|Vision-Essay)", text):
            err(f"{name}: the DOI badge is not labelled as the Vision essay")
    cff = ROOT / "CITATION.cff"                                                      # M7
    if cff.exists() and re.search(r"^type:\s*generic", cff.read_text(encoding="utf-8"), re.M):
        err("CITATION.cff with invalid 'type: generic' is still present")
    for p in ROOT.rglob("*.md"):
        if "node_modules" in p.parts or "dist" in p.parts:
            continue
        t = p.read_text(encoding="utf-8")
        if re.search(r"\]\(CITATION\.cff\)|\(\.\./CITATION\.cff\)", t):
            err(f"{p.relative_to(ROOT)}: links to the removed CITATION.cff")
    form = ROOT / ".github" / "ISSUE_TEMPLATE" / "text-correction.yml"          # M9 issue form
    try:
        y = yaml.safe_load(form.read_text(encoding="utf-8"))
        ids = [b.get("id") for b in y["body"] if b.get("id")]
        if not (y.get("name") and y.get("description") and y.get("body")) or len(ids) != len(set(ids)):
            err("issue form: name, description, body required and ids unique")
        for need in ("chapter", "quote", "problem", "suggestion", "source"):
            if need not in ids:
                err(f"issue form: field {need} missing")
    except Exception as e:  # noqa: BLE001
        err(f"issue form is not valid YAML: {e}")
    for p in sorted((ROOT / ".github" / "workflows").glob("*.yml")):                # M10 workflows
        try:
            w = yaml.safe_load(p.read_text(encoding="utf-8"))
            if w.get("permissions") != {"contents": "read"}:
                err(f"{p.name}: top-level permissions must be exactly contents: read")
            for job in w["jobs"].values():
                for step in job["steps"]:
                    u = step.get("uses", "")
                    if u and not re.search(r"@[0-9a-f]{40}\b", u):
                        err(f"{p.name}: action not pinned to a commit SHA: {u}")
        except Exception as e:  # noqa: BLE001
            err(f"{p.name}: not valid workflow YAML: {e}")
    if errors:
        print("\n".join(errors))
        print(f"META: FAIL ({len(errors)} problem(s))")
        return 1
    print(f"META: OK (CITATION.bib {len(entries)} records, version {version}, state {'released' if released else 'draft'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
