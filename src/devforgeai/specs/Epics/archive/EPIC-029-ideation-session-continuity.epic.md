---
id: EPIC-029
title: Ideation Session Continuity & Error Resilience
business-value: Prevent data loss during 60-question sessions and improve error recovery
status: Planning
priority: High
complexity-score: 37
architecture-tier: Tier 3
created: 2025-12-22
estimated-points: 25-30
target-sprints: 2-3
source-brainstorm: BRAINSTORM-001
dependencies:
  - EPIC-028 (refactored command structure required)
---

# EPIC-029: Ideation Session Continuity & Error Resilience

## Business Goal

Implement checkpoint protocol to preserve user data during long ideation sessions (10-60 questions, 30-90 minutes). Enable resume-from-checkpoint after disconnects or context window clears. Improve error handling for skill loading failures and malformed brainstorm data.

**Success Metrics:**
- Zero data loss when session disconnects (100% recovery)
- Resume success rate >95% (checkpoint read + replay)
- Skill loading failures result in HALT with repair instructions (not silent failure)
- Malformed brainstorm YAML detected and recovered gracefully

## Features

### Feature 1: File-Based Checkpoint Protocol
**Description:** Write session state to devforgeai/temp/ at phase boundaries to survive context clears

**User Stories (high-level):**
1. As a user, I want my 60 answers preserved if my session disconnects
2. As a user, I want to resume from where I left off without re-answering questions
3. As a framework maintainer, I want checkpoints to survive context window clears

**Implementation:**
- Create checkpoint files: `devforgeai/temp/.ideation-checkpoint-{session-id}.yaml`
- Write checkpoints after Phase 1, 2, 3, 4, 5 (before Phase 6 artifact generation)
- Checkpoint content:
  ```yaml
  session_id: {uuid}
  timestamp: {iso8601}
  current_phase: {1-6}
  brainstorm_context: {if applicable}
  discovered_data:
    problem_statement: {text}
    user_personas: [{persona objects}]
    requirements: [{requirement objects}]
    complexity_score: {0-60}
    epics: [{epic summaries}]
  phase_completion:
    phase_1: {complete|incomplete}
    phase_2: {complete|incomplete}
    # ... etc
  ```
- Use Write tool (not Bash) to create checkpoint file

**Estimated Effort:** Medium (8 points)

---

### Feature 2: Resume-from-Checkpoint Logic
**Description:** Detect checkpoint files at skill start, offer resume, replay from last phase with pre-filled answers

**User Stories (high-level):**
1. As a user resuming after disconnect, I want to see my previous answers and confirm/update them
2. As a user resuming after context clear, I want to continue from my last completed phase
3. As a framework maintainer, I want resume logic to handle partial phases gracefully

**Implementation:**
- At skill invocation (Phase 1 Step 0), check for checkpoint files:
  ```
  checkpoints = Glob(pattern="devforgeai/temp/.ideation-checkpoint-*.yaml")
  IF len(checkpoints) > 0:
    AskUserQuestion: "Resume from checkpoint or start fresh?"
  ```
- If resume selected:
  - Read checkpoint file
  - Display summary of progress: "{completed_phases}/6 phases complete"
  - Resume from last incomplete phase
  - Pre-fill answers from checkpoint (display, allow editing)
- Replay strategy: Start at phase beginning, show previous answers, ask "Keep or update?"

**Estimated Effort:** Large (12 points)

---

### Feature 3: Auto-Cleanup Completed Checkpoints
**Description:** Delete checkpoint files when ideation completes successfully

**User Stories (high-level):**
1. As a user, I don't want stale checkpoint files accumulating
2. As a framework maintainer, I want automatic cleanup to prevent disk bloat
3. As a developer, I want checkpoints preserved if ideation fails (for debugging)

**Implementation:**
- At Phase 6 successful completion:
  ```bash
  # Delete checkpoint file for current session
  rm devforgeai/temp/.ideation-checkpoint-{session_id}.yaml
  ```
- If ideation fails/interrupted: Keep checkpoint for recovery
- Add cleanup command: `/ideate --clean-checkpoints` to manually remove old checkpoints

**Estimated Effort:** Small (3 points)

---

### Feature 4: Skill Loading Failure Recovery
**Description:** HALT with repair instructions if SKILL.md is corrupted or missing (E1 fix)

**User Stories (high-level):**
1. As a user, I want clear error messages if skill fails to load
2. As a framework maintainer, I want users to self-recover from skill corruption
3. As a developer, I want guidance on how to fix broken skill files

**Implementation:**
- At skill invocation, wrap in error handler:
  ```
  TRY:
    Skill(command="devforgeai-ideation")
  CATCH SkillLoadError:
    HALT with message:
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     ❌ Skill Loading Failure
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    The devforgeai-ideation skill failed to load.

    Possible causes:
    - SKILL.md has invalid YAML frontmatter
    - SKILL.md file is missing or corrupted
    - Reference files in references/ are missing

    Recovery steps:
    1. Check: .claude/skills/devforgeai-ideation/SKILL.md exists
    2. Validate YAML frontmatter (lines 1-10)
    3. Compare with GitHub version: [link]
    4. Run: git checkout .claude/skills/devforgeai-ideation/

    If issue persists, report at: https://github.com/anthropics/claude-code/issues"
  ```

**Estimated Effort:** Small (4 points)

---

### Feature 5: YAML-Malformed Brainstorm Detection
**Description:** Validate brainstorm YAML on load, graceful fallback if corrupted (W1 fix)

**User Stories (high-level):**
1. As a user, I want clear error if my brainstorm file is corrupted
2. As a framework maintainer, I want graceful degradation (skip brainstorm, continue with fresh ideation)
3. As a developer, I want YAML parsing errors to be caught early

