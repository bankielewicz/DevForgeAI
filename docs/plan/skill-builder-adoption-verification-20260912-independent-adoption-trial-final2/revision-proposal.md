# Concrete first revision proposal

Target: the receipt-totals package identified in trial-state.json.

Manage exactly SKILL.md and scripts/receipt_totals.py. Update the entrypoint's
usage and error contract, and replace the executable implementation to satisfy
the complete reviewed origin-spec.md behavior. Use standard-library Decimal
arithmetic, round only the grand total half-up to two decimal places, and return
the total as a string plus integer line_count. Validate exact headers and row
width, nonempty items, finite nonnegative quantities/prices, and decimal syntax.
Invalid input produces exit 2, readable stderr and no stdout JSON. Empty receipts
produce the specified zero total. No dependency installation or input writes.

Retain notes.txt as user-owned with unchanged bytes. Record adoption independently,
then stage and evaluate the authorized specification candidate before any target
change. A conflict requires a separate concrete resolution instruction.

This proposal is awaiting the coordinating user's distinct review direction;
the specification review label alone is not revision authority.
