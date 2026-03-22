---
id: STORY-341
title: Create Session Memory Layer
type: feature
epic: EPIC-052
sprint: Backlog
status: QA Approved
points: 8
depends_on: ["STORY-339"]
priority: High
assigned_to: Unassigned
created: 2026-01-30
format_version: "2.7"
---

# Story: Create Session Memory Layer

## Description

**As a** Framework Owner,
**I want** each story to have a session memory file that persists observations throughout the story lifecycle,
**so that** all observations from phases 02-08 are consolidated in one location and can be reviewed after completion.

## Provenance

```xml
<provenance>
  <origin document="EPIC-052" section="Feature 2">
    <quote>"Create per-story session memory that persists observations throughout story lifecycle and archives on completion."</quote>
    <line_reference>lines 171-237</line_reference>
    <quantified_impact>Session memory files created for each story during /dev workflow</quantified_impact>
  </origin>

  <decision rationale="per-story-isolation">
    <selected>One session memory file per story ({STORY_ID}-session.md)</selected>
    <rejected alternative="single-global-file">
      Would create concurrency issues with parallel story development
    </rejected>
    <trade_off>More files to manage but better isolation</trade_off>
  </decision>

  <stakeholder role="Framework Owner" goal="consolidated-observations">
    <quote>"Each story to have a session memory file, so that all observations from the story lifecycle are consolidated."</quote>
    <source>EPIC-052, User Story 2</source>
  </stakeholder>

  <hypothesis id="H5" validation="file-creation" success_criteria="Session memory files created for each story">
    Multi-layer memory enables learning - session layer captures per-story context
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Session Memory Created at Phase 01

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>A story enters Phase 01 (Preflight) of /dev workflow</given>
  <when>Phase 01 completes successfully</when>
  <then>Session memory file created at .claude/memory/sessions/{STORY_ID}-session.md</then>
  <verification>
    <source_files>
      <file hint="Phase 01 preflight">.claude/skills/devforgeai-development/phases/phase-01-preflight.md</file>
    </source_files>
    <test_file>tests/STORY-341/test_ac1_session_created.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Observations Appended After Each Phase

```xml
<acceptance_criteria id="AC2" implements="COMP-002">
  <given>A phase (02-08) completes</given>
  <when>Phase exit gate executes</when>
  <then>Observations from that phase appended to session memory file</then>
  <verification>
    <source_files>
      <file hint="Phase files">.claude/skills/devforgeai-development/phases/phase-02-test-first.md</file>
      <file hint="Phase files">.claude/skills/devforgeai-development/phases/phase-03-implementation.md</file>
    </source_files>
    <test_file>tests/STORY-341/test_ac2_observations_appended.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Session Memory Archived on Completion

```xml
<acceptance_criteria id="AC3" implements="COMP-003">
  <given>A story reaches QA Approved status</given>
  <when>Story completion is finalized</when>
  <then>Session memory status field set to "archived" or file moved to archive/</then>
  <verification>
    <source_files>
      <file hint="Session memory schema">.claude/memory/sessions/{STORY_ID}-session.md</file>
    </source_files>
    <test_file>tests/STORY-341/test_ac3_session_archived.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Schema Matches Specification

```xml
<acceptance_criteria id="AC4" implements="COMP-001">
  <given>A session memory file exists</given>
  <when>File content is validated</when>
  <then>Schema matches EPIC-052 specification with YAML frontmatter and markdown sections</then>
  <verification>
    <source_files>
      <file hint="Session memory file">.claude/memory/sessions/{STORY_ID}-session.md</file>
    </source_files>
    <test_file>tests/STORY-341/test_ac4_schema_valid.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Stale Sessions Cleaned Up

