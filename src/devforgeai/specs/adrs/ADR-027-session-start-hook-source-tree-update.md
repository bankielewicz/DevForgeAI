# ADR-027: Source Tree Update for SessionStart Event-Driven Hook

**Date:** 2026-03-03
**Status:** Accepted
**Acceptance Date:** 2026-03-03
**Deciders:** Solo Developer, DevForgeAI Framework
**Tags:** source-tree, hooks, EPIC-086, STORY-529

## Context

STORY-529 implemented a SessionStart hook (`inject-phase-context.sh`) that injects workflow state after resume/compact events. During QA deep validation, the anti-pattern-scanner flagged 3 HIGH structure violations:

1. **Hook file not listed in source-tree.md** — The `.claude/hooks/` directory listing only shows `pre-tool-use.sh` and `post-qa-debt-detection.sh`. The new hook is undocumented.
2. **Naming convention mismatch** — source-tree.md specifies `post-{workflow}-{action}.sh` (EPIC-048 workflow hooks). The new hook `inject-phase-context.sh` is an event-driven hook responding to Claude Code `SessionStart` events, not a post-workflow hook.
3. **hooks.yaml registration** — `devforgeai/config/hooks.yaml` registers DevForgeAI feedback/retrospective hooks. The SessionStart hook is a Claude Code native hook registered in `.claude/settings.json`, not a DevForgeAI feedback hook. hooks.yaml registration does not apply.

The current naming convention was designed for EPIC-048 workflow lifecycle hooks (post-dev, post-qa). EPIC-086 introduces a new category: Claude Code event-driven hooks that respond to system events (SessionStart, Stop, etc.).

## Decision

1. **Add `inject-phase-context.sh`** to the `.claude/hooks/` listing in `devforgeai/specs/context/source-tree.md`.
2. **Expand the naming convention** to include event-driven hooks alongside workflow hooks:
   - Workflow hooks (EPIC-048): `post-{workflow}-{action}.sh`, `pre-{tool}-{action}.sh`
   - Event-driven hooks (EPIC-086): `inject-{context}-context.sh`
3. **Clarify hooks.yaml scope** — `devforgeai/config/hooks.yaml` registers DevForgeAI feedback hooks only. Claude Code native hooks (SessionStart, Stop, etc.) are registered in `.claude/settings.json` and do not require hooks.yaml entries.

## Rationale

1. Source-tree.md must reflect all files in the project to prevent structure violation false positives during QA.
2. Event-driven hooks serve a fundamentally different purpose than workflow lifecycle hooks — they respond to Claude Code system events rather than DevForgeAI workflow completions. A distinct naming pattern makes the distinction clear.
3. The `inject-` prefix communicates the hook's purpose: injecting context into the session, not triggering feedback or analysis.
4. hooks.yaml was designed for DevForgeAI's feedback system (operation_type: command/skill/subagent). Claude Code native hooks use `.claude/settings.json` configuration with event matchers.

## Consequences

### Positive
- QA anti-pattern-scanner will no longer flag inject-phase-context.sh as a structure violation
- Future EPIC-086 hooks have a documented naming convention to follow
- Clear separation between DevForgeAI feedback hooks (hooks.yaml) and Claude Code event hooks (settings.json)

### Negative
- Two naming convention patterns to maintain (workflow + event-driven)

### Risks
- Future hooks may not fit either pattern — mitigated by documenting both patterns as examples, not exhaustive rules

## Alternatives Considered

1. **Rename hook to `post-sessionstart-context-injection.sh`** — Rejected. Forces event-driven hooks into a workflow naming pattern that doesn't semantically fit. SessionStart is not a "post-workflow" event.
2. **Add to hooks.yaml** — Rejected. hooks.yaml registers DevForgeAI feedback hooks with operation_type/trigger_status fields. A Claude Code native hook doesn't have these properties.

## Enforcement

### Context File Updates Required

| File | Change | Type |
|------|--------|------|
| `devforgeai/specs/context/source-tree.md` | Add `inject-phase-context.sh` to `.claude/hooks/` listing, expand naming convention | Update |

### Affected Skills

| Skill | Change |
|-------|--------|
| devforgeai-qa | anti-pattern-scanner will recognize the new hook as documented |

### New Artifacts

| Artifact | Location |
|----------|----------|
| ADR-027 | `devforgeai/specs/adrs/ADR-027-session-start-hook-source-tree-update.md` |
