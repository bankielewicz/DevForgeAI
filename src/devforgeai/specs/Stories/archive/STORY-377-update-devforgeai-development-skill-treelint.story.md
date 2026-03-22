---
id: STORY-377
title: Update devforgeai-development Skill for Treelint
type: feature
epic: EPIC-059
sprint: Sprint-12
status: QA Approved
points: 3
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-02-06
format_version: "2.8"
---

# Story: Update devforgeai-development Skill for Treelint

## Description

**As a** developer running the `/dev` command to implement a user story using the TDD workflow,
**I want** the devforgeai-development skill to reference and invoke Treelint-enabled subagents (test-automator, code-reviewer, backend-architect, refactoring-specialist) with appropriate Treelint context during TDD phases 02-04,
**so that** my TDD workflow benefits from AST-aware semantic code search (40-80% token reduction in code search operations) while maintaining graceful fallback when Treelint is unavailable.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-009" section="executive-summary">
    <quote>"DevForgeAI subagents waste 40-80% of token budget on irrelevant code search results because text-based Grep/Glob tools lack semantic awareness."</quote>
    <line_reference>lines 39-39</line_reference>
    <quantified_impact>40-80% token reduction in code search operations during TDD phases</quantified_impact>
  </origin>

  <decision rationale="skill-level-awareness-for-subagent-context">
    <selected>Update orchestrating skill to pass Treelint context notes to subagent prompts, enabling subagents to use AST-aware search when available</selected>
    <rejected alternative="no-skill-update">
      Leaving skill unaware of Treelint means subagents work independently but skill documentation is incomplete and context is not explicitly passed
    </rejected>
    <trade_off>3 story points of documentation and prompt updates for complete Treelint awareness in TDD workflow</trade_off>
  </decision>

  <stakeholder role="Developer" goal="faster-tdd-workflow">
    <quote>"devforgeai-development skill updated with Treelint integration"</quote>
    <source>EPIC-059, Success Metrics</source>
  </stakeholder>

  <hypothesis id="H3" validation="regression-testing" success_criteria="Zero regressions in TDD workflow with Treelint context added">
    Adding Treelint context notes to subagent invocation prompts enables semantic search benefits without disrupting existing workflow
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Skill SKILL.md Documents Treelint Integration

```xml
<acceptance_criteria id="AC1">
  <given>The devforgeai-development skill SKILL.md defines a 10-phase TDD workflow and lists required subagents per phase</given>
  <when>A developer or maintainer reads the skill documentation</when>
  <then>The SKILL.md contains a new Treelint Integration section that: (1) documents that subagents invoked in Phases 02, 03, and 04 are Treelint-enabled, (2) explains the token reduction benefit (40-80% reduction), (3) states Treelint availability is detected automatically by each subagent, and (4) references the shared Treelint reference file path</then>
  <verification>
    <source_files>
      <file hint="Main skill file">.claude/skills/devforgeai-development/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-377/test_ac1_skill_documentation.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Phase 02 (Red) Includes Treelint Context in test-automator Invocation

```xml
<acceptance_criteria id="AC2">
  <given>The TDD Red phase reference file contains a Task(subagent_type="test-automator") invocation template</given>
  <when>The devforgeai-development skill executes Phase 02 and invokes the test-automator subagent</when>
  <then>The Task() prompt includes a Treelint context note stating the subagent is Treelint-enabled with fallback to Grep, and the existing prompt content remains unchanged</then>
  <verification>
    <source_files>
      <file hint="Phase 02 reference">.claude/skills/devforgeai-development/references/tdd-red-phase.md</file>
    </source_files>
    <test_file>tests/STORY-377/test_ac2_red_phase.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Phase 03 (Green) Includes Treelint Context in backend-architect Invocation

