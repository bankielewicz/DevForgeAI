---
id: STORY-453
title: "Flatten Nested Reference Chains"
type: documentation
epic: EPIC-070
sprint: Sprint-14
status: QA Approved
points: 3
depends_on: ["STORY-452"]
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-02-19
format_version: "2.9"
---

# Story: Flatten Nested Reference Chains

## Description

**As a** framework maintainer,
**I want** all reference file chains flattened to one-level-deep by adding direct Read() load instructions in SKILL.md for each chained target file,
**so that** Claude reads complete reference files instead of partial previews during discovering-requirements skill execution, eliminating the 6 two-level-deep chains that violate Anthropic's one-level-deep rule.

## Provenance

```xml
<provenance>
  <origin document="discovering-requirements-conformance-analysis.md" section="Category 3 — Progressive Disclosure">
    <quote>"Multiple reference files chain to other reference files (ref-A → ref-B pattern)... This creates 2-level-deep reference chains that may cause Claude to use head -100 preview reads instead of full reads, resulting in incomplete information."</quote>
    <line_reference>lines 181-206</line_reference>
    <quantified_impact>6 reference chains violate Anthropic's one-level-deep rule; Claude may silently fail to read chained files completely</quantified_impact>
  </origin>

  <decision rationale="option-a-direct-loads-no-merges">
    <selected>Option A: Add direct Read() instructions in SKILL.md phase sections for each chained target file, then remove redundant chained Read() from source reference files. No file merges.</selected>
    <rejected alternative="option-b-merge-file-pairs">
      Merging file pairs creates large files (879-1027 lines) and invalidates existing STORY-450 file targets.
    </rejected>
    <trade_off>Option A adds ~6 lines to SKILL.md (407→~413) but preserves all existing file targets and is fully reversible.</trade_off>
  </decision>

  <stakeholder role="Framework Maintainer" goal="conformance-remediation">
    <quote>"Keep references one level deep from SKILL.md."</quote>
    <source>Anthropic best-practices.md lines 345-371</source>
  </stakeholder>
</provenance>
```

## Acceptance Criteria

### AC#1: All 6 Chains Flattened — Direct Load Instructions Added to SKILL.md

```xml
<acceptance_criteria id="AC1">
  <given>SKILL.md currently loads 6 reference files that internally chain to other reference files, creating 2-level-deep chains: self-validation-workflow→validation-checklists, requirements-elicitation-workflow→requirements-elicitation-guide, user-input-integration-guide→user-input-guidance, error-type-1→requirements-elicitation-guide, error-type-3→complexity-assessment-matrix, error-type-4→validation-checklists</given>
  <when>Direct Read() instructions are added to SKILL.md in the appropriate phase sections for each chained target file</when>
  <then>SKILL.md contains direct Read() calls for: validation-checklists.md (Phase 3.3), requirements-elicitation-guide.md (Phase 2), and the cross-skill reference is resolved per AC3. Each Read() is placed within its relevant phase section (not a single upfront block). SKILL.md line count remains under 500 lines. user-input-guidance.md is confirmed already loaded in Step 0.5 (no change needed).</then>
  <verification>
    <source_files>
      <file hint="Skill main file">.claude/skills/discovering-requirements/SKILL.md</file>
    </source_files>
    <test_file>tests/results/STORY-453/ac1-skill-direct-loads-verification.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Redundant Chained Read() Calls Removed from Source Reference Files

```xml
<acceptance_criteria id="AC2">
  <given>6 source reference files contain Read() calls that chain to other reference files: self-validation-workflow.md loads validation-checklists.md, requirements-elicitation-workflow.md loads requirements-elicitation-guide.md, user-input-integration-guide.md loads user-input-guidance.md, error-type-1 loads requirements-elicitation-guide.md, error-type-3 loads complexity-assessment-matrix.md, error-type-4 loads validation-checklists.md</given>
  <when>Each source reference file is edited to remove the specific chained Read() call after SKILL.md has been updated with direct loads</when>
  <then>Each of the 6 source files no longer contains the executable Read() call that created the chain. Prose mentions of the chained file may remain as documentation. No other Read() calls or content are removed. No new chains introduced.</then>
  <verification>
    <source_files>
      <file hint="Chain source 1">.claude/skills/discovering-requirements/references/self-validation-workflow.md</file>
      <file hint="Chain source 2">.claude/skills/discovering-requirements/references/requirements-elicitation-workflow.md</file>
      <file hint="Chain source 3">.claude/skills/discovering-requirements/references/user-input-integration-guide.md</file>
      <file hint="Chain source 4">.claude/skills/discovering-requirements/references/error-type-1-incomplete-answers.md</file>
      <file hint="Chain source 5">.claude/skills/discovering-requirements/references/error-type-3-complexity-errors.md</file>
      <file hint="Chain source 6">.claude/skills/discovering-requirements/references/error-type-4-validation-failures.md</file>
    </source_files>
    <test_file>tests/results/STORY-453/ac2-redundant-reads-removed-verification.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Cross-Skill Reference in error-type-3 Resolved and Documented

