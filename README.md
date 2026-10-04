# DevForgeAI

DevForgeAI is a Claude Code plugin, `devforgeai`, of spec-driven planning skills. It takes an idea
from a brainstorm through a product requirements document (PRD) and its architecture to epics. Each
step is written as a Markdown document with stable item IDs and traceable links, and every judgment
call it records (which ideas to pursue, priorities, what ships now) is left to you. A context skill
writes the project's stack, layout and convention documents from the architecture's decisions. Three
skills work outside that chain: a documents updater for a repository's README, CHANGELOG and guides,
a git workflow skill that takes work through commits and pull requests to a merge, and a spec lookup
that cites what a project's specs and ADRs already decided before Claude proposes anything new. A
progress tracker shows each brainstorm and architecture run's checklist steps as they happen.

It is for people who plan software with Claude Code. It is unreleased: load the plugin from this
repository's source.

## Prerequisites

- [Claude Code](https://code.claude.com). The recorded eval runs used versions 2.1.283 to 2.1.289;
  each specification's §9 names the version of each run.
- Python 3, used by the skills' scripts: the brainstorm validator, the policy and context checkers,
  the documents updater's Markdown checker, the git scripts, the spec lookup and the progress
  tracker's evaluator.
- For the `git` skill: git, and for its `pr` and `merge` phases the GitHub CLI (`gh`), signed in.
  GitHub is the only supported host; the other phases work with any git remote.

## Quick start

1. From the project where you want the planning documents, start Claude Code with the plugin loaded,
   replacing `<devforgeai>` with the path to this repository:

   ```bash
   claude --plugin-dir <devforgeai>/src/claude/DevForgeAI
   ```

2. Start a brainstorm, for example `/devforgeai:brainstorm ways to cut appointment no-shows`, or ask
   in plain words to brainstorm. Confirm which ideas to promote and whether the brainstorm is done.
   The skill writes `docs/specs/brainstorm/BRN-001.md` in your project.
3. Turn the promoted ideas into a PRD:

   ```text
   /devforgeai:prd BRN-001
   ```

   The skill asks only about what the brainstorm leaves open, writes
   `docs/specs/prd/PRD-001.md` (the next free number), and names the next step.
4. Define the architecture the PRD's epics must share:

   ```text
   /devforgeai:architecture PRD-001
   ```

   The skill settles each shared architectural question only by your decision, an accepted ADR or
   approved policy, writes `docs/specs/arch/ARCH-001.md` plus an ADR for each decision you make, and
   reports which requirements are ready for epics.
5. Write the project's context documents (tech stack, source tree, testing and each
   layer's conventions) in `docs/specs/context/` from the architecture's decisions and the conventions
   you confirm:

   ```text
   /devforgeai:context
   ```

   The epic skill doesn't read them; they are written for the story and spec steps
   ([ADR-004](docs/specs/adr/ADR-004.md)).
6. Group the ready requirements into epics:

   ```text
   /devforgeai:epic PRD-001
   ```

   The skill proposes a grouping of the ready, current-release requirements, writes
   `docs/specs/epic/EPIC-NNN.md` for each epic once you confirm it, and lists every requirement it left
   out with the reason.

## Skills

| Skill | Invoke | What it does | Status |
| --- | --- | --- | --- |
| `brainstorm` | `/devforgeai:brainstorm [topic]` | Runs a structured brainstorm and writes a BRN document with problems, ideas, assumptions and the dispositions you confirmed | Implemented ([SPEC-001](docs/specs/spec/SPEC-001.md)) |
| `prd` | `/devforgeai:prd [BRN-NNN]` | Drafts a PRD from a converged brainstorm's promoted ideas, interviews you only for the gaps, and applies any approved policy | Implemented ([SPEC-002](docs/specs/spec/SPEC-002.md)) |
| `documents-updater` | `/devforgeai:documents-updater [base-revision-or-range] [propose]` | Updates a repository's README, CHANGELOG and guides from its git changes, or proposes the edits | Implemented ([SPEC-006](docs/specs/spec/SPEC-006.md)) |
| `architecture` | `/devforgeai:architecture [PRD-NNN]` | Identifies the architectural questions separate epics must share, settles each only by your decision, an accepted ADR or approved policy, and writes an ARCH document with ADRs and a report of which requirements are ready for epics | Implemented ([SPEC-003](docs/specs/spec/SPEC-003.md)) |
| `epic` | `/devforgeai:epic [PRD-NNN]` | Groups a PRD's ready, current-release requirements into epics you confirm, and reports every requirement left out and why | Implemented ([SPEC-004](docs/specs/spec/SPEC-004.md)) |
| `context` | `/devforgeai:context [document]` | Writes and maintains the context documents in `docs/specs/context/` from accepted ADRs, approved policy, the ARCH and conventions you confirm; cites every decision and labels observed practice | Implemented ([SPEC-011](docs/specs/spec/SPEC-011.md)) |
| `spec-lookup` | `/devforgeai:spec-lookup [ID or term]` | Searches the project's `docs/specs/` and cites each match by file, line, version and status; anything with no match is a question for you, never something to build. Other skills run it through the `devforgeai:spec-lookup` agent | Implemented ([SPEC-014](docs/specs/spec/SPEC-014.md)) |
| `git` | `/devforgeai:git [status\|connect\|start\|commit\|push\|pr\|merge\|sync\|prune] [details]` | Commits and pushes work from its own branch and worktree, opens or updates a GitHub pull request, merges only a PR that an independent QA session approved for its head commit and you confirm, fast-forwards the default branch without discarding local edits, and prunes merged worktrees | Implemented; the source is v3, which is in review and not yet evaluated (v2 is the last approved version) ([SPEC-007](docs/specs/spec/SPEC-007.md), [qualification](docs/runbooks/git-v3-checks.md)) |

The planning chain is Brainstorm → PRD → Architecture Definition → Epic → Story → Spec; the first
four steps are implemented. The story skill is specified as a draft ([SPEC-009](docs/specs/spec/SPEC-009.md));
until it is built, the epic skill's handoff says to write stories by hand from the story template.

## Progress tracker

The plugin includes a progress tracker for the `brainstorm` and `architecture` skills
([SPEC-012](docs/specs/spec/SPEC-012.md), [SPEC-013](docs/specs/spec/SPEC-013.md)). It is a Claude
Code mod, so it runs only where Claude Code loads plugin hook modules.

- Each run's checklist steps appear in the status line and in a band above the prompt. The skills keep
  their checklist in Claude Code's task list, and tag each question with the step it belongs to.
- Each run is recorded under `devforgeai/progress/` in the project. Files older than 30 days are
  removed when a later session starts its first tracked run (the plugin's `retentionDays` setting).
- Observe mode, the default, only reports. Enforce mode, switched on from the band, refuses a question
  that isn't tagged with the step marked in progress, and a write that records a decision of yours
  without your answer. The choice is saved in `.claude/devforgeai.local.md`.
- When your request says to proceed without questions, the skill asks once whether to proceed
  without questions; the tracker records your answer as a waiver. At the end of a run it reviews any
  refusals and flags with you.
- Set the plugin's `tracking` setting to `off` to turn the tracker off; the skills work the same either
  way.

## Where documents go

Skills write to `docs/specs/<type>/<ID>.md` in your project, such as
`docs/specs/prd/PRD-002.md`, and allocate each ID themselves. Values you haven't decided stay
`null` or carry a `[NEEDS CLARIFICATION]` marker instead of a guess. The document format, IDs, links
and provenance rules are in the [templates README](src/templates/README.md), and the JSON Schemas
are in [`src/schemas/`](src/schemas/).

The `prd`, `architecture` and `context` skills also read optional policy: approved organization or project policy
documents in `docs/specs/policy/` (template: [`src/templates/policy.md`](src/templates/policy.md)), and a
user-local `.claude/devforgeai.local.md` for interaction defaults such as `interview.max_calls`.
[ADR-003](docs/specs/adr/ADR-003.md) defines the rules. The `epic` skill reads policy only to check
that each setting the architecture relied on is still approved, active and at the version it linked.

## Evaluate the skills

Each implemented skill has an eval suite in `src/claude/DevForgeAI/evals/<skill>/`. Run it from a
plain terminal, not inside a Claude Code session, at the repository root:

```bash
A="--allow-tools Write Edit Bash --scaffold --judge-model sonnet --threshold 0.8"
claude plugin eval src/claude/DevForgeAI --tag prd $A --output-dir tmp/eval-results/prd
```

The run prints a score per case; the bar is 0.8 per case over three runs. [CLAUDE.md](CLAUDE.md)
covers the options, the manual checks and how the plugin is deployed.

## Documentation

- [Specifications](docs/specs/spec/): what each skill must do, with its verification items.
- [ADRs](docs/specs/adr/): the build and deploy process, the architecture step, and the policy contract.
- [Brainstorm manual test runbook](docs/runbooks/brainstorm-manual-test.md): the checks evals can't automate.
- [CLAUDE.md](CLAUDE.md) and [AGENTS.md](AGENTS.md): instructions for AI agents working in this repository.
- [Changelog](CHANGELOG.md): notable changes, all unreleased so far.
- [Codex port](src/codex/devforgeai/README.md): the brainstorm, prd, architecture and documents-updater
  skills adapted for Codex, as source only; the prd and architecture ports are drafts (see their import
  reports).
