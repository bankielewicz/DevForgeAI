---
id: STORY-436
title: Add Epic Creation Phases to Architecture SKILL.md
type: feature
epic: EPIC-068
sprint: Sprint-2
status: QA Approved
points: 5
depends_on: ["STORY-432", "STORY-433", "STORY-434", "STORY-435"]
priority: High
advisory: false
assigned_to: Unassigned
created: 2026-02-17
format_version: "2.9"
---

# Story: Add Epic Creation Phases to Architecture SKILL.md

## Description

**As a** DevForgeAI framework architect,
**I want** the architecture skill (SKILL.md) to include a new Phase 6: Epic Creation with 8 sub-phases, progressive disclosure references to all migrated epic files, registered subagent invocations, and a defined input format accepting YAML requirements from the structured schema,
**so that** the architecture skill becomes the single owner of epic creation — receiving structured requirements from ideation and producing complete epic documents.

**Business Context:**
After Sprints 1 (file migrations + scoring unification) and Feature 4 (requirements schema), all epic-related reference files are in architecture and the input format is defined. This story wires them together by adding a new Phase 6 to architecture SKILL.md that replaces orchestration's Phase 4A. The architecture skill grows from 279 lines to ~380 lines (well under the 1,000-line limit), with detailed workflow loaded on-demand from reference files.

## Provenance

```xml
<provenance>
  <origin document="EPIC-068" section="Feature 5">
    <quote>"Add Phase 6: Epic Creation with 8 sub-phases (from orchestration's Phase 4A); add progressive disclosure references to all migrated files; register subagent invocations for requirements-analyst and architect-reviewer; define input format (accepts YAML requirements from F4 schema)"</quote>
    <line_reference>lines 139-143</line_reference>
    <quantified_impact>Architecture SKILL.md grows from 279 → ~380 lines; gains complete epic creation capability</quantified_impact>
  </origin>

  <decision rationale="architect-role-owns-epic-creation">
    <selected>Add Phase 6 to architecture skill with progressive disclosure</selected>
    <rejected alternative="keep-epic-creation-in-orchestration">
      Orchestration is a coordinator, not a content creator; epic creation is architectural work
    </rejected>
    <trade_off>Architecture skill gains ~100 lines and 14 reference files; progressive disclosure keeps SKILL.md under 1,000 lines</trade_off>
  </decision>

  <stakeholder role="Framework Architect" goal="complete-architect-workflow">
    <quote>"Architecture skill becomes the 'Architect' role — receives structured requirements, produces epics"</quote>
    <source>EPIC-068, Feature 5 User Value</source>
  </stakeholder>
</provenance>
```

## Acceptance Criteria

### AC#1: Phase 6 Epic Creation Added to Architecture SKILL.md

```xml
<acceptance_criteria id="AC1" implements="PHASE-001">
  <given>The architecture SKILL.md currently has 5 phases (Phase 1-5) and is 279 lines</given>
  <when>Phase 6: Epic Creation is added</when>
  <then>SKILL.md contains Phase 6 with 8 sub-phases (4A.1 through 4A.8 mapping from orchestration), listed after the existing Phase 5, with progressive disclosure Read() references to detailed workflow files</then>
  <verification>
    <source_files>
      <file hint="Architecture SKILL.md">src/claude/skills/designing-systems/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-436/test_ac1_phase6_added.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Progressive Disclosure References for All Migrated Files

```xml
<acceptance_criteria id="AC2" implements="REFS-001">
  <given>14 epic-related reference files exist in architecture/references/ (7 from orchestration via STORY-432, up to 6 from ideation via STORY-433, plus merged files from STORY-434)</given>
  <when>Phase 6 sub-phases are defined</when>
  <then>Each sub-phase includes Read() references to the specific reference file(s) needed for that sub-phase, loaded on-demand (not preloaded)</then>
  <verification>
    <source_files>
      <file hint="Architecture SKILL.md Phase 6">src/claude/skills/designing-systems/SKILL.md</file>
      <file hint="Architecture references dir">src/claude/skills/designing-systems/references/</file>
    </source_files>
    <test_file>tests/STORY-436/test_ac2_progressive_disclosure.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Subagent Invocations Registered

