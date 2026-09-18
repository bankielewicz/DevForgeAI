"""Sum finite two-place decimal CSV amounts; no network operations."""
import argparse
import csv
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        total, count = Decimal("0.00"), 0
        with Path(args.input).open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            if not reader.fieldnames or "amount" not in reader.fieldnames:
                raise ValueError("CSV requires an amount column")
            for row in reader:
                raw = row.get("amount")
                if raw is None or not raw.strip():
                    raise ValueError("amount is required")
                value = Decimal(raw)
                if not value.is_finite() or value.as_tuple().exponent < -2:
                    raise ValueError("amount must be finite with at most two decimal places")
                total += value
                count += 1
        result = {"count": count, "total": format(total, ".2f")}
        with Path(args.output).open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(result, stream, sort_keys=True)
            stream.write("\n")
        print(json.dumps(result, sort_keys=True))
        return 0
    except (OSError, ValueError, InvalidOperation) as exc:
        print(str(exc), file=sys.stderr)
        return 2
if __name__ == "__main__":
    sys.exit(main())
