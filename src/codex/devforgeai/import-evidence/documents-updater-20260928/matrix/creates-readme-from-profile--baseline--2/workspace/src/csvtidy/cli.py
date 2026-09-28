"""Command-line entry point for csvtidy."""
import argparse
import csv
import sys


def tidy(rows, drop_empty):
    for row in rows:
        cells = [cell.strip() for cell in row]
        if drop_empty and not any(cells):
            continue
        yield cells


def main(argv=None):
    parser = argparse.ArgumentParser(prog="csvtidy", description="Trim every cell of a CSV file.")
    parser.add_argument("input", help="CSV file to read")
    parser.add_argument("-o", "--output", help="file to write (default: standard output)")
    parser.add_argument("--drop-empty", action="store_true", help="drop rows whose cells are all empty")
    args = parser.parse_args(argv)
    with open(args.input, newline="", encoding="utf-8") as f:
        rows = list(tidy(csv.reader(f), args.drop_empty))
    out = open(args.output, "w", newline="", encoding="utf-8") if args.output else sys.stdout
    csv.writer(out).writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