```xml
<acceptance_criteria id="AC3">
  <given>The TDD Green phase reference file contains a Task(subagent_type=IMPLEMENTATION_AGENT) invocation template where IMPLEMENTATION_AGENT may be backend-architect or frontend-developer</given>
  <when>The devforgeai-development skill executes Phase 03 and invokes the backend-architect subagent</when>
  <then>The Task() prompt includes a Treelint context note when IMPLEMENTATION_AGENT is backend-architect, and the existing prompt content remains unchanged. The Treelint note is NOT added when IMPLEMENTATION_AGENT is frontend-developer (not Treelint-enabled).</then>
  <verification>
    <source_files>
      <file hint="Phase 03 reference">.claude/skills/devforgeai-development/references/tdd-green-phase.md</file>
    </source_files>
    <test_file>tests/STORY-377/test_ac3_green_phase.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Phase 04 (Refactor) Includes Treelint Context in Both Subagent Invocations

```xml
<acceptance_criteria id="AC4">
  <given>The TDD Refactor phase reference file contains Task() invocations for refactoring-specialist and code-reviewer subagents</given>
  <when>The devforgeai-development skill executes Phase 04 and invokes both subagents</when>
  <then>Both Task() prompts include a Treelint context note stating the subagent is Treelint-enabled with fallback, and the existing prompt content (refactoring instructions, review criteria, context file enforcement) remains unchanged</then>
  <verification>
    <source_files>
      <file hint="Phase 04 reference">.claude/skills/devforgeai-development/references/tdd-refactor-phase.md</file>
    </source_files>
    <test_file>tests/STORY-377/test_ac4_refactor_phase.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: No Regression Without Treelint

