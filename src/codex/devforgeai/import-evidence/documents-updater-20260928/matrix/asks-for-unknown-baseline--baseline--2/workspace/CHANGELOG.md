# Changelog

## Unreleased

### Added

- CSV export support through `export_csv`, including a header row.
- Week filtering through `since`, retaining rows on or after the specified ISO week.

### Fixed

- ISO week parsing through `parse_week` for values such as `2026-W37`.