```xml
<acceptance_criteria id="AC5" implements="COMP-004">
  <given>Session files older than 7 days with status "active" exist</given>
  <when>Cleanup check runs (at Phase 01 of any story)</when>
  <then>Stale session files are archived or deleted</then>
  <verification>
    <source_files>
      <file hint="Phase 01 cleanup logic">.claude/skills/devforgeai-development/phases/phase-01-preflight.md</file>
    </source_files>
    <test_file>tests/STORY-341/test_ac5_stale_cleanup.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "DataModel"
      name: "Session Memory"
      table: "N/A (Markdown file)"
      purpose: "Per-story observation persistence during story lifecycle"
      fields:
        - name: "story_id"
          type: "String"
          constraints: "Required, STORY-NNN format"
          description: "Story identifier"
          test_requirement: "Test: Validate story_id in frontmatter"
        - name: "created"
          type: "DateTime"
          constraints: "Required, ISO8601"
          description: "Session creation timestamp"
          test_requirement: "Test: Validate ISO8601 format"
        - name: "last_updated"
          type: "DateTime"
          constraints: "Required, ISO8601"
          description: "Last modification timestamp"
          test_requirement: "Test: Validate updated on each append"
        - name: "status"
          type: "Enum"
          constraints: "Required, active|archived"
          description: "Session lifecycle status"
          test_requirement: "Test: Validate status transitions"

    - type: "Configuration"
      name: "phase-01-preflight.md"
      file_path: ".claude/skills/devforgeai-development/phases/phase-01-preflight.md"
      required_keys:
        - key: "Session Memory Creation"
          type: "section"
          required: true
          test_requirement: "Test: Grep for session memory creation instructions"
        - key: "Stale Session Cleanup"
          type: "section"
          required: true
          test_requirement: "Test: Grep for cleanup instructions"

    - type: "Configuration"
      name: "Phase exit gates (02-08)"
      file_path: ".claude/skills/devforgeai-development/phases/phase-{02-08}-*.md"
      required_keys:
        - key: "Session Memory Update"
          type: "section"
          required: true
          test_requirement: "Test: Grep for session memory append instructions"

  business_rules:
    - id: "BR-001"
      rule: "Session memory file must be created at Phase 01 completion"
      trigger: "Phase 01 exit gate"
      validation: "File exists at .claude/memory/sessions/{STORY_ID}-session.md"
      error_handling: "Create file if missing, warn if creation fails"
      test_requirement: "Test: Verify file creation at Phase 01 exit"
      priority: "Critical"
    - id: "BR-002"
      rule: "Observations must be appended after each phase (02-08)"
      trigger: "Phase exit gate (02-08)"
      validation: "Phase section exists in session memory"
      error_handling: "Append section if missing"
      test_requirement: "Test: Verify observations appended for each phase"
      priority: "Critical"
    - id: "BR-003"
      rule: "Stale sessions (>7 days, status=active) must be cleaned up"
      trigger: "Phase 01 of any story"
      validation: "No stale session files remain"
      error_handling: "Archive stale files"
      test_requirement: "Test: Verify cleanup with 8-day-old session"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Storage"
      requirement: "Session memory file size"
      metric: "5-20KB per story"
      test_requirement: "Test: Verify file size within range after full lifecycle"
      priority: "Low"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Session memory operations minimal overhead"
      metric: "<100ms per append operation"
      test_requirement: "Test: Measure append time"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Storage

**Session Memory Size:**
- 5-20KB per story (typical)
- Archive sessions >30 days old

### Performance

**Operation Time:**
- Session creation: <50ms
- Observation append: <100ms
- Stale cleanup: <500ms (batch operation)

### Reliability

**Atomic Writes:**
- Session updates should be atomic
- No partial writes on failure

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-339:** Create ADR for Source Tree Memory Directories
  - **Why:** ADR must approve .claude/memory/sessions/ directory
  - **Status:** Backlog

### External Dependencies

- [ ] **EPIC-051:** Framework Feedback Capture System
  - **Owner:** DevForgeAI Core
  - **ETA:** Feb 9, 2026
  - **Status:** In Progress
  - **Impact if delayed:** Observations won't exist to store in session memory

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95% for session memory operations

**Test Scenarios:**
1. **Happy Path:**
   - Session created at Phase 01
   - Observations appended at each phase
   - Session archived on completion
2. **Edge Cases:**
   - No observations for a phase (empty section)
   - Very large observation (>1KB per phase)
   - Concurrent story development (isolation)
3. **Error Cases:**
   - Directory doesn't exist (create it)
   - Write permission denied
   - Malformed session file

---

## Acceptance Criteria Verification Checklist

### AC#1: Session Memory Created at Phase 01

- [ ] Write() instruction added to phase-01-preflight.md - **Phase:** 3 - **Evidence:** Grep for Write() pattern
- [ ] File path uses STORY_ID variable - **Phase:** 3 - **Evidence:** Path pattern validation
- [ ] YAML frontmatter includes required fields - **Phase:** 3 - **Evidence:** Schema validation

### AC#2: Observations Appended After Each Phase

- [ ] Edit/Append instruction added to phase-02 - **Phase:** 3 - **Evidence:** Grep for Edit() pattern
- [ ] Edit/Append instruction added to phase-03 - **Phase:** 3 - **Evidence:** Grep for Edit() pattern
- [ ] Edit/Append instructions for phases 04-08 - **Phase:** 3 - **Evidence:** Grep for Edit() pattern
- [ ] Observations include category, note, severity - **Phase:** 3 - **Evidence:** Schema check

### AC#3: Session Memory Archived on Completion

- [ ] Archive logic in story completion workflow - **Phase:** 3 - **Evidence:** Grep for "archived"
- [ ] Status field updated or file moved - **Phase:** 3 - **Evidence:** Logic inspection

### AC#4: Schema Matches Specification

- [ ] YAML frontmatter with story_id, created, last_updated, status - **Phase:** 3 - **Evidence:** Schema validation
- [ ] Observations section with phase headers - **Phase:** 3 - **Evidence:** Section check
- [ ] Reflections section present - **Phase:** 3 - **Evidence:** Section check

### AC#5: Stale Sessions Cleaned Up

- [ ] Cleanup logic in Phase 01 preflight - **Phase:** 3 - **Evidence:** Grep for cleanup
- [ ] 7-day threshold enforced - **Phase:** 3 - **Evidence:** Threshold check

---

**Checklist Progress:** 0/14 items complete (0%)

---

## Definition of Done

### Implementation
- [x] phase-01-preflight.md modified with session creation
- [x] Phase files 02-08 modified with observation append
- [x] Story completion workflow archives session
- [x] Cleanup logic for stale sessions implemented
- [x] Session memory schema documented

### Quality
- [x] All 5 acceptance criteria have passing tests
- [x] Edge cases covered (empty phases, large observations)
- [x] Schema matches EPIC-052 specification exactly

### Testing
- [x] Test for AC#1: Session created at Phase 01
- [x] Test for AC#2: Observations appended
- [x] Test for AC#3: Session archived
- [x] Test for AC#4: Schema validation
- [x] Test for AC#5: Stale cleanup

### Documentation
- [x] Session memory schema documented in EPIC-052 or dedicated file
- [x] Phase files changelog updated

## Implementation Notes

- [x] phase-01-preflight.md modified with session creation - Completed: 2026-02-02
- [x] Phase files 02-08 modified with observation append - Completed: 2026-02-02
- [x] Story completion workflow archives session - Completed: 2026-02-02
- [x] Cleanup logic for stale sessions implemented - Completed: 2026-02-02
- [x] Session memory schema documented - Completed: 2026-02-02
- [x] All 5 acceptance criteria have passing tests - Completed: 2026-02-02
- [x] Edge cases covered (empty phases, large observations) - Completed: 2026-02-02
- [x] Schema matches EPIC-052 specification exactly - Completed: 2026-02-02
- [x] Test for AC#1: Session created at Phase 01 - Completed: 2026-02-02
- [x] Test for AC#2: Observations appended - Completed: 2026-02-02
- [x] Test for AC#3: Session archived - Completed: 2026-02-02
- [x] Test for AC#4: Schema validation - Completed: 2026-02-02
- [x] Test for AC#5: Stale cleanup - Completed: 2026-02-02
- [x] Session memory schema documented in EPIC-052 or dedicated file - Completed: 2026-02-02
- [x] Phase files changelog updated - Completed: 2026-02-02

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-02

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-30 14:00 | claude/create-story | Created | Story created for EPIC-052 Feature 2 | STORY-341.story.md |
| 2026-02-02 | claude/dev | Dev Complete | TDD implementation complete, all 5 ACs pass | src/claude/skills/devforgeai-development/phases/*.md, tests/STORY-341/*.sh |
| 2026-02-02 | claude/qa-result-interpreter | QA Deep | PASSED: 7/7 tests, 0 blocking violations | devforgeai/qa/reports/STORY-341-qa-report.md |

## Notes

**Session Memory Schema (from EPIC-052):**
```markdown
---
story_id: STORY-XXX
created: 2026-01-26T12:00:00Z
last_updated: 2026-01-26T14:30:00Z
status: active | archived
---