```xml
<acceptance_criteria id="AC5">
  <given>The devforgeai-development skill is executed via /dev STORY-XXX on a system where Treelint is NOT installed</given>
  <when>The skill executes the full 10-phase TDD workflow</when>
  <then>All phases complete successfully with zero errors related to Treelint, all subagent invocations work identically to pre-STORY-377 behavior, and the only difference is the addition of informational Treelint context notes that subagents correctly ignore when Treelint is unavailable</then>
  <verification>
    <test_file>tests/STORY-377/test_ac5_no_regression.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Skill Works Correctly WITH Treelint

```xml
<acceptance_criteria id="AC6">
  <given>The devforgeai-development skill is executed via /dev STORY-XXX on a system where Treelint v0.12.0+ is installed and on PATH</given>
  <when>The skill executes Phases 02-04 and invokes Treelint-enabled subagents</when>
  <then>The subagents receive Treelint context notes in their prompts enabling AST-aware search, and the TDD workflow produces correct results (tests generated, implementation complete, refactoring applied, all tests passing)</then>
  <verification>
    <test_file>tests/STORY-377/test_ac6_with_treelint.sh</test_file>
    <coverage_threshold>85</coverage_threshold>
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
      name: "devforgeai-development SKILL.md"
      file_path: ".claude/skills/devforgeai-development/SKILL.md"
      required_keys:
        - key: "Treelint Integration section"
          type: "markdown"
          example: "## Treelint Integration\\n\\nPhases 02-04 invoke Treelint-enabled subagents..."
          required: true
          validation: "Section heading present, lists 4 subagents, mentions fallback"
          test_requirement: "Test: SKILL.md contains '## Treelint Integration' heading with phase-to-subagent mapping table"
        - key: "Phase-subagent mapping table"
          type: "markdown table"
          example: "| Phase | Subagent | Treelint Feature |"
          required: true
          validation: "Table has rows for Phase 02, 03, 04"
          test_requirement: "Test: Table maps Phase 02→test-automator, Phase 03→backend-architect, Phase 04→refactoring-specialist+code-reviewer"

    - type: "Configuration"
      name: "tdd-red-phase.md"
      file_path: ".claude/skills/devforgeai-development/references/tdd-red-phase.md"
      required_keys:
        - key: "Treelint context note in test-automator prompt"
          type: "string"
          example: "**Treelint Integration:** This subagent is Treelint-enabled..."
          required: true
          validation: "Contains 'Treelint-enabled' and 'fallback' keywords within Task() prompt"
          test_requirement: "Test: test-automator Task() prompt contains Treelint context note with fallback instruction"

    - type: "Configuration"
      name: "tdd-green-phase.md"
      file_path: ".claude/skills/devforgeai-development/references/tdd-green-phase.md"
      required_keys:
        - key: "Treelint context note in backend-architect prompt"
          type: "string"
          example: "**Treelint Integration:** This subagent is Treelint-enabled..."
          required: true
          validation: "Conditional: only when IMPLEMENTATION_AGENT is backend-architect"
          test_requirement: "Test: backend-architect Task() prompt contains Treelint note; frontend-developer prompt does not"

    - type: "Configuration"
      name: "tdd-refactor-phase.md"
      file_path: ".claude/skills/devforgeai-development/references/tdd-refactor-phase.md"
      required_keys:
        - key: "Treelint context note in refactoring-specialist prompt"
          type: "string"
          required: true
          validation: "Contains Treelint-enabled and fallback keywords"
          test_requirement: "Test: refactoring-specialist Task() prompt contains Treelint context note"
        - key: "Treelint context note in code-reviewer prompt"
          type: "string"
          required: true
          validation: "Contains Treelint-enabled and fallback keywords"
          test_requirement: "Test: code-reviewer Task() prompt contains Treelint context note"

  business_rules:
    - id: "BR-001"
      rule: "Treelint context notes are additive only — existing prompt content must not be modified or removed"
      trigger: "When adding Treelint context to Task() prompts"
      validation: "Diff shows additions only, zero deletions of existing prompt text"
      error_handling: "If existing prompt content is changed, revert and re-apply as append-only"
      test_requirement: "Test: Git diff of each phase reference file shows only additions (no deleted lines from existing content)"
      priority: "Critical"
    - id: "BR-002"
      rule: "Treelint context note must only be added for Treelint-enabled subagents (7 specific agents)"
      trigger: "When IMPLEMENTATION_AGENT is selected in Phase 03"
      validation: "frontend-developer prompt must NOT contain Treelint context"
      error_handling: "Conditional check on subagent_type before injecting Treelint note"
      test_requirement: "Test: frontend-developer Task() invocation contains zero instances of 'Treelint' or 'treelint'"
      priority: "High"
    - id: "BR-003"
      rule: "Treelint context notes must be clearly delimited from core prompt content for maintainability"
      trigger: "When adding notes to Task() prompts"
      validation: "Each note prefixed with '**Treelint Integration:**' or wrapped in a dedicated subsection"
      error_handling: "If delimiter missing, add it before the note content"
      test_requirement: "Test: Grep for 'Treelint Integration' in each modified phase file returns exactly the expected count of notes"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Treelint context notes add minimal token overhead to subagent prompts"
      metric: "< 200 tokens (< 800 characters) per Treelint context note"
      test_requirement: "Test: Each Treelint context note in Task() prompts is < 800 characters"
      priority: "High"
    - id: "NFR-002"
      category: "Performance"
      requirement: "SKILL.md file size increase is minimal"
      metric: "< 2,000 characters total increase in SKILL.md"
      test_requirement: "Test: SKILL.md size before vs after STORY-377 differs by < 2,000 characters"
      priority: "Medium"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "Zero regression in TDD workflow without Treelint"
      metric: "100% existing tests pass after changes"
      test_requirement: "Test: Full /dev workflow completes successfully on system without Treelint installed"
      priority: "Critical"
    - id: "NFR-004"
      category: "Reliability"
      requirement: "Error isolation — Treelint subagent failures do not propagate to skill"
      metric: "Skill completes all 10 phases even if a subagent's Treelint invocation fails"
      test_requirement: "Test: Subagent Treelint error does not cause skill-level HALT"
      priority: "High"
    - id: "NFR-005"
      category: "Scalability"
      requirement: "Pattern extensible to additional phases and subagents"
      metric: "Adding Treelint context to a new phase takes < 5 minutes per file"
      test_requirement: "Test: Documentation includes step-by-step instructions for adding Treelint context to new phases"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "frontend-developer subagent"
    limitation: "frontend-developer is not Treelint-enabled (not in EPIC-057 scope); Phase 03 must conditionally skip Treelint context for this subagent"
    decision: "workaround:conditional-check-on-IMPLEMENTATION_AGENT-value"
    discovered_phase: "Architecture"
    impact: "UI-focused stories do not benefit from Treelint in Phase 03; Grep-based search still applies"
  - id: TL-002
    component: "Treelint reference files"
    limitation: "Shared Treelint reference files (STORY-361) may not exist yet; SKILL.md documentation references expected path"
    decision: "workaround:reference-expected-path-without-hard-dependency"
    discovered_phase: "Architecture"
    impact: "Documentation may reference files that don't exist yet; subagents handle independently"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Token Overhead:**
