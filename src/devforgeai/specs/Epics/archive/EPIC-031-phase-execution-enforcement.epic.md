# EPIC-031: Phase Execution Enforcement System

**Status:** Active
**Created:** 2025-12-23
**Priority:** P0 - Critical
**Brainstorm:** BRAINSTORM-002
**Plan File:** `/home/bryan/.claude/plans/moonlit-meandering-bumblebee.md`

---

## Epic Summary

External verification mechanism to prevent Claude from skipping mandatory TDD phases during `/dev` workflow. Implements 3-layer enforcement architecture using external validation scripts and hooks - enforcement comes from external tools, not skill structure.

---

## Problem Statement

**Root Cause (RCA-022):** Claude executes skill content as OPTIONAL GUIDANCE rather than MANDATORY PROTOCOL.

**Evidence:** During STORY-128, multiple mandatory phases were skipped:
- Phase 01: tech-stack-detector NOT invoked
- Phase 03: context-validator NOT invoked
- Phase 04: refactoring-specialist NOT invoked
- Phase 06: deferral-validator NOT invoked
- Phase 07: DoD Update Bridge workflow skipped

**Business Impact:**
- Quality regression - Stories pass QA without proper validation
- Technical debt - Missing tests, incomplete implementations
- Trust erosion - Users lose confidence in the framework

---

## Solution Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    3-LAYER ENFORCEMENT ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  LAYER 1: State File Tracking (Evidence)                                │
│  - devforgeai/workflows/STORY-XXX-phase-state.json                      │
│  - Records: phase started, subagents invoked, phase completed           │
│  - Provides audit trail for all phase execution                         │
│                                                                          │
│  LAYER 2: External Validation Script (Blocking)                         │
│  - validate_phase_completion.py                                          │
│  - BLOCKS progression if previous phase incomplete                       │
│  - Exit codes: 0=proceed, 1=blocked, 2=error                            │
│  - Called at each phase transition                                       │
│                                                                          │
│  LAYER 3: Claude Code Hooks (Enforcement)                                │
│  - pre-phase-transition hook validates state file                        │
│  - post-subagent hook records invocations                                │
│  - HALTS workflow on missing phases                                      │
│  - External to Claude's decision-making                                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

Key Insight: Enforcement comes from EXTERNAL validation (Layers 1-3),
not from skill file structure. Single SKILL.md with validation calls
is simpler and equally effective.
```

---

## Features

### Feature 1: Phase State Tracking (Layer 1)
JSON state file created at workflow start, updated by each phase/subagent, validated before transitions.

**Stories:** STORY-148

### Feature 2: External Phase Validation (Layer 2)
Python validation scripts that BLOCK phase transitions with exit codes.

**Stories:** STORY-149

### Feature 3: Hook-Based Enforcement (Layer 3)
Pre-phase-transition and post-subagent hooks integrated with Claude Code.

**Stories:** STORY-150, STORY-151

### Feature 4: Skill Integration
Update devforgeai-development SKILL.md to add validation calls at each phase transition.

**Stories:** STORY-153

### Feature 5: Integration Testing
End-to-end validation that RCA-022 scenario is impossible.

**Stories:** STORY-154

---

## Story Breakdown

| Story ID | Title | Points | Priority | Depends On |
|----------|-------|--------|----------|------------|
| STORY-148 | Phase State File Module | 3 | P0 | - |
| STORY-149 | Phase Validation Script | 3 | P0 | STORY-148 |
| STORY-150 | Pre-Phase-Transition Hook | 2 | P0 | STORY-149 |
| STORY-151 | Post-Subagent Recording Hook | 2 | P0 | STORY-148 |
| STORY-153 | Skill Validation Integration | 3 | P1 | STORY-150, STORY-151 |
| STORY-154 | Integration Testing | 3 | P1 | STORY-153 |
| STORY-306 | Subagent Enforcement in Phase Completion | 3 | P0 | - |
| STORY-307 | Update Test Fixtures for Subagent Enforcement | 2 | P2 | STORY-306 |
| STORY-464 | Fix phase_check_command OR-Logic Crash | 3 | P0 | - |

**Total:** 22 story points (16 original + 3 for STORY-306 + 3 for STORY-464)

---

## Success Criteria

1. **Every `/dev` creates state file** - Verifiable artifact
2. **Every subagent invocation recorded** - Audit trail
3. **Phase transitions blocked if incomplete** - External enforcement via validation scripts
4. **Hooks enforce validation** - Pre-phase hooks check state before allowing progression
5. **RCA-022 scenario impossible** - External validation prevents phase skipping

---

## Confirmed Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Skill structure | **Single SKILL.md** | Simpler, Layer 4 removed - enforcement from external validation |
| Blocking strictness | HALT | Zero tolerance |
| State file cleanup | Archive to `completed/` | Audit trail |
| Implementation priority | Layers 1-3 | External enforcement sufficient |

---

## Related Documents

| Document | Path |
|----------|------|
| RCA-022 | `devforgeai/RCA/RCA-022-mandatory-tdd-phases-skipped.md` |
| Brainstorm | `devforgeai/specs/brainstorms/BRAINSTORM-002-phase-execution-enforcement.brainstorm.md` |
| Implementation Plan | `/home/bryan/.claude/plans/moonlit-meandering-bumblebee.md` |

---

## Progress Tracking

### Layer 1: State File Module
- [ ] STORY-148: Create `installer/phase_state.py`
- [ ] Structure validation (stdlib only)
- [ ] `devforgeai/workflows/` directory structure

### Layer 2: Validation Script
- [ ] STORY-149: Create validation CLI commands
- [ ] `devforgeai-validate phase-check`
- [ ] `devforgeai-validate record-subagent`
- [ ] `devforgeai-validate complete-phase`

### Layer 3: Hooks
- [ ] STORY-150: Pre-phase-transition hook
- [ ] STORY-151: Post-subagent recording hook
- [ ] Hook registration in hooks.yaml

### Skill Integration
- [ ] STORY-153: Add validation calls to devforgeai-development SKILL.md

### Integration Testing
- [ ] STORY-154: End-to-end testing
- [ ] RCA-022 scenario verification
