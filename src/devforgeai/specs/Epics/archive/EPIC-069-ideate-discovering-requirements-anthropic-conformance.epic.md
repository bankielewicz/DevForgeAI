---
id: EPIC-069
title: "/ideate & discovering-requirements Anthropic Conformance Remediation (v2)"
status: Cancelled (superseded by EPIC-070)
start_date: 2026-02-18
target_date: 2026-03-18
total_points: 34
completed_points: 0
created: 2026-02-18
owner: DevForgeAI Framework Team
tech_lead: DevForgeAI AI Agent
team: DevForgeAI
source_analysis: src/devforgeai/specs/analysis/ideate-discovering-requirements-conformance-audit.md
supersedes: EPIC-067
---

# Epic: /ideate & discovering-requirements Anthropic Conformance Remediation (v2)

## Business Goal

Bring the `/ideate` command and `discovering-requirements` skill into full Anthropic conformance by remediating all 28 actionable findings from the 2026-02-18 audit. This supersedes EPIC-067 (which targeted 21 findings against the old `devforgeai-ideation` skill, now renamed).

**Problem:** The audit scored 10 categories: 3 FAIL (Role Definition, Examples/Multishot, Prompt Structure), 6 PARTIAL, 1 PASS. 14 findings persist from the prior audit (none were fixed during the rename). 17 new findings were identified. The `/ideate` command is the first skill new users encounter — non-conformance degrades discovery quality and wastes context tokens.

**Value:** Conformant skill improves Claude's requirements analysis accuracy, reduces context waste, ensures reliable inter-phase data flow, and aligns with platform vendor best practices.

**Source:** `src/devforgeai/specs/analysis/ideate-discovering-requirements-conformance-audit.md` (10/10 categories, 44 findings, 28 actionable)

## Success Metrics

- **Metric 1:** All 9 FAIL findings resolved and verified (from 9 to 0)
- **Metric 2:** All 23 PARTIAL findings resolved or deferred with ADR justification (target: ≤3 remaining PARTIAL)
- **Metric 3:** Re-audit shows 0 FAIL categories, ≤2 PARTIAL categories, ≥8 PASS categories
- **Metric 4:** No regression — all existing ideation workflows continue to work

**Measurement Plan:**
- Tracked via story completion in `devforgeai/specs/Stories/`
- Re-run conformance audit after Sprint 1 (high-priority) to validate progress
- Final re-audit after all features complete
- Review frequency: per-sprint

## Scope

### In Scope

7 features implementing 28 findings across 3 sprints, grouped by theme for efficient implementation.

**Primary files modified:**
- `src/claude/skills/discovering-requirements/SKILL.md` (339 lines)
- `src/claude/commands/ideate.md` (~567 lines)
- `src/claude/skills/discovering-requirements/references/` (25 files)
- `src/claude/skills/discovering-requirements/assets/templates/` (5 files)

### Out of Scope

- ❌ Skill functional changes (no new phases or capabilities)
- ❌ Other skill conformance (separate epics for /dev, /qa, etc.)
- ❌ Anthropic spec changes (we conform to current spec, not propose changes)
- ❌ Box-drawing character replacement (Finding 5.4 — acceptable for CLI display)

## Features

### Feature 1: Role Prompt & Identity (Findings 4.1, 4.2) — 3 pts
Add explicit role assignment per Anthropic `give-claude-a-role.md` guidance.

**Stories:**
- Add "You are an expert Product Manager and Requirements Analyst..." role section to SKILL.md after execution model
- Add orchestrator role context to ideate.md command

**Files:** SKILL.md, ideate.md
**Priority:** High (FAIL findings, highest impact on output quality)

### Feature 2: Multishot Examples & Quality Demos (Findings 5.1, 5.2, 5.5, 8.3 from prior) — 8 pts
Create input/output examples per Anthropic multishot guidance.

**Stories:**
- Create `references/examples.md` with 2-3 multishot examples (discovery session, epic decomposition, complexity scoring)
- Add completed example for output-templates.md (filled-in Completion Summary)
- Add usage examples to domain-specific-patterns.md
- Reference examples from SKILL.md phase instructions

**Files:** New `references/examples.md`, output-templates.md, domain-specific-patterns.md, SKILL.md
**Priority:** High (FAIL finding, dramatically improves consistency)

### Feature 3: XML Tag Structural Separation (Findings 5.3, 3.2, 6.3, 8.3) — 8 pts
Introduce XML tags for instruction structure, phase handoffs, and multi-source context per Anthropic `use-xml-tags.md`.

**Stories:**
- Wrap SKILL.md sections in `<instructions>`, `<context>`, `<output_format>` tags
- Define `<phase-N-output>` XML handoff schemas between phases
- Replace `**Business Idea:**` markdown markers with `<ideation-context>` XML tags in both command and skill
- Wrap multi-source inputs in `<brainstorm_context>`, `<user_input>`, `<project_context>` XML tags