```xml
<acceptance_criteria id="AC3" implements="SUBAGENT-001">
  <given>Phase 6 requires two subagents: requirements-analyst (feature decomposition) and architect-reviewer (technical assessment)</given>
  <when>Phase 6 sub-phases are defined</when>
  <then>The SKILL.md explicitly registers both subagent invocations with: (a) which sub-phase invokes each subagent, (b) what input is provided, (c) what output is expected, and (d) Task() call template with correct subagent_type</then>
  <verification>
    <source_files>
      <file hint="Architecture SKILL.md">src/claude/skills/designing-systems/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-436/test_ac3_subagent_registration.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Input Format Accepts YAML Structured Requirements

```xml
<acceptance_criteria id="AC4" implements="INPUT-001">
  <given>Feature 4 (STORY-435) defined a YAML requirements schema as the handoff artifact from ideation</given>
  <when>Phase 6 input specification is defined</when>
  <then>Phase 6 explicitly documents that it accepts: (a) YAML-structured requirements.md as primary input (from ideation), (b) the required schema fields it reads (decisions, scope, success_criteria, constraints, nfrs, stakeholders), and (c) fallback behavior if legacy narrative requirements are provided instead</then>
  <verification>
    <source_files>
      <file hint="Architecture SKILL.md Phase 6 input">src/claude/skills/designing-systems/SKILL.md</file>
      <file hint="Requirements schema">src/claude/skills/devforgeai-ideation/assets/templates/requirements-schema.yaml</file>
    </source_files>
    <test_file>tests/STORY-436/test_ac4_input_format.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: SKILL.md Stays Under 1,000-Line Limit

