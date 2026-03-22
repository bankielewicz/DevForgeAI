---
id: STORY-574
title: Sprint Dependency Chain Validation in Phase 03S
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

# STORY-574: Sprint Dependency Chain Validation in Phase 03S

## Description

**As a** DevForgeAI framework user,
**I want** sprint planning to validate dependency chains for all selected stories,
**so that** sprints are not created with unresolvable blocking dependencies or circular dependencies.

## Provenance

<provenance>
  <origin type="research">RESEARCH-002 (Epic vs Sprint in SDLC) + ADR-046 (Gate 0S)</origin>
  <decision>Invoke dependency-graph-analyzer during Phase 03S</decision>
  <stakeholder>Project Owner</stakeholder>
  <hypothesis>Pre-sprint dependency validation prevents blocked stories from entering sprints</hypothesis>
</provenance>

## Acceptance Criteria

### AC#1: dependency-graph-analyzer invoked for stories with dependencies

<acceptance_criteria id="AC#1" title="dependency-graph-analyzer invoked for stories with dependencies">
  <given>stories selected for sprint with depends_on entries</given>
  <when>Phase 03S Step 2.5 executes</when>
  <then>dependency-graph-analyzer subagent is invoked for each story with dependencies, passing the sprint selection list as context</then>
  <verification>
    <source_files>src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md</source_files>
    <test_file>tests/STORY-574/test_ac1_dependency_invocation.sh</test_file>
  </verification>
</acceptance_criteria>

### AC#2: BLOCKED status for unresolved external dependencies

<acceptance_criteria id="AC#2" title="BLOCKED status for unresolved external dependencies">
  <given>a dependency NOT in the selected sprint AND NOT completed (Dev Complete/QA Approved/Released)</given>
  <when>validation runs</when>
  <then>BLOCKED status returned with blocking dependency name and current status</then>
  <verification>
    <source_files>src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md</source_files>
    <test_file>tests/STORY-574/test_ac2_blocked_unresolved.sh</test_file>
  </verification>
</acceptance_criteria>

### AC#3: Intra-sprint dependencies satisfied

<acceptance_criteria id="AC#3" title="Intra-sprint dependencies satisfied">
  <given>a dependency IS in the selected sprint</given>
  <when>validation runs</when>
  <then>the dependency is satisfied (intra-sprint dependency valid)</then>
  <verification>
    <source_files>src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md</source_files>
    <test_file>tests/STORY-574/test_ac3_intrasprint_valid.sh</test_file>
  </verification>
</acceptance_criteria>

### AC#4: Circular dependency detection

<acceptance_criteria id="AC#4" title="Circular dependency detection">
  <given>circular dependency among selected stories (STORY-A depends STORY-B, STORY-B depends STORY-A)</given>
  <when>validation runs</when>
  <then>BLOCKED with cycle path displayed</then>
  <verification>
    <source_files>src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md</source_files>
    <test_file>tests/STORY-574/test_ac4_circular_dependency.sh</test_file>
  </verification>
</acceptance_criteria>

### AC#5: BLOCKED resolution via AskUserQuestion

<acceptance_criteria id="AC#5" title="BLOCKED resolution via AskUserQuestion">
  <given>BLOCKED result</given>
  <when>user prompted via AskUserQuestion</when>
  <then>options presented: remove blocking stories / proceed with documented exception / HALT</then>
  <verification>
    <source_files>src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md</source_files>
    <test_file>tests/STORY-574/test_ac5_blocked_user_options.sh</test_file>
  </verification>
</acceptance_criteria>

## Technical Specification