```xml
<acceptance_criteria id="AC3">
  <given>error-type-3-complexity-errors.md references complexity-assessment-matrix.md which resides in the designing-systems skill directory (.claude/skills/designing-systems/references/), creating a cross-skill dependency; complexity scoring was removed from this skill during the devforgeai-ideation→discovering-requirements refactor</given>
  <when>The implementer evaluates whether the cross-skill reference is intentional or stale</when>
  <then>One outcome is implemented: (a) if intentional — SKILL.md includes cross-skill Read() with inline comment, or (b) if stale — the Read() is removed from error-type-3 and the decision is documented in story Notes section</then>
  <verification>
    <source_files>
      <file hint="Cross-skill reference file">.claude/skills/discovering-requirements/references/error-type-3-complexity-errors.md</file>
      <file hint="Designing-systems target">.claude/skills/designing-systems/references/complexity-assessment-matrix.md</file>
      <file hint="SKILL.md">.claude/skills/discovering-requirements/SKILL.md</file>
    </source_files>
    <test_file>tests/results/STORY-453/ac3-cross-skill-reference-resolution-verification.md</test_file>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "SKILL.md Phase 2 Direct Load"
      file_path: ".claude/skills/discovering-requirements/SKILL.md"
      required_keys:
        - key: "Phase 2 requirements-elicitation-guide.md load"
          type: "string"
          required: true
          validation: "Must appear in Phase 2 section after requirements-elicitation-workflow.md load"
          test_requirement: "Test: Grep SKILL.md for requirements-elicitation-guide.md Read() in Phase 2"

    - type: "Configuration"
      name: "SKILL.md Phase 3.3 Direct Load"
      file_path: ".claude/skills/discovering-requirements/SKILL.md"
      required_keys:
        - key: "Phase 3.3 validation-checklists.md load"
          type: "string"
          required: true
          validation: "Must appear in Phase 3 self-validation section"
          test_requirement: "Test: Grep SKILL.md for validation-checklists.md Read() in Phase 3"

    - type: "Configuration"
      name: "6 Source Reference Files — Remove Chained Reads"
      file_path: ".claude/skills/discovering-requirements/references/"
      required_keys:
        - key: "self-validation-workflow.md chained Read()"
          type: "string"
          required: true
          validation: "File must not contain executable Read() for validation-checklists.md"
          test_requirement: "Test: Grep returns zero matches for Read.*validation-checklists"
        - key: "requirements-elicitation-workflow.md chained Read()"
          type: "string"
          required: true
          validation: "File must not contain executable Read() for requirements-elicitation-guide.md"
          test_requirement: "Test: Grep returns zero matches"
        - key: "user-input-integration-guide.md chained Read()"
          type: "string"
          required: true
          validation: "File must not contain executable Read() for user-input-guidance.md"
          test_requirement: "Test: Grep returns zero matches"
        - key: "error-type-1 chained Read()"
          type: "string"
          required: true
          validation: "Must not contain executable Read() for requirements-elicitation-guide.md"
          test_requirement: "Test: Grep returns zero matches"
        - key: "error-type-3 chained Read()"
          type: "string"
          required: true
          validation: "Executable Read() for complexity-assessment-matrix.md removed regardless of AC3 decision"
          test_requirement: "Test: Grep returns zero executable Read() matches"
        - key: "error-type-4 chained Read()"
          type: "string"
          required: true
          validation: "Must not contain executable Read() for validation-checklists.md"
          test_requirement: "Test: Grep returns zero matches"

  business_rules:
    - id: "BR-001"
      rule: "All reference files must be reachable via single-level Read() from SKILL.md. No reference file may chain-load another reference file."
      trigger: "Any modification to SKILL.md loading or reference file content"
      validation: "Grep all reference files for Read() targeting other reference files — zero matches"
      error_handling: "Chain found → flatten before story completion"
      test_requirement: "Test: Grep all 25 reference files for inter-reference Read() returns zero"
      priority: "Critical"

    - id: "BR-002"
      rule: "Cross-skill references require explicit documentation of intentionality"
      trigger: "Any Read() in SKILL.md pointing outside discovering-requirements"
      validation: "Notes section documents decision; inline comment in SKILL.md explains dependency"
      error_handling: "Undocumented cross-skill reference → treat as stale and remove"
      test_requirement: "Test: Cross-skill Read() has inline comment or is removed"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "SKILL.md must remain under 500 lines after all additions"
      metric: "SKILL.md <= 500 lines (baseline 407, adding ~6-12 lines → ~413-420)"
      test_requirement: "Test: wc -l SKILL.md returns <= 500"
      priority: "High"

    - id: "NFR-002"
      category: "Reliability"
      requirement: "No existing reference file content altered beyond targeted Read() removals"
      metric: "git diff for each file shows only targeted Read() removal lines"
      test_requirement: "Test: git diff scoped to targeted lines only"
      priority: "Critical"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "complexity-assessment-matrix.md (cross-skill)"
    limitation: "File lives in designing-systems skill. Whether discovering-requirements should depend on it requires understanding if complexity scoring is still used during error recovery."
    decision: "pending"
    discovered_phase: "Architecture"
    impact: "AC3 resolution depends on this decision. Preliminary assessment: likely stale since complexity scoring was removed from this skill."
```

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-452:** Portability Fix — Remove Hardcoded WSL Path
  - **Why:** Clarifies user-input-integration-guide → user-input-guidance chain intent before flattening
  - **Status:** Not Started

