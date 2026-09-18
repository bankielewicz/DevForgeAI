---
skill_name: receipt-totals
status: reviewed
---

# Receipt totals behavior

Read one UTF-8 CSV path from the command line. The header must be exactly
item,quantity,unit_price in that order. Each item is nonempty after trimming.
Quantity and unit_price are finite nonnegative decimal numbers; fractional
quantities are allowed. Calculate with decimal arithmetic from the input strings.
Do not round individual line products. Round the grand total once to two decimal
places using round-half-up. Write exactly one JSON object with total as a two-place
decimal string and line_count as an integer. An empty data section returns
{"total":"0.00","line_count":0}. Reject missing/extra cells, malformed headers,
negative or nonfinite numbers, and invalid decimal text with exit 2, a readable
stderr error, and no stdout JSON. Successful execution exits 0. Do not modify the
input CSV, contact services, install dependencies, or create receipt output files.
Use Python 3.10+ standard library only. The skill activates for receipt aggregation
requests and routes the user to its bundled executable script. Manage SKILL.md and
scripts/receipt_totals.py only; notes.txt remains user owned.
