---
paths:
  - "docs/specs/**"
  - "src/schemas/**"
---

# Spec paths vs. disk

The specs were written against another repository's layout. Most of their paths now match this
workspace; translate the rest before using them:

| Specs say | Here |
|---|---|
| `src/claude/DevForgeAI/` (plugin source) | The same. It deploys to `.claude/skills/devforgeai/` (CLAUDE.md, "Source and deployed copy") |
| `src/staging/templates/` | `src/templates/` |
| `src/staging/examples/` | The same. `policy-two-orgs/` and `prd-production-mvp/` were copied unchanged from DevForgeAI-SDF2 (`ef78b83`) on 2026-09-27; `context-cli-service-rdbms/` came with PR #22 |
| `src/schemas/`, `schemas/*.schema.json` | `src/schemas/`. Documents a skill writes are checked against its `references/output-rules.md` (and brainstorm's validator script), not a schema. The one schema read at run time is policy: prd and architecture validate approved policy against their `references/schemas/` copies with `scripts/validate_policy.py` |
| PRD-001, STORY-001..005, ADR-001..003 | ADR-001..003, PRD-001 and STORY-002 are in `docs/specs/adr/`, `prd/` and `story/`, copied unchanged from DevForgeAI-SDF2 (`ef78b83`) on 2026-09-27. STORY-001, STORY-003..005 and the epics they cite are absent. ADR-001's worktree process applies here: `architecture` was built in `.claude/worktrees/story-003-architecture` |
| `devforgeai check` ("the checker") | Does not exist. SPEC-004 §2: never trust anything named `devforgeai` on PATH |

`src/schemas/spec.schema.json` requires a VER item's `upstream` only when the spec specifies a story.
A spec derived from another document, such as SPEC-005 or SPEC-006, may leave it out.
