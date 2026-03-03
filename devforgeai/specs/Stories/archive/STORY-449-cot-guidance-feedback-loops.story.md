---
id: STORY-449
title: "Add Chain-of-Thought Guidance and Feedback Loops"
epic: EPIC-069
status: QA Approved
priority: Medium
points: 4
type: documentation
created: 2026-02-18
sprint: Sprint-3
---

# STORY-449: Add Chain-of-Thought Guidance and Feedback Loops

## Description

Add Chain-of-Thought (CoT) guidance and feedback loop patterns to the discovering-requirements skill per Anthropic best practices. This story addresses conformance findings:

- **3.1** (PARTIAL, Medium): Missing `<thinking>` tag instructions for complexity scoring
- **3.3** (PARTIAL, Low): No guided reasoning between discovery question batches
- **10.2** (PARTIAL, Medium): Success criteria not presented as live-updated checklist
- **10.3** (PARTIAL, Medium): Validate-halt pattern instead of validate-fix-repeat feedback loop

## Acceptance Criteria

<acceptance_criteria>

### AC#1: Complexity Assessment CoT Instructions

**Given** the complexity assessment workflow reference (new file or equivalent section)
**When** the agent performs multi-dimensional complexity scoring
**Then** the reference contains `<thinking>` tag instructions directing the agent to score each of 4 dimensions (scope, technical risk, integration surface, domain novelty) with explicit reasoning before presenting a conclusion.

**Files:** `src/claude/skills/discovering-requirements/references/discovery-workflow.md` (complexity assessment section, or new `complexity-assessment-workflow.md`)

### AC#2: Guided Reasoning Between Question Batches

**Given** the discovery-workflow.md reference file
**When** the agent transitions between question batches during requirements elicitation
**Then** a guided reasoning step is present: "Before asking the next question, think through what you've learned and identify the biggest remaining ambiguity."

**Files:** `src/claude/skills/discovering-requirements/references/discovery-workflow.md`

### AC#3: Live-Updated Success Criteria Checklist

**Given** the SKILL.md success criteria section
**When** the agent begins a discovering-requirements phase
**Then** the section is prefixed with: "Copy this checklist into your response at phase start. Update checkboxes as you complete each item:"

**Files:** `src/claude/skills/discovering-requirements/SKILL.md`

### AC#4: Validate-Fix-Repeat Feedback Loop

**Given** the completion-handoff.md reference (Phase 3.3)
**When** validation discovers fixable issues during handoff
**Then** the workflow implements a validate-fix-repeat loop: auto-fix where possible, re-validate, only halt on unfixable critical failures. Replaces the current validate-halt pattern.

**Files:** `src/claude/skills/discovering-requirements/references/completion-handoff.md`

</acceptance_criteria>

## Technical Specification

### Files to Modify

| File | Change |
|------|--------|
| `src/claude/skills/discovering-requirements/references/discovery-workflow.md` | Add `<thinking>` tag instructions for complexity scoring (AC#1); add guided reasoning step between question batches (AC#2) |
| `src/claude/skills/discovering-requirements/SKILL.md` | Prefix success criteria section with live-checklist instruction (AC#3) |
| `src/claude/skills/discovering-requirements/references/completion-handoff.md` | Replace validate-halt with validate-fix-repeat loop in Phase 3.3 (AC#4) |

### Notes

- AC#1: If no standalone `complexity-assessment-workflow.md` exists, add the CoT section directly to `discovery-workflow.md` under a new heading.
- AC#4: The feedback loop must still HALT on unfixable critical failures (e.g., missing required context files). Only auto-fixable issues (formatting, missing optional fields) should be retried.

## Definition of Done

- [x] `<thinking>` tag CoT instructions present for complexity scoring
- [x] Guided reasoning step added between question batches
- [x] Success criteria checklist instruction added to SKILL.md
- [x] Validate-fix-repeat feedback loop implemented in completion-handoff.md
- [x] All modified files pass markdown lint

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-18

- [x] `<thinking>` tag CoT instructions present for complexity scoring - Completed: Added Step 1.3.5 with 4-dimension scoring template in discovery-workflow.md
- [x] Guided reasoning step added between question batches - Completed: Added "Guided Reasoning Between Question Batches" section in discovery-workflow.md
- [x] Success criteria checklist instruction added to SKILL.md - Completed: Prefixed success criteria with live-checklist instruction
- [x] Validate-fix-repeat feedback loop implemented in completion-handoff.md - Completed: Added Step 3.3.5 with auto-fix/re-validate/HALT pattern
- [x] All modified files pass markdown lint - Completed: All 3 files validated, 13/13 tests pass

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Phase 02 (Red) | ✅ Complete | 13 tests generated, all failing |
| Phase 03 (Green) | ✅ Complete | 13/13 tests passing |
| Phase 04 (Refactor) | ✅ Complete | No refactoring needed |
| Phase 05 (Integration) | ✅ Complete | Cross-file consistency verified |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/discovering-requirements/references/discovery-workflow.md | Modified | +40 (CoT + guided reasoning) |
| src/claude/skills/discovering-requirements/SKILL.md | Modified | +2 (live-checklist instruction) |
| src/claude/skills/discovering-requirements/references/completion-handoff.md | Modified | +48 (validate-fix-repeat loop) |
| tests/STORY-449/test-story-449-cot-guidance.sh | Created | 113 (test suite) |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| YYYY-MM-DD HH:MM | .claude/story-requirements-analyst | Created | Story created | STORY-XXX.story.md |
| 2026-02-19 00:03 | claude/qa-result-interpreter | QA Deep | PASSED: 13/13 tests, 0 blocking violations | - |

---

## Notes
