"""Total a CSV amount column exactly and create one new JSON output."""
import argparse
import csv
from decimal import Decimal, DecimalException, localcontext
import json
import os
from pathlib import Path
import re
import sys

NUMBER = re.compile(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z')


def summarize(source):
    values = []
    with source.open('r', encoding='utf-8-sig', newline='') as stream:
        rows = csv.DictReader(stream, strict=True)
        if rows.fieldnames is None or rows.fieldnames.count('amount') != 1:
            raise ValueError('CSV requires exactly one amount column')
        for number, row in enumerate(rows, 2):
            raw = row.get('amount')
            if raw is None or not raw.strip():
                raise ValueError(f'row {number}: missing amount')
            text = raw.strip()
            if not NUMBER.fullmatch(text):
                raise ValueError(f'row {number}: amount must be a finite decimal')
            value = Decimal(text)
            if not value.is_finite():
                raise ValueError(f'row {number}: amount must be finite')
            if value.as_tuple().exponent < -2:
                raise ValueError(f'row {number}: amount has more than two decimal places')
            values.append(value)
    # Include integer places, cents, and carry digits for every row. This avoids
    # the default decimal context rounding long totals during summation.
    integer_places = max((max(1, value.adjusted() + 1) for value in values), default=1)
    with localcontext() as context:
        context.prec = max(28, integer_places + 2 + len(str(len(values))) + 2)
        total = sum(values, Decimal('0.00'))
        if total == 0:
            total = Decimal('0.00')
        formatted = format(total, '.2f')
    return {'count': len(values), 'total': formatted}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args(argv)
    created = False
    try:
        if os.path.lexists(args.output):
            raise ValueError('output already exists; choose a new output path')
        result = summarize(args.input)
        payload = json.dumps(result, ensure_ascii=False, allow_nan=False) + '\n'
        with args.output.open('x', encoding='utf-8', newline='\n') as stream:
            created = True
            stream.write(payload)
        print(payload, end='')
        return 0
    except (OSError, UnicodeError, ValueError, csv.Error, DecimalException) as exc:
        if created:
            try:
                args.output.unlink()
            except OSError as cleanup_error:
                print('Could not remove incomplete new output: ' + str(cleanup_error), file=sys.stderr)
        print('Cannot total CSV: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
