---
id: STORY-452
title: "Portability Fix — Remove Hardcoded WSL Path in user-input-guidance.md"
type: documentation
epic: EPIC-070
sprint: Sprint-14
status: QA Approved
points: 1
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-02-19
format_version: "2.9"
---

# Story: Portability Fix — Remove Hardcoded WSL Path in user-input-guidance.md

## Description

**As a** DevForgeAI framework contributor working on any machine or operating system,
**I want** all reference file load instructions in `user-input-guidance.md` to use project-relative paths,
**so that** the discovering-requirements skill operates portably across developer environments and CI systems without breaking on machine-specific WSL mount points.

## Provenance

```xml
<provenance>
  <origin document="discovering-requirements-conformance-analysis.md" section="Category 4 — Clarity and Directness">
    <quote>"user-input-guidance.md (line 590) contains a hardcoded absolute path: Read(file_path='/mnt/c/Projects/DevForgeAI2/.claude/skills/discovering-requirements/references/user-input-guidance.md') This path is machine-specific (WSL mount point) and will break on any other system. It also self-references (the file loads itself), which is likely a copy-paste error."</quote>
    <line_reference>lines 297-301</line_reference>
    <quantified_impact>100% failure rate on any non-WSL system or any WSL installation where the project is not at /mnt/c/Projects/DevForgeAI2</quantified_impact>
  </origin>

  <decision rationale="replace-with-relative-path">
    <selected>Replace the absolute path with project-relative path and investigate whether the self-reference is intentional or a copy-paste error.</selected>
    <rejected alternative="remove-the-instruction-entirely">
      Removing the Integration Instructions block would eliminate the defect but also remove useful guidance showing skills how to load this file.
    </rejected>
    <trade_off>Investigation step ensures fix is accurate, not just syntactically correct.</trade_off>
  </decision>

  <stakeholder role="Framework Contributor" goal="cross-machine-portability">
    <quote>"File paths matter: Claude navigates your skill directory like a filesystem. Use forward slashes, not backslashes."</quote>
    <source>discovering-requirements-conformance-analysis.md, Finding 4.1 (citing best-practices.md lines 808-810)</source>
  </stakeholder>
</provenance>
```

## Acceptance Criteria

### AC#1: Hardcoded WSL Absolute Path Replaced with Relative Path

```xml
<acceptance_criteria id="AC1" implements="CFG-001">
  <given>The file .claude/skills/discovering-requirements/references/user-input-guidance.md exists and line 590 contains the machine-specific absolute path Read(file_path="/mnt/c/Projects/DevForgeAI2/.claude/skills/discovering-requirements/references/user-input-guidance.md")</given>
  <when>The story implementation edits line 590 to replace the absolute path with a project-relative path</when>
  <then>Line 590 reads Read(file_path=".claude/skills/discovering-requirements/references/user-input-guidance.md") using a forward-slash relative path from the project root, and no other lines in the file contain the string /mnt/c/Projects/DevForgeAI2</then>
  <verification>
    <source_files>
      <file hint="Reference file containing the defect">.claude/skills/discovering-requirements/references/user-input-guidance.md</file>
    </source_files>
    <test_file>tests/STORY-452/test_ac1_relative_path.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Self-Reference Investigated and Resolved

```xml
<acceptance_criteria id="AC2" implements="CFG-001">
  <given>Line 590 of user-input-guidance.md instructs a skill to load user-input-guidance.md itself (a self-reference), appearing inside an Integration Instructions code block</given>
  <when>The implementer reads lines 585-610 to determine whether the self-reference is (a) intentional generic example or (b) a copy-paste error</when>
  <then>One of the following outcomes is recorded in Implementation Notes: (a) if intentional — self-reference retained with relative path and inline comment added, or (b) if copy-paste error — path corrected to intended target file</then>
  <verification>
    <source_files>
      <file hint="File under investigation">.claude/skills/discovering-requirements/references/user-input-guidance.md</file>
    </source_files>
    <test_file>tests/STORY-452/test_ac2_self_reference_resolved.sh</test_file>
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
      name: "user-input-guidance.md"
      file_path: ".claude/skills/discovering-requirements/references/user-input-guidance.md"
      required_keys:
        - key: "Integration Instructions file_path (line 590)"
          type: "string"
          example: ".claude/skills/discovering-requirements/references/user-input-guidance.md"
          required: true
          validation: "Must be project-relative path (no /mnt/c/ prefix). Forward slashes only."
          test_requirement: "Test: Grep for '/mnt/c/' returns zero matches"

  business_rules:
    - id: "BR-001"
      rule: "All file path references in skill reference documents must use project-relative paths, not absolute paths tied to local filesystem mount points"
      trigger: "Any reference file containing Read() or file-load instructions"
      validation: "Grep for absolute path prefixes returns zero matches"
      error_handling: "Absolute path found → create documentation story to fix"
      test_requirement: "Test: Grep '/mnt/c/Projects/DevForgeAI2' returns exit code 1 (no match)"
      priority: "High"

    - id: "BR-002"
      rule: "Self-referential file load instructions must include an inline comment clarifying they are examples"
      trigger: "Integration Instructions code block where file_path points to the file containing that block"
      validation: "Self-reference has clarifying comment or path corrected to different target"
      error_handling: "Self-reference without comment → add comment; copy-paste error → replace path"
      test_requirement: "Test: Manual review of lines 585-603 confirms resolution"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Skill must load user-input-guidance.md on any system where project root is CWD"
      metric: "Zero path-related load failures across Linux, macOS, Windows (WSL)"
      test_requirement: "Test: Relative path resolves to existing file from project root"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "user-input-guidance.md self-reference investigation"
    limitation: "Intent of self-referencing load instruction cannot be determined without reading surrounding context (lines 585-610)"
    decision: "workaround:implementer reads lines 585-610 and documents conclusion"
    discovered_phase: "Architecture"
    impact: "Adds one manual investigation step (< 5 minutes)"