```yaml
technical_specification:
  components:
    - name: "Phase 03S Step 2.5 Enhancement"
      type: "skill_phase"
      file_path: "src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md"
      action: "edit"
      description: "Insert Step 2.5 between existing Step 2 (line 82) and Step 3 (line 84) for dependency chain validation"

    - name: "dependency-graph-analyzer subagent"
      type: "subagent"
      file_path: ".claude/agents/dependency-graph-analyzer.md"
      action: "reuse"
      description: "Invoked via Task for dependency resolution — no modifications to subagent"

  test_files:
    - path: "tests/STORY-574/test_ac1_dependency_invocation.sh"
      type: "unit"
      target_ac: "AC#1"
    - path: "tests/STORY-574/test_ac2_blocked_unresolved.sh"
      type: "unit"
      target_ac: "AC#2"
    - path: "tests/STORY-574/test_ac3_intrasprint_valid.sh"
      type: "unit"
      target_ac: "AC#3"
    - path: "tests/STORY-574/test_ac4_circular_dependency.sh"
      type: "unit"
      target_ac: "AC#4"
    - path: "tests/STORY-574/test_ac5_blocked_user_options.sh"
      type: "unit"
      target_ac: "AC#5"
```

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Phase 03S Step 2.5"
    limitation: "Insertion point depends on current Step 2/Step 3 heading text and line positions"
    decision: "Use heading-based section detection, not hardcoded line numbers"
    discovered_phase: "planning"
    impact: "Tests must tolerate content growth in phase-03S-sprint-planning.md"

  - id: TL-002
    component: "dependency-graph-analyzer"
    limitation: "Subagent availability cannot be guaranteed at runtime"
    decision: "Graceful fallback to WARN if subagent unavailable, do not BLOCK sprint creation"
    discovered_phase: "planning"
    impact: "Sprint may proceed without dependency validation if subagent fails"

  - id: TL-003
    component: "Transitive dependency resolution"
    limitation: "Deep transitive chains (>10 levels) may exceed reasonable validation time"
    decision: "Cap transitive resolution at 10 levels with WARN for deeper chains"
    discovered_phase: "planning"
    impact: "Extremely deep dependency chains may not be fully validated"
```

## Non-Functional Requirements (NFRs)

### Performance
- Dependency check adds < 15 seconds per subagent invocation
- Full sprint validation (all stories) completes within 2 minutes for typical sprint sizes (5-15 stories)

### Security
- No secrets or credentials in validation logic
- Story file reads are read-only during validation phase

### Reliability
- Graceful fallback if dependency-graph-analyzer unavailable (WARN, don't BLOCK)
- Partial failures (some stories validated, some not) produce clear per-story status
- All validation results logged for auditability

### Scalability
- Validation scales linearly with number of stories in sprint
- Cycle detection uses DFS with visited-set to avoid exponential blowup

## Dependencies

### Prerequisite Stories
- STORY-561 (Gate 0S ADR must be accepted first — establishes Gate 0S framework)

### External Dependencies
- dependency-graph-analyzer subagent exists at .claude/agents/dependency-graph-analyzer.md
- Phase 03S skill file exists at src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md

### Technology Dependencies
- Bash (test scripts)
- Grep (content verification in tests)
- YAML frontmatter parsing (story file status reads)

## Test Strategy

### Unit Tests
- AC#1: Verify Step 2.5 exists in phase-03S and references dependency-graph-analyzer invocation with sprint context
- AC#2: Verify BLOCKED status output format includes dependency name and current status for unresolved external deps
- AC#3: Verify intra-sprint dependency satisfaction logic (dependency in sprint selection list = valid)
- AC#4: Verify circular dependency detection produces BLOCKED with cycle path (DFS-based)
- AC#5: Verify AskUserQuestion prompt contains all three resolution options

### Integration Tests
- End-to-end sprint planning with mixed dependency states (some resolved, some blocked, some circular)

### Edge Cases
1. Stories with empty depends_on: [] -- skip dependency check for that story
2. Transitive dependencies: STORY-A depends STORY-B depends STORY-C -- must resolve entire chain
3. All dependencies already completed -- all checks pass, no user prompt
4. Mixed: some deps in sprint, some completed, some unresolved -- partial BLOCKED
5. Single story sprint -- no intra-sprint dependencies possible, passes trivially

## AC Verification Checklist

- [ ] AC#1: dependency-graph-analyzer invoked for each story with depends_on entries
- [ ] AC#2: BLOCKED status with dependency name and status for unresolved external deps
- [ ] AC#3: Intra-sprint dependencies marked as satisfied
- [ ] AC#4: Circular dependencies detected with cycle path displayed
- [ ] AC#5: AskUserQuestion presents remove / proceed with exception / HALT options

## Definition of Done

- [ ] Step 2.5 inserted in phase-03S-sprint-planning.md
- [ ] dependency-graph-analyzer invoked with sprint selection list context
- [ ] BLOCKED status for unresolved dependencies
- [ ] Cycle detection via DFS
- [ ] AskUserQuestion for BLOCKED resolution
- [ ] All TDD tests written and passing
- [ ] No modifications to dependency-graph-analyzer agent

## Implementation Guide

This section provides the exact pseudocode and Task() prompt template a fresh Claude session needs.

### Step 2.5 Pseudocode (Insert in phase-03S-sprint-planning.md)

Insert this step between existing Step 2 and Step 3. Follow the EXECUTE-VERIFY-RECORD pattern used by all existing steps.

```markdown
### Step 2.5: Dependency Chain Validation [Gate 0S]

