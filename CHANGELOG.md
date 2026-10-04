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
- Added the `context` skill, `/devforgeai:context [document]`: it writes and maintains a project's
  context documents in `docs/specs/context/` (index, architecture, tech stack, source tree, testing,
  and one per component kind) from accepted ADRs, approved policy, the ARCH and conventions you
  confirm. It cites each decision, labels observed practice, and hands undecided significant choices
  back to Architecture Definition. Specified by [SPEC-011](docs/specs/spec/SPEC-011.md).
- Added the `spec-lookup` skill, `/devforgeai:spec-lookup [ID or term]`: it searches a project's
  `docs/specs/`, cites each match by file and line with the document's version and status, and treats
  a topic with no match as your decision to ask about. The plugin's `devforgeai:spec-lookup` agent runs
  the same lookup during another skill's workflow. Specified by [SPEC-014](docs/specs/spec/SPEC-014.md).
- Added a progress tracker for `brainstorm` and `architecture` runs
  ([SPEC-012](docs/specs/spec/SPEC-012.md), [SPEC-013](docs/specs/spec/SPEC-013.md)). It records each
  run in `devforgeai/progress/`, checks the run's checklist steps against evidence, and shows them in
  the status line and a band above the prompt. Observe mode, the default, only reports; enforce mode,
  switched from the band and saved as `progress.mode` in `.claude/devforgeai.local.md`, refuses a
  write or question that breaks the checklist and says how to recover. The plugin settings `tracking`
  (`on` or `off`) and `retentionDays` (default 30) turn it off and set how long its files are kept.
- Added an end-of-run review: after a tracked run, the tracker asks you about each refusal and flag,
  one at a time, and records your answers.
- Added the waiver question: when a request says to proceed without questions, `brainstorm` and
  `architecture` ask once whether to proceed without questions, and the tracker records your answer.
- Added six `testing.*` organizational-policy settings
  ([ADR-005](docs/specs/adr/ADR-005.md)) and rule SV-08, checked by the shared policy script.
- Added component kinds to architecture: each ARCH component names its kinds, the skill asks when a
  kind is uncertain, and the context skill writes one document per kind.
- Added a draft architecture port to the Codex package in `src/codex/devforgeai/` (manifest 0.3.0).
  Its [import report](src/codex/devforgeai/ARCHITECTURE-IMPORT-REPORT.md) records that SPEC-003
  qualification isn't established and that manual checks VER-12 and VER-13 haven't run.
- Added a draft PRD port to the Codex package; see its README for each port's status.

### Changed

- Prepared git SKL-006 v3: push and PR requests check the requested
  branch for unrelated history before rebasing; carrying work from any branch asks before including
  commits outside the default branch, while reusing explicit inclusion; password assignments in
  explicitly named local/example Compose files warn and require confirmation. Other Compose
  literals, known tokens and private keys remain blocked. v3 is the `git` skill's source on `main`;
  its native and manual qualification and approval are pending; see
  [the verification record](docs/runbooks/git-v3-checks.md).
- `brainstorm` and `architecture` keep their checklist in Claude Code's task list and tag each
  question with its step, which the question shows as "Step N". `brainstorm` runs its validator,
  `scripts/validate_brn.py`, as its own command.
- `architecture` confirms the outcome with you whenever it writes to an existing ARCH, also after a
  confirmation typed in the request. A failed amendment leaves an approved ARCH in review, and a failed
  supersession restores the older ADR. With no PRD, it points to `/devforgeai:prd`.
- `prd` keeps a PRD whose extension fails in review with its approval cleared, and validates with the
  policy script it shares with `architecture`. With no usable brainstorm, it says why and points to
  `/devforgeai:brainstorm`. A success signal that measures no promoted idea gets no upstream link but
  keeps the baseline, target and measure you give. A `[NEEDS ADR]` marker holds epics back until the
  architecture step resolves that exact decision.
- `epic` reports every FR once and every NFR at least once, flags a blocked NFR that an active epic
  refines, sends a requirement whose policy platform changed back to architecture, and names no story
  step when nothing is eligible.
- `git` (SKL-006 v2) creates worktrees under the main checkout by absolute path, never discards content
  that exists only in the index, catches `sk-proj-`, `sk-svcacct-` and `sk-admin-` keys, warns instead
  of blocking on credentials in local or example URLs, and always asks before deleting a remote branch,
  naming it.
- An impossible date is an ordinary `schema` error in the prd, architecture and epic validators and in
  the policy script.
- `check_docs.py` (documents-updater) no longer reports footnote definitions as broken links,
  repeated sub-bullets as duplicate `Unreleased` entries, or an empty `Unreleased` section as an
  error, and no longer reads a leading horizontal rule as front matter.
- Refreshed SPEC-008 and SPEC-010's SPEC-007 citations for the v3 candidate. SPEC-010 v3 awaits
  approval; its posting contract is unchanged. Git tests now collect alongside other skills' tests.
- The `architecture` skill's final next step now tells you to run `/devforgeai:epic PRD-NNN`, instead
  of saying the epic workflow isn't built.
- Moved the epic document template from `src/templates/epic.md` to
  `src/claude/DevForgeAI/skills/epic/assets/epic.md`.

### Fixed

- The shared policy script rejects a NaN value, such as `testing.coverage_threshold: .nan`, as a
  schema error.
- `brainstorm`'s validator rejects an impossible date, empty template defaults such as `owner: ""`,
  and frontmatter keys it didn't check before, with and without PyYAML; a non-UTF-8 file gets an
  error message instead of a traceback.
