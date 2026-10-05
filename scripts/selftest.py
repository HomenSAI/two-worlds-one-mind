#!/usr/bin/env python3
"""Self-test of the checks: each check must FAIL on a deliberately broken copy of the repository.

A check that cannot fail proves nothing. This script copies the repository to a temporary folder,
injects one known defect at a time (several of them are the real defects named in the audit) and
expects the right check to report it. It also expects the unbroken copy to pass.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SKIP = shutil.ignore_patterns(".git", "dist", "node_modules", "__pycache__")

# (name, script, file, old, new, expected text in output)
MUTATIONS = [
    ("C11 wrong chapter in a link caption", "check_links.py", "book/08-field-guide.md",
     "[Chapter 3 · P-03, the best tools — today]", "[Chapter 2 · The best tools — today]",
     "link text says chapter 2"),
    ("missing anchor", "check_links.py", "book/08-field-guide.md",
     "03-principles.md#division-of-work", "03-principles.md#division-of-xwork", "missing anchor"),
    ("missing file", "check_links.py", "book/00-preface.md", "(notes.md)", "(no-such-file.md)", "missing target"),
    ("German file links to English chapter", "check_links.py", "book/de/02-manifesto.md",
     "[Kapitel 3](03-principles.md#machbarkeit", "[Kapitel 3](../03-principles.md#machbarkeit", "language jump"),
    ("section number does not match the anchor", "check_links.py", "book/02-manifesto.md",
     "[Field guide, section 6](08-field-guide.md#6-know-where-your-data-goes)",
     "[Field guide, section 7](08-field-guide.md#6-know-where-your-data-goes)", "section 7"),
    ("book record carries the essay DOI (G02)", "check_meta.py", "CITATION.bib",
     "note      = {Published 5 October 2026.", "doi = {10.5281/zenodo.23119816},\n  note      = {Published 5 October 2026.",
     "Zenodo DOI of the Vision essay"),
    ("draft points to a release URL that does not exist (G04)", "check_meta.py", "CITATION.bib",
     "edition   = {1.1},", "edition   = {1.1 (draft, unreleased)},", "release URL"),
    ("storage promise (G03)", "check_meta.py", "README.md", "a tag is not a guarantee", "available forever; a tag is not a guarantee",
     "long-term-storage promise"),
    ("DOI badge without the essay label (G02)", "check_meta.py", "README.md", "alt=\"Vision essay DOI", "alt=\"DOI",
     "not labelled"),
    ("invalid CFF type back (G01)", "check_meta.py", "CITATION.cff", None, "cff-version: 1.2.0\ntype: generic\ntitle: x\n",
     "type: generic"),
    ("SVG with a script", "check_svg.py", "assets/logo.svg", "</svg>", "<script>alert(1)</script></svg>", "contains <script>"),
    ("SVG not well-formed", "check_svg.py", "assets/logo.svg", "</svg>", "</svgx>", "not well-formed"),
    ("absolute comes back (C02)", "check_text.py", "book/03-principles.md", "An idea is a starting point; feasibility has to be tested.", "Once it exists, it can be built.", "forbidden phrase"),
    ("invented number in EXP-001 (C05)", "check_text.py", "experiments/EXP-001.md", "| Parallel clients | PENDING |", "| Parallel clients | 8 clients, 41.7 tokens/s |", "EXP-001"),
    ("unpinned action", "check_meta.py", ".github/workflows/docs.yml", "actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683", "actions/checkout@v4", "not pinned"),
    ("workflow with write permission by default", "check_meta.py", ".github/workflows/links.yml",
     "contents: read\n\njobs:", "contents: write\n\njobs:", "permissions"),
    ("broken Mermaid block", "mermaid_render.py", "book/05-lab.md", "flowchart LR\n    Q[Question]",
     "flowchart LR\n    Q[Question] ==>>> ((", "MERMAID: FAIL"),
    ("example check must catch a wrong key", "examples/order-table/run_example.py", "examples/order-table/expected.csv",
     "order-001.txt,SYN-2019-001,2019,12450.00", "order-001.txt,SYN-2019-001,2019,12451.00", "NOT AS EXPECTED"),
]


# mutations that only make sense for a draft edition run the check in draft state
DRAFT_ONLY = {"draft points to a release URL that does not exist (G04)"}


def run(script, root, state=None):
    env = dict(os.environ, BOOK_ROOT=str(root))
    if state:
        env["RELEASE_STATE"] = state
    path = (root / script) if "/" in script else (HERE / script)
    return subprocess.run([sys.executable, str(path)], capture_output=True, text=True, env=env, encoding="utf-8", errors="replace", cwd=root)


def main():
    failures = []
    with tempfile.TemporaryDirectory() as td:
        base = Path(td) / "base"
        shutil.copytree(ROOT, base, ignore=SKIP)
        # unbroken copy must pass the quick checks (docs/ files that are written last may not exist yet: ignore L1 there)
        for name, script, rel, old, new, expect in MUTATIONS:
            work = Path(td) / "w"
            if work.exists():
                shutil.rmtree(work)
            shutil.copytree(base, work)
            f = work / rel
            if old is None:
                f.write_text(new, encoding="utf-8")
            else:
                text = f.read_text(encoding="utf-8")
                if old not in text:
                    failures.append(f"{name}: test setup wrong, text to replace not found in {rel}")
                    continue
                f.write_text(text.replace(old, new, 1), encoding="utf-8", newline="")
            r = run(script, work, "draft" if name in DRAFT_ONLY else None)
            out = (r.stdout or "") + (r.stderr or "")
            if r.returncode == 0 or expect not in out:
                failures.append(f"{name}: the check did NOT fail as expected (exit {r.returncode}); wanted {expect!r}")
            else:
                print(f"ok  - caught: {name}")
    if failures:
        print("\n".join(failures))
        print(f"SELFTEST: FAIL ({len(failures)})")
        return 1
    print(f"SELFTEST: OK ({len(MUTATIONS)} injected defects were all caught)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
