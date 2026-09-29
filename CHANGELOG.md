# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

Entries start with the epic skill. Earlier work is described in each specification's Change Log in
[`docs/specs/spec/`](docs/specs/spec/).

## Unreleased

### Added

- Added the `epic` skill, `/devforgeai:epic PRD-NNN`: it groups a PRD's ready, current-release
  requirements into epics you confirm, writes `docs/specs/epic/EPIC-NNN.md`, and lists every
  requirement left out with its reason and next action.
- Added a draft architecture port to the Codex package in `src/codex/devforgeai/` (manifest 0.3.0).
  Its [import report](src/codex/devforgeai/ARCHITECTURE-IMPORT-REPORT.md) records that SPEC-003
  qualification isn't established and that manual checks VER-12 and VER-13 haven't run.

### Changed

- The `architecture` skill's final next step now tells you to run `/devforgeai:epic PRD-NNN`, instead
  of saying the epic workflow isn't built.
- Moved the epic document template from `src/templates/epic.md` to
  `src/claude/DevForgeAI/skills/epic/assets/epic.md`.
