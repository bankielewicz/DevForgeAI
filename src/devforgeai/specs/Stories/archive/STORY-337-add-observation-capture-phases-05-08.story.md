---
id: STORY-337
title: Add Observation Capture to Phases 05-08 (Post-TDD)
type: feature
epic: EPIC-051
sprint: Sprint-2
status: QA Approved
points: 4
depends_on: ["STORY-336"]
priority: High
assigned_to: TBD
created: 2026-01-30
format_version: "2.7"
---

# Story: Add Observation Capture to Phases 05-08 (Post-TDD)

## Description

**As a** Framework Owner,
**I want** phases 05 (Integration), 06 (Deferral), 07 (DoD Update), and 08 (Git Workflow) to automatically capture observations from subagent outputs at phase exit gates,
**so that** phase-state.json is populated with actionable insights from the post-TDD workflow phases, completing the observation capture coverage for the entire /dev lifecycle.

## Provenance

```xml
<provenance>
  <origin document="EPIC-051" section="Feature 3: Phase State Integration">
    <quote>"Files to Modify: phase-05-integration.md, phase-06-deferral.md, phase-07-dod-update.md, phase-08-git-workflow.md - Add observation capture before exit"</quote>
    <line_reference>lines 148-152</line_reference>
    <quantified_impact>Completes observation capture for 100% of /dev workflow phases (02-08)</quantified_impact>
  </origin>

  <decision rationale="complete-phase-coverage">
    <selected>Cover all post-TDD phases (05-08) in a single story</selected>
    <rejected alternative="individual-story-per-phase">Would create 4 tiny stories with redundant structure</rejected>
    <trade_off>Larger story but logical grouping of post-TDD phases</trade_off>
  </decision>

  <stakeholder role="Framework Owner" goal="complete-observation-coverage">
    <quote>"I want phase-state.json to contain all observations from a story's lifecycle"</quote>
    <source>EPIC-051, User Stories section</source>
  </stakeholder>

  <hypothesis id="H1" validation="observation-population" success_criteria="100% of /dev phases capture observations">
    Completing observation capture for phases 05-08 will ensure full lifecycle observation coverage
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Phase 05 Observation Capture at Exit Gate

```xml
<acceptance_criteria id="AC1" implements="FR-4">
  <given>Phase 05 (Integration & Validation) is completing and subagents (integration-tester, ac-compliance-verifier) have returned outputs</given>
  <when>The phase exit gate is reached before transitioning to Phase 06</when>
  <then>An "Observation Capture (EPIC-051)" section is executed that: (1) collects explicit observations from subagent returns if observations[] present, (2) invokes observation-extractor for implicit observations from integration-tester and ac-compliance-verifier outputs, (3) appends observations to phase-state.json observations[] array with unique IDs (OBS-05-{timestamp})</then>
  <verification>
    <source_files>
      <file hint="Phase 05 file">.claude/skills/devforgeai-development/phases/phase-05-integration.md</file>
      <file hint="Source copy">src/claude/skills/devforgeai-development/phases/phase-05-integration.md</file>
    </source_files>
    <test_file>tests/STORY-337/test_ac1_phase05_observation_capture.sh</test_file>
    <coverage_threshold>100</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Phase 06 Observation Capture at Exit Gate