**Files:** SKILL.md, ideate.md, discovery-workflow.md, requirements-elicitation-workflow.md
**Priority:** High (FAIL finding, reduces misinterpretation)

### Feature 4: YAML Frontmatter Compliance (Findings 1.1, 1.2, 1.3, 1.5, 7.5) — 3 pts
Fix allowed-tools format, tool names, and add metadata per Agent Skills spec.

**Stories:**
- Convert SKILL.md `allowed-tools` from YAML array to space-delimited string
- Replace `Bash(git:*)` with `Bash`, `Skill` with `Task`
- Fix ideate.md comma-delimited allowed-tools to space-delimited
- Add `metadata:` section (author, version, category) to SKILL.md
- Standardize `model` field across SKILL.md and ideate.md

**Files:** SKILL.md, ideate.md
**Priority:** Medium (FAIL findings but quick fixes — 30 min total)

### Feature 5: Command-Skill Separation Cleanup (Findings 8.1, 8.2) — 5 pts
Move business logic from command to skill references per lean orchestration.

**Stories:**
- Extract 175 lines of error handling from ideate.md to skill `references/command-error-handling.md`; replace with 5-line reference pointer
- Simplify Phase 0 brainstorm parsing — command passes file path, skill handles YAML extraction

**Files:** ideate.md, new `references/command-error-handling.md`, brainstorm-handoff-workflow.md
**Priority:** Medium (reduces command from ~567 to ~390 lines)

### Feature 6: Chain-of-Thought & Feedback Loops (Findings 3.1, 3.3, 10.2, 10.3) — 4 pts
Add CoT guidance and feedback loop patterns per Anthropic best practices.

**Stories:**
- Add `<thinking>` tag instructions for complexity scoring in complexity-assessment workflow
- Add guided reasoning step between question batches in discovery-workflow.md
- Add "Copy this checklist and track your progress" instruction to SKILL.md success criteria
- Convert validate-halt to validate-fix-repeat feedback loop in Phase 3.3

**Files:** complexity-assessment-workflow.md, discovery-workflow.md, SKILL.md, completion-handoff.md
**Priority:** Medium

### Feature 7: Cleanup & Consistency (Findings 9.1, 9.2, 9.5, 6.2, 1.4, 1.6, 10.5) — 3 pts
Remove duplicates, fix stale references, add TOCs.

**Stories:**
- Delete or thin-redirect `error-handling.md` (1063 lines duplicated by error-type-1 through error-type-6)
- Add missing error types 3 and 5 to SKILL.md error handling list
- Fix "Step 6.4" stale reference in self-validation-workflow.md to "Phase 3.3"
- Add TOC to large reference files (brainstorm-data-mapping.md, user-input-guidance.md, etc.)
- Standardize model field format across files
- Add error recovery conversation examples to user-interaction-patterns.md

**Files:** error-handling.md, SKILL.md, self-validation-workflow.md, multiple reference files
**Priority:** Low (housekeeping)

## Target Sprints

### Sprint 1: High-Impact Fixes (Features 1, 2, 4)
**Goal:** Resolve all 9 FAIL findings + YAML frontmatter
**Estimated Points:** 14
**Features:**
- Feature 1: Role Prompt (3 pts)
- Feature 2: Multishot Examples (8 pts)
- Feature 4: YAML Frontmatter (3 pts)

**Key Deliverables:**
- Role prompt in SKILL.md
- examples.md with 2-3 multishot examples
- Compliant YAML frontmatter in both files
- Mid-sprint re-audit checkpoint

### Sprint 2: Structural Improvements (Features 3, 5)
**Goal:** XML tags and command-skill separation
**Estimated Points:** 13
**Features:**
- Feature 3: XML Tag Separation (8 pts)
- Feature 5: Command-Skill Cleanup (5 pts)

**Key Deliverables:**
- XML-tagged sections in SKILL.md and ideate.md
- Error handling extracted from command to skill
- Command reduced to ~390 lines

### Sprint 3: Polish & Verification (Features 6, 7)
**Goal:** CoT patterns, cleanup, final re-audit
**Estimated Points:** 7
**Features:**
- Feature 6: CoT & Feedback Loops (4 pts)
- Feature 7: Cleanup & Consistency (3 pts)

**Key Deliverables:**
- Thinking tag guidance for complexity scoring
- Duplicate error-handling.md removed
- Final conformance re-audit showing ≥8 PASS categories

## User Stories

