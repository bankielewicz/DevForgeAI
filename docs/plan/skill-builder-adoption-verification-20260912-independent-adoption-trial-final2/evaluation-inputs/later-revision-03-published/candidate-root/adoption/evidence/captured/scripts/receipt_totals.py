import csv
import json
import sys

with open(sys.argv[1], newline='', encoding='utf-8') as handle:
    rows = list(csv.DictReader(handle))
total = sum(float(row['quantity']) * float(row['unit_price']) for row in rows)
print(json.dumps({'total': total, 'line_count': len(rows)}))
