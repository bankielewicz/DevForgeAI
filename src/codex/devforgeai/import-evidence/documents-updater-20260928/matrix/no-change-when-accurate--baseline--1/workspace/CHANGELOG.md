# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## Unreleased

### Added

- Added `--json` to print the word and line counts as a JSON object, for use in scripts.

### Changed

- Extracted `count_words(text)` and `count_lines(text)` helpers in `wordcount.cli`.
  The existing `count(text)` function delegates to them, preserving counting behavior and CLI output.
