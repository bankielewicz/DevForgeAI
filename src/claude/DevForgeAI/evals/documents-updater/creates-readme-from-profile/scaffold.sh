#!/usr/bin/env bash
# Fixture F (VER-07): a git repository with no commits holding the csvtidy CLI package, untracked,
# with no README, no CHANGELOG and no LICENSE.
set -euo pipefail
git init -q -b main
mkdir -p src/csvtidy tests
cat > pyproject.toml <<'FIXTURE'
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "csvtidy"
version = "0.1.0"
description = "Clean up CSV files: trim cells and drop empty rows"
requires-python = ">=3.11"

[project.scripts]
csvtidy = "csvtidy.cli:main"
FIXTURE
printf '' > src/csvtidy/__init__.py
cat > src/csvtidy/cli.py <<'FIXTURE'
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
FIXTURE
cat > tests/test_cli.py <<'FIXTURE'
from csvtidy.cli import tidy


def test_tidy_drops_empty_rows():
    assert list(tidy([[" a ", "b"], ["", " "]], drop_empty=True)) == [["a", "b"]]
FIXTURE
