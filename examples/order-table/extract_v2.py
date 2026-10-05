"""Attempt 2 - after the failed check.

Changes against attempt 1 (each answers a failure reported by check_result.py):
  * the amount is read from the total line only, with the currency token next to it;
  * number formats are interpreted by explicit rules (see parse_number);
  * a number that can be read in two ways is NOT guessed: the row gets status 'review';
  * a missing amount, a two-digit year or an unknown format also give 'review';
  * the 'Total (gross)' line wins over 'Net'; currencies are kept, never converted.
"""
import csv
import re
import sys
from decimal import Decimal
from pathlib import Path

CURRENCIES = {"EUR": "EUR", "USD": "USD", "JPY": "JPY", "€": "EUR"}
TOTAL_LABELS = ("Total (gross)", "Total", "Gesamtbetrag")


class Ambiguous(Exception):
    pass


def parse_number(token):
    """Return a Decimal, or raise Ambiguous when the format allows two readings."""
    t = token.strip().replace(" ", " ")
    if re.fullmatch(r"\d{1,3}( \d{3})+", t):                    # 3 200
        return Decimal(t.replace(" ", ""))
    if re.fullmatch(r"\d{1,3}(,\d{3})+\.\d{1,2}", t):           # 12,450.00
        return Decimal(t.replace(",", ""))
    if re.fullmatch(r"\d{1,3}(\.\d{3})+,\d{1,2}", t):           # 8.900,50
        return Decimal(t.replace(".", "").replace(",", "."))
    if re.fullmatch(r"\d{1,3}(,\d{3}){2,}", t):                 # 1,250,000
        return Decimal(t.replace(",", ""))
    if re.fullmatch(r"\d{1,3}(\.\d{3}){2,}", t):                # 1.250.000
        return Decimal(t.replace(".", ""))
    if re.fullmatch(r"\d+[.,]\d{1,2}", t):                      # 2,10 / 2.10
        return Decimal(t.replace(",", "."))
    if re.fullmatch(r"\d{1,3}[.,]\d{3}", t):                    # 1.250 or 7,500: two readings
        raise Ambiguous("amount ambiguous")
    if re.fullmatch(r"\d+", t):
        return Decimal(t)
    raise Ambiguous("amount format unknown")


def find_total(text):
    for label in TOTAL_LABELS:
        m = re.search(rf"^{re.escape(label)}:\s*(.+)$", text, re.M)
        if m:
            return m.group(1).strip()
    return None


def read_year(text):
    m = re.search(r"^(?:Date|Datum):\s*(.+)$", text, re.M)
    if not m:
        return None, "year missing"
    d = m.group(1).strip()
    for pat in (r"(\d{4})-\d{2}-\d{2}", r"\d{1,2}\.\d{1,2}\.(\d{4})", r"\d{1,2}/\d{1,2}/(\d{4})"):
        mm = re.fullmatch(pat, d)
        if mm:
            return mm.group(1), None
    return None, "year ambiguous"


def fmt_amount(value, currency):
    if currency == "JPY":
        return str(int(value))
    return format(value.quantize(Decimal("0.01")), "f")


def extract(path):
    text = Path(path).read_text(encoding="utf-8")
    row = {"file": Path(path).name, "order_id": re.search(r"^Order:\s*(\S+)", text, re.M).group(1),
           "year": "", "amount": "", "currency": "", "status": "ok", "reason": ""}

    def flag(reason):
        if row["status"] == "ok":  # keep the first reason
            row["status"], row["reason"] = "review", reason

    year, why = read_year(text)
    if year:
        row["year"] = year
    else:
        flag(why)
    raw = find_total(text)
    if raw is None or not re.search(r"\d", raw):
        flag("amount missing")
        return row
    cur = sorted({v for k, v in CURRENCIES.items() if k in raw})
    number = re.sub("|".join(map(re.escape, CURRENCIES)), "", raw).strip()
    try:
        value = parse_number(number)
    except Ambiguous as e:
        flag(str(e))
        return row
    if len(cur) != 1:
        flag("currency unclear")
        return row
    row["amount"] = fmt_amount(value, cur[0])
    row["currency"] = cur[0]
    return row


def main(data_dir, out_csv):
    rows = [extract(p) for p in sorted(Path(data_dir).glob("order-*.txt"))]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file", "order_id", "year", "amount", "currency", "status", "reason"],
                           lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
