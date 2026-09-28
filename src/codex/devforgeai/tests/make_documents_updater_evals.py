"""Generates evals/documents-updater/<case>/ (SPEC-006 VER-01..08): prompts, graders, case.yaml and
the inline scaffold fixtures. Edit fixtures and graders here, then regenerate; it overwrites the case
files and never deletes a grader, so remove renamed ones by hand. Run from the repository root:

    python3 src/codex/devforgeai/tests/make_documents_updater_evals.py
"""
import os
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "evals/documents-updater"
TOOLS = "[exec_command, apply_patch, request_user_input]"

GIT_ENV = """\
set -euo pipefail
export GIT_AUTHOR_NAME="Dana Reyes" GIT_AUTHOR_EMAIL="dana@example.com"
export GIT_COMMITTER_NAME="Dana Reyes" GIT_COMMITTER_EMAIL="dana@example.com"
commit() { # commit <ISO date> <message>
  GIT_AUTHOR_DATE="$1" GIT_COMMITTER_DATE="$1" git -c commit.gpgsign=false commit -q -m "$2"
}
"""

WORDCOUNT_PYPROJECT = """\
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
"""

WORDCOUNT_CLI_BASE = """\
cat > src/wordcount/cli.py <<'FIXTURE'
\"\"\"Command-line entry point for wordcount.\"\"\"
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
"""

WORDCOUNT_CLI_JSON = """\
cat > src/wordcount/cli.py <<'FIXTURE'
\"\"\"Command-line entry point for wordcount.\"\"\"
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
"""

WORDCOUNT_README_BASE = """\
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
"""

WORDCOUNT_TEST_BASE = """\
cat > tests/test_cli.py <<'FIXTURE'
from wordcount.cli import count


def test_count():
    assert count("a b\\nc") == {"words": 3, "lines": 2}
FIXTURE
"""

WORDCOUNT_TEST_JSON = """\
cat > tests/test_json.py <<'FIXTURE'
import json

from wordcount.cli import main


def test_json_output(tmp_path, capsys):
    path = tmp_path / "t.txt"
    path.write_text("a b\\nc")
    main([str(path), "--json"])
    assert json.loads(capsys.readouterr().out) == {"words": 3, "lines": 2}
FIXTURE
"""

FIXTURE_A = (
    "#!/usr/bin/env bash\n"
    "# Fixture A (VER-01, VER-02, VER-08; identical in updates-readme-and-changelog,\n"
    "# proposal-mode-no-edits and ignores-unrelated-request): a git repository for the wordcount CLI\n"
    "# with a README and no CHANGELOG, then an uncommitted --json option (staged) and its test (untracked).\n"
    + GIT_ENV
    + "git init -q -b main\nmkdir -p src/wordcount tests\n"
    + WORDCOUNT_PYPROJECT
    + "printf '' > src/wordcount/__init__.py\n"
    + WORDCOUNT_CLI_BASE + WORDCOUNT_README_BASE + WORDCOUNT_TEST_BASE
    + "git add -A\ncommit 2026-09-01T10:00:00Z \"Add wordcount CLI\"\n"
    + "# The work to document: uncommitted.\n"
    + WORDCOUNT_CLI_JSON
    + "git add src/wordcount/cli.py\n"
    + WORDCOUNT_TEST_JSON
)

README_JSON = WORDCOUNT_README_BASE.replace(
    "| `--lines` | Print only the line count |",
    "| `--lines` | Print only the line count |\n"
    "| `--json` | Print the counts as a JSON object, for example `{\"words\": 12, \"lines\": 3}` |")

CHANGELOG_JSON = """\
cat > CHANGELOG.md <<'FIXTURE'
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## Unreleased

### Added

- Added `--json` to print the word and line counts as a JSON object, for use in scripts.
FIXTURE
"""

