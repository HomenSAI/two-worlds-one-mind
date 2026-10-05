"""Acceptance check for the order table. It was written BEFORE the extraction scripts.

Criteria (see README.md):
  C1  every input file appears exactly once in the table;
  C2  a value that is not certain is never guessed: such rows have status 'review' and an empty cell;
  C3  every cell equals the answer key (expected.csv), including which rows need review;
  C4  the sum of confirmed EUR amounts equals the key's sum.
Exit code 0 = all criteria met, 1 = at least one failed. Prints one line per failure.
"""
import csv
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

FIELDS = ["order_id", "year", "amount", "currency", "status", "reason"]


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(s):
    try:
        return Decimal(s)
    except (InvalidOperation, TypeError):
        return None


def eur_sum(rows):
    return sum((num(r["amount"]) or Decimal(0)) for r in rows
               if r["status"] == "ok" and r["currency"] == "EUR")


def check(result_csv, key_csv, data_dir):
    result, key = load(result_csv), load(key_csv)
    failures = []
    files = sorted(p.name for p in Path(data_dir).glob("order-*.txt"))
    got = [r["file"] for r in result]
    if sorted(got) != files or len(set(got)) != len(got):  # C1
        failures.append(f"C1 files in table {len(got)} (unique {len(set(got))}) vs {len(files)} input files")
    by_file = {r["file"]: r for r in result}
    for k in key:  # C2, C3
        r = by_file.get(k["file"])
        if r is None:
            continue
        for fld in FIELDS:
            a, b = r[fld], k[fld]
            same = (num(a) == num(b)) if fld == "amount" and a and b else (a == b)
            if not same:
                kind = "C2" if (k["status"] == "review" and r["status"] == "ok") else "C3"
                failures.append(f"{kind} {k['file']}: {fld} = {a!r}, expected {b!r}")
    if eur_sum(result) != eur_sum(key):  # C4
        failures.append(f"C4 sum of confirmed EUR: {eur_sum(result)} vs key {eur_sum(key)}")
    return failures


if __name__ == "__main__":
    found = check(sys.argv[1], sys.argv[2], sys.argv[3])
    for line in found:
        print(line)
    print(f"RESULT: {'PASS' if not found else 'FAIL'} ({len(found)} failure(s))")
    sys.exit(1 if found else 0)
