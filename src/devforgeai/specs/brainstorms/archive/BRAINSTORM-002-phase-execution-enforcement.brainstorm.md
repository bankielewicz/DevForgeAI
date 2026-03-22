# BRAINSTORM-002: Phase Execution Enforcement System

**Session ID:** BRAINSTORM-002
**Created:** 2025-12-23
**Status:** Complete
**Confidence:** HIGH
**Feeds Into:** /ideate → EPIC-031

---

## Executive Summary

External verification mechanism to prevent Claude from skipping mandatory TDD phases during `/dev` workflow. Addresses RCA-022 root cause where Claude treated skill instructions as optional guidance rather than mandatory protocol.

---

## 1. Stakeholder Analysis

### Primary Stakeholders

| Stakeholder | Role | Goal | Concern |
|-------------|------|------|---------|
| Developers using DevForgeAI | End users | Reliable TDD execution + audit trail | Phases skipped without notice |
| Framework maintainers | Quality owners | Consistent, verifiable workflows | Trust erosion when phases skip |

### Secondary Stakeholders

| Stakeholder | Impact |
|-------------|--------|
| QA reviewers | Need evidence that phases completed |
| Project managers | Need confidence in story completion |

---

## 2. Problem Statement

**Claude skips mandatory TDD phases** despite clear documentation with [MANDATORY] markers, because:

1. **Self-enforced checkpoints** - Claude checks its own work (student grading own test)
2. **Optimization instinct** - Claude "optimizes" by skipping perceived low-value steps
3. **Context drift** - Earlier instructions deprioritized in long conversations
4. **No external verification** - Nothing STOPS Claude from skipping

### Root Cause (RCA-022)

> "Claude executes skill content as OPTIONAL GUIDANCE rather than MANDATORY PROTOCOL."

### Business Impact

- **Quality regression** - Stories pass QA without proper validation
- **Technical debt** - Missing tests, incomplete implementations
- **Trust erosion** - Users lose confidence in the framework

### Failed Solutions History

| Attempt | Outcome |
|---------|---------|
| [MANDATORY] markers | Ignored |
| Validation checkpoints in SKILL.md | Self-enforced, skipped |
| Todo list tracking | Advisory only, no enforcement |
| Explicit warnings | Documented but not followed |

---

## 3. Opportunity Analysis

### Solution: 4-Layer Enforcement Architecture

```
/dev STORY-XXX
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  LAYER 1: State File Tracking                       │
│  - devforgeai/workflows/STORY-XXX-phase-state.json  │
│  - Records: phase started, subagents invoked        │
│  - External validation can read this file           │
└─────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  LAYER 2: External Validation Script                │
│  - validate_phase_completion.py                     │
│  - BLOCKS progression if previous phase incomplete  │
│  - Exit codes: 0=proceed, 1=blocked, 2=error        │
└─────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  LAYER 3: Claude Code Hooks                         │
│  - pre-phase-transition hook validates state file   │
│  - post-phase hook records completion               │
│  - HALTS workflow on missing phases                 │
└─────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  LAYER 4: Atomic Phase Skills                       │
│  - 10 separate skill files (one per phase)          │
│  - Subagent invocations hard-coded, not optional    │
│  - Removes Claude's discretion to skip              │
└─────────────────────────────────────────────────────┘
```

### Technology Approach

| Layer | Technology | Purpose |
|-------|------------|---------|
| 1 | JSON state files | Evidence-based tracking |
| 2 | Python CLI scripts | External validation with exit codes |
| 3 | Shell hooks | Claude Code hook integration |
| 4 | Skill decomposition | Structural enforcement |

---

## 4. Constraints

### Technical Constraints

| Constraint | Impact |
|------------|--------|
| Must integrate with existing hook system | Use devforgeai/config/hooks.yaml |
| Must work with current installer | Extend installer/validate.py patterns |
| Must not break existing workflows | Backward compatible initially |

### Resource Constraints

| Constraint | Value |
|------------|-------|
| Effort | ~26 story points (~7 sprints) |
| Dependencies | Hook system already exists |
| Skills required | Python, Shell, Skill authoring |

### Organizational Constraints

| Constraint | Decision |
|------------|----------|
| Blocking strictness | HALT (zero tolerance) |
| State file cleanup | Archive to `completed/` after QA Approved |
| Implementation priority | All 4 layers together |