**Implementation:**
- In brainstorm-handoff-workflow.md Section 2.2:
  ```
  FUNCTION validate_brainstorm_context(context):
    TRY:
      parse_yaml_frontmatter(context)
    CATCH YAMLParseError:
      Display:
      "⚠ Brainstorm file has invalid YAML

       File: {brainstorm_path}
       Error: {parse_error}

       Proceeding with fresh ideation (brainstorm skipped)"

      RETURN null  # Skip brainstorm, start fresh
  ```
- Add YAML validation checklist to error-handling.md

**Estimated Effort:** Small (4 points)

---

### Feature 6: Question Duplication Elimination
**Description:** Enforce single-source-of-truth: skill owns all questions, command only validates args (D1 fix)

**User Stories (high-level):**
1. As a user, I want to answer "project type" ONCE, not twice
2. As a framework maintainer, I want question logic in skill, not scattered across command + skill
3. As a developer, I want clear ownership: command orchestrates, skill asks

**Implementation:**
- Remove project type question from command Phase 1
- Remove all discovery questions from command
- Skill Phase 1 asks all questions (including project type if not provided)
- Command Phase 1 responsibilities:
  - Validate business idea argument is non-empty
  - Detect brainstorms (offer selection)
  - Pass business idea + brainstorm context to skill
- Discovery-workflow.md owns all question templates

**Estimated Effort:** Medium (6 points)

---

## Requirements Summary

### Functional Requirements
- Checkpoint protocol writes state at phase boundaries
- Resume logic detects checkpoints, offers resume, pre-fills answers
- Auto-cleanup removes completed checkpoints
- Skill loading failures result in HALT with repair instructions
- YAML validation catches brainstorm corruption
- Question ownership: skill asks, command orchestrates

### Data Model
**Entities:**
- Checkpoint file (.ideation-checkpoint-{session-id}.yaml): Session state snapshot
- Session metadata: Session ID, timestamp, phase completion status
- Discovered data: Problem, personas, requirements, complexity, epics

**Relationships:**
- Session → Checkpoint (1:N during session, 1:0 after completion)
- Checkpoint → Skill phases (captures state of each phase)

### Integration Points
1. **File system:** Write/Read checkpoint files to devforgeai/temp/
2. **Error handlers:** Wrap skill invocation, YAML parsing
3. **Cleanup hooks:** Delete checkpoints on success

### Non-Functional Requirements

**Data Preservation:**
- 100% recovery rate for disconnects (if checkpoint written before disconnect)
- Checkpoint files survive context window clears

**User Experience:**
- Resume offers choice: "Resume or start fresh?"
- Pre-filled answers save time (user can edit)
- Clear error messages for skill loading failures

**Reliability:**
- Checkpoints written atomically (Write tool)
- YAML validation prevents silent failures
- Graceful degradation when brainstorm corrupted

## Architecture Considerations

**Complexity Tier:** Tier 3 (Complex System)

**Recommended Architecture:**
- **Pattern:** State Management with Persistence
- **Layers:** Session management (checkpoints), Error handling (validation), Recovery (resume logic)
- **Data Storage:** File-based (YAML in devforgeai/temp/)

**Technology Recommendations:**
- YAML for checkpoint serialization (human-readable, editable)
- UUID for session IDs (collision-free)
- ISO8601 for timestamps (standard format)

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Checkpoint file corruption | MEDIUM | Validate checkpoint YAML on read, catch parse errors, offer fresh start |
| Resume logic bugs (incomplete phase handling) | HIGH | Comprehensive testing: disconnect at every phase, verify resume works |
| Context overflow during resume (loading checkpoint + skill) | LOW | Checkpoints are concise (<5KB), skill loads progressively |
| Users confused by "resume or fresh" prompt | LOW | Clear display of progress: "{completed_phases}/6 phases complete" |
| Auto-cleanup deletes checkpoint before user reviews output | LOW | Cleanup AFTER Phase 6.6 (user confirms next action) |

## Dependencies

**Prerequisites:**
- **EPIC-028:** Refactored command structure (simplified phases make checkpoint integration cleaner)

**Dependents:**
- None (EPIC-030 can run in parallel)

## Next Steps

1. **Dependency:** Wait for EPIC-028 completion (refactored command structure)
2. **Implementation Order:**
   - Feature 1 (checkpoint protocol) first - foundational
   - Feature 2 (resume logic) second - depends on Feature 1
   - Feature 3 (auto-cleanup) third - simple addition to Feature 2
   - Features 4, 5, 6 (error handling) - can run in parallel with 1-3
3. **Testing:** Disconnect scenarios, context clear scenarios, YAML corruption, skill load failures
4. **Documentation:** Update skill workflow docs, add checkpoint file format spec

---

**Created from:** BRAINSTORM-001 (HIGH confidence)

## Stories

| Story ID | Feature | Title | Status | Points | Depends On |
|----------|---------|-------|--------|--------|------------|
| STORY-136 | F1 | File-Based Checkpoint Protocol | Backlog | 8 | - |
| STORY-137 | F2 | Resume-from-Checkpoint Logic | Backlog | 12 | STORY-136 |
| STORY-138 | F3 | Auto-Cleanup Completed Checkpoints | Backlog | 3 | STORY-137 |
| STORY-139 | F4 | Skill Loading Failure Recovery | Backlog | 4 | - |
| STORY-140 | F5 | YAML-Malformed Brainstorm Detection | Backlog | 4 | - |
| STORY-141 | F6 | Question Duplication Elimination | Backlog | 6 | - |

**Total Points:** 37
