---
name: receipt-total
description: Compute an exact decimal total from a JSON list of receipt amounts. Use for receipt aggregation; do not use for forecasts or repairs.
---

# Receipt total

Read the supplied UTF-8 JSON input path. Each row has an amount expressed as a decimal string. Run [total.py](scripts/total.py) with that path. Return its JSON stdout to the user. A missing/invalid amount or malformed input returns a concrete stderr error with exit 2 and no success object. The script is read-only. Never install dependencies or contact external services. Decimal zero for an empty list is valid. Preserve input bytes.
