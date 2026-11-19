# Backlog

Work that was deferred, with where it came from. One row per item; nothing here is decided or built.

- Each row names its **source**: the spec section, review or issue that holds the detail. The source is the
  record; this file is the index that makes a deferred item easy to find again.
- Add rows at the end. Change a row's **Status** in place (`deferred`, `picked up: <PR or spec version>`,
  `dropped: <who, date>`); never delete or renumber a row.
- Before starting an item, follow CLAUDE.md, "Look it up before building it": read the source and ask Bryan.
  An item that changes a spec needs a new version of that spec, approved, before any build.
- IDs are `DEF-NNN`, in order of adding. (`BL-NNN` IDs belong to another repository's backlog.)

| ID | Item | Source | Deferred by | Status |
|---|---|---|---|---|
| DEF-001 | precompact: send START-HERE.md's Write as a call of its own and read its result before RESUME-PROMPT.md and TASKS.md are written | `docs/specs/spec/SPEC-015.md` §13, record of 2026-11-18, item 1; §9, "VER-11 (live)", observation in (g) | Bryan, 2026-11-18 | deferred |
| DEF-002 | precompact: the report names the learnings the session saved to memory before the skill ran | SPEC-015 §13, record of 2026-11-18, item 2; §9, "VER-11 (live)", note in (c) | Bryan, 2026-11-18 | deferred |
| DEF-003 | precompact: say what the report states when pruning is skipped by a read-only file system; whether the skill names the sandbox setting is Bryan's to decide | SPEC-015 §13, record of 2026-11-18, item 3; §9, "Sandbox probe of the real store" | Bryan, 2026-11-18 | deferred |
| DEF-004 | precompact: correct ERR-08's condition, §10 and CHANGELOG.md, which say a sandboxed session stays on the fallback; the probe showed its Write tool reaches the store | SPEC-015 §13, record of 2026-11-18, item 4; §9, "Sandbox probe of the real store" | Bryan, 2026-11-18 | deferred |
| DEF-005 | precompact: the resume prompt's template names "the folder this run wrote", not "the handoff folder" | SPEC-015 §13, record of 2026-11-18, item 5; `docs/process/plugin-workflow/reviews/20261118T0354Z-plugin-dev-921e165.md`, "Open, by choice" | Bryan, 2026-11-18 | deferred |
| DEF-006 | precompact: a guard that refuses writes under another session's handoff folder (offered, not decided; today the rule rests on the skill's text and `check_handoff.py --session`) | SPEC-015 §13, record of 2026-11-18, last sentence; §9, "Sandbox probe of the real store", consequences | not decided | deferred |
| DEF-007 | brainstorm: four more frameworks, the selection rules and the task list first in SKILL.md | `docs/specs/brainstorming/framework-catalog.md` | Bryan asked for the specs, 2026-11-18; not built | deferred |
| DEF-008 | brainstorm: project kind, the intake question sets, sources and evidence, the Target users and success-signal shapes | `docs/specs/brainstorming/intake-and-evidence.md` | as DEF-007 | deferred |
| DEF-009 | brainstorm: brownfield runs that read the project's documents and earlier BRNs and revisit assumptions | `docs/specs/brainstorming/brownfield-iteration.md` | as DEF-007 | deferred |
| DEF-010 | brainstorm: assumption risk ranking and a first release cut the user confirms | `docs/specs/brainstorming/mvp-and-prototype-path.md` | as DEF-007 | deferred |
| DEF-011 | prd: take the project kind, users, first release cut and signals from the richer BRN (needs a SPEC-002 version) | `docs/specs/brainstorming/prd-handoff-contract.md` | as DEF-007; its PRD side is built after DEF-007 to DEF-010 under SPEC-002 v10 and before the PRD interview-at-scale build (Bryan, 2026-11-19), its one brainstorm item (BEH-34) with them | deferred |
| DEF-012 | a brainstorm pane and hand-off screen: a design system for the look (the asset is named in the source), the five chosen boards regenerated with their remaining states, then a decision whether to build | `docs/specs/brainstorming/design/README.md` | not decided | deferred |

DEF-001 to DEF-005 are meant for one version together (SPEC-015 v5, then SKL-012 v3): each alone is too small to
pay for a plugin iteration, a gate and a version bump.

DEF-007 to DEF-010 are built together as one brainstorm skill version, one commit for each
(`docs/specs/brainstorming/README.md` §8), the fourth carrying DEF-011's report-block item; DEF-011's PRD side
afterwards.
