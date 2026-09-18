---
name: receipt-totals
description: Aggregate item, quantity, and unit_price receipt CSV files into decimal JSON totals.
---

# Receipt Totals

Run `python -B -X utf8 <skill-directory>/scripts/receipt_totals.py RECEIPT.csv`
using the bundled [receipt script](scripts/receipt_totals.py).
The CSV header is exactly item,quantity,unit_price. Quantities and prices must
be finite nonnegative decimals; items must be nonempty. Output is a JSON object
with a two-place string total, rounded half-up once, and integer line_count.
An empty receipt returns total 0.00 and zero lines. Invalid input exits 2,
writes a readable stderr error, and emits no JSON. Inputs remain unchanged.
Requires Python 3.10+ standard library. Resolve the script relative to this skill
and receipt paths relative to the caller's working directory. Notes are user-owned.
