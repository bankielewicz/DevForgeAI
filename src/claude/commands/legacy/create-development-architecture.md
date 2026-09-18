---
description: Produce a per-feature Development Architecture Document from the Solution Architecture
argument-hint: [feature-id] [--solution-architecture=<path or SOLARCH-NNN>] [--resume DEVARCH-NNN]
model: opus
allowed-tools: Read, Skill, AskUserQuestion
---

# Create Development Architecture Command

Invokes the `spec-driven-development-architecture` skill — the micro / per-feature
Development Architect phase. Consumes the Solution Architecture Document
(`/create-solution-architecture` output), and for one feature produces an
implementation-ready design: a layer-placement map, design patterns, a module
structure, a dependency-wiring graph, per-component test-strategy hooks, and the
`SEED-NNN` story seeds — emitted as a self-contained HTML Development Architecture
Document with an embedded JSON data island.

Pipeline: `/create-solution-architecture` → **`/create-development-architecture`** → `/create-story`.

## Invocation

```
Skill(command="spec-driven-development-architecture")
```

The skill expands inline and owns the entire 8-phase workflow: Solution Architecture
ingestion & validation, feature framing, layer placement mapping, design pattern
selection, module structure & dependency wiring, test strategy hooks, story seed
generation, and document synthesis. After invocation, execute the skill's phases
sequentially.

## Scope boundary

This skill produces **design only**. It writes no story files — that is
`/create-story` — and no production code — that is the `backend-architect` subagent
inside `/dev`. The `story_seeds` it emits are inputs for `/create-story`.

## Arguments

- `feature-id` (optional) — the `F-NN` feature this Development Architecture details;
  the skill selects the feature from the Solution Architecture's `feature_decomposition`
  in Phase 02 when omitted.
- `--solution-architecture=<path or SOLARCH-NNN>` (optional) — explicit reference to
  the source Solution Architecture Document; the skill auto-detects it in
  `devforgeai/specs/architecture/` when omitted.
- `--resume DEVARCH-NNN` (optional) — resume an interrupted session from its checkpoint.

**Prerequisite:** a Solution Architecture Document from `/create-solution-architecture`
at `devforgeai/specs/architecture/SOLARCH-NNN-{epic}.solution-architecture.html`, and
the project test plan at `devforgeai/specs/context/test-plan.ai.yaml`.