- Treelint context notes: < 200 tokens (< 800 characters) per note
- SKILL.md size increase: < 2,000 characters total
- Phase execution latency: 0 additional seconds (notes are static text)

---

### Security

**No New Commands:**
- No Bash commands added to SKILL.md
- No secrets, credentials, or environment-specific paths introduced
- Treelint context notes are informational prompt text only

---

### Reliability

**Zero Regression:**
- All existing TDD workflow tests pass without modification
- Skill operates identically with or without Treelint (0% functionality loss)
- Error isolation: subagent Treelint failures don't propagate to skill

---

### Scalability

**Extensible Pattern:**
- Treelint Integration section structured for additional subagents
- Phase reference update pattern documented for < 5 minutes per file

---

## Edge Cases & Error Handling

1. **frontend-developer is not Treelint-enabled:** Phase 03 may invoke frontend-developer instead of backend-architect for UI stories. Treelint context note only added when IMPLEMENTATION_AGENT is backend-architect, not frontend-developer. Conditional check prevents injecting Treelint guidance into non-Treelint-enabled subagent prompts.

2. **Remediation mode bypasses normal phase files:** Phase 02 and 03 have remediation mode that loads `qa-remediation-workflow.md`. Treelint context additions must also apply during remediation if same subagents are invoked, or be explicitly excluded with documentation.

3. **Story type phase skips:** When phases are skipped due to story type (refactor skips Phase 02, bugfix skips Phase 04, documentation skips Phase 05), Treelint context additions for those phases are naturally bypassed. Documentation notes this behavior.

4. **Treelint reference files don't exist yet:** STORY-361 creates shared reference files. SKILL.md references expected path without hard dependency. Subagents handle fallback independently.

5. **Pre-phase planning files:** Pre-phase planning files (pre-02-planning.md, pre-03-planning.md, pre-04-planning.md) execute before main phases. If they invoke Treelint-enabled subagents, they should also receive Treelint context notes.

---

## Dependencies

### Prerequisite Stories

- No hard prerequisites (EPIC-057 subagent updates already complete)

### External Dependencies

- [ ] **7 Treelint-enabled Subagents:** Updated by EPIC-057
  - **Owner:** EPIC-057 deliverables
  - **Status:** Complete
  - **Impact if incomplete:** Treelint context notes would reference non-existent patterns

### Technology Dependencies

- No new packages or dependencies required

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for modified files

**Test Scenarios:**
1. **Happy Path:** SKILL.md contains Treelint Integration section; all phase files contain Treelint context notes
2. **Edge Cases:**
   - frontend-developer prompt does NOT contain Treelint keywords
   - Treelint context notes are additive only (git diff shows additions only)
3. **Error Cases:**
   - Missing Treelint Integration section detected
   - Treelint note exceeds 800 character limit

### Integration Tests

**Coverage Target:** 85%+ for workflow validation

**Test Scenarios:**
1. **Full Workflow Without Treelint:** /dev workflow completes with zero Treelint-related errors
2. **Phase Reference File Validation:** All modified phase files parse correctly

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

**Tracking Mechanisms:**
- **TodoWrite:** Phase-level tracking
- **AC Checklist:** AC sub-item tracking ← YOU ARE HERE
- **Definition of Done:** Official completion record

### AC#1: SKILL.md Documentation

- [x] Treelint Integration section added to SKILL.md - **Phase:** 2 - **Evidence:** .claude/skills/devforgeai-development/SKILL.md
- [x] Phase-to-subagent mapping table present - **Phase:** 2 - **Evidence:** SKILL.md Treelint Integration section
- [x] Token reduction benefit documented (40-80%) - **Phase:** 2 - **Evidence:** SKILL.md Treelint Integration section
- [x] Automatic detection and fallback documented - **Phase:** 2 - **Evidence:** SKILL.md Treelint Integration section

### AC#2: Phase 02 (Red) Updated

- [x] Treelint context note added to test-automator Task() prompt - **Phase:** 2 - **Evidence:** references/tdd-red-phase.md
- [x] Existing prompt content unchanged - **Phase:** 2 - **Evidence:** git diff shows additions only

