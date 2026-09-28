#!/usr/bin/env bash
# Fixture D (VER-05): pollwatch with a Keep a Changelog CHANGELOG (one Unreleased entry, published
# 1.0.0 and 0.9.0), README and docs/configuration.md naming poll_interval, then an uncommitted rename
# of that key to poll_interval_seconds in the code (staged) and the example file (unstaged), and a
# pyproject version bump to 1.1.0 (staged) with no tag. README.md and docs/configuration.md are not
# in the diff.
set -euo pipefail
export GIT_AUTHOR_NAME="Dana Reyes" GIT_AUTHOR_EMAIL="dana@example.com"
export GIT_COMMITTER_NAME="Dana Reyes" GIT_COMMITTER_EMAIL="dana@example.com"
commit() { # commit <ISO date> <message>
  GIT_AUTHOR_DATE="$1" GIT_COMMITTER_DATE="$1" git -c commit.gpgsign=false commit -q -m "$2"
}
git init -q -b main
mkdir -p src/pollwatch docs
cat > pyproject.toml <<'FIXTURE'
[project]
name = "pollwatch"
version = "1.0.0"
description = "Poll an HTTP endpoint and log status changes"
requires-python = ">=3.11"

[project.scripts]
pollwatch = "pollwatch.cli:main"
FIXTURE
printf '' > src/pollwatch/__init__.py
cat > src/pollwatch/cli.py <<'FIXTURE'
"""Command-line entry point for pollwatch."""
import argparse
import time
import urllib.request

from pollwatch.config import load


def main(argv=None):
    parser = argparse.ArgumentParser(prog="pollwatch")
    parser.add_argument("--config", default="pollwatch.toml")
    args = parser.parse_args(argv)
    config = load(args.config)
    last = None
    while True:
        with urllib.request.urlopen(config["url"]) as response:
            status = response.status
        if status != last:
            print(f"status {status}")
            last = status
        time.sleep(int(config["poll_interval"]))
FIXTURE
cat > src/pollwatch/config.py <<'FIXTURE'
"""Loads pollwatch.toml."""
import tomllib

DEFAULTS = {"url": None, "poll_interval": 30}


def load(path="pollwatch.toml"):
    with open(path, "rb") as f:
        data = tomllib.load(f)
    config = {**DEFAULTS, **data}
    if not config["url"]:
        raise ValueError("pollwatch.toml must set url")
    if int(config["poll_interval"]) < 5:
        raise ValueError("poll_interval must be at least 5")
    return config
FIXTURE
cat > pollwatch.example.toml <<'FIXTURE'
url = "https://status.example.com/health"
poll_interval = 30
FIXTURE
cat > README.md <<'FIXTURE'
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
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

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
FIXTURE
git add -A
commit 2026-06-02T09:00:00Z "Release 1.0.0"
git tag v1.0.0
# After the release: --once, recorded under Unreleased.
cat > src/pollwatch/cli.py <<'FIXTURE'
"""Command-line entry point for pollwatch."""
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
cat > CHANGELOG.md <<'FIXTURE'
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
FIXTURE
git add -A
commit 2026-07-14T09:00:00Z "Add --once"
# The work to document: uncommitted.
cat > src/pollwatch/config.py <<'FIXTURE'
"""Loads pollwatch.toml."""
import tomllib

DEFAULTS = {"url": None, "poll_interval_seconds": 30}


def load(path="pollwatch.toml"):
    with open(path, "rb") as f:
        data = tomllib.load(f)
    config = {**DEFAULTS, **data}
    if not config["url"]:
        raise ValueError("pollwatch.toml must set url")
    if int(config["poll_interval_seconds"]) < 5:
        raise ValueError("poll_interval_seconds must be at least 5")
    return config
FIXTURE
sed -i 's/config\["poll_interval"\]/config["poll_interval_seconds"]/' src/pollwatch/cli.py
sed -i 's/^version = "1.0.0"/version = "1.1.0"/' pyproject.toml
git add src/pollwatch/config.py src/pollwatch/cli.py pyproject.toml
cat > pollwatch.example.toml <<'FIXTURE'
url = "https://status.example.com/health"
poll_interval_seconds = 30
FIXTURE
