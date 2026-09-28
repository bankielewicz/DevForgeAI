---
type: regex
target: {source: file, path: CHANGELOG.md}
match: contains
---
## \[1\.0\.0\] - 2026-06-02\n\n### Added\n\n- Added TLS certificate checks for HTTPS endpoints\.\n\n### Fixed\n\n- Fixed a crash when the endpoint returned an empty body\.\n\n## \[0\.9\.0\] - 2026-04-15\n\n### Added\n\n- First public release: poll an HTTP endpoint and log status changes\.\n
