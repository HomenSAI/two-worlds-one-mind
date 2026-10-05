# Worked example: from a pile of order confirmations to a checked table

[Contents](../../README.md) · [Deutsch](README.de.md) · [Field guide](../../book/08-field-guide.md)

**What this is.** One complete walk through the checklists of the
[Field guide](../../book/08-field-guide.md): intent card, constraints, definition of "done",
procedure, a failure, the fix, the verification and the conclusion. It is a **teaching example**.
It is not a case from the author's career and it is **not evidence for
[EXP-001](../../experiments/EXP-001.md)** (the local inference server) or for the planned
archive experiment EXP-003.

**Synthetic data.** The twelve files in [`data/`](data/) are invented for this example. They
contain no real orders, customers, contracts or personal data, and each says so in its first
line. Every result below was produced by actually running the scripts in this folder
(Python 3, standard library only).

Run it yourself from the repository root:

```bash
python3 examples/order-table/run_example.py
```

## 1. The task

A small firm has a folder of text files, one per order confirmation. A colleague needs a table:
order number, year, amount and currency. Doing it by hand takes an afternoon and invites typing
errors, so the work is handed to a script (written by a person, or by an AI assistant — the method
is the same).

## 2. The intent card, filled in

```text
INTENT CARD
-----------
What do I want?
  A table with one row per order file: order number, year, amount, currency.
Why?
  The colleague can sort and sum the orders without opening 12 files.
For whom?
  A colleague who will use the numbers in a report.
What does "done" look like?
  check_result.py reports PASS: every file once; every cell equal to the
  answer key; no guessed values; the sum of confirmed EUR amounts matches.
What must NOT happen?
  A wrong number that looks right. A silent guess. Converting currencies.
What do I already know?
  The files are text. Labels vary ("Total", "Gesamtbetrag"). Number formats
  differ between files (12,450.00 and 8.900,50 and 3 200).
What is uncertain?
  Which formats really occur; what to do when a number can be read two ways.
How will I check it?
  By an answer key made by hand from the 12 files (expected.csv) and a
  script that compares the table with it. I can read all 12 files myself.
```

## 3. Constraints and the definition of done

- **Constraint:** the data stays on this computer; nothing is sent anywhere. (The scripts use no
  network and no external packages.)
- **Constraint:** amounts keep their own currency; no conversion.
- **Constraint:** if a value is not certain, the cell stays empty and the row is marked `review`
  with a reason. A human decides; the script does not guess.

The acceptance criteria are in [`check_result.py`](check_result.py), written before the extraction:

| ID | Criterion |
|----|-----------|
| C1 | Every input file appears exactly once in the table. |
| C2 | A value that is not certain is never guessed (empty cell, status `review`). |
| C3 | Every cell equals the answer key [`expected.csv`](expected.csv), including which rows need review. |
| C4 | The sum of confirmed EUR amounts equals the key's sum (81,452.60 EUR). |

## 4. Procedure

1. Read all twelve files and write the answer key by hand (`expected.csv`). Four files cannot be
   resolved with certainty: `order-004` and `order-010` (an amount such as `1.250` or `7.500` can
   mean 1.25 or 1,250 — and 7.5 or 7,500), `order-005` (no amount yet) and `order-012` (the date
   `14.3.22` has a two-digit year).
2. Write the acceptance check (`check_result.py`).
3. Write the first version of the extraction ([`extract_v1.py`](extract_v1.py)) and run it.

## 5. The failure

Attempt 1 is deliberately the kind of quick script one gets first. Its result, copied from
[`results/check_v1.txt`](results/check_v1.txt):

```text
C3 order-002.txt: amount = '8.9005', expected '8900.50'
C2 order-004.txt: amount = '1.25', expected ''
C2 order-004.txt: status = 'ok', expected 'review'
C2 order-005.txt: status = 'ok', expected 'review'
C3 order-008.txt: amount = '45.0', expected '45000.00'
C3 order-009.txt: currency = '', expected 'JPY'
C2 order-010.txt: amount = '7.5', expected ''
C3 order-011.txt: amount = '210.0', expected '2.10'
C2 order-012.txt: status = 'ok', expected 'review'
C4 sum of confirmed EUR: 27827.6505 vs key 81452.60
RESULT: FAIL (18 failure(s))
```

(The full file lists all 18 lines.) Look at what kind of failures these are. The script did not
crash. It produced a tidy table in which the German number format became a wrong number
(8.900,50 → 8.9005) and in which ambiguous or missing values turned into confident numbers. This
is the dangerous kind of failure: it looks like success. Only the check against the key shows it.

## 6. The fix

[`extract_v2.py`](extract_v2.py) changes the approach, not only a regular expression:

- number formats are read by explicit rules (thousands and decimal separators in all the formats
  that occur);
- the amount is taken from the total line with its currency token, and the gross total is
  preferred to the net amount;
- a number that can be read in two ways, a missing amount or a two-digit year is **not guessed**:
  the cell is left empty and the row gets `review` and a reason.

## 7. Verification

Result of `python3 examples/order-table/run_example.py` (also kept in
[`results/`](results/)):

```text
--- attempt 1: RESULT: FAIL (18 failure(s))
--- attempt 2: RESULT: PASS (0 failure(s))
EXAMPLE OK
```

The final table is [`results/table_v2.csv`](results/table_v2.csv): eight rows are confirmed, four
rows are marked `review` with their reasons.

## 8. Conclusion

- The method did the work, not the script: **an answer key and written criteria existed before
  the code**, so the first, wrong result could be recognised as wrong.
- "Done" was not "the script ran". It was "the check passes", and the check included the
  question *what must not happen* from the intent card.
- Four rows are handed back to a person. Handing them back is the correct result for those rows,
  not a defect.
- **Limits of this example.** Twelve invented files, one author-chosen set of formats, a key made
  by the same person who wrote the check. The check proves the scripts match *this* key on *this*
  data; it does not prove that the script would handle a real archive. For that you would need real
  samples, a second pair of eyes and a bigger test.