REFACTOR_CLI = WORDCOUNT_CLI_JSON.replace(
    'def count(text):\n    return {"words": len(text.split()), "lines": len(text.splitlines())}',
    'def count_words(text):\n    return len(text.split())\n\n\n'
    'def count_lines(text):\n    return len(text.splitlines())\n\n\n'
    'def count(text):\n    return {"words": count_words(text), "lines": count_lines(text)}')
assert REFACTOR_CLI != WORDCOUNT_CLI_JSON

FIXTURE_C = (
    "#!/usr/bin/env bash\n"
    "# Fixture C (VER-03): wordcount whose README and CHANGELOG already document --json, then an\n"
    "# uncommitted internal refactor (count split into helpers, unstaged) and a new helper test (untracked).\n"
    + GIT_ENV
    + "git init -q -b main\nmkdir -p src/wordcount tests\n"
    + WORDCOUNT_PYPROJECT
    + "printf '' > src/wordcount/__init__.py\n"
    + WORDCOUNT_CLI_BASE + WORDCOUNT_README_BASE + WORDCOUNT_TEST_BASE
    + "git add -A\ncommit 2026-09-01T10:00:00Z \"Add wordcount CLI\"\n"
    + WORDCOUNT_CLI_JSON + README_JSON + CHANGELOG_JSON + WORDCOUNT_TEST_JSON
    + "git add -A\ncommit 2026-09-10T10:00:00Z \"Add --json output\"\n"
    + "# The work to document: uncommitted.\n"
    + REFACTOR_CLI
    + """cat > tests/test_helpers.py <<'FIXTURE'
from wordcount.cli import count_lines, count_words


def test_helpers():
    assert count_words("a b\\nc") == 3
    assert count_lines("a b\\nc") == 2
FIXTURE
"""
)

JOBS_CLI_BASE = """\
cat > src/wordcount/cli.py <<'FIXTURE'
\"\"\"Command-line entry point for wordcount.\"\"\"
import argparse
import sys


def count_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return {"words": len(text.split()), "lines": len(text.splitlines())}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="wordcount", description="Count words and lines in text files.")
    parser.add_argument("paths", nargs="+", help="text files to count")
    args = parser.parse_args(argv)
    for path in args.paths:
        counts = count_file(path)
        print(f"{path}: {counts['words']} words, {counts['lines']} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
FIXTURE
"""

JOBS_CLI = """\
cat > src/wordcount/cli.py <<'FIXTURE'
\"\"\"Command-line entry point for wordcount.\"\"\"
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor


def count_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return {"words": len(text.split()), "lines": len(text.splitlines())}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="wordcount", description="Count words and lines in text files.")
    parser.add_argument("paths", nargs="+", help="text files to count")
    parser.add_argument("--jobs", type=int, default=1, metavar="N",
                        help="count up to N files at the same time (default: 1)")
    args = parser.parse_args(argv)
    if args.jobs < 1:
        parser.error("--jobs must be at least 1")
    # Roughly 3x faster on big batches.
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(count_file, args.paths))
    for path, counts in zip(args.paths, results):
        print(f"{path}: {counts['words']} words, {counts['lines']} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
FIXTURE
"""

JOBS_README = """\
cat > README.md <<'FIXTURE'
# wordcount

Counts the words and lines in text files, for anyone scripting over plain text.

## Prerequisites

- Python 3.10 or later

## Install

From the repository root:

```bash
pip install .
```

## Usage

```bash
wordcount notes.txt draft.txt
```

Prints one line per file, such as `notes.txt: 12 words, 3 lines`.
FIXTURE
"""

