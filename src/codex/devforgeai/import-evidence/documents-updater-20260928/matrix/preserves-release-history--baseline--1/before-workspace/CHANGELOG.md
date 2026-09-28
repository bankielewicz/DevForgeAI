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