**EXECUTE:**

# 1. Collect dependencies from all valid stories
stories_with_deps = []
FOR story_id in valid_stories:
  story_file = Glob(pattern=f"devforgeai/specs/Stories/{story_id}*.story.md")[0]
  Read(file_path=story_file)
  depends_on = extract "depends_on:" from YAML frontmatter

  IF depends_on is not empty and depends_on != []:
    stories_with_deps.append({
      "story_id": story_id,
      "depends_on": depends_on
    })

IF stories_with_deps is empty:
  Display: "Step 2.5: No dependencies found — PASS"
  GOTO Step 2.6

# 2. Invoke dependency-graph-analyzer for batch validation
Task(
  subagent_type="dependency-graph-analyzer",
  description="Sprint dependency validation for Gate 0S",
  prompt=f"""
Validate dependency graph for sprint planning.

Selected sprint stories: {valid_stories}
Stories with dependencies: {stories_with_deps}

For EACH story with depends_on entries:
1. Check if each dependency is in the selected sprint stories list — if YES, dependency is SATISFIED (intra-sprint)
2. Check if each dependency has status Dev Complete, QA Approved, or Released — if YES, dependency is SATISFIED (completed)
3. If dependency is NOT in sprint AND NOT completed — mark as BLOCKED with dependency name and current status
4. Check for circular dependencies among ALL selected stories using DFS cycle detection

Return JSON with:
- status: PASS | BLOCKED
- blocked_dependencies: [{story_id, blocked_by, blocked_by_status}]
- cycles: [{cycle_path}] (if circular dependencies found)
- satisfied: [{story_id, dependency, resolution: "intra-sprint" | "completed"}]
"""
)

# 3. Process results
IF result.status == "BLOCKED" OR result.cycles is not empty:
  issues = format_issues(result.blocked_dependencies, result.cycles)

  AskUserQuestion:
    Question: f"Sprint dependency validation found issues:\n{issues}"
    Header: "Gate 0S: Dependencies"
    Options:
      - label: "Remove blocking stories"
        description: "Remove stories with unmet dependencies from sprint"
      - label: "Proceed with documented exception"
        description: "Accept risk and document exception in sprint notes"
      - label: "HALT"
        description: "Cancel sprint creation to fix dependencies first"

  IF "Remove blocking stories":
    valid_stories = [s for s in valid_stories if s not in blocked_story_ids]
    Display: f"Removed {len(blocked_story_ids)} stories. Remaining: {len(valid_stories)}"
  ELIF "Proceed with documented exception":
    sprint_exceptions.append("Dependency exception: " + issues)
    Display: "Exception documented. Proceeding."
  ELIF "HALT":
    HALT -- "Sprint creation cancelled by user due to dependency issues"

ELSE:
  Display: f"Step 2.5: All dependencies satisfied — PASS ({len(stories_with_deps)} stories checked)"

**VERIFY:**
Dependency validation executed (result variable populated with PASS or BLOCKED status).

**RECORD:**
Update checkpoint: phases["03S"].steps_completed.append("2.5")
```

### Plan Reference

Full design context: `/home/bryan/.claude/plans/delightful-bubbling-puzzle.md`
ADR reference: `devforgeai/specs/adrs/ADR-046-sprint-planning-quality-gate.md`

## Change Log

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|-------------|--------|----------------|
| 2026-03-22 | DevForgeAI | Story Creation | Initial story created from EPIC-088 plan | STORY-574 |

## Notes

- This story reuses the existing dependency-graph-analyzer subagent without modification. It is invoked via Task during Phase 03S Step 2.5.
- Step 2.5 is inserted between the existing Step 2 (line 82) and Step 3 (line 84) in phase-03S-sprint-planning.md.
- Circular dependency detection uses depth-first search (DFS) with a visited set to identify cycles.
- The graceful fallback NFR means that if the dependency-graph-analyzer subagent is unavailable, sprint creation proceeds with a WARN rather than blocking entirely.
- Research reference: RESEARCH-002 (devforgeai/specs/research/shared/RESEARCH-002-epic-vs-sprint-sdlc-relationship.md)
- ADR reference: ADR-046 (devforgeai/specs/adrs/ADR-046-sprint-planning-quality-gate.md)
- Plan reference: /home/bryan/.claude/plans/delightful-bubbling-puzzle.md (contains full design context and upstream gap documentation)