```xml
<acceptance_criteria id="AC5" implements="SIZE-001">
  <given>The architecture SKILL.md is currently 279 lines and will grow with Phase 6</given>
  <when>Phase 6 is fully added</when>
  <then>The total SKILL.md line count is ≤ 400 lines (target ~380) and well under the 1,000-line maximum per tech-stack.md constraints</then>
  <verification>
    <source_files>
      <file hint="Architecture SKILL.md">src/claude/skills/designing-systems/SKILL.md</file>
      <file hint="Size constraints">devforgeai/specs/context/tech-stack.md</file>
    </source_files>
    <test_file>tests/STORY-436/test_ac5_line_count.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Post-Epic Feedback Hook Preserved

```xml
<acceptance_criteria id="AC6" implements="HOOK-001">
  <given>Orchestration Phase 4A.9 includes a post-epic feedback hook (STORY-028)</given>
  <when>Phase 6 is added to architecture</when>
  <then>The post-epic feedback hook is included in the architecture Phase 6 workflow as the final sub-phase, with the same non-blocking invocation behavior</then>
  <verification>
    <source_files>
      <file hint="Architecture SKILL.md Phase 6 final sub-phase">src/claude/skills/designing-systems/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-436/test_ac6_feedback_hook.py</test_file>
    <coverage_threshold>95</coverage_threshold>
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
      name: "Architecture SKILL.md Phase 6 Addition"
      file_path: "src/claude/skills/designing-systems/SKILL.md"
      purpose: "Add Phase 6: Epic Creation with 8 sub-phases to architecture skill"
      required_keys:
        - key: "phase_6_subphases"
          type: "array"
          example: |
            Phase 6.1: Discovery & Context Loading
            Phase 6.2: Requirements Input Parsing
            Phase 6.3: Feature Decomposition (subagent: requirements-analyst)
            Phase 6.4: Technical Assessment (subagent: architect-reviewer)
            Phase 6.5: Epic Document Generation
            Phase 6.6: Validation & Self-Healing
            Phase 6.7: Epic File Creation
            Phase 6.8: Post-Epic Feedback Hook
          required: true
          test_requirement: "Test: Verify all 8 sub-phases present in SKILL.md"
        - key: "reference_mapping"
          type: "object"
          example: |
            Phase 6.1: epic-management.md
            Phase 6.3: feature-decomposition.md (merged), feature-analyzer.md, dependency-graph.md
            Phase 6.4: complexity-assessment-workflow.md, complexity-assessment-matrix.md
            Phase 6.6: epic-validation-checklist.md
            Phase 6.7: epic-template.md, epic-validation-hook.md
          required: true
          test_requirement: "Test: Verify each sub-phase has Read() reference to correct file"
        - key: "current_line_count"
          type: "integer"
          example: 279
          required: true
          test_requirement: "Test: Verify starting line count matches expected"
        - key: "target_line_count"
          type: "integer"
          example: 380
          required: true
          test_requirement: "Test: Verify final line count ≤ 400"

  business_rules:
    - id: "BR-001"
      rule: "Phase 6 must use progressive disclosure — detailed workflows loaded via Read() references, not inlined"
      trigger: "When adding Phase 6 content to SKILL.md"
      validation: "Each sub-phase has Read() call, no sub-phase exceeds 15 lines in SKILL.md"
      error_handling: "If sub-phase requires >15 lines, extract to reference file"
      test_requirement: "Test: Count lines per sub-phase, verify all ≤ 15"
      priority: "Critical"

    - id: "BR-002"
      rule: "Phase 6 must accept YAML structured requirements as primary input"
      trigger: "When defining Phase 6.2 (Requirements Input Parsing)"
      validation: "Input spec references requirements-schema.yaml from STORY-435"
      error_handling: "Fallback to legacy narrative parsing if YAML not detected"
      test_requirement: "Test: Verify Phase 6.2 references requirements-schema.yaml"
      priority: "Critical"

    - id: "BR-003"
      rule: "Both subagents (requirements-analyst, architect-reviewer) must be explicitly registered"
      trigger: "When defining Phase 6.3 and 6.4"
      validation: "Task() call templates present with correct subagent_type"
      error_handling: "HALT if subagent not found in agent registry"
      test_requirement: "Test: Verify Task() templates reference correct subagent_type values"
      priority: "High"

    - id: "BR-004"
      rule: "Post-epic feedback hook must be non-blocking (STORY-028 behavior preserved)"
      trigger: "When defining Phase 6.8"
      validation: "Hook invocation uses try/catch with graceful error handling"
      error_handling: "Log warning if hook fails, do not block epic creation"
      test_requirement: "Test: Simulate hook failure, verify epic creation not blocked"
      priority: "High"

    - id: "BR-005"
      rule: "SKILL.md total line count must not exceed 1,000 lines"
      trigger: "After Phase 6 addition"
      validation: "wc -l SKILL.md ≤ 1,000"
      error_handling: "Extract content to reference files if approaching limit"
      test_requirement: "Test: Count final lines, verify ≤ 1,000 (target ≤ 400)"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Phase 6 progressive disclosure must minimize upfront token cost"
      metric: "Phase 6 section in SKILL.md adds ≤ 100 lines (detailed workflow in reference files)"
      test_requirement: "Test: Count Phase 6 lines in SKILL.md, verify ≤ 100"
      priority: "High"

    - id: "NFR-002"
      category: "Reliability"
      requirement: "Phase 6 must produce valid epic documents"
      metric: "Epic documents pass epic-validation-checklist.md checks (Phase 6.6)"
      test_requirement: "Test: Generate sample epic, run validation, expect pass"
      priority: "Critical"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Progressive Disclosure"
    limitation: "Reference file names may have changed during STORY-434 (merge/unification); Phase 6 Read() paths must match the post-merge filenames"
    decision: "workaround:Verify actual filenames in architecture/references/ before writing Read() paths"
    discovered_phase: "Architecture"
    impact: "Must run STORY-432, 433, 434 first to know final filenames"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Token Budget:**
- Phase 6 section in SKILL.md: ≤ 100 lines
- Reference files loaded on-demand (not preloaded)
- Total SKILL.md: ≤ 400 lines target

---

### Security

**No security impact** — SKILL.md is prompt documentation.

---

### Scalability

