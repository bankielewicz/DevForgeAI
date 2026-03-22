---
id: STORY-561
title: Gate 0S ADR Acceptance and Quality Gates Reference Update
type: documentation
epic: EPIC-088
sprint: Sprint-31
status: Ready for Dev
points: 3
depends_on: []
priority: High
advisory: false
assigned_to: null
created: 2026-03-22
format_version: "2.9"
---

# STORY-561: Gate 0S ADR Acceptance and Quality Gates Reference Update

## Description

**As a** DevForgeAI framework maintainer,
**I want** Gate 0S (Sprint Planning Quality Gate) to be formally documented in the quality gates reference and rules summary, with ADR-046 verified through TDD,
**so that** the sprint planning validation checks (dependency chains, cycle detection, file overlaps, feature cohesion) are discoverable, enforceable, and architecturally grounded alongside Gates 1-4.

## Provenance

<provenance>
  <origin type="research">RESEARCH-002 (Epic vs Sprint in the SDLC)</origin>
  <decision>ADR-046 establishes Gate 0S for sprint planning validation</decision>
  <stakeholder>Project Owner — decision authority on gate strictness</stakeholder>
  <hypothesis>Adding quality gates to sprint planning prevents incomplete feature releases</hypothesis>
</provenance>

## Acceptance Criteria

### AC#1: ADR-046 exists and passes structural TDD verification

<acceptance_criteria id="AC#1" title="ADR-046 exists and passes structural TDD verification">
  <given>ADR-046 exists at devforgeai/specs/adrs/ADR-046-sprint-planning-quality-gate.md</given>
  <when>a TDD test verifies the ADR file for required structural elements (Status: Accepted, Context section, Decision section, Consequences section, References section, Gate 0S naming, and bypassable gate property)</when>
  <then>the test passes confirming ADR-046 contains all required ADR sections, references Gate 0S by name, documents the 3 new steps (2.5, 2.6, 2.7), specifies the gate as bypassable with user approval, and lists the gate hierarchy showing Gate 0S before Gate 1</then>
  <verification>
    <source_files>devforgeai/specs/adrs/ADR-046-sprint-planning-quality-gate.md</source_files>
    <test_file>tests/STORY-561/test_ac1_adr_structure.sh</test_file>
  </verification>
</acceptance_criteria>

### AC#2: Gate 0S section added to quality-gates.md reference before Gate 1

<acceptance_criteria id="AC#2" title="Gate 0S section added to quality-gates.md reference before Gate 1">
  <given>the quality gates reference at src/claude/skills/spec-driven-lifecycle/references/quality-gates.md documents Gates 1-4</given>
  <when>Gate 0S documentation is added as a new section BEFORE the Gate 1 section and the Gate Hierarchy overview is updated</when>
  <then>the quality-gates.md file contains a Gate 0S section with: Purpose, Location in Workflow, When Evaluated, Pass Criteria with 4 checks (dependency chain, cycle detection, file overlap, feature cohesion + multi-sprint), Failure Actions, and Bypass Mechanism, AND the Gate Hierarchy diagram is updated to show Gate 0S above Gate 1</then>
  <verification>
    <source_files>src/claude/skills/spec-driven-lifecycle/references/quality-gates.md</source_files>
    <test_file>tests/STORY-561/test_ac2_quality_gates_reference.sh</test_file>
  </verification>
</acceptance_criteria>

### AC#3: Quality gates rule summary updated with Gate 0S

<acceptance_criteria id="AC#3" title="Quality gates rule summary updated with Gate 0S">
  <given>the quality gates rule at .claude/rules/core/quality-gates.md contains a summary of Gates 1-4</given>
  <when>a Gate 0S entry is added before the Gate 1 entry in the rule summary</when>
  <then>the file contains a Gate 0S section with Transition (Story Selection to Sprint Creation), Enforced By (spec-driven-lifecycle / Phase 03S), and Requirements listing the 4 checks</then>
  <verification>
    <source_files>.claude/rules/core/quality-gates.md</source_files>
    <test_file>tests/STORY-561/test_ac3_quality_gates_rule.sh</test_file>
  </verification>
</acceptance_criteria>

### AC#4: TDD tests verify all three documentation artifacts

<acceptance_criteria id="AC#4" title="TDD tests verify all three documentation artifacts">
  <given>the three documentation files have been updated</given>
  <when>TDD tests run against the src/ tree</when>
  <then>tests confirm: (1) ADR-046 contains "Gate 0S" and "Status: Accepted", (2) quality-gates.md reference contains "Gate 0S" heading before "Gate 1", (3) rule summary contains "Gate 0S" before "Gate 1", (4) Gate Hierarchy includes "Gate 0S", (5) all 4 checks documented</then>
  <verification>
    <test_file>tests/STORY-561/test_ac4_all_artifacts.sh</test_file>
  </verification>