FIXTURE_B = (
    "#!/usr/bin/env bash\n"
    "# Fixture B (VER-04): wordcount for several files with a README and no CHANGELOG, then an\n"
    "# uncommitted --jobs option (unstaged) and its test (untracked). A code comment claims it is ~3x\n"
    "# faster, but no benchmark and no test run exist.\n"
    + GIT_ENV
    + "git init -q -b main\nmkdir -p src/wordcount tests\n"
    + WORDCOUNT_PYPROJECT
    + "printf '' > src/wordcount/__init__.py\n"
    + JOBS_CLI_BASE + JOBS_README
    + "git add -A\ncommit 2026-09-01T10:00:00Z \"Add wordcount CLI\"\n"
    + "# The work to document: uncommitted.\n"
    + JOBS_CLI
    + """cat > tests/test_jobs.py <<'FIXTURE'
from wordcount.cli import main


def test_jobs(tmp_path, capsys):
    paths = []
    for name in ("a.txt", "b.txt"):
        path = tmp_path / name
        path.write_text("one two")
        paths.append(str(path))
    main(paths + ["--jobs", "2"])
    assert capsys.readouterr().out.count("2 words") == 2
FIXTURE
"""
)

POLL_CHANGELOG = """\
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Added the `--once` flag to poll a single time and exit, for use in cron jobs.

## [1.0.0] - 2026-06-02

### Added

- Added TLS certificate checks for HTTPS endpoints.

### Fixed

- Fixed a crash when the endpoint returned an empty body.

## [0.9.0] - 2026-04-15

### Added

- First public release: poll an HTTP endpoint and log status changes.

[Unreleased]: https://github.com/example/pollwatch/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/example/pollwatch/compare/v0.9.0...v1.0.0
[0.9.0]: https://github.com/example/pollwatch/releases/tag/v0.9.0
"""


POLL_CHANGELOG_1_0 = POLL_CHANGELOG.replace(
    "### Added\n\n- Added the `--once` flag to poll a single time and exit, for use in cron jobs.\n\n", "")
assert POLL_CHANGELOG_1_0 != POLL_CHANGELOG

ONCE_CLI = """cat > src/pollwatch/cli.py <<'FIXTURE'
\"\"\"Command-line entry point for pollwatch.\"\"\"
import argparse
import time
import urllib.request

from pollwatch.config import load


def main(argv=None):
    parser = argparse.ArgumentParser(prog="pollwatch")
    parser.add_argument("--config", default="pollwatch.toml")
    parser.add_argument("--once", action="store_true", help="poll one time and exit")
    args = parser.parse_args(argv)
    config = load(args.config)
    last = None
    while True:
        with urllib.request.urlopen(config["url"]) as response:
            status = response.status
        if status != last:
            print(f"status {status}")
            last = status
        if args.once:
            return 0
        time.sleep(int(config["poll_interval"]))
FIXTURE
"""
RELEASE_CLI = ONCE_CLI.replace(
    '    parser.add_argument("--once", action="store_true", help="poll one time and exit")\n', "").replace(
    "        if args.once:\n            return 0\n", "")
assert "once" not in RELEASE_CLI

def config_py(key):
    return f"""\
cat > src/pollwatch/config.py <<'FIXTURE'
\"\"\"Loads pollwatch.toml.\"\"\"
import tomllib

DEFAULTS = {{"url": None, "{key}": 30}}


def load(path="pollwatch.toml"):
    with open(path, "rb") as f:
        data = tomllib.load(f)
    config = {{**DEFAULTS, **data}}
    if not config["url"]:
        raise ValueError("pollwatch.toml must set url")
    if int(config["{key}"]) < 5:
        raise ValueError("{key} must be at least 5")
    return config
FIXTURE
"""


def example_toml(key):
    return f"""\
cat > pollwatch.example.toml <<'FIXTURE'
url = "https://status.example.com/health"
{key} = 30
FIXTURE
"""


