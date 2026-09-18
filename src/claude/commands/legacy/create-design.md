---
description: Create or extract design specifications and framework-agnostic design.md
argument-hint: [STORY-ID | component-description] [--extract <path>] [--url=<url>] [--origin=<skill:id>]
model: opus
allowed-tools: Read, Skill, AskUserQuestion
---

# Create Design Command

Invokes the `spec-driven-design` skill — the design specification phase. Produces the
`design.md` Design Source of Truth consumed by `/dev`, `/qa`, and 5 other skills.

Pipeline: `/create-solution-architecture` → *(if UI-bearing)* **`/create-design`** → `/create-development-architecture` → `/create-story` → `/dev`.

## Invocation

```
Skill(command="spec-driven-design")
```

The skill expands inline and owns the entire 9-phase workflow. Phase 00
(inline) handles argument parsing, story-file lookup, and mode selection
(`story` / `standalone` / `extract`).

**Prerequisite:** the 6 constitutional context files exist; tech-stack.md defines a frontend stack.
