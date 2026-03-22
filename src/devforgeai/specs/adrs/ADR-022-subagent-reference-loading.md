# ADR-022: Subagent Reference Loading Mechanism

## Status

Accepted

## Date

2026-02-23

## Context

EPIC-082 (Domain Reference Generation) introduces `project-*.md` domain reference files that are auto-generated from context files and placed in `.claude/agents/{agent}/references/` directories for four targeted subagents: `backend-architect`, `test-automator`, `security-auditor`, and `code-reviewer`.

Once these files are generated, a mechanism is needed for subagents to discover and load them during task execution. Without a defined loading mechanism, the generated reference files will exist on disk but go unused — defeating the purpose of EPIC-082.

Three candidate approaches were identified during EPIC-082 architecture review:

| Approach | Mechanism | Pros | Cons |
|----------|-----------|------|------|
| **A: Orchestration-driven** | implementing-stories skill passes project reference paths to subagent `Task()` calls | No subagent prompt changes; clean SRP | Requires implementing-stories awareness of project-*.md file existence |
| **B: Explicit opt-in** | Add conditional loading hint to subagent prompts: "If project-*.md exists, load it" | Self-contained per agent; no orchestrator changes | Requires modifying all 4 agent prompts; adds conditional logic to agent definitions |
| **C: Framework auto-load** | Lightweight loader in designing-systems discovers and pre-loads references before agent invocation | Centralized, DRY approach | Adds coupling between designing-systems and subagent internals; breaks SRP slightly |

This decision is an architectural decision affecting the 4 targeted subagents and the implementing-stories skill. It requires an ADR per the framework's documented constraint that architectural decisions affecting multiple components must be recorded (Source: `devforgeai/specs/context/architecture-constraints.md`).

## Decision

**Approach A (Orchestration-driven) is selected as the reference loading mechanism for EPIC-082 domain reference files.**

The implementing-stories skill is responsible for detecting the presence of `project-*.md` reference files in the relevant subagent `references/` directories and passing their paths as context in the `Task()` call prompt when invoking those subagents.

Specifically:

1. Before invoking `backend-architect`, `test-automator`, `security-auditor`, or `code-reviewer` via `Task()`, the implementing-stories skill checks whether a corresponding `project-*.md` file exists in that agent's `references/` directory.
2. If a project reference file exists, its path is included in the `Task()` call prompt, instructing the subagent to load it as supplementary domain context.
3. If no project reference file exists, the `Task()` call proceeds unchanged — no behavior difference for projects without domain references.

## Rationale

Approach A is selected because:

- **Single Responsibility Principle (SRP):** Subagent definitions remain focused on their core function. Loading project-specific context is an orchestration concern, not an agent-definition concern. (Source: `devforgeai/specs/context/architecture-constraints.md`, Single Responsibility section)
- **No subagent prompt modifications required:** The 4 targeted subagent `.md` files remain unmodified (SC-4 from EPIC-082 success metrics: "Core agent files unmodified — Git diff verification: 0 modifications to *.md agent files").
- **Consistent with ADR-012 (Progressive Disclosure):** Project references are loaded only when present and only when relevant. The implementing-stories skill already orchestrates which subagents to invoke and with what context — adding reference path discovery is a natural extension of this orchestration role.
- **Backward compatible:** Projects without generated domain references experience no behavioral change. The check for `project-*.md` existence adds negligible overhead.

Approach B was rejected because modifying all 4 agent prompt files violates SC-4 and adds conditional logic that must be maintained across agent updates. Approach C was rejected because it introduces coupling between designing-systems and subagent internals, conflicting with the SRP constraint in architecture-constraints.md.

## Consequences

### Positive

- Subagent core `.md` files remain unmodified — framework agents stay generic and framework-agnostic
- Clear ownership: orchestration skill owns context assembly; subagents own domain logic
- Projects with no triggered heuristics (no `project-*.md` generated) incur zero overhead
- Aligns with existing Task() call pattern already used in implementing-stories skill
- ADR-012 (progressive disclosure) pattern honored: references loaded only when present

### Negative

- implementing-stories skill must be updated to perform file existence checks before Task() calls for the 4 targeted agents
- If implementing-stories skill is bypassed (direct Task() calls outside the skill), project references will not be loaded automatically
- Discovery logic in implementing-stories must be kept in sync if new targeted agents are added in future epics

### Neutral

- The 4 targeted `references/` directories already exist (verified during EPIC-082 planning) — no directory creation needed

## Implementation Notes

When implementing EPIC-082 Feature 3 (Phase 5.7 Workflow Integration, STORY-478) and Feature 4 (/audit-alignment --generate-refs, STORY-479), the following convention applies to all generated `project-*.md` files:

- Files are written to `.claude/agents/{agent}/references/project-{type}.md`
  - `project-domain.md` — for `backend-architect`
  - `project-testing.md` — for `test-automator`
  - `project-security.md` — for `security-auditor`
  - `project-review.md` — for `code-reviewer`
- The auto-generation header in each file includes a `Load via:` line showing the exact `Read(file_path=...)` call, serving as discoverable documentation for the implementing-stories skill

## Enforcement

- EPIC-082 Feature 3 (STORY-478) MUST implement the orchestration-driven loading mechanism in implementing-stories skill
- EPIC-082 Feature 4 (STORY-479) MUST document the loading convention in regenerated file headers
- Subagent core `.md` files MUST NOT be modified for reference loading purposes (SC-4 enforcement)
- New targeted agents added in future epics MUST follow the same orchestration-driven pattern

## References

- `devforgeai/specs/Epics/EPIC-082-domain-reference-generation.epic.md` — Epic defining domain reference generation scope
- `devforgeai/specs/adrs/ADR-012-subagent-progressive-disclosure.md` — Progressive disclosure pattern (on-demand loading)
- `devforgeai/specs/context/architecture-constraints.md` — Single Responsibility Principle constraint
- `devforgeai/specs/Stories/STORY-481-resolve-subagent-reference-loading.story.md` — Story that produced this ADR
- `.claude/skills/implementing-stories/SKILL.md` — Orchestration skill responsible for Task() invocation

---

**ADR Template Version:** 1.0
**Created:** 2026-02-23
**Author:** DevForgeAI AI Agent (STORY-481)
**Epic:** EPIC-082 Domain Reference Generation
