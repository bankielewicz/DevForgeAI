import csv
import json
import re
import sys
from decimal import Decimal, DecimalException, ROUND_HALF_UP, localcontext

NUMBER = re.compile(r"[+]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z")

def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError("usage: receipt_totals.py RECEIPT.csv")
        values = []
        with open(sys.argv[1], newline='', encoding='utf-8') as handle:
            reader = csv.reader(handle, strict=True)
            if next(reader, None) != ['item', 'quantity', 'unit_price']:
                raise ValueError('expected header item,quantity,unit_price')
            for line, row in enumerate(reader, 2):
                if len(row) != 3 or not row[0].strip():
                    raise ValueError(f'row {line}: expected nonempty item and exactly three cells')
                numbers = []
                for value in row[1:]:
                    value = value.strip()
                    if not NUMBER.fullmatch(value):
                        raise ValueError(f'row {line}: expected finite nonnegative decimal')
                    number = Decimal(value)
                    if not number.is_finite() or number < 0:
                        raise ValueError(f'row {line}: expected finite nonnegative decimal')
                    numbers.append(number)
                values.append(numbers)
        with localcontext() as context:
            context.prec = max(50, sum(len(n.as_tuple().digits) + abs(n.as_tuple().exponent) for pair in values for n in pair) + 10)
            total = sum((quantity * price for quantity, price in values), Decimal(0))
            result = {'total': format(total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP), '.2f'), 'line_count': len(values)}
            quantity = sum((pair[0] for pair in values), Decimal(0))
            result['total_quantity'] = format(quantity, 'f')
        print(json.dumps(result))
        return 0
    except (OSError, UnicodeError, csv.Error, ValueError, DecimalException) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
