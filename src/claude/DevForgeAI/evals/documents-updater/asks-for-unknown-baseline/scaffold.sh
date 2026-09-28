#!/usr/bin/env bash
# Fixture E (VER-06): reportgen on its only branch, topic, with four commits by two authors, no tags,
# no remote, no other branch and a clean working tree. Nothing shows where the user's work began.
set -euo pipefail
export GIT_AUTHOR_NAME="Dana Reyes" GIT_AUTHOR_EMAIL="dana@example.com"
export GIT_COMMITTER_NAME="Dana Reyes" GIT_COMMITTER_EMAIL="dana@example.com"
commit() { # commit <ISO date> <message>
  GIT_AUTHOR_DATE="$1" GIT_COMMITTER_DATE="$1" git -c commit.gpgsign=false commit -q -m "$2"
}
git init -q -b topic
mkdir -p src/reportgen
cat > README.md <<'FIXTURE'
# reportgen

Builds weekly activity reports from a CSV export of the team tracker.

## Usage

```bash
python -m reportgen tracker.csv
```
FIXTURE
cat > src/reportgen/__main__.py <<'FIXTURE'
import csv
import sys


def main(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(f"{len(rows)} items")


if __name__ == "__main__":
    main(sys.argv[1])
FIXTURE
git add -A
commit 2026-07-06T09:00:00Z "Initial import of reportgen"
cat >> src/reportgen/__main__.py <<'FIXTURE'


def export_csv(rows, out):
    writer = csv.DictWriter(out, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
FIXTURE
git add -A
GIT_AUTHOR_NAME="Sam Okafor" GIT_AUTHOR_EMAIL="sam@example.com" commit 2026-08-12T14:00:00Z "Add CSV export"
cat >> src/reportgen/__main__.py <<'FIXTURE'


def parse_week(value):
    """Parse an ISO week date such as 2026-W37."""
    year, week = value.split("-W")
    return int(year), int(week)
FIXTURE
git add -A
commit 2026-09-03T11:00:00Z "Fix date parsing for ISO week dates"
cat >> src/reportgen/__main__.py <<'FIXTURE'


def since(rows, week):
    return [r for r in rows if parse_week(r["week"]) >= week]
FIXTURE
git add -A
GIT_AUTHOR_NAME="Sam Okafor" GIT_AUTHOR_EMAIL="sam@example.com" commit 2026-09-20T16:00:00Z "Add --since filter"
