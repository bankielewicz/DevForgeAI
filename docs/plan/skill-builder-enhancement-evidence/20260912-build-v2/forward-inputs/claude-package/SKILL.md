---
name: decimal-ledger-import
description: Sum the amount column in a local CSV and return a JSON count and exact two-place decimal total.
---
# Decimal ledger report

Use this skill to summarize a supplied local CSV. Do not use it to edit the CSV or categorize transactions.

Use Read to inspect [the output contract](assets/result.schema.json). Run [the CSV helper](scripts/sum_amounts.py) with Bash using explicit --input and --output paths. The helper requires an amount column, rejects missing or non-finite amounts and values with more than two decimal places, and writes count and total. A negative amount is valid. Preserve the input file. If the output path exists or input is invalid, report the error without replacing output bytes.