### External Dependencies

- None.

### Technology Dependencies

- None.

---

## Test Strategy

### Unit Tests

**Coverage Target:** N/A (documentation story)

**Test Scenarios:**
1. All 6 chained Read() calls absent from source reference files (grep verification)
2. All required direct Read() calls present in SKILL.md phase sections
3. No other Read() calls removed (git diff review)
4. user-input-guidance.md not double-loaded (exactly 1 Read() in Step 0.5)
5. SKILL.md line count <= 500
6. No new 2-level chains introduced (grep all 25 reference files)

---

## Acceptance Criteria Verification Checklist

### AC#1: Direct Loads Added to SKILL.md

- [ ] Read() for requirements-elicitation-guide.md in Phase 2 — **Phase:** 3 — **Evidence:** SKILL.md
- [ ] Read() for validation-checklists.md in Phase 3.3 — **Phase:** 3 — **Evidence:** SKILL.md
- [ ] Cross-skill reference resolved per AC3 — **Phase:** 3 — **Evidence:** SKILL.md + Notes
- [ ] user-input-guidance.md confirmed in Step 0.5 — **Phase:** 1 — **Evidence:** SKILL.md
- [ ] SKILL.md <= 500 lines — **Phase:** 3 — **Evidence:** wc -l

### AC#2: Chained Reads Removed

- [ ] self-validation-workflow.md — chained Read() removed — **Phase:** 3
- [ ] requirements-elicitation-workflow.md — chained Read() removed — **Phase:** 3
- [ ] user-input-integration-guide.md — chained Read() removed — **Phase:** 3
- [ ] error-type-1 — chained Read() removed — **Phase:** 3
- [ ] error-type-4 — chained Read() removed — **Phase:** 3
- [ ] No other content removed (git diff review) — **Phase:** 4

### AC#3: Cross-Skill Reference Resolved

- [ ] Decision made: intentional or stale — **Phase:** 1 — **Evidence:** Notes section
- [ ] error-type-3 executable Read() removed — **Phase:** 3
- [ ] Decision documented with rationale — **Phase:** 3

---

**Checklist Progress:** 0/14 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers (like "### Definition of Done Status") before DoD items
3. The extract_section() validator stops at the first ### header it encounters
4. If DoD items are under a ### subsection, the validator cannot find them → commit blocked
5. The ### Additional Notes subsection is OK because it comes AFTER DoD items
See: src/claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-19

- [x] SKILL.md updated with direct Read() for all 6 chained target files in appropriate phase sections - Completed: Added direct Read() for requirements-elicitation-guide.md in Phase 2 (line 265) and validation-checklists.md in Phase 3.3 (line 279). user-input-guidance.md confirmed already loaded in Step 0.5.
- [x] All 6 source reference files updated to remove chained Read() calls - Completed: Removed executable Read() from self-validation-workflow.md, requirements-elicitation-workflow.md, user-input-integration-guide.md, error-type-1, error-type-3, error-type-4. Replaced with HTML comments.
- [x] AC3 cross-skill reference decision documented in Notes - Completed: complexity-assessment-matrix.md reference in error-type-3 determined stale. Read() removed with inline comment.
- [x] All modified files verified via Read() to confirm edits applied - Completed: Grep verification confirmed 0 executable chained Read() calls remain.
- [x] All 3 acceptance criteria verified with evidence in tests/results/STORY-453/ - Completed: ac-compliance-verifier confirmed all 3 ACs pass.
- [x] No other reference file content inadvertently modified - Completed: Only targeted Read() lines changed.
- [x] SKILL.md <= 500 lines - Completed: 391 lines.
- [x] No new chains introduced - Completed: Grep scan shows zero inter-reference chains.
- [x] ac1-skill-direct-loads-verification.md created - Completed: Test specification in src/tests/results/STORY-453/.
- [x] ac2-redundant-reads-removed-verification.md created - Completed: Test specification in src/tests/results/STORY-453/.
- [x] ac3-cross-skill-reference-resolution-verification.md created - Completed: Test specification in src/tests/results/STORY-453/.
- [x] Grep scan of all reference files for inter-reference Read() returns 0 matches - Completed: Verified.
- [x] Notes section records AC3 cross-skill reference decision with rationale - Completed: See Notes section.
- [x] Change Log updated with all files modified - Completed: See Change Log.

