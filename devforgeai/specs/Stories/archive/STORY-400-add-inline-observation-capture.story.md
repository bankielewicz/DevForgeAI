---
id: STORY-400
title: Add Inline Observation Capture to Phase State Updates
type: refactor
epic: EPIC-063
sprint: Backlog
status: QA Approved
priority: High
points: 3
created: 2026-02-08
updated: 2026-02-08
assignee: unassigned
tags: [framework, observations, tdd, phase-state, refactor]
source_recommendation: REC-STORY368-003
template_version: "2.8"
---

# STORY-400: Add Inline Observation Capture to Phase State Updates

## Description

Add observation capture steps after each TDD phase (02-08) completes in the devforgeai-development SKILL.md. Currently observations are ONLY captured in Phase 09 by the framework-analyst subagent, which means real-time insights from intermediate phases are lost by the time Phase 09 executes.

<!-- provenance>
  <origin document="EPIC-063" section="Feature 2">
    <quote>Currently observations are ONLY captured in Phase 09 by the framework-analyst subagent, which means real-time insights from intermediate phases are lost</quote>
    <line_reference>lines 138-201</line_reference>
  </origin>
  <decision rationale="Inline capture provides richer data for Phase 09 synthesis">
    <selected>Add observation capture after each phase (02-08)</selected>
    <rejected>Keep observations only in Phase 09</rejected>
    <trade_off>Richer data vs workflow complexity</trade_off>
  </decision>
</provenance -->

## User Story

**As a** DevForgeAI framework maintainer,
**I want** the devforgeai-development SKILL.md to include explicit inline observation capture steps after each TDD phase (02-08) completes,
**So that** real-time insights from subagent outputs are accumulated in phase-state.json during workflow execution rather than being lost before Phase 09's framework-analyst synthesizes recommendations.

## Acceptance Criteria

<acceptance_criteria id="AC1" title="Phase 02 (Red) observation capture from test-automator">
  <given>Phase 02 (Test-First) has completed and the test-automator subagent has returned output</given>
  <when>The phase completion flow executes the inline observation capture step</when>
  <then>Observations extracted from the test-automator output are appended to the `observations` array in `devforgeai/workflows/STORY-XXX-phase-state.json` with `phase: "02"` and `source: "test-automator"`</then>
  <verification>
    <method>Run /dev workflow, check phase-state.json after Phase 02</method>
    <expected_result>observations array contains entry with phase="02", source="test-automator"</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/skills/devforgeai-development/SKILL.md" hint="Phase Orchestration Loop"/>
    <file path="src/claude/skills/devforgeai-development/phases/phase-02-test-first.md" hint="test-automator invocation"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC2" title="Phase 03 (Green) observation capture from backend-architect">
  <given>Phase 03 (Implementation) has completed and the backend-architect subagent has returned output</given>
  <when>The phase completion flow executes the inline observation capture step</when>
  <then>Observations extracted from the backend-architect output are appended to the `observations` array in `devforgeai/workflows/STORY-XXX-phase-state.json` with `phase: "03"` and `source: "backend-architect"`</then>
  <verification>
    <method>Run /dev workflow, check phase-state.json after Phase 03</method>
    <expected_result>observations array contains entry with phase="03", source="backend-architect"</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/skills/devforgeai-development/SKILL.md" hint="Phase Orchestration Loop"/>
    <file path="src/claude/skills/devforgeai-development/phases/phase-03-implementation.md" hint="backend-architect invocation"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC3" title="Phase 04 (Refactor) observation capture from refactoring-specialist">
  <given>Phase 04 (Refactoring) has completed and the refactoring-specialist subagent has returned output</given>
  <when>The phase completion flow executes the inline observation capture step</when>
  <then>Observations extracted from the refactoring-specialist output are appended to the `observations` array in `devforgeai/workflows/STORY-XXX-phase-state.json` with `phase: "04"` and `source: "refactoring-specialist"`</then>
  <verification>
    <method>Run /dev workflow, check phase-state.json after Phase 04</method>
    <expected_result>observations array contains entry with phase="04", source="refactoring-specialist"</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/skills/devforgeai-development/SKILL.md" hint="Phase Orchestration Loop"/>
    <file path="src/claude/skills/devforgeai-development/phases/phase-04-refactoring.md" hint="refactoring-specialist invocation"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC4" title="Observation schema compliance">
  <given>An observation is captured from any phase (02 through 08)</given>
  <when>The observation entry is appended to the phase-state.json `observations` array</when>
  <then>The entry contains all required fields: `phase` (string), `source` (string matching subagent name), `type` (one of "friction", "success", "gap", "idea"), `content` (string, max 200 chars), and `timestamp` (ISO 8601 format)</then>
  <verification>
    <method>Validate observation entries against JSON schema</method>
    <expected_result>All entries pass schema validation</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/skills/devforgeai-development/references/observation-capture.md" hint="Schema definition"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC5" title="Phase 09 framework-analyst reads accumulated observations">
  <given>Phases 02 through 08 have completed and observations have been accumulated in phase-state.json</given>
  <when>Phase 09 executes and the framework-analyst subagent is invoked</when>
  <then>The framework-analyst receives and processes the accumulated observations array from phase-state.json without any changes to the existing Phase 09 workflow</then>
  <verification>
    <method>Run complete /dev workflow, verify Phase 09 output references accumulated observations</method>
    <expected_result>framework-analyst synthesizes recommendations from accumulated observations</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/skills/devforgeai-development/phases/phase-09-feedback.md" hint="Must remain unchanged"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC6" title="Backward compatibility with empty observations array">
  <given>A phase-state.json file created by a prior version that has an empty `observations` array or no `observations` field</given>
  <when>The inline observation capture step attempts to append observations</when>
  <then>The capture step initializes the `observations` array if absent, appends normally, and does not throw errors or halt the workflow</then>
  <verification>
    <method>Run /dev on story with legacy phase-state.json (no observations field)</method>
    <expected_result>Workflow completes, observations array created and populated</expected_result>
  </verification>
  <source_files>
    <file path="devforgeai/workflows/STORY-370-phase-state.json" hint="Example with empty observations"/>
  </source_files>
