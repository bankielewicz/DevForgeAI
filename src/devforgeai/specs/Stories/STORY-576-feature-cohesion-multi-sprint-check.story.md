---
id: STORY-576
title: Feature Cohesion Validation and Multi-Sprint Assignment Check
type: feature
epic: EPIC-088
sprint: Sprint-31
status: Ready for Dev
points: 3
depends_on: [STORY-561]
priority: Medium
advisory: false
assigned_to: null
created: 2026-03-22
format_version: "2.9"
---

# STORY-576: Feature Cohesion Validation and Multi-Sprint Assignment Check

## Description

**As a** DevForgeAI framework user,
**I want** sprint planning to warn about partial feature sets and block multi-sprint story assignment,
**so that** I don't inadvertently ship incomplete functional areas or double-assign stories.

## Provenance

<provenance>
  <origin type="research">RESEARCH-002 (vertical slicing best practice) + ADR-046 (Gate 0S)</origin>
  <decision>Parse epic Target Sprints section for feature-to-story mapping</decision>
  <stakeholder>Project Owner</stakeholder>
  <hypothesis>Feature cohesion checks prevent partial feature shipments</hypothesis>
</provenance>

## Acceptance Criteria

### AC#1: Epic Target Sprints section parsed for feature-to-story mapping

<acceptance_criteria id="AC#1" title="Epic Target Sprints section parsed for feature-to-story mapping">
  <given>an epic linked to the sprint AND the epic has a populated "## Target Sprints" section</given>
  <when>Phase 03S Step 2.7 executes</when>
  <then>the feature-to-story mapping is parsed from the epic's Target Sprints section</then>
  <verification>
    <source_files>src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md</source_files>
    <test_file>tests/STORY-576/test_ac1_feature_mapping.sh</test_file>
  </verification>
</acceptance_criteria>

### AC#2: WARNING raised for incomplete feature sets

<acceptance_criteria id="AC#2" title="WARNING raised for incomplete feature sets">
  <given>selected stories include SOME but not ALL stories for a feature mapped to this sprint</given>
  <when>cohesion check runs</when>
  <then>WARNING raised identifying the incomplete feature and listing missing stories</then>
  <verification>
    <source_files>src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md</source_files>
    <test_file>tests/STORY-576/test_ac2_partial_feature_warning.sh</test_file>
  </verification>
</acceptance_criteria>

### AC#3: WARNING raised for sprint mismatch

<acceptance_criteria id="AC#3" title="WARNING raised for sprint mismatch">
  <given>selected stories include stories mapped to a DIFFERENT sprint in the epic's Target Sprints section</given>
  <when>check runs</when>
  <then>WARNING raised with sprint mismatch detail</then>
  <verification>
    <source_files>src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md</source_files>
    <test_file>tests/STORY-576/test_ac3_sprint_mismatch_warning.sh</test_file>
  </verification>
</acceptance_criteria>

### AC#4: Check SKIPPED gracefully when no Target Sprints section or no epic

<acceptance_criteria id="AC#4" title="Check SKIPPED gracefully when no Target Sprints section or no epic">
  <given>epic has NO Target Sprints section OR no epic is linked</given>
  <when>cohesion check runs</when>
  <then>check SKIPPED with informational message (graceful degradation)</then>
  <verification>
    <source_files>src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md</source_files>
    <test_file>tests/STORY-576/test_ac4_graceful_skip.sh</test_file>
  </verification>
</acceptance_criteria>

### AC#5: BLOCKED for multi-sprint assignment

<acceptance_criteria id="AC#5" title="BLOCKED for multi-sprint assignment">
  <given>a selected story already has a non-empty sprint field (not "Backlog" or "null")</given>
  <when>multi-sprint assignment check runs</when>
  <then>BLOCKED (story already assigned to another sprint)</then>
  <verification>
    <source_files>src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md</source_files>
    <test_file>tests/STORY-576/test_ac5_multi_sprint_block.sh</test_file>
  </verification>
</acceptance_criteria>

## Technical Specification

