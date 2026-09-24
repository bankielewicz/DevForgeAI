# Framework defaults (layer 1 of policy resolution)

These are the lowest layer in `policy.md` step R2 and R4. Organization policy, project policy and local
preferences layer on top of them as `policy.md` describes. The classes are those of ADR-003 A2.

| Key | Class | Default value | `overridable_by` | Resolution-line entry when no policy sets it |
|---|---|---|---|---|
| `quality.required_categories` | organizational policy | no categories beyond the operating-context floor (BEH-03) | `project` | `quality.required_categories=floor only (default)` |
| `architecture.mandated_platforms` | organizational policy | none | `project` | `architecture.mandated_platforms=none (default)` |
| `interview.max_calls` | interaction default | `8` | `project`, `local` | `interview.max_calls=8 (default)` |

## Not settings

These values look configurable but are not. No policy or local file changes them.

| Value | Class | Why |
|---|---|---|
| Quality floor per operating context (`interview.md`, Quality floor) | framework requirement | Policy may add categories, never remove floor ones |
| Validation attempts: 3 | framework requirement | SPEC-002 BEH-12 |
| `stage`, `operating_context`, `priority`, `release` values; NFR categories; item prefixes | document contract | Downstream steps depend on them |
| The AI never decides stage, context, priority or release | framework requirement | PRD-001 FR-003 |
| At most 4 questions per AskUserQuestion call, 2–4 options each | platform limit | Claude Code |
