---
id: STORY-157
title: Batch Story Creation from RCA Recommendations
type: feature
epic: EPIC-032
priority: Medium
points: 5
depends_on: ["STORY-155", "STORY-156"]
status: QA Approved
created: 2025-12-25
---

# STORY-157: Batch Story Creation from RCA Recommendations

## User Story

**As a** DevForgeAI developer,
**I want** to create multiple stories from selected RCA recommendations in batch mode,
**So that** stories are created efficiently and match the quality of epic-generated stories.

## Acceptance Criteria

### AC#1: Map Recommendation Fields to Story Batch Markers

**Given** selected recommendations with priority, title, description, effort, and success criteria
**When** preparing for story creation
**Then** fields are mapped to devforgeai-story-creation batch context markers (Story ID, Epic ID, Feature Name, Priority, Points, Type, Sprint, Batch Mode: true)

### AC#2: Invoke Story Creation Skill in Batch Mode

**Given** batch context markers are set for a recommendation
**When** invoking devforgeai-story-creation skill
**Then** the skill executes in batch mode (skipping Phase 1 questions, executing Phases 2-7)

### AC#3: Create Stories Sequentially with Progress Display

**Given** multiple recommendations are selected for story creation
**When** creating stories
**Then** each story is created sequentially with progress display: "[N/Total] Creating: {title}"

### AC#4: Handle Story Creation Failure

**Given** story creation fails for a recommendation (e.g., validation error)
**When** the failure occurs
**Then** log the error, continue to next recommendation (BR-004), and include in failure report

### AC#5: Report Success and Failure Summary

**Given** all selected recommendations have been processed
**When** batch creation completes
**Then** display summary: "✅ Created: N stories" and "❌ Failed: M stories" with story IDs and failure reasons

## CRITICAL: Constitutional Document Requirements

**BEFORE generating tests or implementation, Claude MUST read ALL 6 DevForgeAI constitutional documents:**

1. `devforgeai/specs/context/tech-stack.md` - Framework implementation constraints
2. `devforgeai/specs/context/source-tree.md` - Directory structure rules
3. `devforgeai/specs/context/dependencies.md` - Framework dependencies
4. `devforgeai/specs/context/coding-standards.md` - Code patterns
5. `devforgeai/specs/context/architecture-constraints.md` - Design rules
6. `devforgeai/specs/context/anti-patterns.md` - Forbidden patterns

**Key Constraints for This Story:**
- `.claude/commands/` contains **Markdown files ONLY** (not JavaScript modules)
- Framework components are **pseudocode in Markdown** - NOT executable code
- Commands invoke skills and subagents via `Skill()` and `Task()` - NOT function calls
- Tests for Markdown commands are **shell/Bash tests** validating Claude execution output

**Failure Mode (Documented 2025-12-30):**
Previous test-automator session generated Jest tests expecting a `.js` module at `.claude/commands/batch-story-creator.js`, violating tech-stack.md lines 22-25 and source-tree.md line 562 which prohibit executable code in `.claude/commands/`.

---

## Technical Specification

```yaml
technical_specification:
  version: "2.0"
  components:
    - type: Service
      name: BatchStoryCreator
      path: .claude/commands/create-stories-from-rca.md
      description: Create stories from recommendations using batch mode
      dependencies:
        - devforgeai-story-creation skill
        - STORY-156 selected recommendations
      test_requirement: Creator invokes skill in batch mode for each selected recommendation

    - type: Configuration
      name: BatchContextMarkers
      description: Context markers for batch story creation
      fields:
        - name: story_id
          source: Next available STORY-NNN
          required: true
        - name: epic_id
          source: RCA source epic or standalone
          required: false
        - name: feature_name
          source: recommendation.title
          required: true
        - name: feature_description
          source: recommendation.description
          required: true
        - name: priority
          source: recommendation.priority (mapped to High/Medium/Low)
          required: true
        - name: points
          source: recommendation.effort_points or default 5
          required: true
        - name: type
          value: feature
          required: true
        - name: sprint
          source: User selection or Backlog
          required: true
        - name: batch_mode
          value: true
          required: true
        - name: source_rca
          source: RCA ID (e.g., RCA-022)
          required: true
        - name: source_recommendation
          source: Recommendation ID (e.g., REC-1)
          required: true
      test_requirement: All batch markers set correctly before skill invocation

    - type: DataModel
      name: BatchResult
      description: Result tracking for batch creation
      fields:
        - name: success
          type: array
          items: {story_id, feature_title}
        - name: failed
          type: array
          items: {feature_title, error_message}
      test_requirement: Results correctly categorized as success or failed

  business_rules:
    - id: BR-001
      name: Priority Mapping
      description: Map RCA priority to story priority (CRITICAL/HIGH → High, MEDIUM → Medium, LOW → Low)
      test_requirement: CRITICAL RCA priority maps to High story priority

    - id: BR-002
      name: Points Calculation
      description: Use recommendation effort_points if available, else default to 5
      test_requirement: Recommendation with 3 points creates 3-point story

    - id: BR-003
      name: Story ID Generation
      description: Generate next sequential STORY-NNN ID for each story
      test_requirement: Stories created with sequential IDs (no gaps)

    - id: BR-004
      name: Failure Isolation
      description: Failure in story N does not affect story N+1 creation
      test_requirement: After failure, next story creation proceeds normally

  non_functional_requirements:
    - category: Performance
      requirement: Story creation completes in <30 seconds per story
      metric: execution_time < 30000ms per story
      test_requirement: Batch of 5 stories completes in under 3 minutes

    - category: Reliability
      requirement: Partial success preserved on failure
      metric: Successfully created stories not affected by later failures
      test_requirement: 3/5 stories created successfully even if 2 fail
```

