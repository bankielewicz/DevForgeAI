#!/usr/bin/env bash
# Fixture A (VER-01, VER-02, VER-08; identical in updates-readme-and-changelog,
# proposal-mode-no-edits and ignores-unrelated-request): a git repository for the wordcount CLI
# with a README and no CHANGELOG, then an uncommitted --json option (staged) and its test (untracked).
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
# The work to document: uncommitted.
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
git add src/wordcount/cli.py
cat > tests/test_json.py <<'FIXTURE'
import json

from wordcount.cli import main


def test_json_output(tmp_path, capsys):
    path = tmp_path / "t.txt"
    path.write_text("a b\nc")
    main([str(path), "--json"])
    assert json.loads(capsys.readouterr().out) == {"words": 3, "lines": 2}
FIXTURE
