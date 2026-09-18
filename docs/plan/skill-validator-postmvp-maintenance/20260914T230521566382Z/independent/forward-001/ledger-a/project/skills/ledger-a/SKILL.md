---
name: ledger-a
description: Total integer JSON arrays into a selected JSON output file. Use when asked to sum an array stored in a JSON file.
---

# Integer array totals

Use the user's input JSON file and selected output path. Run `python scripts/total.py INPUT OUTPUT`, resolving the script relative to this skill. The helper checks the input and writes the JSON result. Read the delivered file back before reporting completion. Preserve the source and unrelated files. On invalid input, report the helper diagnostic; do not invent a total or create a substitute output.
