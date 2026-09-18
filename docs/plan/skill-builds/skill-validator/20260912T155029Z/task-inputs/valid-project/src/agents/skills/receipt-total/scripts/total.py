import decimal, json, sys
from pathlib import Path
try:
    rows = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if not isinstance(rows, list): raise ValueError("expected list")
    amounts = []
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("amount"), str): raise ValueError("amount must be string")
        amount=decimal.Decimal(row["amount"])
        if not amount.is_finite(): raise ValueError("amount must be finite")
        amounts.append(amount)
    print(json.dumps({"total":str(sum(amounts,decimal.Decimal("0"))),"count":len(rows)}))
except (ValueError, decimal.InvalidOperation, OSError, IndexError) as exc:
    print(str(exc),file=sys.stderr); sys.exit(2)
