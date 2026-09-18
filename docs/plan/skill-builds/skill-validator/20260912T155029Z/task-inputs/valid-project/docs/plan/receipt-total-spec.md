---
id: RECEIPT-TOTAL-001
skill_name: receipt-total
target: codex
status: approved
---
# Receipt totals
Compute exact decimal total from a local UTF-8 JSON list of objects with amount string. Return stdout JSON with total string and count integer. Empty input list returns total "0" and count 0. Malformed JSON, non-list input, missing/non-string/nonfinite amount produce exit 2, stderr diagnosis and no success JSON. Preserve source and input bytes; read-only with no network/dependencies. Activation is receipt aggregation, excluding forecasts or repairs. SKILL.md routes scripts/total.py. Required cases: 0.10+0.20=0.30 count2; empty list; missing amount; malformed JSON. No installation or additional resources are required.