FIXTURE_D = (
    "#!/usr/bin/env bash\n"
    "# Fixture D (VER-05): pollwatch with a Keep a Changelog CHANGELOG (one Unreleased entry, published\n"
    "# 1.0.0 and 0.9.0), README and docs/configuration.md naming poll_interval, then an uncommitted rename\n"
    "# of that key to poll_interval_seconds in the code (staged) and the example file (unstaged), and a\n"
    "# pyproject version bump to 1.1.0 (staged) with no tag. README.md and docs/configuration.md are not\n"
    "# in the diff.\n"
    + GIT_ENV
    + "git init -q -b main\nmkdir -p src/pollwatch docs\n"
    + """cat > pyproject.toml <<'FIXTURE'
[project]
name = "pollwatch"
version = "1.0.0"
description = "Poll an HTTP endpoint and log status changes"
requires-python = ">=3.11"

[project.scripts]
pollwatch = "pollwatch.cli:main"
FIXTURE
printf '' > src/pollwatch/__init__.py
"""
    + RELEASE_CLI
    + """"""
    + config_py("poll_interval") + example_toml("poll_interval")
    + """cat > README.md <<'FIXTURE'
# pollwatch

Polls an HTTP endpoint and logs each change in its status code, for operators who want a
lightweight uptime check.

## Prerequisites

- Python 3.11 or later

## Quick start

1. Install from the repository root:

   ```bash
   pip install .
   ```

2. Copy the example configuration and set your endpoint:

   ```bash
   cp pollwatch.example.toml pollwatch.toml
   ```

3. Run it:

   ```bash
   pollwatch
   ```

## Configuration

`pollwatch.toml` holds the endpoint and how often to poll it:

```toml
url = "https://status.example.com/health"
poll_interval = 30
```

See the [configuration reference](docs/configuration.md) for every setting.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
FIXTURE
cat > docs/configuration.md <<'FIXTURE'
# Configuration

pollwatch reads `pollwatch.toml` from the working directory, or the file given with `--config`.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| `url` | string | none (required) | The endpoint to poll |
| `poll_interval` | integer | `30` | Seconds between polls; at least `5` |

## Example

```toml
url = "https://status.example.com/health"
poll_interval = 60
```
FIXTURE
cat > CHANGELOG.md <<'FIXTURE'
"""
    + POLL_CHANGELOG_1_0
    + "FIXTURE\n"
    + "git add -A\ncommit 2026-06-02T09:00:00Z \"Release 1.0.0\"\n"
    + "git tag v1.0.0\n"
    + "# After the release: --once, recorded under Unreleased.\n"
    + ONCE_CLI
    + "cat > CHANGELOG.md <<'FIXTURE'\n" + POLL_CHANGELOG + "FIXTURE\n"
    + "git add -A\ncommit 2026-07-14T09:00:00Z \"Add --once\"\n"
    + "# The work to document: uncommitted.\n"
    + config_py("poll_interval_seconds").replace("cat >", "cat >", 1)
    + "sed -i 's/config\\[\"poll_interval\"\\]/config[\"poll_interval_seconds\"]/' src/pollwatch/cli.py\n"
    + "sed -i 's/^version = \"1.0.0\"/version = \"1.1.0\"/' pyproject.toml\n"
    + "git add src/pollwatch/config.py src/pollwatch/cli.py pyproject.toml\n"
    + example_toml("poll_interval_seconds")
)

FIXTURE_E = (
    "#!/usr/bin/env bash\n"
    "# Fixture E (VER-06): reportgen on its only branch, topic, with four commits by two authors, no tags,\n"
    "# no remote, no other branch and a clean working tree. Nothing shows where the user's work began.\n"
    + GIT_ENV
    + "git init -q -b topic\nmkdir -p src/reportgen\n"
    + """cat > README.md <<'FIXTURE'
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
    \"\"\"Parse an ISO week date such as 2026-W37.\"\"\"
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
"""
)

FIXTURE_F = (
    "#!/usr/bin/env bash\n"
    "# Fixture F (VER-07): a git repository with no commits holding the csvtidy CLI package, untracked,\n"
    "# with no README, no CHANGELOG and no LICENSE.\n"
    + "set -euo pipefail\n"
    + "git init -q -b main\nmkdir -p src/csvtidy tests\n"
    + """cat > pyproject.toml <<'FIXTURE'
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
\"\"\"Command-line entry point for csvtidy.\"\"\"
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
"""
)