```yaml
technical_specification:
  components:
    - name: "Phase 03S Step 2.7 Enhancement"
      type: "skill_phase"
      file_path: "src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md"
      action: "edit"
      description: "Insert Step 2.7 after Step 2.6 for feature cohesion and multi-sprint assignment checks"

  parsing_approach: "Matches gap-detector.sh Strategy 2 (markdown section extraction)"
  subagent_required: false
  operations: "Lightweight Read/Grep operations only"

  test_files:
    - path: "tests/STORY-576/test_ac1_feature_mapping.sh"
      type: "unit"
      target_ac: "AC#1"
    - path: "tests/STORY-576/test_ac2_partial_feature_warning.sh"
      type: "unit"
      target_ac: "AC#2"
    - path: "tests/STORY-576/test_ac3_sprint_mismatch_warning.sh"
      type: "unit"
      target_ac: "AC#3"
    - path: "tests/STORY-576/test_ac4_graceful_skip.sh"
      type: "unit"
      target_ac: "AC#4"
    - path: "tests/STORY-576/test_ac5_multi_sprint_block.sh"
      type: "unit"
      target_ac: "AC#5"
```

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Epic Target Sprints parser"
    limitation: "Epic Target Sprints may use prose format instead of clean story list"
    decision: "Use Grep STORY-\\d+ to extract story IDs regardless of prose formatting"
    discovered_phase: "planning"
    impact: "Parser must be format-tolerant; tests must cover prose and list formats"

  - id: TL-002
    component: "Multi-epic sprint handling"
    limitation: "Sprint may reference multiple epics, making cohesion check ambiguous"
    decision: "Cohesion check skipped when EPIC_ID is 'Multiple' or not set"
    discovered_phase: "planning"
    impact: "Feature cohesion only enforced for single-epic sprints"
```

## Edge Cases

```yaml
edge_cases:
  - id: EC-001
    scenario: "Epic Target Sprints uses prose format (not clean story list)"
    handling: "Grep STORY-\\d+ extracts IDs regardless of surrounding prose"

  - id: EC-002
    scenario: "Multi-epic sprint (EPIC_ID is 'Multiple' or not set)"
    handling: "Cohesion check skipped with informational message"

  - id: EC-003
    scenario: "Feature has all stories completed (Released/QA Approved)"
    handling: "Feature is already delivered, no warning raised"

  - id: EC-004
    scenario: "Story has sprint: 'Backlog'"
    handling: "Valid for assignment (not a multi-sprint conflict)"

  - id: EC-005
    scenario: "Story has sprint: null"
    handling: "Valid for assignment (not a multi-sprint conflict)"

  - id: EC-006
    scenario: "Older epics without Target Sprints section"
    handling: "Check gracefully skipped with informational message"
```

## Non-Functional Requirements (NFRs)

### Performance
- Cohesion check adds < 5 seconds (Read + Grep only, no subagent invocation)
- No build step required

### Security
- No secrets or credentials in any documentation file
- No executable code in phase definition (pseudocode in fenced code blocks only)

### Reliability
- Graceful degradation when epic lacks Target Sprints section
- Phase file remains valid Markdown after edits
- Tests use heading-based detection, not hardcoded line numbers

### Scalability
- Step 2.7 follows same structural pattern as Steps 2.5-2.6, enabling future gate checks

## Dependencies

### Prerequisite Stories
- STORY-561 (Gate 0S ADR must be accepted first — establishes the Gate 0S framework)

### External Dependencies
- Epic files with Target Sprints section (optional — graceful degradation when absent)

### Technology Dependencies
- Bash (test scripts)
- Grep (story ID extraction and section detection in tests)

## Test Strategy

### Unit Tests
- AC#1: Verify feature-to-story mapping parsed from epic Target Sprints section
- AC#2: Verify WARNING raised for partial feature sets with missing story list
- AC#3: Verify WARNING raised for sprint mismatch detail
- AC#4: Verify SKIPPED with informational message when no Target Sprints or no epic
- AC#5: Verify BLOCKED for story already assigned to another sprint

### Integration Tests
- N/A (skill phase enhancement — Phase 05 Integration handled by lifecycle)

## AC Verification Checklist

- [ ] AC#1: Epic Target Sprints section parsed for feature-to-story mapping
- [ ] AC#2: WARNING raised for incomplete feature sets with missing story list
- [ ] AC#3: WARNING raised for sprint mismatch
- [ ] AC#4: Check SKIPPED gracefully when no Target Sprints section or no epic
- [ ] AC#5: BLOCKED for multi-sprint assignment

## Definition of Done

- [ ] Step 2.7 inserted in phase-03S-sprint-planning.md after Step 2.6
- [ ] Epic Target Sprints section parsed for feature-to-story mapping
- [ ] WARNING for partial feature sets with missing story list
- [ ] WARNING for sprint mismatch (story mapped to different sprint)
- [ ] SKIPPED gracefully when no Target Sprints section or no epic
- [ ] BLOCKED for multi-sprint assignment
- [ ] AskUserQuestion for WARNING/BLOCKED resolution
- [ ] All TDD tests written and passing

## Implementation Guide

This section provides the exact pseudocode a fresh Claude session needs. No subagent required — Read/Grep only.

### Step 2.7 Pseudocode (Insert in phase-03S-sprint-planning.md)

Insert this step after Step 2.6. Follow the EXECUTE-VERIFY-RECORD pattern.

```markdown
### Step 2.7: Feature Cohesion + Multi-Sprint Assignment Check [Gate 0S]