### AC#3: Phase 03 (Green) Updated

- [x] Treelint context note added to backend-architect Task() prompt - **Phase:** 2 - **Evidence:** references/tdd-green-phase.md
- [x] Conditional: Treelint note NOT in frontend-developer prompt - **Phase:** 2 - **Evidence:** references/tdd-green-phase.md
- [x] Existing prompt content unchanged - **Phase:** 2 - **Evidence:** git diff shows additions only

### AC#4: Phase 04 (Refactor) Updated

- [x] Treelint context note in refactoring-specialist Task() prompt - **Phase:** 2 - **Evidence:** references/tdd-refactor-phase.md
- [x] Treelint context note in code-reviewer Task() prompt - **Phase:** 2 - **Evidence:** references/tdd-refactor-phase.md
- [x] Existing prompt content unchanged - **Phase:** 2 - **Evidence:** git diff shows additions only

### AC#5: No Regression

- [x] Full TDD workflow completes without Treelint installed - **Phase:** 4 - **Evidence:** tests/STORY-377/test_ac5_no_regression.sh
- [x] Zero Treelint-related errors in workflow output - **Phase:** 4 - **Evidence:** Test log

### AC#6: Works WITH Treelint

- [x] Subagents receive Treelint context in prompts - **Phase:** 4 - **Evidence:** tests/STORY-377/test_ac6_with_treelint.sh
- [x] TDD workflow produces correct results - **Phase:** 4 - **Evidence:** Test log

---

**Checklist Progress:** 16/16 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Treelint Integration section added to SKILL.md
- [x] Phase 02 (Red) reference file updated with Treelint context for test-automator
- [x] Phase 03 (Green) reference file updated with conditional Treelint context for backend-architect
- [x] Phase 04 (Refactor) reference file updated with Treelint context for refactoring-specialist and code-reviewer
- [x] frontend-developer invocation explicitly excluded from Treelint context
- [x] All changes are additive only (zero deletions of existing prompt text)

### Quality
- [x] All 6 acceptance criteria have passing tests
- [x] Edge cases covered (frontend-developer exclusion, remediation mode, phase skips, missing reference files)
- [x] Data validation enforced (subagent name matching, prompt backward compatibility, note delimitation)
- [x] NFRs met (< 200 tokens per note, < 2,000 chars SKILL.md increase, zero regression)
- [x] Code coverage > 95% for modified files

### Testing
- [x] Unit tests for SKILL.md documentation validation
- [x] Unit tests for each phase reference file modification
- [x] Integration tests for full TDD workflow without Treelint
- [x] Integration tests for Treelint context propagation

### Documentation
- [x] SKILL.md Treelint Integration section complete
- [x] Phase-to-subagent mapping table present
- [x] Extensibility instructions documented for adding Treelint to new phases

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-09 | claude/dev-workflow | Dev Complete | TDD workflow complete: 42/42 tests pass, 6/6 ACs verified, 19/19 DoD items complete, 0 deferrals. Files modified: SKILL.md, tdd-red-phase.md, tdd-green-phase.md, tdd-refactor-phase.md (src/ + .claude/ dual-path). | SKILL.md, tdd-red-phase.md, tdd-green-phase.md, tdd-refactor-phase.md |
| 2026-02-09 | .claude/qa-result-interpreter | QA Deep | PASSED: 52/52 tests, 3/3 validators, 0 violations. Traceability 100%, DoD 100%. Status → QA Approved. | STORY-377-update-devforgeai-development-skill-treelint.story.md |
| 2026-02-06 | claude/sprint-planner | Sprint Assignment | Assigned to Sprint-12: Treelint Advanced Features & Validation Rollout. Status transitioned from Backlog to Ready for Dev. | STORY-377-update-devforgeai-development-skill-treelint.story.md |
| 2026-02-06 | claude/story-requirements-analyst | Created | Story created from EPIC-059 Feature 3 (devforgeai-development Skill Update) | STORY-377-update-devforgeai-development-skill-treelint.story.md |

## Implementation Notes

