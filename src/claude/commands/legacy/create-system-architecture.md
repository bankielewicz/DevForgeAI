---
description: Produce the System Architecture Document and constitutional context files
argument-hint: [project-name] [--pm-plan=<path>] [--resume SYSARCH-NNN]
model: opus
allowed-tools: Read, Skill, AskUserQuestion
---

# Create System Architecture Command

Invokes the `spec-driven-system-architecture` skill — the macro / constitutional
architect phase. Consumes the Project Management plan (`/ideate` output), locks the
technology stack, defines system boundaries and integration topology, and emits the
6 immutable context files, their `.ai.md` companions, `test-plan.ai.yaml`, the ADRs,
and a self-contained HTML System Architecture Document.

Pipeline: `/ideate` (PM) → **`/create-system-architecture`** → `/create-solution-architecture`.

## Invocation

```
Skill(command="spec-driven-system-architecture")
```

The skill expands inline and owns the entire 7-phase workflow: PM plan ingestion &
validation, context discovery, constitutional context files, ADR creation, system
design, architecture review, and document synthesis. After invocation, execute the
skill's phases sequentially.

## Arguments

- `project-name` (optional) — defaults to the PM plan `project` field.
- `--pm-plan=<path>` (optional) — explicit path to the requirements file; the skill
  auto-detects it in `devforgeai/specs/requirements/` when omitted.
- `--resume SYSARCH-NNN` (optional) — resume an interrupted session from its checkpoint.

**Prerequisite:** a PM plan from `/ideate` at `devforgeai/specs/requirements/{project}-requirements.md`.