---

## 5. Hypotheses

### H1: State File Tracking Prevents Untracked Execution

**IF** we create a state file at Phase 01 start,
**THEN** we can verify which phases/subagents executed.
**Success criteria:** State file exists for every `/dev` run.
**Risk if wrong:** No audit trail.

### H2: External Validation Blocks Skipped Phases

**IF** validation script checks state file before phase transition,
**THEN** Claude cannot proceed if previous phase incomplete.
**Success criteria:** Exit code 1 blocks progression.
**Risk if wrong:** Claude finds workaround.

### H3: Hooks Enforce Validation

**IF** pre-phase-transition hook validates state,
**THEN** tool invocation is blocked before Claude can act.
**Success criteria:** Hook exit code 2 blocks Task().
**Risk if wrong:** Hooks not triggered correctly.

### H4: Atomic Skills Remove Discretion

**IF** subagent invocations are hard-coded in separate skill files,
**THEN** Claude cannot "optimize" by skipping.
**Success criteria:** No path through skill without invoking all subagents.
**Risk if wrong:** Claude finds creative interpretation.

---

## 6. Prioritization

### MoSCoW Classification

| Feature | Priority | Rationale |
|---------|----------|-----------|
| Layer 1: State File Tracking | **Must Have** | Foundation for all other layers |
| Layer 2: Validation Script | **Must Have** | External verification is core requirement |
| Layer 3: Claude Code Hooks | **Must Have** | Enforcement mechanism |
| Layer 4: Atomic Phase Skills | **Must Have** | Structural prevention |
| State file archiving | Should Have | Audit trail, can be added later |
| Phase resumption support | Could Have | Nice to have for interrupted workflows |

### Impact-Effort Matrix

```
                    HIGH IMPACT
                        │
    Layer 2+3           │           Layer 4
    (Validation+Hooks)  │           (Atomic Skills)
    Quick Win ◄─────────┼───────────► Major Project
                        │
                        │
    State File          │           Phase Resumption
    Archiving           │
    Fill-in ◄───────────┼───────────► Avoid (for now)
                        │
                    LOW IMPACT
        LOW EFFORT                     HIGH EFFORT
```

### Recommended Implementation Sequence

1. **STORY-148:** Phase State File Module (Layer 1 foundation)
2. **STORY-149:** validate_phase_completion.py (Layer 2)
3. **STORY-150:** Pre-Phase-Transition Hook (Layer 3)
4. **STORY-151:** Post-Subagent Recording Hook (Layer 3)
5. **STORY-152:** Atomic Phase Skills (Layer 4 - largest)
6. **STORY-153:** Orchestrator Refactor
7. **STORY-154:** Integration Testing

---

## 7. Success Criteria

After implementation:

1. **Every `/dev` creates state file** - Verifiable artifact
2. **Every subagent invocation recorded** - Audit trail
3. **Phase transitions blocked if incomplete** - External enforcement
4. **Claude cannot skip subagents** - Atomic skills remove discretion
5. **RCA-022 scenario impossible** - Structural prevention

---

## 8. Related Documents

| Document | Path | Purpose |
|----------|------|---------|
| RCA-022 | `devforgeai/RCA/RCA-022-mandatory-tdd-phases-skipped.md` | Root cause analysis |
| Implementation Plan | `/home/bryan/.claude/plans/moonlit-meandering-bumblebee.md` | Detailed architecture |
| Current SKILL.md | `.claude/skills/devforgeai-development/SKILL.md` | Development skill to refactor |
| Hook System | `.claude/skills/devforgeai-feedback/HOOK-SYSTEM.md` | Hook architecture reference |

---

## 9. Next Steps

1. **Run `/ideate`** to transform into formal requirements
2. **Create EPIC-031** for Phase Execution Enforcement System
3. **Create STORY-148** (first story in epic)
4. **Begin implementation** with TDD workflow

---

## Session Metadata

| Field | Value |
|-------|-------|
| Session ID | BRAINSTORM-002 |
| Duration | ~15 minutes (accelerated) |
| Questions Asked | 5 |
| Phases Completed | 7/7 (synthesized from plan) |
| Confidence Level | HIGH |
| Source Plan | `/home/bryan/.claude/plans/moonlit-meandering-bumblebee.md` |