**Progressive Disclosure:**
- Future sub-phases can be added without inflating SKILL.md
- Reference files can grow independently

---

### Reliability

**Epic Creation Quality:**
- Phase 6.6 validation must catch common issues
- Phase 6.8 feedback hook provides continuous improvement signal
- Fallback to legacy input format if YAML requirements not available

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-432:** Move Epic Creation References from Orchestration → Architecture
  - **Why:** Reference files must be in architecture before SKILL.md can reference them
  - **Status:** Backlog

- [ ] **STORY-433:** Move Epic Analysis References from Ideation → Architecture
  - **Why:** Additional reference files must be in architecture
  - **Status:** Backlog

- [ ] **STORY-434:** Unify Complexity Scoring Systems
  - **Why:** Unified scoring files must exist before Phase 6.4 can reference them
  - **Status:** Backlog

- [ ] **STORY-435:** Define Structured Requirements Schema
  - **Why:** Phase 6.2 input specification depends on the YAML schema definition
  - **Status:** Backlog

### External Dependencies

None.

### Technology Dependencies

None — Markdown prompt file changes only.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95% for SKILL.md structure validation

**Test Scenarios:**
1. **Happy Path:** Phase 6 with 8 sub-phases present, all Read() references valid, line count ≤ 400
2. **Edge Cases:**
   - Reference file renamed during unification (Read() path must match)
   - SKILL.md approaching 400 lines (verify still under 1,000 hard limit)
3. **Error Cases:**
   - Missing reference file for sub-phase (should detect and report)
   - Missing subagent registration (should detect)

---

### Integration Tests

**Coverage Target:** 85%

**Test Scenarios:**
1. **End-to-End Epic Creation:** Architecture skill Phase 6 produces valid epic from YAML requirements
2. **Subagent Invocation:** requirements-analyst and architect-reviewer respond correctly
3. **Feedback Hook:** Post-epic feedback hook fires without blocking

---

## Acceptance Criteria Verification Checklist

### AC#1: Phase 6 Epic Creation Added

- [ ] Phase 6 header added after Phase 5 - **Phase:** 3 - **Evidence:** tests/STORY-436/test_ac1_phase6_added.py
- [ ] 8 sub-phases defined (6.1 through 6.8) - **Phase:** 3 - **Evidence:** tests/STORY-436/test_ac1_phase6_added.py
- [ ] Sub-phases map to orchestration Phase 4A.1-4A.8 - **Phase:** 3 - **Evidence:** tests/STORY-436/test_ac1_phase6_added.py

### AC#2: Progressive Disclosure References

- [ ] Phase 6.1 references epic-management.md - **Phase:** 3 - **Evidence:** tests/STORY-436/test_ac2_progressive_disclosure.py
- [ ] Phase 6.3 references feature decomposition files - **Phase:** 3 - **Evidence:** tests/STORY-436/test_ac2_progressive_disclosure.py
- [ ] Phase 6.4 references complexity assessment files - **Phase:** 3 - **Evidence:** tests/STORY-436/test_ac2_progressive_disclosure.py
- [ ] Phase 6.6 references epic-validation-checklist.md - **Phase:** 3 - **Evidence:** tests/STORY-436/test_ac2_progressive_disclosure.py
- [ ] Phase 6.7 references epic-template.md - **Phase:** 3 - **Evidence:** tests/STORY-436/test_ac2_progressive_disclosure.py

### AC#3: Subagent Invocations Registered

- [ ] requirements-analyst registered for Phase 6.3 - **Phase:** 3 - **Evidence:** tests/STORY-436/test_ac3_subagent_registration.py
- [ ] architect-reviewer registered for Phase 6.4 - **Phase:** 3 - **Evidence:** tests/STORY-436/test_ac3_subagent_registration.py
- [ ] Task() call templates with correct subagent_type - **Phase:** 3 - **Evidence:** tests/STORY-436/test_ac3_subagent_registration.py

### AC#4: Input Format Accepts YAML Requirements

