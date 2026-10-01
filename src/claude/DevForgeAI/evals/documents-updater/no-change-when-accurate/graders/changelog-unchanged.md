---
type: regex
target: {source: file, path: CHANGELOG.md}
match: contains
---
^# Changelog\n\nAll notable changes to this project are documented in this file\.\n\nThe format is based on \[Keep a Changelog\]\(https://keepachangelog\.com/en/1\.1\.0/\)\.\n\n## Unreleased\n\n### Added\n\n- Added `--json` to print the word and line counts as a JSON object, for use in scripts\.\n$
