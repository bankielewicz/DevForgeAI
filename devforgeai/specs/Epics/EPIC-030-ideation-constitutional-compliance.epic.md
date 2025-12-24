---
id: EPIC-030
title: Ideation Constitutional Compliance & Documentation
business-value: Fix critical constitutional violations and improve reference file maintainability
status: Planning
priority: High
complexity-score: 37
architecture-tier: Tier 3
created: 2025-12-22
estimated-points: 15-20
target-sprints: 1-2
source-brainstorm: BRAINSTORM-001
dependencies: []  # Can run in parallel with EPIC-028 and EPIC-029
---

# EPIC-030: Ideation Constitutional Compliance & Documentation

## Business Goal

Fix critical constitutional violations (Bash used for file operations, missing documentation) and improve reference file maintainability by splitting oversized files and eliminating structural debt. Ensure all ideation workflows comply with DevForgeAI's 6 context files.

**Success Metrics:**
- Zero constitutional violations (Bash file operations eliminated)
- user-input-guidance.md documented in SKILL.md (S2 fixed)
- error-handling.md split from 1,062 lines to 6 files (each <250 lines)
- TodoWrite enforced in all 6 phases (100% compliance)
- All orphaned files integrated or removed (clean codebase)

## Features

### Feature 1: Replace Bash mkdir with Write/.gitkeep
**Description:** Fix C1 constitutional violation - use Write tool instead of Bash for directory creation

**User Stories (high-level):**
1. As a framework maintainer, I want ideation to comply with anti-patterns.md (no Bash for file operations)
2. As a user, I want consistent file operation behavior (Write tool for all creates)
3. As a code reviewer, I want constitutional compliance to pass before merging

**Implementation:**
- **Current violation:** Command or skill uses `Bash(command="mkdir -p devforgeai/specs/Epics")`
- **Fix:** Use `Write(file_path="devforgeai/specs/Epics/.gitkeep", content="")`
- **Locations to check:**
  - .claude/commands/ideate.md (Phase 0, 6)
  - .claude/skills/devforgeai-ideation/SKILL.md (Phase 6)
  - artifact-generation.md reference file
- **Validation:** Grep for `Bash.*mkdir` in ideation files, assert zero matches

**Estimated Effort:** Small (3 points)

---

### Feature 2: Document user-input-guidance.md in SKILL.md
**Description:** Fix S2 critical issue - add index section to SKILL.md referencing user-input-guidance.md patterns

**User Stories (high-level):**
1. As a developer using ideation skill, I want to know when to load user-input-guidance.md
2. As a framework maintainer, I want all reference files documented in SKILL.md
3. As a new contributor, I want clear documentation of what each reference file provides

**Implementation:**
- Add to SKILL.md "Reference Files" section:
  ```markdown
  ### User Input Patterns (NEW - loaded in Phase 2 Step 0.5)
  - **user-input-guidance.md** - Framework-internal guidance for eliciting complete requirements (898 lines)
    - 15 elicitation patterns across 5 categories (Functional, NFR, Edge Cases, Integration, Constraints)
    - 28 AskUserQuestion templates (copy-paste ready)
    - NFR quantification table (maps vague terms like "fast" to metrics)
    - Integration guide for 5 skills (ideation, story-creation, architecture, ui-generator, orchestration)
  ```
- Add cross-reference in Phase 2 workflow section:
  ```markdown
  **Step 0.5 - Load User Input Patterns (Error-Tolerant):**
  Before proceeding with discovery questions, attempt to load guidance patterns:
  `Read(file_path=".claude/skills/devforgeai-ideation/references/user-input-guidance.md")`
  ```

**Estimated Effort:** Small (2 points)

---

### Feature 3: Integrate or Remove Orphaned Files
**Description:** Fix S3 issue - review orphaned files (user-input-integration-guide.md, brainstorm-data-mapping.md), integrate if valuable, remove if redundant

**User Stories (high-level):**
1. As a framework maintainer, I want a clean codebase without orphaned files
2. As a developer, I want valuable content integrated into workflow files
3. As a code reviewer, I want clear justification for every file in the repository

**Implementation:**
- **Review process:**
  1. Read each orphaned file
  2. Check if content is referenced anywhere (Grep for filename)
  3. Assess value: Does it provide guidance not found elsewhere?
  4. Decision:
     - **If valuable:** Integrate into relevant workflow file (e.g., merge user-input-integration-guide.md into user-input-guidance.md Section 5)
     - **If redundant:** Delete file, document reason in commit message
     - **If unclear:** Time-box review to 30 minutes, default to delete
