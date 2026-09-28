# DevForgeAI

DevForgeAI is a Claude Code plugin, `devforgeai`, of spec-driven planning skills. It takes an idea
from a brainstorm to a product requirements document (PRD). Each step is written as a Markdown
document with stable item IDs and traceable links, and every judgment call it records (which ideas
to pursue, priorities, what ships now) is left to you.

It is for people who plan software with Claude Code. It is unreleased: load the plugin from this
repository's source.

## Prerequisites

- [Claude Code](https://code.claude.com). The skills were built and evaluated with version 2.1.283.
- Python 3, used by the brainstorm skill's validator and the documents updater's Markdown checker.

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

## Skills

| Skill | Invoke | What it does | Status |
| --- | --- | --- | --- |
| `brainstorm` | `/devforgeai:brainstorm [topic]` | Runs a structured brainstorm and writes a BRN document with problems, ideas, assumptions and the dispositions you confirmed | Implemented ([SPEC-001](docs/specs/spec/SPEC-001.md)) |
| `prd` | `/devforgeai:prd [BRN-NNN]` | Drafts a PRD from a converged brainstorm's promoted ideas, interviews you only for the gaps, and applies any approved policy | Implemented ([SPEC-002](docs/specs/spec/SPEC-002.md)) |
| `documents-updater` | `/devforgeai:documents-updater [base-revision-or-range] [propose]` | Updates a repository's README, CHANGELOG and guides from its git changes, or proposes the edits | Implemented ([SPEC-006](docs/specs/spec/SPEC-006.md)) |
| `architecture` | — | Architecture Definition: an ARCH document and ADRs for a PRD | Specified only ([SPEC-003](docs/specs/spec/SPEC-003.md)) |
| `epic` | — | Epics refining PRD requirements | Specified only ([SPEC-004](docs/specs/spec/SPEC-004.md)) |

The planning chain is Brainstorm → PRD → Architecture Definition → Epic → Story → Spec; the first
two steps are implemented. Until the architecture skill exists, the PRD skill's handoff says to write
ADRs by hand.

## Where documents go

Skills write to `docs/specs/<type>/<ID>.md` in your project, such as
`docs/specs/prd/PRD-002.md`, and allocate each ID themselves. Values you haven't decided stay
`null` or carry a `[NEEDS CLARIFICATION]` marker instead of a guess. The document format, IDs, links
and provenance rules are in the [templates README](src/templates/README.md), and the JSON Schemas
are in [`src/schemas/`](src/schemas/).

The `prd` skill also reads optional policy: approved organization or project policy documents in
`docs/specs/policy/` (template: [`src/templates/policy.md`](src/templates/policy.md)), and a
user-local `.claude/devforgeai.local.md` for interaction defaults such as `interview.max_calls`.
[ADR-003](docs/specs/adr/ADR-003.md) defines the rules.

## Evaluate the skills

Each implemented skill has an eval suite in `src/claude/DevForgeAI/evals/<skill>/`. Run it from a
plain terminal, not inside a Claude Code session, at the repository root:

```bash
claude plugin eval src/claude/DevForgeAI --tag prd --allow-tools Write Edit Bash --scaffold \
  --judge-model sonnet --threshold 0.8 --output-dir tmp/eval-results/prd
```

The run prints a score per case; the bar is 0.8 per case over three runs. [CLAUDE.md](CLAUDE.md)
covers the options, the manual checks and how the plugin is deployed.

## Documentation

- [Specifications](docs/specs/spec/): what each skill must do, with its verification items.
- [ADRs](docs/specs/adr/): the build and deploy process, the architecture step, and the policy contract.
- [Brainstorm manual test runbook](docs/runbooks/brainstorm-manual-test.md): the checks evals can't automate.
- [CLAUDE.md](CLAUDE.md) and [AGENTS.md](AGENTS.md): instructions for AI agents working in this repository.
- [Codex port](src/codex/devforgeai/README.md): the brainstorm skill adapted for Codex.
