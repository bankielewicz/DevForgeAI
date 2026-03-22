---
id: STORY-575
title: Sprint File Overlap Detection in Phase 03S
type: feature
epic: EPIC-088
sprint: Sprint-31
status: Ready for Dev
points: 5
depends_on: [STORY-561]
priority: High
advisory: false
assigned_to: null
created: 2026-03-22
format_version: "2.9"
---

# STORY-575: Sprint File Overlap Detection in Phase 03S

## Description

**As a** DevForgeAI framework user,
**I want** sprint planning to detect file overlaps between selected stories,
**so that** I can sequence parallel development to avoid merge conflicts.

## Provenance

<provenance>
  <origin type="research">RESEARCH-002 + ADR-046 (Gate 0S)</origin>
  <decision>Invoke file-overlap-detector during Phase 03S in pre-flight mode</decision>
  <stakeholder>Project Owner</stakeholder>
  <hypothesis>Pre-sprint overlap detection reduces merge conflict risk</hypothesis>
</provenance>

## Acceptance Criteria

### AC#1: File-overlap-detector invoked in pre-flight mode during Phase 03S Step 2.6

<acceptance_criteria id="AC#1" title="File-overlap-detector invoked in pre-flight mode during Phase 03S Step 2.6">
  <given>stories selected for sprint</given>
  <when>Phase 03S Step 2.6 executes</when>
  <then>file-overlap-detector is invoked in pre-flight mode across all selected stories</then>
  <verification>
    <source_files>src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md</source_files>
    <test_file>tests/STORY-575/test_ac1_overlap_invocation.sh</test_file>
  </verification>
</acceptance_criteria>

### AC#2: WARNING with recommended execution order for 1-9 overlapping files

<acceptance_criteria id="AC#2" title="WARNING with recommended execution order for 1-9 overlapping files">
  <given>overlapping files between stories (1-9 files)</given>
  <when>overlap detected</when>
  <then>WARNING status returned with recommended execution order based on dependency and overlap analysis</then>
  <verification>
    <source_files>src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md</source_files>
    <test_file>tests/STORY-575/test_ac2_warning_execution_order.sh</test_file>
  </verification>
</acceptance_criteria>

### AC#3: BLOCKED status for 10+ overlapping files

<acceptance_criteria id="AC#3" title="BLOCKED status for 10+ overlapping files">
  <given>overlapping files exceed threshold (10+ files)</given>
  <when>overlap detected</when>
  <then>BLOCKED status returned</then>
  <verification>
    <source_files>src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md</source_files>
    <test_file>tests/STORY-575/test_ac3_blocked_threshold.sh</test_file>
  </verification>
</acceptance_criteria>

### AC#4: Dependency chain overlaps filtered from conflict count

<acceptance_criteria id="AC#4" title="Dependency chain overlaps filtered from conflict count">
  <given>overlapping stories are in a depends_on chain (intentional sequencing)</given>
  <when>overlap detected</when>
  <then>overlap filtered out and not counted as conflict</then>
  <verification>
    <source_files>src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md</source_files>
    <test_file>tests/STORY-575/test_ac4_dependency_chain_filter.sh</test_file>
  </verification>
</acceptance_criteria>

### AC#5: AskUserQuestion for WARNING resolution with options

<acceptance_criteria id="AC#5" title="AskUserQuestion for WARNING resolution with options">
  <given>WARNING result from overlap detection</given>
  <when>user prompted via AskUserQuestion</when>
  <then>recommended execution order displayed with options: accept recommendation / proceed without ordering / HALT</then>
  <verification>
    <source_files>src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md</source_files>
    <test_file>tests/STORY-575/test_ac5_warning_user_options.sh</test_file>
  </verification>
</acceptance_criteria>

## Technical Specification