- [ ] Phase 6.2 references requirements-schema.yaml - **Phase:** 3 - **Evidence:** tests/STORY-436/test_ac4_input_format.py
- [ ] Schema fields enumerated (decisions, scope, etc.) - **Phase:** 3 - **Evidence:** tests/STORY-436/test_ac4_input_format.py
- [ ] Legacy fallback documented - **Phase:** 3 - **Evidence:** tests/STORY-436/test_ac4_input_format.py

### AC#5: SKILL.md Under 1,000-Line Limit

- [ ] Final line count ≤ 400 (target) - **Phase:** 3 - **Evidence:** tests/STORY-436/test_ac5_line_count.py
- [ ] Final line count ≤ 1,000 (hard limit) - **Phase:** 3 - **Evidence:** tests/STORY-436/test_ac5_line_count.py

### AC#6: Post-Epic Feedback Hook Preserved

- [ ] Phase 6.8 includes feedback hook - **Phase:** 3 - **Evidence:** tests/STORY-436/test_ac6_feedback_hook.py
- [ ] Non-blocking behavior specified - **Phase:** 3 - **Evidence:** tests/STORY-436/test_ac6_feedback_hook.py

---

**Checklist Progress:** 0/21 items complete (0%)

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
- [x] Phase 6: Epic Creation added to architecture SKILL.md with 8 sub-phases
- [x] Progressive disclosure Read() references for all epic-related reference files
- [x] requirements-analyst subagent registered for Phase 6.3
- [x] architect-reviewer subagent registered for Phase 6.4
- [x] Input format specification accepts YAML structured requirements (with legacy fallback)
- [x] Post-epic feedback hook preserved as Phase 6.8

### Quality
- [x] All 6 acceptance criteria have passing tests
- [x] SKILL.md total line count ≤ 400 (well under 1,000-line limit)
- [x] Each sub-phase ≤ 15 lines in SKILL.md (progressive disclosure)
- [x] All Read() paths reference files that exist in architecture/references/

### Testing
- [x] Unit test: test_ac1_phase6_added.py passes
- [x] Unit test: test_ac2_progressive_disclosure.py passes
- [x] Unit test: test_ac3_subagent_registration.py passes
- [x] Unit test: test_ac4_input_format.py passes
- [x] Unit test: test_ac5_line_count.py passes
- [x] Unit test: test_ac6_feedback_hook.py passes

### Documentation
- [x] Story changelog updated
- [x] Phase 6 sub-phase mapping to orchestration Phase 4A documented in Notes
- [x] Integration section in SKILL.md updated (receives from ideation, not orchestration)

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Phase 02 (Red) | ✓ Complete | 51 tests generated across 6 files, all failing initially |
| Phase 03 (Green) | ✓ Complete | Phase 6 with 8 sub-phases added, 51/51 tests passing |
| Phase 04 (Refactor) | ✓ Complete | Optimized to 393 lines, all tests remain green |
| Phase 4.5 (AC Verify) | ✓ Complete | All 6 ACs verified PASS |
| Phase 05 (Integration) | ✓ Complete | Cross-component validation, path fix for epic-template.md |
| Phase 5.5 (Final AC) | ✓ Complete | Final verification, all 6 ACs PASS |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/designing-systems/SKILL.md | Modified | 393 (was 280) |
| tests/STORY-436/test_ac1_phase6_added.py | Created | ~80 |
| tests/STORY-436/test_ac2_progressive_disclosure.py | Created | ~80 |
| tests/STORY-436/test_ac3_subagent_registration.py | Created | ~70 |
| tests/STORY-436/test_ac4_input_format.py | Created | ~90 |
| tests/STORY-436/test_ac5_line_count.py | Created | ~40 |
| tests/STORY-436/test_ac6_feedback_hook.py | Created | ~50 |

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-18

