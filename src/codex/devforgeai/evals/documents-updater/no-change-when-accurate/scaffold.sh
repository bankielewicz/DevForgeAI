#!/usr/bin/env bash
# Fixture C (VER-03): wordcount whose README and CHANGELOG already document --json, then an
# uncommitted internal refactor (count split into helpers, unstaged) and a new helper test (untracked).
set -euo pipefail
export GIT_AUTHOR_NAME="Dana Reyes" GIT_AUTHOR_EMAIL="dana@example.com"
export GIT_COMMITTER_NAME="Dana Reyes" GIT_COMMITTER_EMAIL="dana@example.com"
commit() { # commit <ISO date> <message>
  GIT_AUTHOR_DATE="$1" GIT_COMMITTER_DATE="$1" git -c commit.gpgsign=false commit -q -m "$2"
}
git init -q -b main
mkdir -p src/wordcount tests
cat > pyproject.toml <<'FIXTURE'
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "wordcount"
version = "1.0.0"
description = "Count words and lines in text files"
requires-python = ">=3.10"

[project.scripts]
wordcount = "wordcount.cli:main"
FIXTURE
printf '' > src/wordcount/__init__.py
cat > src/wordcount/cli.py <<'FIXTURE'
"""Command-line entry point for wordcount."""
import argparse
import sys


def count(text):
    return {"words": len(text.split()), "lines": len(text.splitlines())}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="wordcount", description="Count words and lines in a text file.")
    parser.add_argument("path", help="text file to count")
    parser.add_argument("--lines", action="store_true", help="print only the line count")
    args = parser.parse_args(argv)
    with open(args.path, encoding="utf-8") as f:
        counts = count(f.read())
    if args.lines:
        print(counts["lines"])
    else:
        print(f"{counts['words']} words, {counts['lines']} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
FIXTURE
cat > README.md <<'FIXTURE'
# wordcount

Counts the words and lines in a text file, for anyone scripting over plain text.

## Prerequisites

- Python 3.10 or later

## Install

From the repository root:

```bash
pip install .
```

## Usage

```bash
wordcount notes.txt
```

Prints `12 words, 3 lines`.

| Option | Effect |
| --- | --- |
| `--lines` | Print only the line count |
FIXTURE
cat > tests/test_cli.py <<'FIXTURE'
from wordcount.cli import count


def test_count():
    assert count("a b\nc") == {"words": 3, "lines": 2}
FIXTURE
git add -A
commit 2026-09-01T10:00:00Z "Add wordcount CLI"
cat > src/wordcount/cli.py <<'FIXTURE'
"""Command-line entry point for wordcount."""
import argparse
import json
import sys


def count(text):
    return {"words": len(text.split()), "lines": len(text.splitlines())}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="wordcount", description="Count words and lines in a text file.")
    parser.add_argument("path", help="text file to count")
    parser.add_argument("--lines", action="store_true", help="print only the line count")
    parser.add_argument("--json", action="store_true", help="print the counts as a JSON object")
    args = parser.parse_args(argv)
    with open(args.path, encoding="utf-8") as f:
        counts = count(f.read())
    if args.json:
        print(json.dumps(counts))
    elif args.lines:
        print(counts["lines"])
    else:
        print(f"{counts['words']} words, {counts['lines']} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
FIXTURE
cat > README.md <<'FIXTURE'
# wordcount

Counts the words and lines in a text file, for anyone scripting over plain text.

## Prerequisites

- Python 3.10 or later

## Install

From the repository root:

```bash
pip install .
```

## Usage

```bash
wordcount notes.txt
```

Prints `12 words, 3 lines`.

| Option | Effect |
| --- | --- |
| `--lines` | Print only the line count |
| `--json` | Print the counts as a JSON object, for example `{"words": 12, "lines": 3}` |
FIXTURE
cat > CHANGELOG.md <<'FIXTURE'
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## Unreleased

### Added

- Added `--json` to print the word and line counts as a JSON object, for use in scripts.
FIXTURE
cat > tests/test_json.py <<'FIXTURE'
import json

from wordcount.cli import main


def test_json_output(tmp_path, capsys):
    path = tmp_path / "t.txt"
    path.write_text("a b\nc")
    main([str(path), "--json"])
    assert json.loads(capsys.readouterr().out) == {"words": 3, "lines": 2}
FIXTURE
git add -A
commit 2026-09-10T10:00:00Z "Add --json output"
# The work to document: uncommitted.
cat > src/wordcount/cli.py <<'FIXTURE'
"""Command-line entry point for wordcount."""
import argparse
import json
import sys


def count_words(text):
    return len(text.split())


def count_lines(text):
    return len(text.splitlines())


def count(text):
    return {"words": count_words(text), "lines": count_lines(text)}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="wordcount", description="Count words and lines in a text file.")
    parser.add_argument("path", help="text file to count")
    parser.add_argument("--lines", action="store_true", help="print only the line count")
    parser.add_argument("--json", action="store_true", help="print the counts as a JSON object")
    args = parser.parse_args(argv)
    with open(args.path, encoding="utf-8") as f:
        counts = count(f.read())
    if args.json:
        print(json.dumps(counts))
    elif args.lines:
        print(counts["lines"])
    else:
        print(f"{counts['words']} words, {counts['lines']} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
FIXTURE
cat > tests/test_helpers.py <<'FIXTURE'
from wordcount.cli import count_lines, count_words


def test_helpers():
    assert count_words("a b\nc") == 3
    assert count_lines("a b\nc") == 2
FIXTURE