</acceptance_criteria>

## Technical Specification

### Component Overview

| Component | Type | Description |
|-----------|------|-------------|
| SKILL.md | Configuration | Main development skill orchestration file |
| phase-state.json | DataModel | Workflow state storage with observations array |

### Technical Details

```yaml
technical_specification:
  version: "2.0"
  components:
    - type: Configuration
      name: Inline Observation Capture Steps
      file_path: src/claude/skills/devforgeai-development/SKILL.md
      description: Add observation capture instruction blocks to Phase Orchestration Loop
      dependencies:
        - devforgeai/workflows/STORY-XXX-phase-state.json (observations array)
        - src/claude/skills/devforgeai-development/references/observation-capture.md (schema)
        - observation-extractor subagent (optional - for complex extraction)
      extraction_method: >
        Extract observations by analyzing the subagent's Task() return value. Look for
        friction points (errors, retries, workarounds), success patterns (clean execution,
        reusable approaches), coverage gaps (missing tests, uncovered paths), and improvement
        ideas. Append as structured JSON entries to phase-state.json observations array.
      test_requirement: After Phase 02 completes, phase-state.json observations array contains at least one entry with phase="02"

  business_rules:
    - rule: Phase-to-subagent mapping
      description: |
        Phase 02 -> test-automator
        Phase 03 -> backend-architect
        Phase 04 -> refactoring-specialist
        Phase 04.5 -> ac-compliance-verifier
        Phase 05 -> integration-tester
        Phase 05.5 -> ac-compliance-verifier
        Phase 06 -> deferral-validator
        Phase 07 -> skip (no subagent)
        Phase 08 -> skip (no subagent)
      test_requirement: Each phase maps to correct subagent in observations

    - rule: Observation type enum
      description: >
        Type must be one of friction, success, gap, idea.
        These 4 types are the standard categories for inline phase observation capture.
        The framework-analyst in Phase 09 may use additional categories during its deeper analysis.
      test_requirement: All observation entries have valid type values

    - rule: Non-blocking capture
      description: Observation capture failures must not halt TDD workflow
      test_requirement: Simulated capture failure allows exit gate to proceed

  non_functional_requirements:
    - category: Performance
      requirement: Observation capture adds minimal overhead
      metric: < 2 seconds per phase
      test_requirement: Measure phase completion time with and without capture

    - category: Reliability
      requirement: Non-blocking capture with graceful degradation
      metric: 0 workflow halts due to observation capture failures
      test_requirement: Workflow completes even when capture fails

    - category: Scalability
      requirement: Support up to 50 observations per workflow
      metric: No parse time degradation up to 50 entries
      test_requirement: Benchmark with 50 observations
```

### Observation Schema

```json
{
  "phase": "02",
  "source": "test-automator",
  "type": "friction|success|gap|idea",  // Standard inline capture types (subset of full observation taxonomy)
  "content": "Description of the observation (max 200 chars)",
  "timestamp": "2026-02-08T10:00:00Z"
}
```

### Files to Modify

| File | Action | Description |
|------|--------|-------------|
| `src/claude/skills/devforgeai-development/SKILL.md` | Edit | Add observation capture steps to Phase Orchestration Loop |

### Phase-to-Subagent Mapping

| Phase | Subagent | Capture Observations |
|-------|----------|---------------------|
| Phase 02 (Red) | test-automator | Yes |
| Phase 03 (Green) | backend-architect | Yes |
| Phase 04 (Refactor) | refactoring-specialist | Yes |
| Phase 04.5 (AC Verify) | ac-compliance-verifier | Yes |
| Phase 05 (Integration) | integration-tester | Yes |
| Phase 05.5 (AC Verify) | ac-compliance-verifier | Yes |
| Phase 06 (Deferral) | deferral-validator | Yes (if deferrals exist) |
| Phase 07 (DoD Update) | None | No (skip) |
| Phase 08 (Git) | None | No (skip) |

## Edge Cases

1. **Phase produces no extractable observations:** Skip appending without error. Zero observations for a phase is valid.