## Edge Cases

1. **Single recommendation:** Batch mode works with single item (N=1).

2. **All creations fail:** Report all failures with reasons, no stories created.

3. **Story ID conflict:** ID already exists. Increment and retry once.

4. **Skill not available:** devforgeai-story-creation skill missing. HALT with clear error.

5. **Context window limit:** Too many recommendations. Process in batches of 5.

## Non-Functional Requirements

- **Performance:** <30 seconds per story creation
- **Reliability:** Partial success preserved (failure isolation)
- **Traceability:** Source RCA and recommendation ID included in story metadata

## Definition of Done

### Implementation
- [x] Batch context marker mapping implemented
- [x] devforgeai-story-creation skill invocation in batch mode
- [x] Sequential processing with progress display
- [x] Failure handling with continuation
- [x] Success/failure summary report

### Quality
- [x] All 5 acceptance criteria have passing tests
- [ ] Stories match quality of manual creation - DEFERRED: Requires runtime comparison during QA (User approved: 2025-12-30)
- [x] Failures logged with actionable messages

### Testing
- [x] Unit test for marker mapping
- [x] Integration test with skill invocation
- [ ] End-to-end test with real RCA - DEFERRED: Requires actual RCA execution during QA (User approved: 2025-12-30)

### Documentation
- [x] Batch creation flow documented
- [x] Failure recovery documented

## Implementation Notes

- [x] Batch context marker mapping implemented - Completed: Maps RCA recommendation fields to story batch context markers (AC#1)
- [x] devforgeai-story-creation skill invocation in batch mode - Completed: Invokes skill with --batch flag, skips Phase 1 questions (AC#2)
- [x] Sequential processing with progress display - Completed: FOR loop with "[N/Total] Creating: {title}" format (AC#3)
- [x] Failure handling with continuation - Completed: BR-004 failure isolation, tracks failed_stories array (AC#4)
- [x] Success/failure summary report - Completed: Displays "✅ Created: N" and "❌ Failed: M" with details (AC#5)
- [x] All 5 acceptance criteria have passing tests - Completed: 7/7 Bash tests pass
- [x] Failures logged with actionable messages - Completed: Error types and recovery documented in Error Handling section
- [x] Unit test for marker mapping - Completed: test-ac1-marker-mapping.sh validates AC#1
- [x] Integration test with skill invocation - Completed: test-ac2-batch-mode-invocation.sh validates AC#2
- [x] Batch creation flow documented - Completed: batch-creation-workflow.md reference file (321 lines)
- [x] Failure recovery documented - Completed: Error Handling section with 4 error types
- [x] Refactored from 800 lines to 278 lines with progressive disclosure pattern
- [ ] Stories match quality of manual creation - DEFERRED: Requires runtime comparison during QA (User approved: 2025-12-30)
- [ ] End-to-end test with real RCA - DEFERRED: Requires actual RCA execution during QA (User approved: 2025-12-30)

**Developer:** claude/opus
**Implemented:** 2025-12-30

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-25 | DevForgeAI | Story created via /create-missing-stories batch mode |
| 2025-12-30 | claude/opus | Added CRITICAL section: Constitutional document requirements after test-automator generated incorrect Jest tests expecting .js module |
| 2025-12-30 | claude/test-automator | Red (Phase 02) | Generated 7 failing Bash test files validating command file structure | devforgeai/tests/STORY-157/ |
| 2025-12-31 | claude/qa-result-interpreter | QA Deep | PASSED: 7/7 tests, 0 violations, 2 valid deferrals | devforgeai/qa/reports/STORY-157-qa-report.md |
