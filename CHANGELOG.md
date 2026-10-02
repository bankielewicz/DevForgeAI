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
- Added the `git` skill, `/devforgeai:git [phase] [details]`. It classifies changes before staging,
  blocks secrets and oversized files, runs the repository's checks, commits and pushes work from its
  own branch and worktree, and opens or updates a GitHub pull request. It merges only a PR whose
  `merge-approved` label and QA verdict name the current head commit, after you confirm; syncs the
  default branch by fast-forward without discarding local edits; and prunes worktrees that are merged
  and clean. Built from the draft [SPEC-007](docs/specs/spec/SPEC-007.md).
- Added a draft architecture port to the Codex package in `src/codex/devforgeai/` (manifest 0.3.0).
  Its [import report](src/codex/devforgeai/ARCHITECTURE-IMPORT-REPORT.md) records that SPEC-003
  qualification isn't established and that manual checks VER-12 and VER-13 haven't run.

### Changed

- Prepared git SKL-006 v3 (plugin 0.9.1 candidate): push and PR requests check the requested
  branch for unrelated history before rebasing; carrying work from any branch asks before including
  commits outside the default branch, while reusing explicit inclusion; password assignments in
  explicitly named local/example Compose files warn and require confirmation. Other Compose
  literals, known tokens and private keys remain blocked. Native and manual qualification, approval
  and deployment are pending; see [the verification record](docs/runbooks/git-v3-checks.md).
- Refreshed SPEC-008 and SPEC-010's SPEC-007 citations for the v3 candidate. SPEC-010 v3 awaits
  approval; its posting contract is unchanged. Git tests now collect alongside other skills' tests.
- The `architecture` skill's final next step now tells you to run `/devforgeai:epic PRD-NNN`, instead
  of saying the epic workflow isn't built.
- Moved the epic document template from `src/templates/epic.md` to
  `src/claude/DevForgeAI/skills/epic/assets/epic.md`.