**EXECUTE:**

cohesion_warnings = []
multi_sprint_blocked = []

# --- Part A: Multi-Sprint Assignment Check ---
# (runs regardless of epic linkage)

FOR story_id in valid_stories:
  story_file = Glob(pattern=f"devforgeai/specs/Stories/{story_id}*.story.md")[0]
  Read(file_path=story_file)
  sprint_value = Grep(pattern="^sprint:", path=story_file, output_mode="content")

  # Extract sprint value from "sprint: Sprint-29" or "sprint: Backlog"
  IF sprint_value is not empty:
    sprint_field = sprint_value.split(":")[1].strip()
    IF sprint_field != "Backlog" AND sprint_field != "null" AND sprint_field != "" AND sprint_field != current_sprint_id:
      multi_sprint_blocked.append({
        "story_id": story_id,
        "existing_sprint": sprint_field
      })

IF multi_sprint_blocked:
  AskUserQuestion:
    Question: f"Multi-sprint assignment detected:\n" +
      "\n".join([f"  - {s['story_id']} already in {s['existing_sprint']}" for s in multi_sprint_blocked])
    Header: "Gate 0S: Multi-Sprint"
    Options:
      - label: "Remove conflicting stories"
        description: "Remove stories already assigned to other sprints"
      - label: "Proceed with documented exception"
        description: "Accept dual assignment risk"
      - label: "HALT"
        description: "Cancel sprint creation"

  IF "Remove conflicting stories":
    valid_stories = [s for s in valid_stories if s not in [b['story_id'] for b in multi_sprint_blocked]]

# --- Part B: Feature Cohesion Check ---
# (only runs when single epic is linked)