```

---

## Dependencies

### Prerequisite Stories

- None. Self-contained single-file fix.

### External Dependencies

- None.

### Technology Dependencies

- None.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 100% of the single finding verified.

**Test Scenarios:**
1. **AC1:** Absolute path absent, relative path present
2. **AC2:** Self-reference resolved (context output for manual review)

---

## Acceptance Criteria Verification Checklist

### AC#1: Hardcoded WSL Absolute Path Replaced

- [ ] Read lines 585-603 to confirm current state — **Phase:** 1 — **Evidence:** Read tool output
- [ ] Confirm line 590 contains absolute path — **Phase:** 1 — **Evidence:** line 590
- [ ] Edit line 590 to relative path — **Phase:** 2 — **Evidence:** user-input-guidance.md line 590
- [ ] Grep entire file for /mnt/c/ returns zero — **Phase:** 2 — **Evidence:** test_ac1
- [ ] test_ac1_relative_path.sh passes — **Phase:** 3 — **Evidence:** exit code 0

### AC#2: Self-Reference Investigated

- [ ] Read lines 585-610 for context — **Phase:** 1 — **Evidence:** Read tool output
- [ ] Determine: intentional or copy-paste error — **Phase:** 1 — **Evidence:** Implementation Notes
- [ ] Apply resolution — **Phase:** 2 — **Evidence:** user-input-guidance.md
- [ ] Document conclusion in Implementation Notes — **Phase:** 2 — **Evidence:** story file
- [ ] test_ac2_self_reference_resolved.sh passes — **Phase:** 3 — **Evidence:** exit code 0

---

**Checklist Progress:** 0/10 items complete (0%)

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

## Definition of Done

### Implementation
- [x] Line 590 absolute WSL path replaced with relative path
- [x] Self-reference investigated and determination documented
- [x] Resolution applied (comment added or path corrected)
- [x] No other lines unintentionally modified

### Quality
- [x] Both acceptance criteria have passing tests
- [x] Grep for /mnt/c/Projects/DevForgeAI2 returns zero matches
- [x] File remains valid Markdown

### Testing
- [x] tests/STORY-452/test_ac1_relative_path.sh passes
- [x] tests/STORY-452/test_ac2_self_reference_resolved.sh passes

### Documentation
- [x] Implementation Notes records self-reference determination and resolution

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-19

- [x] Line 590 absolute WSL path replaced with relative path - Completed: Changed `/mnt/c/Projects/DevForgeAI2/.claude/skills/discovering-requirements/references/user-input-guidance.md` to `.claude/skills/discovering-requirements/references/user-input-guidance.md`
- [x] Self-reference investigated and determination documented - Completed: Read lines 585-603; the self-reference is intentional — it's inside an Integration Instructions code block showing other skills how to load this file. Not a copy-paste error.
- [x] Resolution applied (comment added or path corrected) - Completed: Added inline comment `# Note: this file loads itself as an example for skill integration` to clarify intent
- [x] No other lines unintentionally modified - Completed: Only line 590 was changed; no other lines affected
- [x] Both acceptance criteria have passing tests - Completed: test_ac1 (2/2 pass) and test_ac2 (2/2 pass)
- [x] Grep for /mnt/c/Projects/DevForgeAI2 returns zero matches - Completed: Verified zero occurrences remain in the file
- [x] File remains valid Markdown - Completed: File structure preserved, only content within code block changed
- [x] tests/STORY-452/test_ac1_relative_path.sh passes - Completed: Exit code 0
- [x] tests/STORY-452/test_ac2_self_reference_resolved.sh passes - Completed: Exit code 0
- [x] Implementation Notes records self-reference determination and resolution - Completed: Documented above — self-reference is intentional (skill integration example), not a copy-paste error

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Red | ✅ | 2 test files created, both fail as expected |
| Green | ✅ | Line 590 path fixed, inline comment added |
| Refactor | ✅ | No refactoring needed (single-line doc fix) |
| Integration | ✅ | No broken references, all tests pass |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/discovering-requirements/references/user-input-guidance.md | Modified | 590 |
| tests/STORY-452/test_ac1_relative_path.sh | Created | 1-43 |
| tests/STORY-452/test_ac2_self_reference_resolved.sh | Created | 1-55 |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-19 | .claude/story-requirements-analyst | Created | Story created from conformance analysis Finding 4.1 | STORY-452-portability-fix-remove-hardcoded-wsl-path.story.md |
| 2026-02-19 | .claude/qa-result-interpreter | QA Deep | PASSED: Tests 4/4, Traceability 100%, 0 violations | - |

## Notes

**Finding Source:** devforgeai/specs/analysis/discovering-requirements-conformance-analysis.md, Finding 4.1 (lines 293-309). Severity: Medium.

**References:**
- Source: devforgeai/specs/analysis/discovering-requirements-conformance-analysis.md
- Epic: devforgeai/specs/Epics/EPIC-070-discovering-requirements-conformance-v3.epic.md

---

Story Template Version: 2.9
Last Updated: 2026-02-19
