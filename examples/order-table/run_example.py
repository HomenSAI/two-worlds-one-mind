"""Run the whole example: attempt 1 (expected to FAIL the check), attempt 2 (expected to PASS).

    python3 examples/order-table/run_example.py

Exit code 0 only if attempt 1 fails the check AND attempt 2 passes it.
Results are written to examples/order-table/results/.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_result  # noqa: E402


def run(version):
    out = HERE / "results" / f"table_{version}.csv"
    out.parent.mkdir(exist_ok=True)
    subprocess.run([sys.executable, str(HERE / f"extract_{version}.py"), str(HERE / "data"), str(out)], check=True)
    failures = check_result.check(out, HERE / "expected.csv", HERE / "data")
    report = "\n".join(failures) + ("\n" if failures else "")
    report += f"RESULT: {'PASS' if not failures else 'FAIL'} ({len(failures)} failure(s))\n"
    (HERE / "results" / f"check_{version}.txt").write_text(report, encoding="utf-8", newline="\n")
    print(f"--- attempt {version[-1]}: {report.strip().splitlines()[-1]}")
    return failures


if __name__ == "__main__":
    f1, f2 = run("v1"), run("v2")
    ok = bool(f1) and not f2
    print("EXAMPLE OK" if ok else "EXAMPLE NOT AS EXPECTED (attempt 1 must fail, attempt 2 must pass)")
    sys.exit(0 if ok else 1)