```xml
<acceptance_criteria id="AC2" implements="FR-4">
  <given>Phase 06 (Deferral Challenge) is completing and deferral decisions have been made</given>
  <when>The phase exit gate is reached before transitioning to Phase 07</when>
  <then>An "Observation Capture (EPIC-051)" section is executed that: (1) captures observations about deferred items (category: gap, severity: medium/high based on deferral impact), (2) invokes observation-extractor for implicit observations, (3) appends observations to phase-state.json observations[] array with unique IDs (OBS-06-{timestamp})</then>
  <verification>
    <source_files>
      <file hint="Phase 06 file">.claude/skills/devforgeai-development/phases/phase-06-deferral.md</file>
      <file hint="Source copy">src/claude/skills/devforgeai-development/phases/phase-06-deferral.md</file>
    </source_files>
    <test_file>tests/STORY-337/test_ac2_phase06_observation_capture.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Phase 07 Observation Capture at Exit Gate

```xml
<acceptance_criteria id="AC3" implements="FR-4">
  <given>Phase 07 (DoD Update) is completing and Definition of Done items have been updated</given>
  <when>The phase exit gate is reached before transitioning to Phase 08</when>
  <then>An "Observation Capture (EPIC-051)" section is executed that: (1) captures observations about DoD completion status (category: success for completed, gap for unchecked items), (2) appends observations to phase-state.json observations[] array with unique IDs (OBS-07-{timestamp})</then>
  <verification>
    <source_files>
      <file hint="Phase 07 file">.claude/skills/devforgeai-development/phases/phase-07-dod-update.md</file>
      <file hint="Source copy">src/claude/skills/devforgeai-development/phases/phase-07-dod-update.md</file>
    </source_files>
    <test_file>tests/STORY-337/test_ac3_phase07_observation_capture.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Phase 08 Observation Capture at Exit Gate

```xml
<acceptance_criteria id="AC4" implements="FR-4">
  <given>Phase 08 (Git Workflow) is completing and git commit/branch operations have been performed</given>
  <when>The phase exit gate is reached before transitioning to Phase 09</when>
  <then>An "Observation Capture (EPIC-051)" section is executed that: (1) captures observations about git operations (category: success for clean commit, friction for issues encountered), (2) invokes observation-extractor for git-validator output if present, (3) appends observations to phase-state.json observations[] array with unique IDs (OBS-08-{timestamp})</then>
  <verification>
    <source_files>
      <file hint="Phase 08 file">.claude/skills/devforgeai-development/phases/phase-08-git-workflow.md</file>
      <file hint="Source copy">src/claude/skills/devforgeai-development/phases/phase-08-git-workflow.md</file>
    </source_files>
    <test_file>tests/STORY-337/test_ac4_phase08_observation_capture.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Consistent Section Structure Across All 4 Phases

```xml
<acceptance_criteria id="AC5" implements="NFR-MAINTAINABILITY">
  <given>Phases 05, 06, 07, and 08 all have observation capture sections added</given>
  <when>A developer compares the observation capture sections across all 4 phase files</when>
  <then>All 4 sections use the identical template structure from STORY-336, with only phase-specific details (phase number, subagent names) varying, ensuring consistency with phases 02-04 from STORY-336</then>
  <verification>
    <source_files>
      <file hint="Phase 05">.claude/skills/devforgeai-development/phases/phase-05-integration.md</file>
      <file hint="Phase 06">.claude/skills/devforgeai-development/phases/phase-06-deferral.md</file>
      <file hint="Phase 07">.claude/skills/devforgeai-development/phases/phase-07-dod-update.md</file>
      <file hint="Phase 08">.claude/skills/devforgeai-development/phases/phase-08-git-workflow.md</file>
    </source_files>
    <test_file>tests/STORY-337/test_ac5_consistent_structure.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Full Lifecycle Observation Coverage Verification