2. **Phase 04.5 and 05.5 dual capture:** Both use ac-compliance-verifier. Use distinct `phase` values ("4.5" and "5.5") to differentiate.

3. **Phase 06 conditional subagent:** Only invokes deferral-validator if deferrals exist. Skip gracefully if no subagent output.

4. **Phases 07 and 08 have no subagents:** Skip observation capture entirely for these phases.

5. **Phase-state.json write failure:** Log warning and proceed. Observation loss is acceptable; halting TDD workflow is not.

6. **Content exceeds 200 characters:** Truncate to 200 characters with ellipsis.

7. **Remediation mode skips phases:** When `$REMEDIATION_MODE == true`, phases 02-08 are skipped. No observation capture for skipped phases.

## Non-Functional Requirements

| Category | Requirement | Metric |
|----------|-------------|--------|
| Performance | Observation capture overhead | < 2 seconds per phase |
| Reliability | Non-blocking capture | 0 workflow halts from capture failures |
| Scalability | Support observation volume | Up to 50 observations per workflow |

## Definition of Done

### Implementation
- [x] Observation capture instruction block added to SKILL.md Phase Orchestration Loop
- [x] Phase-to-subagent mapping table documented in SKILL.md
- [x] Observation capture marked as non-blocking in orchestration flow
- [x] Observation count indicator added to Phase Completion Self-Check Displays

### Quality
- [x] Observation schema matches documented format
- [x] Backward compatibility with empty/missing observations array
- [x] Existing Phase 09 framework-analyst workflow unchanged

### Testing
- [x] Phase 02 capture produces valid observation entry
- [x] Phase 03 capture produces valid observation entry
- [x] Phase 04 capture produces valid observation entry
- [x] All observations have valid schema (phase, source, type, content, timestamp)
- [x] Phase 09 can read and process accumulated observations
- [x] Capture failure does not halt workflow

### Documentation
- [x] Phase-to-subagent mapping documented in SKILL.md

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-09
**Branch:** main

- [x] Observation capture instruction block added to SKILL.md Phase Orchestration Loop - Completed: Added lines 752-789 with capture workflow pseudocode
- [x] Phase-to-subagent mapping table documented in SKILL.md - Completed: Added lines 714-726 with complete phase mapping
- [x] Observation capture marked as non-blocking in orchestration flow - Completed: Added lines 791-802 with TRY/CATCH pattern
- [x] Observation count indicator added to Phase Completion Self-Check Displays - Completed: Added to display template at line 219
- [x] Observation schema matches documented format - Completed: Schema at lines 693-712
- [x] Backward compatibility with empty/missing observations array - Completed: Lines 774-776 and 804-810
- [x] Existing Phase 09 framework-analyst workflow unchanged - Completed: New section integrates without modifying Phase 09
- [x] Phase 02 capture produces valid observation entry - Completed: Test AC1 passes (4/4 assertions)
- [x] Phase 03 capture produces valid observation entry - Completed: Test AC2 passes (2/2 assertions)
- [x] Phase 04 capture produces valid observation entry - Completed: Test AC3 passes (2/2 assertions)
- [x] All observations have valid schema (phase, source, type, content, timestamp) - Completed: Test AC4 passes (6/6 assertions)
- [x] Phase 09 can read and process accumulated observations - Completed: Test AC5 passes (3/3 assertions)
- [x] Capture failure does not halt workflow - Completed: Test AC6 passes (3/3 assertions)
- [x] Phase-to-subagent mapping documented in SKILL.md - Completed: Mapping table at lines 714-726

### Additional Notes

Added "Inline Observation Capture (STORY-400)" section to SKILL.md with complete observation capture workflow for TDD phases 02-08. The implementation includes observation schema, phase-to-subagent mapping, non-blocking capture behavior, backward compatibility, and Phase 09 framework-analyst integration.

Code-reviewer noted field naming difference (type/content vs category/note) - intentional per story spec line 169-173 which defines simplified 4-type enum for inline capture. All 6 ACs pass with 20/20 test assertions.

## Notes

- **Source Recommendation:** REC-STORY368-003 from STORY-368 Phase 09 framework-analyst analysis
- **Root Cause:** Observations only captured in Phase 09, losing real-time insights
- **Impact:** Richer data for framework-analyst synthesis

## Key References

| Reference | Path | Relevance |
|-----------|------|-----------|
| Observation Capture Protocol | `src/claude/skills/devforgeai-development/references/observation-capture.md` | Schema and category definitions |
| Phase 09 Feedback | `src/claude/skills/devforgeai-development/phases/phase-09-feedback.md` | Existing workflow (must remain unchanged) |
| Example Phase State | `devforgeai/workflows/STORY-370-phase-state.json` | Shows empty observations array |

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-08 | claude/opus | Story Creation | Initial story created from EPIC-063 Feature 2 | STORY-400-add-inline-observation-capture.story.md |
| 2026-02-09 | claude/opus | Dev Complete | Implemented inline observation capture with 6/6 ACs passing | SKILL.md, story file |
| 2026-02-09 | .claude/qa-result-interpreter | QA Deep | PASSED: 100% traceability, 0 violations, 2/2 validators | story file |