def regex(target, match, pattern, flags=None):
    t = target if target == "last_message" else "{source: file, path: %s}" % target
    fl = f"flags: {flags}\n" if flags else ""
    return f"---\ntype: regex\ntarget: {t}\nmatch: {match}\n{fl}---\n{pattern}\n"


def exists(path, value):
    return f"---\ntype: file_exists\npath: {path}\nexists: {str(value).lower()}\n---\n"


FIRED = "---\ntype: skill_loaded\npath_suffix: skills/documents-updater/SKILL.md\narm: plugin\n---\n"
NOT_FIRED = "---\ntype: skill_loaded\npath_suffix: skills/documents-updater/SKILL.md\nmin: 0\nmax: 0\narm: both\n---\n"

UNSUPPORTED = (r"[Ff]aster|[Qq]uicker|[Ss]peed|[Pp]erformance|[Ee]fficien|\d+ ?%|\b\d+(?:\.\d+)?x\b|\d ?×"
               r"|times as fast|[Rr]un ?time|[Ww]all[- ]clock|[Tt]ests? pass|[Pp]assing tests")

CASES = {
    "updates-readme-and-changelog": {
        "ver": "01", "scaffold": FIXTURE_A,
        "description": "VER-01: README and a new CHANGELOG document the uncommitted --json option, with no version or date.",
        "prompt": "I've finished adding a --json output option to wordcount; it's in my uncommitted changes.\n"
                  "Please bring the README and the changelog up to date.\n",
        "graders": {
            "skill-fired": FIRED,
            "readme-names-json": regex("README.md", "contains", "--json"),
            "changelog-created": exists("CHANGELOG.md", True),
            "changelog-unreleased": regex("CHANGELOG.md", "contains", r"^## \[?Unreleased\]?[ \t]*$", "m"),
            "changelog-added-json": regex("CHANGELOG.md", "contains", r"^### Added[ \t]*\n(?:(?!#)[^\n]*\n)*?(?!#)[^\n]*--json", "m"),
            "no-version-heading": regex("CHANGELOG.md", "not_contains", r"^##[ \t]+\[?v?\d+\.\d+", "m"),
            "no-date": regex("CHANGELOG.md", "not_contains", r"\b20\d\d-\d\d-\d\d\b"),
            "result-updated": regex("last_message", "contains", r"Result:[ \t*]*updated\b"),
        },
    },
    "proposal-mode-no-edits": {
        "ver": "02", "scaffold": FIXTURE_A,
        "description": "VER-02: a request to draft doc updates without touching files changes nothing and proposes the --json text.",
        "prompt": "Draft the documentation updates for my uncommitted --json change, but don't touch any files yet:\n"
                  "I want to review them first.\n",
        "graders": {
            "skill-fired": FIRED,
            "readme-unchanged": regex("README.md", "not_contains", "--json"),
            "no-changelog": exists("CHANGELOG.md", False),
            "result-proposed": regex("last_message", "contains", r"Result:[ \t*]*proposed\b"),
            "proposes-json": regex("last_message", "contains", "--json"),
        },
    },
    "no-change-when-accurate": {
        "ver": "03", "scaffold": FIXTURE_C,
        "description": "VER-03: docs already describe --json; an internal refactor and a test leave both files unchanged.",
        "prompt": "Refresh the docs for my latest changes.\n",
        "graders": {
            "skill-fired": FIRED,
            "changelog-no-internal-entry": regex("CHANGELOG.md", "not_contains", r"count_words|count_lines|[Rr]efactor|\b[Tt]ests?\b|[Hh]elper"),
            "changelog-single-entry": regex("CHANGELOG.md", "contains", r"### Added\n\n- Added `--json` to print the word and line counts as a JSON object, for use in scripts\.\n?$"),
            "readme-no-internal-names": regex("README.md", "not_contains", r"count_words|count_lines"),
            "result-no-change": regex("last_message", "contains", r"Result:[ \t*]*no_change\b"),
        },
    },
    "no-unsupported-claims": {
        "ver": "04", "scaffold": FIXTURE_B,
        "description": "VER-04: docs for a parallel --jobs option claim no speed-up, percentage or passing tests, though a code comment claims ~3x.",
        "prompt": "I added a --jobs option so wordcount can count several files in parallel. Update the docs and the\n"
                  "changelog for it.\n",
        "graders": {
            "skill-fired": FIRED,
            "readme-names-jobs": regex("README.md", "contains", "--jobs"),
            "changelog-names-jobs": regex("CHANGELOG.md", "contains", "--jobs"),
            "readme-no-unsupported-claim": regex("README.md", "not_contains", UNSUPPORTED),
            "changelog-no-unsupported-claim": regex("CHANGELOG.md", "not_contains", UNSUPPORTED),
        },
    },
    "preserves-release-history": {
        "ver": "05", "scaffold": FIXTURE_D,
        "description": "VER-05: a config key rename plus an untagged manifest bump to 1.1.0 keeps published releases byte-identical, adds a breaking Unreleased entry with no version or date, and fixes docs outside the diff.",
        "prompt": "I renamed the poll_interval setting to poll_interval_seconds. Update the documentation and the\n"
                  "changelog to match.\n",
        "graders": {
            "skill-fired": FIRED,
            "published-sections-unchanged": regex("CHANGELOG.md", "contains",
                r"## \[1\.0\.0\] - 2026-06-02\n\n### Added\n\n- Added TLS certificate checks for HTTPS endpoints\.\n\n### Fixed\n\n- Fixed a crash when the endpoint returned an empty body\.\n\n## \[0\.9\.0\] - 2026-04-15\n\n### Added\n\n- First public release: poll an HTTP endpoint and log status changes\.\n"),
            "keeps-once-entry": regex("CHANGELOG.md", "contains", r"^- Added the `--once` flag to poll a single time and exit, for use in cron jobs\.$", "m"),
            "breaking-entry": regex("CHANGELOG.md", "contains", r"^[^\n]*(?:[Bb]reaking|BREAKING)[^\n]*poll_interval_seconds|^[^\n]*poll_interval_seconds[^\n]*(?:[Bb]reaking|BREAKING)", "m"),
            "no-new-version": regex("CHANGELOG.md", "not_contains", r"^##[ \t]+\[?v?(?!1\.0\.0\]|0\.9\.0\])\d", "m"),
            "no-new-date": regex("CHANGELOG.md", "not_contains", r"\b(?!2026-06-02\b|2026-04-15\b)20\d\d-\d\d-\d\d\b"),
            "no-1-1-0": regex("CHANGELOG.md", "not_contains", r"^(?![^\n]*keepachangelog\.com/en/1\.1\.0)[^\n]*1\.1\.0", "m"),
            "one-unreleased": regex("CHANGELOG.md", "not_contains", r"^##[ \t]+\[?Unreleased[\s\S]*^##[ \t]+\[?Unreleased", "m"),
            "unreleased-first": regex("CHANGELOG.md", "contains", r"^## \[?Unreleased\]?[ \t]*\n[\s\S]*^## \[1\.0\.0\]", "m"),
            "config-doc-updated": regex("docs/configuration.md", "contains", "poll_interval_seconds"),
            "config-doc-old-row-gone": regex("docs/configuration.md", "not_contains", r"^\|[ \t]*`poll_interval`[ \t]*\|", "m"),
            "readme-example-updated": regex("README.md", "not_contains", r"^poll_interval[ \t]*=", "m"),
            "readme-example-renamed": regex("README.md", "contains", r"^poll_interval_seconds[ \t]*=", "m"),
        },
    },
    "asks-for-unknown-baseline": {
        "ver": "06", "scaffold": FIXTURE_E,
        "description": "VER-06: with no tag, remote or integration branch, the skill asks where the branch work began and writes no changelog.",
        "prompt": "Update the changelog with the work on my branch.\n",
        "graders": {
            "skill-fired": FIRED,
            "no-changelog": exists("CHANGELOG.md", False),
            "names-comparison-point": regex("last_message", "contains",
                r"[Cc]omparison point|[Bb]ase (?:revision|commit|branch|ref)|[Bb]aseline|[Ww]here (?:your|the|this) (?:work|branch|changes?) (?:starts?|started|began|begins)|[Ww]hich commit|[Ss]tarting (?:point|commit)|[Ff]irst commit of"),
            "asks-before-claiming": "---\ntype: llm\n---\n\n"
                "PASS if the reply asks the user for, or says it needs, the commit, tag or branch where their\n"
                "work on the branch began before any changelog entries are written, and it neither writes nor\n"
                "proposes changelog entries built from the branch's commits.\n"
                "FAIL if it writes or proposes changelog entries without that answer, or picks a baseline itself\n"
                "(the root commit, the whole history, the last commit or an assumed main branch) and proceeds.\n",
        },
    },
    "creates-readme-from-profile": {
        "ver": "07", "scaffold": FIXTURE_F,
        "description": "VER-07: a new repository without commits gets a README with real commands, no invented license or package-index install, and no template leftovers.",
        "prompt": "This project doesn't have a README yet. Please create one.\n",
        "graders": {
            "skill-fired": FIRED,
            "readme-created": exists("README.md", True),
            "one-title": regex("README.md", "contains", r"^(?:[ \t]*\n)*# \S"),
            "names-command": regex("README.md", "contains", r"csvtidy"),
            "names-python-version": regex("README.md", "contains", r"3\.11"),
            "local-install": regex("README.md", "contains", r"pip install (?:-e |--editable )?\."),
            "no-index-install": regex("README.md", "not_contains", r"pip install csvtidy\b"),
            "no-invented-license": regex("README.md", "not_contains", r"\b(?:MIT|Apache|GPL|BSD|MPL)\b|[Ll]icensed under"),
            "no-template-leftovers": regex("README.md", "not_contains", r"\{\{|<!--\s*guide"),
        },
    },
    "ignores-unrelated-request": {
        "ver": "08", "scaffold": FIXTURE_A, "negative": True,
        "description": "VER-08: a request for a commit message must not trigger the skill or change documentation.",
        "prompt": "Write a commit message for my staged changes.\n",
        "graders": {
            "skill-not-fired": NOT_FIRED,
            "readme-unchanged": regex("README.md", "not_contains", "--json"),
            "no-changelog": exists("CHANGELOG.md", False),
        },
    },
}


def main():
    for name, case in CASES.items():
        d = ROOT / name
        (d / "graders").mkdir(parents=True, exist_ok=True)
        tags = f"[documents-updater, ver-{case['ver']}" + (", negative-trigger]" if case.get("negative") else "]")
        turns, timeout = ("15", "300") if case.get("negative") else ("60", "1200")
        (d / "prompt.md").write_text(
            f"---\ndescription: \"{case['description']}\"\ntags: {tags}\nmax_turns: {turns}\n"
            f"timeout_seconds: {timeout}\nallowed_tools: {TOOLS}\n---\n{case['prompt']}")
        (d / "case.yaml").write_text(f"schema_version: \"1.1\"\nname: {name}\ncontext:\n  scaffold_script: scaffold.sh\n")
        (d / "scaffold.sh").write_text(case["scaffold"])
        os.chmod(d / "scaffold.sh", 0o755)
        for g, body in case["graders"].items():
            (d / "graders" / f"{g}.md").write_text(body)
    print("wrote", len(CASES), "cases")


if __name__ == "__main__":
    main()