## Definition of Done

### Implementation
- [x] SKILL.md updated with direct Read() for all 6 chained target files in appropriate phase sections
- [x] All 6 source reference files updated to remove chained Read() calls
- [x] AC3 cross-skill reference decision documented in Notes
- [x] All modified files verified via Read() to confirm edits applied

### Quality
- [x] All 3 acceptance criteria verified with evidence in tests/results/STORY-453/
- [x] No other reference file content inadvertently modified (git diff review)
- [x] SKILL.md <= 500 lines
- [x] No new chains introduced (grep scan of all 25 reference files)

### Testing
- [x] ac1-skill-direct-loads-verification.md created
- [x] ac2-redundant-reads-removed-verification.md created
- [x] ac3-cross-skill-reference-resolution-verification.md created
- [x] Grep scan of all reference files for inter-reference Read() returns 0 matches

### Documentation
- [x] Notes section records AC3 cross-skill reference decision with rationale
- [x] Change Log updated with all files modified

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Red | ✅ Complete | 3 verification test specs created |
| Green | ✅ Complete | 8 edits: 2 additions to SKILL.md, 6 removals from reference files |
| Refactor | ✅ Complete | No refactoring needed (targeted documentation edits) |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/discovering-requirements/SKILL.md | Modified | +2 lines (direct Read() calls) |
| src/claude/skills/discovering-requirements/references/self-validation-workflow.md | Modified | -3/+1 lines |
| src/claude/skills/discovering-requirements/references/requirements-elicitation-workflow.md | Modified | -3/+1 lines |
| src/claude/skills/discovering-requirements/references/user-input-integration-guide.md | Modified | -3/+2 lines |
| src/claude/skills/discovering-requirements/references/error-type-1-incomplete-answers.md | Modified | -1/+1 lines |
| src/claude/skills/discovering-requirements/references/error-type-3-complexity-errors.md | Modified | -1/+1 lines |
| src/claude/skills/discovering-requirements/references/error-type-4-validation-failures.md | Modified | -1/+1 lines |
| src/tests/results/STORY-453/ac1-skill-direct-loads-verification.md | Created | Test spec |
| src/tests/results/STORY-453/ac2-redundant-reads-removed-verification.md | Created | Test spec |
| src/tests/results/STORY-453/ac3-cross-skill-reference-resolution-verification.md | Created | Test spec |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-19 | .claude/story-requirements-analyst | Created | Story created from conformance analysis Finding 3.1 | STORY-453-flatten-nested-reference-chains.story.md |
| 2026-02-19 | DevForgeAI AI Agent | Dev Complete | Flattened 6 nested reference chains: added 2 direct Read() to SKILL.md, removed 6 chained Read() from reference files, resolved AC3 cross-skill reference as stale | SKILL.md, self-validation-workflow.md, requirements-elicitation-workflow.md, user-input-integration-guide.md, error-type-1-incomplete-answers.md, error-type-3-complexity-errors.md, error-type-4-validation-failures.md |
| 2026-02-19 | .claude/qa-result-interpreter | QA Deep | PASSED: 100% traceability, 1/1 validators passed, 0 violations | STORY-453-qa-report.md |

## Notes

**AC3 Cross-Skill Reference Decision (RESOLVED):**

**Decision: STALE — Reference removed.** The conformance analysis (Category 3, Finding 3.3) states the 3-phase workflow covers "Discovery, Requirements Elicitation, and Documentation/Handoff." Complexity scoring is no longer a phase in this skill — it was removed during the devforgeai-ideation→discovering-requirements refactor. The error-type-3 reference to complexity-assessment-matrix.md (in designing-systems skill) is therefore stale. The executable Read() was removed from error-type-3-complexity-errors.md and replaced with an inline HTML comment documenting the decision.

**Design Decisions:**
- Option A (direct Read(), no merges) selected per architect-reviewer recommendation
- user-input-integration-guide.md NOT merged into user-input-guidance.md (chain eliminated by removing internal Read() only)

**References:**
- Source: devforgeai/specs/analysis/discovering-requirements-conformance-analysis.md, Finding 3.1 (lines 181-206)
- Anthropic guidance: best-practices.md lines 345-371 (one-level-deep rule)
- Epic: devforgeai/specs/Epics/EPIC-070-discovering-requirements-conformance-v3.epic.md

---

Story Template Version: 2.9
Last Updated: 2026-02-19
