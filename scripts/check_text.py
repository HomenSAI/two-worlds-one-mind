#!/usr/bin/env python3
"""Regression check of the editorial corrections (audit C01-C12, section 6) in EN and DE.

T1  phrases that the audit asked to remove must not come back (English calques and absolutes,
    German counterparts of the absolutes);
T2  statements that the corrections added must be present (required phrases);
T3  EXP-001: every protocol field is PENDING or marked as reported; no invented numbers
    (only the numbers named in the author's report are allowed).
This is a guard against regressions, not a proof of good writing.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from booklib import ROOT  # noqa: E402

EN_BOOK = sorted((ROOT / "book").glob("*.md"))
DE_BOOK = sorted((ROOT / "book" / "de").glob("*.md"))

FORBIDDEN_EN = [
    "Once it exists, it can be built", "The only limits are our own", "keep the data at home",
    "so the data does not leave the building", "width of the mind", "on the fingers",
    "gave the resources and controlled", "Tools multiply", "test it on yourself", "one rope",
    "diagrams and schemes", "more technological", "a working position", "The one way a person",
    "Machines already went where", "Hardware (non-IT)", "tolerates vacuum and cold",
    "remote control is impossible", "I write the logic. The programmer codes it",
    "So far I have not met a task that could not", "Chapter 2 · The best tools",
    "Almost everything they described will be built",
]
FORBIDDEN_DE = [
    "Einmal vorhanden, lässt sie sich bauen", "Die einzigen Grenzen sind unsere eigenen",
    "damit die Daten das Haus nicht verlassen", "Weite des Geistes", "an den Fingern",
    "Kapitel 2 · Die besten Werkzeuge",
]
REQUIRED = [  # (file, phrase)
    ("book/02-manifesto.md", "does not remove the need to understand requirements"),
    ("book/03-principles.md", "Feasibility is tested, not assumed"),
    ("book/03-principles.md", "Change the requirements"),
    ("book/03-principles.md", "Stop — and record why"),
    ("book/04-physical-ai.md", "even when the output is text"),
    ("book/04-physical-ai.md", "not an engineering certification"),
    ("book/05-lab.md", "Author-reported; reproducibility details pending"),
    ("book/glossary.md", "Whether data really stays local depends on the complete configuration"),
    ("book/glossary.md", "the author's own name, not a standard step in programming"),
    ("book/08-field-guide.md", "## 6. Know where your data goes"),
    ("book/08-field-guide.md", "(03-principles.md#on-p-03--never-postpone)"),
    ("book/06-path.md", "When 3D came in"),
    ("book/07-vision.md", "real-time remote control is not possible"),
    ("book/07-vision.md", "one possible path to interstellar travel"),
    ("book/07-vision.md", "simplified illustration"),
    ("book/notes.md", "Falls, Susan (2018)"),
    ("book/notes.md", "Viereck"),
    ("book/de/02-manifesto.md", "nimmt uns nicht die Notwendigkeit ab"),
    ("book/de/03-principles.md", "Machbarkeit wird geprüft, nicht vorausgesetzt"),
    ("book/de/08-field-guide.md", "## 6. Wissen, wohin Ihre Daten gehen"),
    ("book/de/07-vision.md", "spekulative Fortsetzung"),
    ("experiments/EXP-001.md", "author-reported; reproducibility details pending"),
]
ALLOWED_NUMBERS_EXP = {"3080", "3.5", "9", "64", "262", "001", "10", "12", "1", "2", "3", "4", "5", "6", "7", "8", "256"}


def main():
    errors = []
    for files, bad in ((EN_BOOK, FORBIDDEN_EN), (DE_BOOK, FORBIDDEN_DE)):
        for p in files:
            t = " ".join(p.read_text(encoding="utf-8").split())
            for phrase in bad:
                if phrase in t:
                    errors.append(f"{p.relative_to(ROOT).as_posix()}: forbidden phrase {phrase!r}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for phrase in ("width of the mind", "available forever", "Zenodo and this repository are updated together"):
        if phrase in readme:
            errors.append(f"README.md: forbidden phrase {phrase!r}")
    for rel, phrase in REQUIRED:
        if " ".join(phrase.split()) not in " ".join((ROOT / rel).read_text(encoding="utf-8").split()):
            errors.append(f"{rel}: required text missing: {phrase!r}")
    exp = (ROOT / "experiments" / "EXP-001.md").read_text(encoding="utf-8")
    rows = [l for l in exp.splitlines() if l.startswith("| ") and "---" not in l]
    section3 = exp.split("## 3.")[1].split("## 4.")[0]
    for l in section3.splitlines():
        if l.startswith("| ") and "---" not in l and not l.startswith("| Field"):
            val = l.split("|")[2].strip()
            if val != "PENDING" and "as reported" not in val:
                errors.append(f"EXP-001 section 3: field has a value that is not PENDING or marked as reported: {l.strip()[:90]}")
    for n in re.findall(r"\d+(?:\.\d+)?", section3):
        if n not in ALLOWED_NUMBERS_EXP:
            errors.append(f"EXP-001 section 3: unexpected number {n} (only the author's reported figures are allowed)")
    if errors:
        print("\n".join(errors))
        print(f"TEXT: FAIL ({len(errors)} problem(s))")
        return 1
    print(f"TEXT: OK ({len(FORBIDDEN_EN)} + {len(FORBIDDEN_DE)} forbidden phrases absent, {len(REQUIRED)} required statements present, EXP-001 fields all PENDING/reported)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
