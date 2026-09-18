# Concrete later behavior revision

After the successful revision-02-resolved generated origin, add total_quantity to
each successful JSON object. Its value is the exact sum of all input quantities,
formatted as a fixed-point decimal string without rounding. An empty receipt has
total_quantity "0". Preserve existing total and line_count values and the entire
validation, error, input-preservation and standard-library contract.

Manage SKILL.md and scripts/receipt_totals.py at the same disposable development
destination. Keep notes.txt user-owned and byte-identical. Use the last successful
revision-02-resolved N as B, preserve original adoption evidence, and publish a
new generated origin only after fresh delivered checks and readback.

This is a concrete proposal for a distinct trial-controller review instruction.