# Session Memory: STORY-XXX

## Observations

### Phase 02 (Test-First)
- [gap] Coverage gap identified in edge cases (high)
- [success] All AC tests written successfully (medium)

### Phase 03 (Implementation)
- [friction] Type mismatch required refactoring (medium)
- [pattern] Used repository pattern effectively (low)

## Reflections

### Reflection 1 (Phase 03, Iteration 2)
- **What happened:** Implementation failed type check
- **Why it failed:** Misread AC#2 expected return type
- **How to improve:** Verify AC types before implementing

## Subagent Invocations

| Timestamp | Subagent | Phase | Duration |
|-----------|----------|-------|----------|
| 12:01:00 | test-automator | 02 | 45s |
| 12:05:00 | backend-architect | 03 | 120s |

## Phase Progression

| Phase | Started | Completed | Iterations |
|-------|---------|-----------|------------|
| 02 | 12:00:00 | 12:05:00 | 1 |
| 03 | 12:05:00 | 12:15:00 | 2 |
```

**Design Decisions:**
- Markdown format for human readability
- Per-story isolation prevents concurrency issues
- 7-day stale threshold balances cleanup with debug needs

**References:**
- EPIC-052: Framework Feedback Display & Memory System (Feature 2, lines 171-237)
- STORY-339: ADR for memory directories (prerequisite)

---

Story Template Version: 2.7
Last Updated: 2026-01-30
