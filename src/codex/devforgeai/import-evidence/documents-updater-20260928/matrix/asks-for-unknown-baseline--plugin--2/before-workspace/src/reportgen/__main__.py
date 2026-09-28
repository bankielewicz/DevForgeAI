import csv
import sys


def main(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(f"{len(rows)} items")


if __name__ == "__main__":
    main(sys.argv[1])


def export_csv(rows, out):
    writer = csv.DictWriter(out, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)


def parse_week(value):
    """Parse an ISO week date such as 2026-W37."""
    year, week = value.split("-W")
    return int(year), int(week)


def since(rows, week):
    return [r for r in rows if parse_week(r["week"]) >= week]
