"""Attempt 1 - the naive version.

Idea: the order id is on the 'Order:' line, the year is the first four-digit number after
'Date', the amount is whatever digits and dots stand on the 'Total' line.
Written quickly, the way one might ask an assistant for "a script that makes a table".
"""
import csv
import re
import sys
from pathlib import Path


def extract(path):
    text = Path(path).read_text(encoding="utf-8")
    order_id = re.search(r"Order:\s*(\S+)", text).group(1)
    m = re.search(r"(?:Date|Datum):.*?(\d{4})", text)
    year = m.group(1) if m else ""
    total_line = next((l for l in text.splitlines() if "Total" in l or "Gesamt" in l), "")
    digits = re.sub(r"[^\d.]", "", total_line)  # keep digits and dots
    amount = float(digits) if digits else ""
    if "EUR" in total_line or "€" in total_line:
        currency = "EUR"
    elif "USD" in total_line:
        currency = "USD"
    else:
        currency = ""
    return {"file": Path(path).name, "order_id": order_id, "year": year,
            "amount": amount, "currency": currency, "status": "ok", "reason": ""}


def main(data_dir, out_csv):
    rows = [extract(p) for p in sorted(Path(data_dir).glob("order-*.txt"))]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file", "order_id", "year", "amount", "currency", "status", "reason"],
                           lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