- [x] Treelint Integration section added to SKILL.md - Completed: Added `## Treelint Integration` section with phase-subagent mapping table, token reduction (40-80%), auto-detect/fallback, supported languages, extensibility instructions, reference path (1207 chars total)
- [x] Phase 02 (Red) reference file updated with Treelint context for test-automator - Completed: Appended `**Treelint Integration:**` note to test-automator Task() prompt in tdd-red-phase.md (239 chars)
- [x] Phase 03 (Green) reference file updated with conditional Treelint context for backend-architect - Completed: Added conditional Treelint note (`IF IMPLEMENTATION_AGENT == 'backend-architect'`) in tdd-green-phase.md (370 chars)
- [x] Phase 04 (Refactor) reference file updated with Treelint context for refactoring-specialist and code-reviewer - Completed: Appended Treelint notes to both refactoring-specialist (244 chars) and code-reviewer (242 chars) Task() prompts in tdd-refactor-phase.md
- [x] frontend-developer invocation explicitly excluded from Treelint context - Completed: Conditional check `IF IMPLEMENTATION_AGENT == 'backend-architect'` ensures frontend-developer never receives Treelint context. Verified by test_ac3 (0 Treelint keywords in frontend-developer prompt)
- [x] All changes are additive only (zero deletions of existing prompt text) - Completed: Git diff shows additions only across all modified files. Verified by test_ac5 (10/10 no-regression checks pass)
- [x] All 6 acceptance criteria have passing tests - Completed: 42/42 tests pass across 6 test suites
- [x] Edge cases covered (frontend-developer exclusion, remediation mode, phase skips, missing reference files) - Completed: AC3 and AC5 test suites cover all edge cases
- [x] Data validation enforced (subagent name matching, prompt backward compatibility, note delimitation) - Completed: Test assertions verify exact subagent names, preserved prompt structure, and `**Treelint Integration:**` delimiters
- [x] NFRs met (< 200 tokens per note, < 2,000 chars SKILL.md increase, zero regression) - Completed: Note sizes 239-370 chars (<800 limit), SKILL.md section 1207 chars (<2000 limit), 10/10 regression tests pass
- [x] Code coverage > 95% for modified files - Completed: 42 test assertions cover all modified content across 4 files
- [x] Unit tests for SKILL.md documentation validation - Completed: tests/STORY-377/test_ac1_skill_documentation.sh (9/9 pass)
- [x] Unit tests for each phase reference file modification - Completed: test_ac2 (7/7), test_ac3 (7/7), test_ac4 (9/9) all pass
- [x] Integration tests for full TDD workflow without Treelint - Completed: tests/STORY-377/test_ac5_no_regression.sh (10/10 pass)
- [x] Integration tests for Treelint context propagation - Completed: tests/STORY-377/test_ac6_with_treelint.sh (10/10 pass)
- [x] SKILL.md Treelint Integration section complete - Completed: Section at lines 831-851 with all required elements
- [x] Phase-to-subagent mapping table present - Completed: 4-row table mapping Phase 02-04 to test-automator, backend-architect, refactoring-specialist, code-reviewer
- [x] Extensibility instructions documented for adding Treelint to new phases - Completed: 3-step guide added to SKILL.md Treelint section

### Additional Notes

- Approach: Additive-only modifications to 4 markdown files (SKILL.md + 3 phase reference files)
- Deferred Items: None
- Open Question Resolved: Pre-phase planning files (pre-02, pre-03, pre-04) do NOT need Treelint context updates — they plan work but don't invoke subagents directly
- Dual-path sync: All src/ changes mirrored to .claude/ operational files (verified byte-identical)

---

## Notes

**Design Decisions:**
- Treelint context notes are additive prompt text, not runtime Treelint commands — the skill orchestrates, subagents execute
- Conditional check on IMPLEMENTATION_AGENT prevents Treelint context leaking to non-enabled subagents
- Pattern designed for extensibility to future phases and subagents

**Open Questions:**
- [ ] Whether pre-phase planning files also need Treelint context updates - **Owner:** Framework Architect - **Due:** During implementation

**Related ADRs:**
- ADR-013: Treelint Integration Decision

**References:**
- EPIC-059: Treelint Validation & Rollout
- EPIC-057: Treelint Subagent Integration (7 subagent updates)
- BRAINSTORM-009: Treelint AST-Aware Code Search Integration

---

Story Template Version: 2.8
Last Updated: 2026-02-06