```xml
<acceptance_criteria id="AC6" implements="FR-4,EPIC-051-SUCCESS">
  <given>A complete /dev workflow has executed phases 02 through 08</given>
  <when>Phase-state.json is examined after Phase 08 completion</when>
  <then>The observations[] array contains observations from all 7 phases (02-08), with phase numbers clearly identifying the source phase, demonstrating 100% lifecycle observation coverage</then>
  <verification>
    <source_files>
      <file hint="Phase state file">devforgeai/workflows/{STORY-ID}-phase-state.json</file>
    </source_files>
    <test_file>tests/STORY-337/test_ac6_full_lifecycle_coverage.sh</test_file>
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
      name: "phase-05-integration.md observation section"
      file_path: ".claude/skills/devforgeai-development/phases/phase-05-integration.md"
      purpose: "Add observation capture at Phase 05 exit gate"
      required_keys:
        - key: "Observation Capture section header"
          type: "markdown_section"
          required: true
          example: "### Observation Capture (EPIC-051)"
          test_requirement: "Test: Section header exists"
        - key: "integration-tester observation handling"
          type: "instruction"
          required: true
          test_requirement: "Test: integration-tester subagent referenced"
        - key: "ac-compliance-verifier observation handling"
          type: "instruction"
          required: true
          test_requirement: "Test: ac-compliance-verifier subagent referenced"
      requirements:
        - id: "P05-001"
          description: "Section handles both integration-tester and ac-compliance-verifier outputs"
          testable: true
          test_requirement: "Test: Both subagents mentioned in section"
          priority: "Critical"

    - type: "Configuration"
      name: "phase-06-deferral.md observation section"
      file_path: ".claude/skills/devforgeai-development/phases/phase-06-deferral.md"
      purpose: "Add observation capture at Phase 06 exit gate"
      required_keys:
        - key: "Observation Capture section header"
          type: "markdown_section"
          required: true
          test_requirement: "Test: Section header exists"
        - key: "Deferral observation handling"
          type: "instruction"
          required: true
          test_requirement: "Test: Deferred items captured as observations"
      requirements:
        - id: "P06-001"
          description: "Deferred items captured with category: gap"
          testable: true
          test_requirement: "Test: Gap category used for deferrals"
          priority: "High"

    - type: "Configuration"
      name: "phase-07-dod-update.md observation section"
      file_path: ".claude/skills/devforgeai-development/phases/phase-07-dod-update.md"
      purpose: "Add observation capture at Phase 07 exit gate"
      required_keys:
        - key: "Observation Capture section header"
          type: "markdown_section"
          required: true
          test_requirement: "Test: Section header exists"
        - key: "DoD completion observation"
          type: "instruction"
          required: true
          test_requirement: "Test: DoD status captured"
      requirements:
        - id: "P07-001"
          description: "DoD completion status captured as observation"
          testable: true
          test_requirement: "Test: Success/gap categories based on DoD status"
          priority: "High"

    - type: "Configuration"
      name: "phase-08-git-workflow.md observation section"
      file_path: ".claude/skills/devforgeai-development/phases/phase-08-git-workflow.md"
      purpose: "Add observation capture at Phase 08 exit gate"
      required_keys:
        - key: "Observation Capture section header"
          type: "markdown_section"
          required: true
          test_requirement: "Test: Section header exists"
        - key: "Git operation observation"
          type: "instruction"
          required: true
          test_requirement: "Test: Git operations captured"
      requirements:
        - id: "P08-001"
          description: "Git operations captured with success/friction categories"
          testable: true
          test_requirement: "Test: Appropriate category based on git outcome"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Observation capture must not block phase progression"
      trigger: "When observation capture encounters an error"
      validation: "Phase continues even if observation capture fails"
      error_handling: "Log error, continue with phase completion"
      test_requirement: "Test: Phase completes even if observation capture fails"
      priority: "Critical"
    - id: "BR-002"
      rule: "Deferral observations use gap category with medium/high severity"
      trigger: "When Phase 06 captures deferral decisions"
      validation: "Category is 'gap', severity based on deferral impact"
      error_handling: "Default to medium severity if impact unclear"
      test_requirement: "Test: Deferral observations have correct category/severity"
      priority: "High"
    - id: "BR-003"
      rule: "DoD observations reflect actual completion status"
      trigger: "When Phase 07 captures DoD update"
      validation: "Success for checked items, gap for unchecked"
      error_handling: "If status unclear, use warning category"
      test_requirement: "Test: DoD observations match actual status"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Observation capture adds <100ms per phase"
      metric: "Time from observation collection start to phase-state.json write complete"
      test_requirement: "Test: Measure observation capture duration"
      priority: "High"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Observation capture never causes phase failure"
      metric: "0 phase failures due to observation capture errors"
      test_requirement: "Test: Phase completes regardless of observation capture status"
      priority: "Critical"
    - id: "NFR-003"
      category: "Maintainability"
      requirement: "Identical section structure with phases 02-04"
      metric: "Template pattern consistent across all 7 phases (02-08)"
      test_requirement: "Test: Structure matches STORY-336 template"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations: []
# No technical limitations identified - follows established pattern from STORY-336
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Execution Speed:**
- Observation capture: < 100ms per phase (same as STORY-336)
- No blocking calls to external services

---

### Security

**No sensitive data:** Observations must not contain git credentials or sensitive commit messages
**Safe defaults:** If observation content appears sensitive, skip capture with warning

---

### Reliability

**Graceful degradation:** If observation capture fails, phase continues normally
**Pattern consistency:** Uses same error handling as STORY-336 phases

---

### Maintainability

**Template pattern:** All 4 phases use identical observation capture section structure from STORY-336
**Documentation consistency:** Comments reference EPIC-051 in all phases

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-336:** Add Observation Capture to Phases 02-04
  - **Why:** Establishes the template pattern for observation capture sections
  - **Status:** Backlog (must complete first to establish pattern)

### External Dependencies

- [ ] **None** - Framework-internal only

### Technology Dependencies

- [ ] **None** - Uses existing phase file and JSON patterns

---

## Test Strategy

### Unit Tests

**Coverage Target:** 100% of acceptance criteria

**Test Scenarios:**
1. **AC1 - Phase 05:** Verify observation capture for integration-tester and ac-compliance-verifier
2. **AC2 - Phase 06:** Verify deferral observations with gap category
3. **AC3 - Phase 07:** Verify DoD status observations
4. **AC4 - Phase 08:** Verify git operation observations
5. **AC5 - Consistency:** Verify identical structure across all 4 phases
6. **AC6 - Full Coverage:** Verify observations from all 7 phases (02-08)

### Edge Cases

1. **No deferrals in Phase 06:** Phase captures nothing (empty observation)
2. **All DoD items checked in Phase 07:** Success observations only
3. **Git commit fails in Phase 08:** Friction observation captured
4. **Phase skipped (documentation type):** Observation capture still runs
5. **Integration test failures:** Captured as gap observations in Phase 05

---

## Acceptance Criteria Verification Checklist

### AC#1: Phase 05 Observation Capture

- [x] Observation Capture section exists in phase-05-integration.md - **Phase:** 3 - **Evidence:** Test passed
- [x] integration-tester observations handled - **Phase:** 3 - **Evidence:** Test passed
- [x] ac-compliance-verifier observations handled - **Phase:** 3 - **Evidence:** Test passed

### AC#2: Phase 06 Observation Capture

- [x] Observation Capture section exists in phase-06-deferral.md - **Phase:** 3 - **Evidence:** Test passed
- [x] Deferrals captured as gap category - **Phase:** 3 - **Evidence:** Test passed

### AC#3: Phase 07 Observation Capture

- [x] Observation Capture section exists in phase-07-dod-update.md - **Phase:** 3 - **Evidence:** Test passed
- [x] DoD status captured - **Phase:** 3 - **Evidence:** Test passed

### AC#4: Phase 08 Observation Capture

- [x] Observation Capture section exists in phase-08-git-workflow.md - **Phase:** 3 - **Evidence:** Test passed
- [x] Git operations captured - **Phase:** 3 - **Evidence:** Test passed

### AC#5: Consistent Structure

- [x] All 4 phases use identical template - **Phase:** 4 - **Evidence:** Test AC5 passed - all phases follow identical template
- [x] Consistency with STORY-336 phases - **Phase:** 4 - **Evidence:** Test AC5 passed - template match verified

### AC#6: Full Lifecycle Coverage

- [x] Observations from phases 02-08 present - **Phase:** 5 - **Evidence:** Test AC6 passed - all 7 phases verified
- [x] Phase numbers identify sources - **Phase:** 5 - **Evidence:** Test AC6 passed - OBS-NN patterns verified

---

**Checklist Progress:** 14/14 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Phase 05 observation capture section added
- [x] Phase 06 observation capture section added
- [x] Phase 07 observation capture section added
- [x] Phase 08 observation capture section added
- [x] All sections match STORY-336 template pattern

### Quality
- [x] All 6 acceptance criteria have passing tests
- [x] Edge cases handled (no deferrals, all DoD checked, git failures)
- [x] Observation capture doesn't block phase progression
- [x] <100ms performance requirement met (file edits only)

### Testing
- [x] Test: Phase 05 observation capture
- [x] Test: Phase 06 observation capture
- [x] Test: Phase 07 observation capture
- [x] Test: Phase 08 observation capture
- [x] Test: Consistent structure
- [x] Test: Full lifecycle coverage

### Documentation
- [x] All 4 phase files updated in both src/ and .claude/

---

## Implementation Notes

- [x] Phase 05 observation capture section added - Completed: 2026-02-01
- [x] Phase 06 observation capture section added - Completed: 2026-02-01
- [x] Phase 07 observation capture section added - Completed: 2026-02-01
- [x] Phase 08 observation capture section added - Completed: 2026-02-01
- [x] All sections match STORY-336 template pattern - Completed: 2026-02-01
- [x] All 6 acceptance criteria have passing tests - Completed: 2026-02-01
- [x] Edge cases handled (no deferrals, all DoD checked, git failures) - Completed: 2026-02-01
- [x] Observation capture doesn't block phase progression - Completed: 2026-02-01
- [x] <100ms performance requirement met - Completed: 2026-02-01
- [x] Test: Phase 05 observation capture - Completed: 2026-02-01
- [x] Test: Phase 06 observation capture - Completed: 2026-02-01
- [x] Test: Phase 07 observation capture - Completed: 2026-02-01
- [x] Test: Phase 08 observation capture - Completed: 2026-02-01
- [x] Test: Consistent structure - Completed: 2026-02-01
- [x] Test: Full lifecycle coverage - Completed: 2026-02-01
- [x] All 4 phase files updated in both src/ and .claude/ - Completed: 2026-02-01

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-01

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-30 11:15 | claude/story-requirements-analyst | Created | Story created from EPIC-051 Feature 3 (phases 05-08) | STORY-337.story.md |
| 2026-02-01 | claude/qa-result-interpreter | QA Deep | PASSED: 6/6 tests, 0 violations, 100% traceability | STORY-337-qa-report.md |

## Notes

**Design Decisions:**
- Combined phases 05-08 into single story (4 smaller phases vs 3 TDD-core phases)
- Deferral observations use gap category (represents incomplete work)
- DoD observations reflect actual checkbox status
- Git observations capture success/friction for commit operations

**Phase-Specific Observation Categories:**
- **Phase 05 (Integration):** success, gap, friction (from integration tests)
- **Phase 06 (Deferral):** gap (for deferred items), warning (for risky deferrals)
- **Phase 07 (DoD Update):** success (checked items), gap (unchecked items)
- **Phase 08 (Git Workflow):** success (clean commit), friction (commit issues)

**Related Stories:**
- STORY-336: Phase 02-04 observation capture (prerequisite, establishes pattern)
- STORY-318: Subagent observation schema (transitive dependency)
- STORY-319: Observation extractor subagent (transitive dependency)

**References:**
- EPIC-051: Framework Feedback Capture System
- BRAINSTORM-007: Feedback System Visibility

---

Story Template Version: 2.7
Last Updated: 2026-01-30