</acceptance_criteria>

### AC#5: Gate 0S documentation references correct enforcement points

<acceptance_criteria id="AC#5" title="Gate 0S documentation references correct enforcement points">
  <given>Gate 0S is enforced within Phase 03S using existing subagents</given>
  <when>the Gate 0S documentation in quality-gates.md reference is reviewed</when>
  <then>documentation references: (1) Phase 03S as enforcement location, (2) dependency-graph-analyzer subagent, (3) file-overlap-detector subagent, (4) epic Target Sprints section for cohesion, (5) ADR-046 as the decision record</then>
  <verification>
    <source_files>src/claude/skills/spec-driven-lifecycle/references/quality-gates.md</source_files>
    <test_file>tests/STORY-561/test_ac5_enforcement_references.sh</test_file>
  </verification>
</acceptance_criteria>

## Technical Specification

```yaml
technical_specification:
  components:
    - name: "ADR-046 Verification"
      type: "configuration"
      file_path: "devforgeai/specs/adrs/ADR-046-sprint-planning-quality-gate.md"
      action: "verify"
      description: "Verify ADR-046 exists with required structural elements"

    - name: "Quality Gates Reference Update"
      type: "configuration"
      file_path: "src/claude/skills/spec-driven-lifecycle/references/quality-gates.md"
      action: "edit"
      description: "Add Gate 0S section before Gate 1, update Gate Hierarchy diagram"

    - name: "Quality Gates Rule Summary Update"
      type: "configuration"
      file_path: ".claude/rules/core/quality-gates.md"
      action: "edit"
      description: "Add Gate 0S entry before Gate 1 in summary"

  test_files:
    - path: "tests/STORY-561/test_ac1_adr_structure.sh"
      type: "unit"
      target_ac: "AC#1"
    - path: "tests/STORY-561/test_ac2_quality_gates_reference.sh"
      type: "unit"
      target_ac: "AC#2"
    - path: "tests/STORY-561/test_ac3_quality_gates_rule.sh"
      type: "unit"
      target_ac: "AC#3"
    - path: "tests/STORY-561/test_ac4_all_artifacts.sh"
      type: "unit"
      target_ac: "AC#4"
    - path: "tests/STORY-561/test_ac5_enforcement_references.sh"
      type: "unit"
      target_ac: "AC#5"
```

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "quality-gates.md reference"
    limitation: "Gate 0S section insertion point depends on current Gate 1 heading text"
    decision: "Use heading-based section detection, not hardcoded line numbers"
    discovered_phase: "planning"
    impact: "Tests must tolerate content growth in quality-gates.md"
```

## Non-Functional Requirements (NFRs)

### Performance
- TDD test suite executes in < 10 seconds (file-read verification only)
- No build step required (documentation changes only)

### Security
- No secrets or credentials in any documentation file
- No executable code in documentation (pseudocode in fenced code blocks only)

### Reliability
- All 3 documentation files remain valid Markdown after edits
- Gate 0S documentation is self-contained (readable without ADR-046)
- Tests use heading-based detection, not hardcoded line numbers

### Scalability
- Gate 0S follows same structural pattern as Gates 1-4, enabling future gates

## Dependencies

### Prerequisite Stories
- None (this is the foundation story)

### External Dependencies
- ADR-046 exists on disk (pre-created during planning)

### Technology Dependencies
- Bash (test scripts)
- Grep (heading detection in tests)

## Test Strategy

### Unit Tests
- AC#1: Verify ADR-046 structure (grep for required sections)
- AC#2: Verify Gate 0S in quality-gates.md reference (heading order validation)
- AC#3: Verify Gate 0S in quality-gates rule (heading order validation)
- AC#4: Cross-file verification of all artifacts
- AC#5: Enforcement reference validation (grep for agent names)

### Integration Tests
- N/A (documentation story — Phase 05 Integration skipped per story type)

## AC Verification Checklist

- [ ] AC#1: ADR-046 structural verification passes
- [ ] AC#2: Gate 0S section in quality-gates.md reference before Gate 1
- [ ] AC#3: Gate 0S entry in quality-gates rule summary before Gate 1
- [ ] AC#4: All three artifacts verified by TDD tests
- [ ] AC#5: Enforcement point references validated

## Definition of Done

- [ ] ADR-046 verified to contain all required sections
- [ ] Gate 0S section added to quality-gates.md reference before Gate 1
- [ ] Gate Hierarchy diagram updated to include Gate 0S
- [ ] Quality-gates rule summary updated with Gate 0S entry
- [ ] All TDD tests written and passing
- [ ] No context files modified (immutability guard)
- [ ] Story file updated with Implementation Notes

## Implementation Guide

This section provides the exact content a fresh Claude session needs to implement this story without interpretation.

### Gate 0S Section for quality-gates.md Reference

Insert this section BEFORE the existing `## Gate 1:` heading in `src/claude/skills/spec-driven-lifecycle/references/quality-gates.md`:

```markdown
## Gate 0S: Sprint Planning Gate

### Purpose
Ensure sprint structural integrity before committing stories to a sprint. Validates dependency chains, detects file overlaps, and checks feature cohesion.

### Location in Workflow
**Checkpoint:** Story Selection → Sprint Creation (within Phase 03S)

### When Evaluated
- During `/create-sprint` command execution
- After story validation (Step 2), before capacity calculation (Step 3)
- Automatically within Phase 03S Steps 2.5, 2.6, 2.7

### Pass Criteria
All 4 checks must pass (or be user-approved via AskUserQuestion):

| Check | Step | Agent | Severity |
|-------|------|-------|----------|
| 1. Dependency chains resolved (all deps in sprint or completed) | 2.5 | dependency-graph-analyzer | BLOCKED |
| 2. No cyclic dependencies among selected stories | 2.5 | dependency-graph-analyzer | BLOCKED |
| 3. File overlaps below blocking threshold (or user-approved) | 2.6 | file-overlap-detector | WARNING/BLOCKED |
| 4. Feature cohesion (no partial features) + no multi-sprint assignment | 2.7 | none (Read/Grep) | WARNING/BLOCKED |

### Failure Actions
1. Report specific validation failures with details (blocking dep name, cycle path, overlapping files, missing stories)
2. Offer remediation options via AskUserQuestion (remove stories, proceed with exception, HALT)
3. Log exception if user bypasses

### Bypass Mechanism
Yes, with documentation. User can proceed via AskUserQuestion with "Proceed with documented exception" option. Exception is recorded in sprint document Notes section.

### References
- ADR-046: devforgeai/specs/adrs/ADR-046-sprint-planning-quality-gate.md
- Phase 03S: src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md
- dependency-graph-analyzer: .claude/agents/dependency-graph-analyzer.md
- file-overlap-detector: .claude/agents/file-overlap-detector.md
```

### Gate Hierarchy Diagram Update

Find the existing Gate Hierarchy diagram in quality-gates.md and prepend Gate 0S:

```
Gate 0S: Sprint Planning (Story Selection → Sprint Creation)
  ↓
Gate 1: Context Validation (Architecture → Ready for Dev)
  ↓
Gate 2: Test Passing (Dev Complete → QA In Progress)
  ↓
Gate 3: QA Approval (QA Approved → Releasing)
  ↓
Gate 4: Release Readiness (Releasing → Released)
```

### Gate 0S Entry for quality-gates.md Rule Summary

Insert BEFORE the existing `## Gate 1:` in `.claude/rules/core/quality-gates.md`:

```markdown
## Gate 0S: Sprint Planning
**Transition:** Story Selection → Sprint Creation
**Enforced By:** spec-driven-lifecycle skill (Phase 03S Steps 2.5-2.7)
**Requirements:**
- All dependency chains resolved (in-sprint or completed)
- No cyclic dependencies among selected stories
- File overlaps below threshold (10+ = BLOCKED, 1-9 = WARNING)
- No partial feature sets (all stories for a feature included)
- No multi-sprint story assignment
```

### ADR-046 Verification Checklist

The ADR file already exists. TDD tests should verify these strings are present:
- `Gate 0S` (name reference)
- `Status: Accepted` (not Draft or Proposed)
- `## Context` (required section)
- `## Decision` (required section)
- `## Consequences` (required section)
- `## References` (required section)
- `Step 2.5` (new step reference)
- `Step 2.6` (new step reference)
- `Step 2.7` (new step reference)
- `bypassable` or `Bypass` (bypass property)
- `Gate 0S` appears before `Gate 1` in gate hierarchy text

## Change Log

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|-------------|--------|----------------|
| 2026-03-22 | DevForgeAI | Story Creation | Initial story created from EPIC-088 plan | STORY-561 |

## Notes

- ADR-046 was pre-created during the planning session. TDD tests verify its content rather than creating it.
- Gate 0S documentation follows the exact structural pattern of Gates 1-4 in quality-gates.md reference.
- The gate hierarchy shows: Gate 0S > Gate 1 > Gate 2 > Gate 3 > Gate 4.
- Plan reference: `/home/bryan/.claude/plans/delightful-bubbling-puzzle.md`
- Research reference: RESEARCH-002 (devforgeai/specs/research/shared/RESEARCH-002-epic-vs-sprint-sdlc-relationship.md)