- [x] Phase 6: Epic Creation added to architecture SKILL.md with 8 sub-phases - Completed: Added lines 212-319 with Phase 6 header and 8 sub-phases (6.1-6.8) per orchestration Phase 4A mapping
- [x] Progressive disclosure Read() references for all epic-related reference files - Completed: Each sub-phase has on-demand Read() calls to appropriate reference files
- [x] requirements-analyst subagent registered for Phase 6.3 - Completed: Task(subagent_type="requirements-analyst") at line 255
- [x] architect-reviewer subagent registered for Phase 6.4 - Completed: Task(subagent_type="architect-reviewer") at line 266
- [x] Input format specification accepts YAML structured requirements (with legacy fallback) - Completed: Phase 6.2 references requirements-schema.yaml with 6 required fields and AskUserQuestion fallback
- [x] Post-epic feedback hook preserved as Phase 6.8 - Completed: TRY/CATCH non-blocking pattern referencing STORY-028
- [x] All 6 acceptance criteria have passing tests - Completed: 51/51 tests pass
- [x] SKILL.md total line count ≤ 400 - Completed: 393 lines (under 400 target, well under 1000 limit)
- [x] Each sub-phase ≤ 15 lines in SKILL.md - Completed: All sub-phases average 10-12 lines
- [x] All Read() paths reference files that exist - Completed: Verified all paths, fixed epic-template.md to use assets/templates/ path
- [x] Integration section updated - Completed: Line 342-344 shows ideation-to-architecture flow with epic document output
- [x] Reference Files section updated - Completed: Added Epic Creation Files (10 files) listing

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-17 12:00 | devforgeai-story-creation | Created | Story created from EPIC-068 Feature 5 | STORY-436-add-epic-creation-phases-to-architecture-skill.story.md |
| 2026-02-18 12:30 | DevForgeAI AI Agent | Dev Complete | Added Phase 6: Epic Creation with 8 sub-phases to architecture SKILL.md | src/claude/skills/designing-systems/SKILL.md, tests/STORY-436/*.py |
| 2026-02-18 10:42 | qa-result-interpreter | QA Deep | PASSED: 51/51 tests, 0 violations, 100% traceability | STORY-436-qa-report.md |

## Notes

**Design Decisions:**
- Phase 6 numbered after existing Phase 5 (architecture validation) — natural flow: validate → create epic
- Progressive disclosure: each sub-phase ≤ 15 lines, loads reference via Read()
- YAML requirements as primary input, legacy narrative as fallback
- Two subagents: requirements-analyst (decomposition) and architect-reviewer (technical assessment)
- Post-epic feedback hook preserved from STORY-028

**Phase Mapping (Orchestration → Architecture):**

| Orchestration Phase 4A | → | Architecture Phase 6 |
|------------------------|---|---------------------|
| 4A.1: Discovery | → | 6.1: Discovery & Context Loading |
| 4A.2: Context Loading | → | 6.2: Requirements Input Parsing |
| 4A.3: Feature Decomposition | → | 6.3: Feature Decomposition |
| 4A.4: Technical Assessment | → | 6.4: Technical Assessment |
| 4A.5: Epic Generation | → | 6.5: Epic Document Generation |
| 4A.6: CLI Hook | → | (merged into 6.7) |
| 4A.7: Validation | → | 6.6: Validation & Self-Healing |
| 4A.8: File Creation | → | 6.7: Epic File Creation |
| 4A.9: Feedback Hook | → | 6.8: Post-Epic Feedback Hook |

**Size Budget:**
- Current SKILL.md: 279 lines
- Phase 6 addition: ~100 lines (8 sub-phases × ~12 lines each)
- Target total: ~380 lines
- Hard limit: 1,000 lines (tech-stack.md constraint)

**Scope Boundaries:**
- This story adds Phase 6 to architecture — it does NOT remove Phase 4A from orchestration
- Orchestration Phase 4A removal is Feature 6 (separate story)
- Command routing update (/create-epic) is Feature 8 (separate story)

**Related ADRs:**
- [ADR-019: Skill Responsibility Restructure](../adrs/ADR-019-skill-responsibility-restructure.md)

**References:**
- EPIC-068 Feature 5: Lines 139-143
- Source: devforgeai/specs/context/tech-stack.md (skill size limits)

---

Story Template Version: 2.9
Last Updated: 2026-02-17