- **Files to review:**
  - user-input-integration-guide.md (likely redundant with user-input-guidance.md)
  - brainstorm-data-mapping.md (likely integrated into brainstorm-handoff-workflow.md)

**Estimated Effort:** Small (3 points)

---

### Feature 4: Split error-handling.md into 6 Error-Type Files
**Description:** Fix S1 issue - split 1,062-line error-handling.md into 6 files organized by error type (target: each <250 lines)

**User Stories (high-level):**
1. As a developer debugging errors, I want to load ONLY the error type I'm handling (token efficiency)
2. As a framework maintainer, I want manageable file sizes (<800 lines per target)
3. As a code reviewer, I want clear file organization by error category

**Implementation:**
- **New file structure:**
  1. `error-type-1-incomplete-answers.md` (~180 lines)
  2. `error-type-2-artifact-failures.md` (~200 lines)
  3. `error-type-3-complexity-errors.md` (~150 lines)
  4. `error-type-4-validation-failures.md` (~180 lines)
  5. `error-type-5-constraint-conflicts.md` (~170 lines)
  6. `error-type-6-directory-issues.md` (~180 lines)
- **Each file contains:**
  - Error detection logic (when does this error occur?)
  - Recovery procedures (self-heal → retry → report)
  - Example scenarios
  - Related patterns (cross-reference to other error types if needed)
- **Update references:**
  - SKILL.md "Error Handling" section: List all 6 files instead of 1
  - Workflow files: Load specific error file when needed (e.g., Phase 2 loads incomplete-answers.md)
- **Master index:** Create `error-handling-index.md` with decision tree: "Which error type am I experiencing?"

**Estimated Effort:** Medium (6 points)

---

### Feature 5: Enforce TodoWrite in All 6 Phases
**Description:** Fix W4 issue - add TodoWrite enforcement to phases that currently skip it (1, 3, 5)

**User Stories (high-level):**
1. As a user, I want consistent progress tracking across all ideation phases
2. As a framework maintainer, I want checkpoints to benefit from TodoWrite metadata
3. As a developer, I want clear phase completion status for debugging

**Implementation:**
- **Add TodoWrite to Phase 1 (Discovery):**
  ```markdown
  At Phase 1 start:
  TodoWrite([
    {"content": "Phase 1: Discovery & Problem Understanding", "status": "in_progress", "activeForm": "Discovering problem space"}
  ])

  At Phase 1 end:
  Mark Phase 1 todo as completed
  ```
- **Add TodoWrite to Phase 3 (Complexity Assessment):**
  ```markdown
  At Phase 3 start:
  TodoWrite([
    {"content": "Phase 3: Complexity Assessment", "status": "in_progress", "activeForm": "Calculating complexity score"}
  ])

  At Phase 3 end:
  Mark Phase 3 todo as completed, display score
  ```
- **Add TodoWrite to Phase 5 (Feasibility):**
  ```markdown
  At Phase 5 start:
  TodoWrite([
    {"content": "Phase 5: Feasibility & Constraints Analysis", "status": "in_progress", "activeForm": "Analyzing constraints"}
  ])

  At Phase 5 end:
  Mark Phase 5 todo as completed
  ```
- **Update workflow files:** discovery-workflow.md, complexity-assessment-workflow.md, feasibility-analysis-workflow.md

**Estimated Effort:** Small (3 points)

---

### Feature 6: Keep Separate Tech Recommendation Files with Smart Referencing
**Description:** Fix D2 issue - maintain 3 separate files for tech recommendations, add cross-references to eliminate duplication

**User Stories (high-level):**
1. As a developer in Phase 3, I want detailed tech recommendations for my complexity tier
2. As a developer in Phase 6, I want brief summary of recommended technologies (not full details)
3. As a framework maintainer, I want single source of truth for tier-specific recommendations

**Implementation:**
- **Keep files:**
  1. `complexity-assessment-matrix.md` - Full tech recommendations per tier (authoritative source)
  2. `output-templates.md` - Brief summary templates (references matrix)
  3. `completion-handoff.md` - Next-step guidance (references matrix)
- **Add smart referencing:**
  - In output-templates.md:
    ```markdown
    **Technology Recommendations:**
    {Brief summary from complexity-assessment-matrix.md lines X-Y}
    For full details, see: complexity-assessment-matrix.md Section {tier}
    ```
  - In completion-handoff.md:
    ```markdown
    **Recommended Next Steps:**
    1. Review technology recommendations in complexity-assessment-matrix.md (Tier {N})
    2. Run `/create-context` to create 6 context files
    ```