```yaml
technical_specification:
  components:
    - name: "Phase 03S Step 2.6 Enhancement"
      type: "skill_phase"
      file_path: "src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md"
      action: "edit"
      description: "Insert Step 2.6 after Step 2.5 to invoke file-overlap-detector in pre-flight mode"

  reuses:
    - name: "file-overlap-detector"
      file_path: ".claude/agents/file-overlap-detector.md"
      action: "invoke_via_task"
      description: "Invoked via Task with pre-flight mode and story list — no modifications to agent"
      note: "Agent must be instructed to analyze provided list rather than filtering by 'In Development' status"

  test_files:
    - path: "tests/STORY-575/test_ac1_overlap_invocation.sh"
      type: "unit"
      target_ac: "AC#1"
    - path: "tests/STORY-575/test_ac2_warning_execution_order.sh"
      type: "unit"
      target_ac: "AC#2"
    - path: "tests/STORY-575/test_ac3_blocked_threshold.sh"
      type: "unit"
      target_ac: "AC#3"
    - path: "tests/STORY-575/test_ac4_dependency_chain_filter.sh"
      type: "unit"
      target_ac: "AC#4"
    - path: "tests/STORY-575/test_ac5_warning_user_options.sh"
      type: "unit"
      target_ac: "AC#5"
```

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "file-overlap-detector"
    limitation: "Agent default mode filters by 'In Development' status; pre-flight mode must override to accept Backlog stories"
    decision: "Pass explicit story list and pre-flight flag in Task invocation"
    discovered_phase: "planning"
    impact: "Task prompt must include clear instructions to analyze provided list, not filter by status"

  - id: TL-002
    component: "Phase 03S Step 2.6"
    limitation: "Stories without technical_specification YAML have no file references for overlap detection"
    decision: "Skip overlap check for stories missing technical_specification"
    discovered_phase: "planning"
    impact: "Incomplete overlap detection when stories lack technical specification"
```

## Edge Cases

```yaml
edge_cases:
  - id: EC-001
    scenario: "Stories with no technical_specification YAML"
    expected_behavior: "Skip overlap check for those stories"
    rationale: "No file references available for comparison"

  - id: EC-002
    scenario: "All stories modify completely different files"
    expected_behavior: "PASS — no overlaps detected"
    rationale: "No conflict risk when files are disjoint"

  - id: EC-003
    scenario: "file-overlap-detector agent not available"
    expected_behavior: "WARN and continue (don't block sprint creation)"
    rationale: "Agent unavailability should not halt sprint planning"

  - id: EC-004
    scenario: "Stories in depends_on chain share files intentionally"
    expected_behavior: "Filtered from overlap count"
    rationale: "Sequential execution via dependency chain already prevents parallel conflicts"

  - id: EC-005
    scenario: "Recommended execution order considers both dependency chain and overlap count"
    expected_behavior: "Order respects dependency constraints first, then minimizes overlap risk"
    rationale: "Dependencies are hard constraints; overlap ordering is advisory"
```

## Non-Functional Requirements (NFRs)

### Performance
- File overlap check adds < 15 seconds per invocation
- No blocking I/O beyond file reads for story technical specifications

### Security
- No secrets or credentials processed during overlap detection
- Story file paths validated before access

### Reliability
- Pre-flight mode works with Backlog status stories (agent default is In Development)
- Agent unavailability degrades gracefully to WARN, not BLOCK
- All test files use heading-based detection, not hardcoded line numbers

### Scalability
- Overlap detection scales with number of selected stories (pairwise comparison)
- Threshold values (1-9 WARNING, 10+ BLOCKED) configurable in future iterations

## Dependencies

### Prerequisite Stories
- STORY-561: Gate 0S ADR must be accepted first (establishes Gate 0S framework)

### External Dependencies
- file-overlap-detector agent exists at .claude/agents/file-overlap-detector.md
- Phase 03S sprint planning phase file exists with Step 2.5

### Technology Dependencies
- Bash (test scripts)
- Grep (content verification in tests)
- Task tool (agent invocation)

## Test Strategy

### Unit Tests
- AC#1: Verify Step 2.6 exists in phase-03S-sprint-planning.md with file-overlap-detector invocation in pre-flight mode
- AC#2: Verify WARNING output includes recommended execution order for 1-9 overlapping files
- AC#3: Verify BLOCKED status returned when 10+ overlapping files detected
- AC#4: Verify depends_on chain overlaps are filtered from conflict count
- AC#5: Verify AskUserQuestion prompt with three options (accept / proceed without ordering / HALT)

### Integration Tests
- N/A (Phase 03S integration tested at sprint-planning level in future stories)

## AC Verification Checklist

- [ ] AC#1: File-overlap-detector invoked in pre-flight mode during Step 2.6
- [ ] AC#2: WARNING with recommended execution order for 1-9 overlapping files
- [ ] AC#3: BLOCKED status for 10+ overlapping files
- [ ] AC#4: Dependency chain overlaps filtered from conflict count
- [ ] AC#5: AskUserQuestion with three resolution options

## Definition of Done

- [ ] Step 2.6 inserted in phase-03S-sprint-planning.md after Step 2.5
- [ ] file-overlap-detector invoked with pre-flight mode and story list
- [ ] WARNING for 1-9 overlapping files with execution order
- [ ] BLOCKED for 10+ overlapping files
- [ ] Dependency chain overlaps filtered
- [ ] AskUserQuestion for WARNING/BLOCKED resolution
- [ ] All TDD tests written and passing
- [ ] No modifications to file-overlap-detector agent

## Implementation Guide

This section provides the exact pseudocode and Task() prompt template a fresh Claude session needs.

### Step 2.6 Pseudocode (Insert in phase-03S-sprint-planning.md)

Insert this step after Step 2.5. Follow the EXECUTE-VERIFY-RECORD pattern.

```markdown
### Step 2.6: File Overlap Detection [Gate 0S]