1. **As a** framework maintainer, **I want** the discovering-requirements skill to have an explicit expert role prompt, **so that** Claude produces domain-quality requirements analysis
2. **As a** framework maintainer, **I want** multishot examples for key skill outputs, **so that** Claude produces consistent, high-quality results
3. **As a** framework maintainer, **I want** XML tags separating instructions from context in the skill, **so that** Claude reliably parses phase boundaries
4. **As a** framework maintainer, **I want** compliant YAML frontmatter, **so that** the skill passes Agent Skills spec validators
5. **As a** framework maintainer, **I want** error handling moved from the command to the skill, **so that** the command follows lean orchestration principles
6. **As a** framework maintainer, **I want** chain-of-thought guidance for complexity scoring, **so that** Claude's scoring is transparent and debuggable
7. **As a** framework maintainer, **I want** duplicate reference files removed, **so that** maintenance burden is reduced and token waste eliminated

## Technical Considerations

### Architecture Impact
- No new services or components — all changes are prompt engineering edits to existing files
- XML tag introduction is additive (wraps existing content, doesn't replace it)
- Command-skill separation moves content between files but doesn't change behavior

### Technology Decisions
- No new technologies — all work is markdown/YAML editing
- XML tags follow Anthropic's documented patterns (not custom invention)

### Security & Compliance
- No security implications — prompt engineering changes only
- No data exposure changes

### Performance Requirements
- SKILL.md must remain under 500 lines after role prompt and XML tag additions (currently 339 — budget of 161 lines)
- Command must decrease in size (from ~567 to ~390 target)
- No new reference files beyond examples.md and command-error-handling.md

## Dependencies

### Internal Dependencies
- [x] **EPIC-065:** Skill gerund naming migration — Complete (discovering-requirements name is live)
- [x] **Conformance audit:** Complete (src/devforgeai/specs/analysis/ideate-discovering-requirements-conformance-audit.md)

### External Dependencies
- None

## Risks & Mitigation

### Risk 1: XML Tag Changes Break Context Marker Detection
- **Probability:** Medium
- **Impact:** High (skill fails to detect business idea from command)
- **Mitigation:** Update both command AND skill simultaneously in Feature 3. Test round-trip handoff.
- **Contingency:** Revert XML tags, keep markdown markers, document as deferred

### Risk 2: SKILL.md Exceeds 500 Lines After Additions
- **Probability:** Low (161-line budget available)
- **Impact:** Medium (performance degradation)
- **Mitigation:** Role prompt ~10 lines, XML tags ~20 lines, checklist instruction ~2 lines. Total ~32 lines → 371 lines (well under)
- **Contingency:** Move any excess to reference files

## Stakeholders

### Primary Stakeholders
- **Product Owner:** DevForgeAI Framework Team
- **Tech Lead:** DevForgeAI AI Agent

## Communication Plan

### Status Updates
- **Frequency:** Per sprint
- **Format:** Story completion tracking
- **Audience:** Framework team

## Timeline

```
Epic Timeline:
════════════════════════════════════════════════════
Week 1-2:  Sprint 1 - Role prompt, examples, YAML (14 pts)
Week 3-4:  Sprint 2 - XML tags, command cleanup (13 pts)
Week 5:    Sprint 3 - CoT, cleanup, re-audit (7 pts)
════════════════════════════════════════════════════
Total Duration: 5 weeks
Total Points: 34
Target Release: 2026-03-18
```

### Key Milestones
- [ ] **Milestone 1:** End Sprint 1 — All FAIL findings resolved, mid-audit checkpoint
- [ ] **Milestone 2:** End Sprint 2 — XML structural separation complete
- [ ] **Milestone 3:** End Sprint 3 — Final re-audit ≥8 PASS categories

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 14 | 3 (STORY-444, 445, 446) | 0 | 0 | 0 |
| Sprint 2 | Not Started | 13 | 2 (STORY-447, 448) | 0 | 0 | 0 |
| Sprint 3 | Not Started | 7 | 2 (STORY-449, 450) | 0 | 0 | 0 |
| **Total** | **0%** | **34** | **7** | **0** | **0** | **0** |

### Burndown
- **Total Points:** 34
- **Completed:** 0
- **Remaining:** 34

## Supersedes

**EPIC-067** (`/ideate Command & devforgeai-ideation Skill Anthropic Conformance Remediation`) is superseded by this epic. Reasons:
- EPIC-067 targeted 21 findings against the old `devforgeai-ideation` skill (now renamed)
- This epic targets 28 actionable findings from a comprehensive 10-category audit against the renamed `discovering-requirements` skill
- 3 findings from the prior audit are RESOLVED (gerund naming, vendor prefix, line count)
- 14 findings PERSIST and 17 are NEW
- EPIC-067 should be marked `Cancelled (superseded by EPIC-069)`

## Retrospective (Post-Epic)

*To be completed after epic completes*

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-18
