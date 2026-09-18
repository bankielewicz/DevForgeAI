---
description: Produce a per-epic Solution Architecture Document from the System Architecture
argument-hint: [epic-id] [--system-architecture=<path or SYSARCH-NNN>] [--resume SOLARCH-NNN]
model: opus
allowed-tools: Read, Skill, AskUserQuestion
---

# Create Solution Architecture Command

Invokes the `spec-driven-solution-architecture` skill — the meso / per-epic
Solution Architect phase. Consumes the System Architecture Document
(`/create-system-architecture` output), decomposes an epic into components,
interface contracts, a data model, an integration design, and a feature
decomposition with feasibility verdicts, and emits a self-contained HTML Solution
Architecture Document with an embedded JSON data island.

Pipeline: `/create-system-architecture` → **`/create-solution-architecture`** → `/create-development-architecture`.

## Invocation

```
Skill(command="spec-driven-solution-architecture")
```

The skill expands inline and owns the entire 8-phase workflow: System Architecture
ingestion & validation, epic framing, component decomposition, interface & contract
design, data-model design, integration design, feature decomposition, and document
synthesis. After invocation, execute the skill's phases sequentially.

## Arguments

- `epic-id` (optional) — the `EPIC-NNN` this Solution Architecture decomposes; the
  skill frames or selects the epic in Phase 02 when omitted.
- `--system-architecture=<path or SYSARCH-NNN>` (optional) — explicit reference to
  the source System Architecture Document; the skill auto-detects it in
  `devforgeai/specs/architecture/` when omitted.
- `--resume SOLARCH-NNN` (optional) — resume an interrupted session from its checkpoint.

**Prerequisite:** a System Architecture Document from `/create-system-architecture`
at `devforgeai/specs/architecture/SYSARCH-NNN-{project}.system-architecture.html`.