IF EPIC_ID is not None AND EPIC_ID != "Multiple" AND EPIC_ID != "Standalone":
  epic_files = Glob(pattern=f"devforgeai/specs/Epics/{EPIC_ID}*.epic.md")

  IF epic_files:
    Read(file_path=epic_files[0])

    # Check for Target Sprints section
    target_sprints_check = Grep(pattern="^## Target Sprints", path=epic_files[0], output_mode="content")

    IF target_sprints_check:
      # Parse feature-to-story mapping from Target Sprints section
      # Read content between "## Target Sprints" and next "## " heading
      # For each "### Sprint N" subsection:
      #   For each line containing "Feature":
      #     Extract all STORY-\d+ IDs from that line
      #     Map: feature_name -> [story_ids]

      feature_story_map = {}

      # Use Grep to find all lines with STORY-NNN under Target Sprints
      # Pattern: lines between "## Target Sprints" and next "##" that contain "Feature"
      feature_lines = Grep(
        pattern="Feature.*STORY-\\d+",
        path=epic_files[0],
        output_mode="content"
      )

      FOR line in feature_lines:
        # Extract feature name (text before the story IDs)
        feature_name = extract text between "Feature" and first "STORY-" or ":"
        # Extract all story IDs
        story_ids = Grep(pattern="STORY-\\d+", text=line)  # findall equivalent
        feature_story_map[feature_name] = story_ids

      # Check cohesion: for each feature, are all stories included?
      FOR feature_name, feature_stories in feature_story_map.items():
        included = [s for s in feature_stories if s in valid_stories]
        missing = [s for s in feature_stories if s not in valid_stories]

        IF included AND missing:
          # Partial feature! Check if missing stories are already completed
          truly_missing = []
          FOR missing_story in missing:
            missing_files = Glob(pattern=f"devforgeai/specs/Stories/{missing_story}*.story.md")
            IF missing_files:
              Read(file_path=missing_files[0], limit=15)
              status = extract "status:" from frontmatter
              IF status not in ["Dev Complete", "QA Approved", "Released", "Releasing"]:
                truly_missing.append({"story_id": missing_story, "status": status})

          IF truly_missing:
            cohesion_warnings.append({
              "feature": feature_name,
              "included": included,
              "missing": truly_missing
            })

      IF cohesion_warnings:
        warning_text = "Partial feature sets detected:\n"
        FOR w in cohesion_warnings:
          warning_text += f"\n  Feature: {w['feature']}\n"
          warning_text += f"    Included: {w['included']}\n"
          warning_text += f"    Missing: {[m['story_id'] + ' (' + m['status'] + ')' for m in w['missing']]}\n"

        AskUserQuestion:
          Question: warning_text
          Header: "Gate 0S: Feature Cohesion"
          Options:
            - label: "Add missing stories"
              description: "Go back and include the missing stories"
            - label: "Proceed with partial feature"
              description: "Accept incomplete feature delivery risk"
            - label: "HALT"
              description: "Cancel sprint creation"
      ELSE:
        Display: "Step 2.7: Feature cohesion check — PASS (all features complete)"

    ELSE:
      Display: f"INFO: Epic {EPIC_ID} has no Target Sprints section. Feature cohesion check skipped."

  ELSE:
    Display: f"INFO: Epic file for {EPIC_ID} not found. Feature cohesion check skipped."

ELSE:
  Display: "INFO: No single epic linked. Feature cohesion check skipped."

# --- Summary ---
IF not multi_sprint_blocked and not cohesion_warnings:
  Display: "Step 2.7: Multi-sprint and feature cohesion checks — PASS"

**VERIFY:**
Both multi-sprint and cohesion checks executed (or explicitly skipped with INFO message).

**RECORD:**
Update checkpoint: phases["03S"].steps_completed.append("2.7")
```

### Parsing Notes

- The `STORY-\d+` regex pattern extracts story IDs from ANY prose format (e.g., "Feature 2: Red-phase test integrity checksums (STORY-502, STORY-503)" → extracts STORY-502, STORY-503)
- This is the same technique used by `devforgeai/traceability/gap-detector.sh` Strategy 2
- Feature names are extracted from text before the story ID references on each line
- Only features with at least one story in the sprint selection are checked (features with zero stories selected are not relevant)

### Plan Reference

Full design context: `/home/bryan/.claude/plans/delightful-bubbling-puzzle.md`
ADR reference: `devforgeai/specs/adrs/ADR-046-sprint-planning-quality-gate.md`

## Change Log

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|-------------|--------|----------------|
| 2026-03-22 | DevForgeAI | Story Creation | Initial story created from EPIC-088 plan | STORY-576 |

## Notes

- Depends on STORY-561 which establishes the Gate 0S framework via ADR-046.
- Step 2.7 is inserted after Step 2.6 in Phase 03S, following the same structural pattern.
- Parsing approach matches gap-detector.sh Strategy 2 (markdown section extraction).
- No subagent needed — lightweight Read/Grep operations only.
- Research reference: RESEARCH-002 (devforgeai/specs/research/shared/RESEARCH-002-epic-vs-sprint-sdlc-relationship.md)
- ADR reference: ADR-046 (devforgeai/specs/adrs/ADR-046-sprint-planning-quality-gate.md)
- Plan reference: /home/bryan/.claude/plans/delightful-bubbling-puzzle.md (contains full design context and upstream gap documentation)
