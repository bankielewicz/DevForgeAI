# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## Unreleased

### Added

- Added `--json` to print the word and line counts as a JSON object, for use in scripts.
- Added `count_words(text)` and `count_lines(text)` helpers in `wordcount.cli` to count strings independently.

### Changed

- Refactored `count(text)` to use the new helpers, preserving its return format and CLI output.
