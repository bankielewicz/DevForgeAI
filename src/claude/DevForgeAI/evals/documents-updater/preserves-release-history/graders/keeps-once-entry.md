---
type: regex
target: {source: file, path: CHANGELOG.md}
match: contains
flags: m
---
^- Added the `--once` flag to poll a single time and exit, for use in cron jobs\.$
