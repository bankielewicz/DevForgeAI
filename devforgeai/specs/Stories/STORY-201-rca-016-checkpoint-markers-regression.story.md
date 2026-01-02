---
id: STORY-201
title: Re-implement RCA-016 REC-1 Checkpoint Markers for 5-Phase Structure
type: fix
epic: EPIC-033
priority: CRITICAL
points: 3
status: Backlog
created: 2025-01-01
source: RCA-016 Regression Record
depends_on: []
---

# STORY-201: Re-implement RCA-016 REC-1 Checkpoint Markers for 5-Phase Structure

## User Story

**As a** DevForgeAI user running QA validation,
**I want** mandatory reference loading checkpoints enforced before each phase,
**So that** phase skipping (the RCA-016 root cause) cannot occur in the new 5-phase structure.

## Background

RCA-016 (QA Skill Phase Skipping During Deep Validation) was implemented on 2025-12-01 with:
- ⚠️ CHECKPOINT markers before Phases 2, 3, 4, 6, 7
- Explicit "Load reference file (REQUIRED)" instructions
- Clarified "on-demand" language (REC-4)

However, a later skill refactoring restructured devforgeai-qa from 7 phases to 5 phases, and the checkpoint enforcement was **not preserved**. This story re-implements REC-1 for the current structure.

**Source RCA:** `devforgeai/RCA/RCA-016-qa-skill-phase-skipping-during-deep-validation.md`

**Git Evidence:**
- Commit 3654474c implemented REC-1 (2025-12-01)
- Later commits restructured skill, losing the fixes
- Current SKILL.md has 5 phases (0-4) without CHECKPOINT markers

## Acceptance Criteria

### AC-1: CHECKPOINT Marker Before Each Phase (1-4)

**Given** the devforgeai-qa skill with 5-phase structure
**When** a phase with reference files is about to execute
**Then** a ⚠️ CHECKPOINT marker exists before the phase content

**Phases requiring CHECKPOINT:**
- Phase 1: Validation (has `traceability-validation-algorithm.md`)
- Phase 2: Analysis (has `anti-pattern-detection-workflow.md`, `parallel-validation.md`, `spec-compliance-workflow.md`, `code-quality-workflow.md`)
- Phase 3: Reporting (has `qa-result-formatting.md`)
- Phase 4: Cleanup (has cleanup workflow)

---

### AC-2: Explicit Reference Loading Requirement

**Given** a phase has a CHECKPOINT marker
**When** Claude reads the CHECKPOINT
**Then** the text includes:
- "You MUST execute ALL steps before proceeding"
- "Step X.0: Load Workflow Reference (REQUIRED)"
- Actual `Read(file_path="...")` command for the reference file
- "Execute ALL steps from the reference file"

---

### AC-3: Clarified Progressive Disclosure Language (REC-4)

**Given** the "QA Workflow (5 Phases)" section introduction
**When** Claude reads the workflow description
**Then** the text explicitly states:
- "On-demand means load when phase starts - NOT loading is optional"
- "IF you skip loading a reference: You will execute the phase incorrectly"

---

### AC-4: Phase Pre-Flight Validation Enhanced

**Given** the existing Phase Pre-Flight markers (check previous phase marker)
**When** enhanced with CHECKPOINT requirements
**Then** the Pre-Flight section includes:
- Previous phase marker check (existing)
- Reference file loading requirement (new)
- Cannot proceed without both checks passing

---

### AC-5: Backward Compatibility with Phase Marker System

**Given** the current Phase Marker Write system is preserved
**When** CHECKPOINT markers are added
**Then** both systems work together:
- CHECKPOINT enforces reference loading at phase start
- Phase Marker Write confirms phase completion
- Pre-Flight checks both previous marker AND reference loading

## Technical Specification

### Files to Modify

| File | Change Type | Description |
|------|-------------|-------------|
| `.claude/skills/devforgeai-qa/SKILL.md` | Modify | Add CHECKPOINT markers to Phases 1-4 |

### CHECKPOINT Pattern Template

Add before each phase section (after Pre-Flight check):

```markdown
### ⚠️ CHECKPOINT: Phase {N} Reference Loading [MANDATORY]

**You MUST execute ALL steps before proceeding to phase content.**

**Step {N}.0: Load Workflow Reference (REQUIRED)**
```
Read(file_path=".claude/skills/devforgeai-qa/references/{reference-file}.md")
```

**This reference contains the complete workflow. Execute ALL steps from the reference file.**

**After loading:** Proceed to Step {N}.1 (in reference file)

**IF you skip this step:** You will execute the phase incorrectly and miss mandatory steps.
```

### Phase-to-Reference Mapping

| Phase | Reference File(s) |
|-------|-------------------|
| Phase 1 | `traceability-validation-algorithm.md` |
| Phase 2 | `anti-pattern-detection-workflow.md`, `parallel-validation.md`, `spec-compliance-workflow.md`, `code-quality-workflow.md` |
| Phase 3 | `qa-result-formatting.md` |
| Phase 4 | (cleanup steps inline, but marker system documented) |

### Workflow Introduction Update (REC-4)

Update line ~77-86 in SKILL.md:

```markdown
## QA Workflow (5 Phases)

**EXECUTION STARTS HERE - You are now executing the skill's workflow.**

**Progressive Disclosure:** Workflow references are loaded when each phase executes (not before) to optimize token usage.

**IMPORTANT:** "On-demand" means "load when phase starts" - NOT "loading is optional."

**Execution Pattern:**
1. Reach phase (e.g., Phase 2: Analysis)
2. See "⚠️ CHECKPOINT" marker
3. Load reference file (REQUIRED)
4. Execute ALL steps from reference file
5. Complete phase marker write
6. Proceed to next phase

**IF you skip loading a reference:** You will execute the phase incorrectly and miss mandatory steps.
```

## Definition of Done

### Implementation
- [ ] ⚠️ CHECKPOINT marker added before Phase 1 (Validation)
- [ ] ⚠️ CHECKPOINT marker added before Phase 2 (Analysis)
- [ ] ⚠️ CHECKPOINT marker added before Phase 3 (Reporting)
- [ ] ⚠️ CHECKPOINT marker added before Phase 4 (Cleanup)
- [ ] "On-demand" clarification language added (REC-4)
- [ ] Reference file paths verified (files exist)

### Testing
- [ ] Run `/qa STORY-001 deep` and verify CHECKPOINT markers visible
- [ ] Verify reference files are Read() during execution
- [ ] Verify no phase skipping occurs

### Documentation
- [ ] Update RCA-016 regression record with implementation status

## Effort Estimate

- **Points:** 3
- **Estimated Hours:** 2-3 hours
  - Add CHECKPOINT markers: 1.5 hours
  - Update workflow introduction: 30 minutes
  - Testing: 1 hour

## Related

- **RCA:** RCA-016-qa-skill-phase-skipping-during-deep-validation.md
- **Original Implementation:** Commit 3654474c (2025-12-01)
- **Related Stories:** STORY-202 (REC-2 Completion Checklists)

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-01-01 | claude/opus | Story created from RCA-016 regression discovery |