- **Eliminate duplication:** Remove redundant tech lists from output-templates.md and completion-handoff.md, replace with references

**Estimated Effort:** Small (3 points)

---

## Requirements Summary

### Functional Requirements
- Bash file operations replaced with Write tool
- user-input-guidance.md documented in SKILL.md
- Orphaned files integrated or removed
- error-handling.md split into 6 error-type files
- TodoWrite enforced in phases 1, 3, 5
- Tech recommendations cross-referenced (not duplicated)

### Data Model
**Entities:**
- Command/skill files: Updated for constitutional compliance
- Reference files: Reorganized (6 error files, cross-referenced tech recs)
- Documentation: SKILL.md updated with user-input-guidance index

**Relationships:**
- SKILL.md → Reference files (documents all 16 files)
- Error workflow files → Error-type files (load specific type)
- Output templates → complexity-assessment-matrix.md (references)

### Integration Points
1. **File operations:** Write tool for directory creation (no Bash)
2. **Documentation:** SKILL.md cross-references to all reference files
3. **Error handling:** Load error-type files on-demand

### Non-Functional Requirements

**Constitutional Compliance:**
- Zero Bash file operations (anti-patterns.md)
- All reference files documented (coding-standards.md)
- File sizes ≤800 lines target (maintainability)

**Maintainability:**
- Error files <250 lines each (easier to maintain)
- Cross-references reduce duplication (DRY principle)
- Clear file organization (by error type, by workflow phase)

## Architecture Considerations

**Complexity Tier:** Tier 3 (Complex System)

**Recommended Architecture:**
- **Pattern:** Documentation-Driven (clear index, progressive disclosure)
- **Layers:** Master index (SKILL.md), Workflow files (phase references), Detail files (error types, tech recs)
- **Organization:** By concern (errors by type, not by phase)

**Technology Recommendations:**
- Markdown for all documentation (existing)
- Cross-references using relative links (e.g., `[Details](error-type-1-incomplete-answers.md)`)

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Content loss during error-handling.md split | MEDIUM | Validate all 1,062 lines accounted for in 6 new files (line count check) |
| Broken cross-references after file split | LOW | Test all links, validate references resolve |
| TodoWrite enforcement adds token overhead | LOW | Phases 1, 3, 5 are short-lived (5-15 minutes), minimal overhead |
| Orphaned file content is valuable but deleted | LOW | Time-box review to 30 minutes, default to integrate if unclear |
| Write/.gitkeep creates commit noise | LOW | Acceptable trade-off for constitutional compliance |

## Dependencies

**Prerequisites:**
- None (this epic can run in parallel with EPIC-028 and EPIC-029)

**Dependents:**
- None (other epics don't depend on compliance fixes)

## Next Steps

1. **Implementation Order:**
   - Feature 1 (Bash→Write) first - critical constitutional fix
   - Feature 2 (document user-input-guidance) second - critical documentation fix
   - Feature 4 (split error-handling.md) third - enables cleaner error handling in EPIC-029
   - Features 3, 5, 6 (orphaned files, TodoWrite, cross-refs) - can run in parallel
2. **Testing:** Validate no Bash file operations remain (Grep check), all cross-references resolve
3. **Documentation:** Update devforgeai/FRAMEWORK-STATUS.md to reflect constitutional compliance

## Stories

| Story ID | Feature | Title | Status | Points |
|----------|---------|-------|--------|--------|
| STORY-142 | Feature 1 | Replace Bash mkdir with Write/.gitkeep Pattern | Backlog | 3 |
| STORY-143 | Feature 2 | Document user-input-guidance.md in SKILL.md | Backlog | 2 |
| STORY-144 | Feature 3 | Integrate or Remove Orphaned Files | Backlog | 3 |
| STORY-145 | Feature 4 | Split error-handling.md into 6 Error-Type Files | Backlog | 6 |
| STORY-146 | Feature 5 | Enforce TodoWrite in All 6 Phases | Backlog | 3 |
| STORY-147 | Feature 6 | Keep Separate Tech Recommendation Files with Smart Referencing | Backlog | 3 |

**Total Points:** 20

---

**Created from:** BRAINSTORM-001 (HIGH confidence)
**Related Stories:** See Stories table above