**EXECUTE:**

# 1. Invoke file-overlap-detector in pre-flight mode
Task(
  subagent_type="file-overlap-detector",
  description="Sprint file overlap detection for Gate 0S",
  prompt=f"""
Analyze file overlaps for sprint planning (pre-flight mode).

Mode: pre-flight
Selected sprint stories: {valid_stories}

IMPORTANT: Do NOT filter by "In Development" status. These stories are in "Backlog" or "Ready for Dev" status. Analyze the provided list directly.

For EACH selected story:
1. Read the story file at devforgeai/specs/Stories/{{story_id}}*.story.md
2. Parse the technical_specification YAML block
3. Extract all file_path values from components

Cross-reference ALL stories against each other:
1. For each pair of stories, check if they share any file_path values
2. If overlapping stories are in a depends_on chain, FILTER the overlap (intentional sequencing)
3. Count remaining (non-dependency) overlaps

Return JSON with:
- status: PASS | WARNING | BLOCKED
- total_overlaps: integer (non-dependency overlaps only)
- overlaps: [{{story_a, story_b, shared_files: [paths]}}]
- dependency_filtered: [{{story_a, story_b, shared_files: [paths], reason: "depends_on chain"}}]
- recommended_order: [story_ids in recommended execution order]
  (Order logic: respect dependency constraints first, then minimize overlap risk by sequencing stories that share files)

Thresholds:
- 0 overlaps: PASS
- 1-9 overlaps: WARNING
- 10+ overlaps: BLOCKED
"""
)

# 2. Process results
IF result.status == "BLOCKED":
  AskUserQuestion:
    Question: f"File overlap detection: BLOCKED ({result.total_overlaps} overlapping files)\n\nOverlaps:\n{format_overlaps(result.overlaps)}"
    Header: "Gate 0S: File Overlaps"
    Options:
      - label: "Remove conflicting stories"
        description: "Remove stories with most overlaps"
      - label: "Proceed with documented exception"
        description: "Accept merge conflict risk"
      - label: "HALT"
        description: "Cancel sprint creation to resolve overlaps"

ELIF result.status == "WARNING":
  AskUserQuestion:
    Question: f"File overlap detection: WARNING ({result.total_overlaps} overlapping files)\n\nOverlaps:\n{format_overlaps(result.overlaps)}\n\nRecommended execution order:\n{format_order(result.recommended_order)}"
    Header: "Gate 0S: File Overlaps"
    Options:
      - label: "Accept recommended order"
        description: f"Execute stories in order: {result.recommended_order}"
      - label: "Proceed without ordering"
        description: "No execution order constraint"
      - label: "HALT"
        description: "Cancel sprint creation"

  IF "Accept recommended order":
    sprint_recommended_order = result.recommended_order
    Display: f"Execution order recorded in sprint document"

ELSE:
  Display: f"Step 2.6: No file overlaps detected — PASS"

# 3. Store for sprint document
IF result.recommended_order:
  # Pass to Step 4 (Sprint-Planner invocation) as additional context
  overlap_context = result

**VERIFY:**
File overlap check executed (result variable populated with PASS, WARNING, or BLOCKED).

**RECORD:**
Update checkpoint: phases["03S"].steps_completed.append("2.6")
```

### Plan Reference

Full design context: `/home/bryan/.claude/plans/delightful-bubbling-puzzle.md`
ADR reference: `devforgeai/specs/adrs/ADR-046-sprint-planning-quality-gate.md`

## Change Log

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|-------------|--------|----------------|
| 2026-03-22 | DevForgeAI | Story Creation | Initial story created from EPIC-088 plan | STORY-575 |

## Notes

- The file-overlap-detector agent is reused as-is. The Task invocation must instruct it to analyze a provided story list rather than filtering by "In Development" status.
- Overlap thresholds: 1-9 files = WARNING, 10+ files = BLOCKED. These align with practical merge conflict risk levels.
- Dependency chain filtering ensures intentionally sequenced stories (via depends_on) are not flagged as conflicts.
- Research reference: RESEARCH-002 (devforgeai/specs/research/shared/RESEARCH-002-epic-vs-sprint-sdlc-relationship.md)
- ADR reference: ADR-046 (devforgeai/specs/adrs/ADR-046-sprint-planning-quality-gate.md)
- Plan reference: /home/bryan/.claude/plans/delightful-bubbling-puzzle.md (contains full design context and upstream gap documentation)
