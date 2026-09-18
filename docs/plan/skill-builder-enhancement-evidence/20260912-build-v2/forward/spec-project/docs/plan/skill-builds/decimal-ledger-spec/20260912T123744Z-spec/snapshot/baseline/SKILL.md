---
name: decimal-ledger-spec
description: Total the amount column of a supplied local CSV into a new JSON file using exact decimal arithmetic. Use for local CSV amount totals; exclude explanation alone, transaction categorization, network retrieval, and edits to the original CSV.
---

# Decimal ledger

Accept the selected input CSV path and a new output JSON path. Resolve relative work-product paths against the identified project root. Require both paths before execution. Use Python 3.10 or newer and the Windows PowerShell terminal; the helper needs only the standard library.

Read the input as UTF-8 with an optional BOM. Support quoted CSV fields and require exactly one `amount` column. Every data row must contain a nonempty, finite decimal amount with at most two decimal places; negative amounts are valid. Reject missing values, NaN, infinity, and excess precision. Preserve the original bytes.

Resolve [the helper](scripts/sum_amounts.py) relative to this loaded skill. Substitute the actual absolute paths in this PowerShell invocation:

```powershell
python -B -X utf8 'C:\actual\loaded-skill\scripts\sum_amounts.py' --input 'C:\actual\project\amounts.csv' --output 'C:\actual\project\total.json'
```

The selected output's parent directory must already exist. The helper writes only the new selected output file, never overwrites an existing output, and makes no network calls. It exits 0 and emits the produced JSON on stdout on success. Invalid input, invalid arguments, and output conflicts exit 2 with diagnostics on stderr. On failure, report the actual diagnostic; do not delete or replace an existing output or silently change paths. Correct the input or select a new output only under the user's instruction. Do not edit the input as part of totaling it.

The output has exactly `count` (an integer number of data rows) and `total` (a decimal string with exactly two places), matching [the schema](assets/result.schema.json). Header-only input produces `{"count": 0, "total": "0.00"}`. Sum with decimal arithmetic; do not use binary floats.

Before execution capture the input SHA-256 with `Get-FileHash -LiteralPath 'C:\actual\project\amounts.csv' -Algorithm SHA256`. After success, perform [result-review](references/workers/result-review.md) against the actual JSON and compare the input digest. Use the available subagent tool if useful; sequential main-agent review is allowed. Return the result, inspected input/output paths, and findings or missing observations. This review organizes work and supplies no framework gate or acceptance decision.

Keep this skill as development source. Do not install it or change runtime configuration. Its runtime requires no other skills, desktop, browser, hooks, registry, or services.
