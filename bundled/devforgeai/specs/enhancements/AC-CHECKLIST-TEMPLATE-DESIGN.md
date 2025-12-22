# AC Verification Checklist Template Design

**Purpose:** Design flexible AC Checklist structure for all story types with real-time TDD workflow integration

**Date:** 2025-11-18
**Related:** RCA-011 (AC Checklist not updated real-time)

---

## Design Principles

1. **Story-Type Agnostic:** Works for CRUD, authentication, refactoring, bug fixes, etc.
2. **Auto-Generated:** devforgeai-story-creation generates checklist from ACs
3. **Phase-Mapped:** Each checklist item maps to specific TDD phase
4. **Granular:** Break ACs into small, checkable sub-items
5. **Evidence-Linked:** Each item references test or implementation evidence

---

## Template Structure

### Generic Format

```markdown
## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation. Check off items as each sub-task completes.

**Note:** This checklist supplements TodoWrite (phase tracking) and Definition of Done (official completion record).

**For AC#{N}: {AC Description}**
- [ ] {Sub-item 1} - **Phase:** {1-5} - **Evidence:** {test file or implementation location}
- [ ] {Sub-item 2} - **Phase:** {1-5} - **Evidence:** {test file or implementation location}
- [ ] {Sub-item 3} - **Phase:** {1-5} - **Evidence:** {test file or implementation location}

**For AC#{N+1}: {AC Description}**
- [ ] {Sub-item 1} - **Phase:** {1-5} - **Evidence:** {test file or implementation location}
...
```

### Example for CRUD Story

```markdown
## Acceptance Criteria Verification Checklist

**For AC#1: Create Endpoint Implementation**
- [ ] POST /api/users endpoint created - **Phase:** 2 - **Evidence:** src/controllers/users.controller.ts
- [ ] Request validation implemented - **Phase:** 2 - **Evidence:** src/validators/user.validator.ts
- [ ] Database insert logic working - **Phase:** 2 - **Evidence:** tests/integration/test_user_create.py passing
- [ ] 201 Created response returned - **Phase:** 4 - **Evidence:** Integration test validates status code

**For AC#2: Input Validation**
- [ ] Email format validation - **Phase:** 2 - **Evidence:** Unit test test_email_validation passing
- [ ] Password strength check - **Phase:** 2 - **Evidence:** Unit test test_password_strength passing
- [ ] 400 Bad Request on invalid input - **Phase:** 2 - **Evidence:** Unit test test_validation_errors passing

**For AC#3: Error Handling**
- [ ] Duplicate email returns 409 - **Phase:** 2 - **Evidence:** Unit test test_duplicate_email passing
- [ ] Database errors logged - **Phase:** 2 - **Evidence:** Logging middleware verified
- [ ] Error message format consistent - **Phase:** 3 - **Evidence:** Code review validates
```

### Example for Refactoring Story (like STORY-038)

```markdown
## Acceptance Criteria Verification Checklist

**For AC#1: Command Size Reduction**
- [ ] Character count ≤15,000 - **Phase:** 2-3 - **Evidence:** wc -c < command.md
- [ ] Line count ≤350 lines - **Phase:** 2-3 - **Evidence:** wc -l < command.md
- [ ] Budget compliance verified - **Phase:** 4 - **Evidence:** Integration test test_command_size_reduction

**For AC#2: Business Logic Extraction**
- [ ] Argument validation only (~30 lines) - **Phase:** 2 - **Evidence:** grep for IF/ELSE in command
- [ ] No deployment logic in command - **Phase:** 2 - **Evidence:** grep verification test passing
- [ ] No smoke test execution in command - **Phase:** 2 - **Evidence:** Code review confirms
- [ ] No rollback logic in command - **Phase:** 2 - **Evidence:** Code review confirms
- [ ] Grep verification passes - **Phase:** 4 - **Evidence:** test_business_logic_extraction passing
```

---

## Phase-to-Checklist Mapping

### Phase 1 (Red - Test Generation)
**Check off items related to:**
- Test count (unit, integration, regression)
- Test coverage of ACs
- Test framework setup
- Test file creation

**Example items:**
- [ ] Unit tests ≥15 generated
- [ ] Integration tests ≥12 generated
- [ ] All ACs have corresponding tests
- [ ] Test files created in correct location

### Phase 2 (Green - Implementation)
**Check off items related to:**
- Code implementation
- Business logic
- API endpoints
- Data models
- File creation/modification

**Example items:**
- [ ] Implementation code written
- [ ] Business logic extracted
- [ ] API endpoints created
- [ ] Character count verified
- [ ] Line count verified

### Phase 3 (Refactor - Code Quality)
**Check off items related to:**
- Code quality metrics
- Refactoring completions
- Code review findings
- Pattern compliance

**Example items:**
- [ ] Cyclomatic complexity <10
- [ ] Code duplication <5%
- [ ] Pattern compliance validated
- [ ] Code review passed

### Phase 4 (Integration - Cross-Component)
**Check off items related to:**
- Integration test results
- Cross-component validations
- Performance metrics
- Coverage thresholds

**Example items:**
- [ ] Integration tests passing
- [ ] Performance targets met
- [ ] Coverage ≥95% (or story-specific threshold)
- [ ] Scenario tests passing

### Phase 4.5 (Deferral Challenge)
**Check off items related to:**
- Deferral validations
- Follow-up story creation
- User approvals

**Example items:**
- [ ] All deferrals validated
- [ ] User approved deferrals (if any)
- [ ] Follow-up stories created (if needed)

### Phase 5 (Git Workflow)
**Check off items related to:**
- Deployment readiness
- Commit creation
- Status updates

**Example items:**
- [ ] Git commit created
- [ ] Story status updated
- [ ] Backward compatibility verified

---

## Auto-Generation Logic (for devforgeai-story-creation)

### Step 1: Parse Acceptance Criteria

```
FOR each AC in story:
  Extract: AC number, description, scenario details
  Identify: testable sub-items from AC text
```

### Step 2: Generate Checklist Items

```
FOR each AC:
  Sub-items = break_into_testable_components(AC)

  FOR each sub-item:
    Determine phase = infer_phase_from_item(sub-item)
    Determine evidence = infer_evidence_location(sub-item, story_type)

    Create checklist_item:
      - [ ] {sub-item} - **Phase:** {phase} - **Evidence:** {evidence}
```

### Step 3: Infer Phase from Sub-Item Type

```
IF sub-item contains "test" or "coverage":
  phase = 1 (Red - test generation)

ELIF sub-item contains "implement" or "create" or "endpoint":
  phase = 2 (Green - implementation)

ELIF sub-item contains "refactor" or "quality" or "complexity":
  phase = 3 (Refactor - code quality)

ELIF sub-item contains "integration" or "performance" or "scenario":
  phase = 4 (Integration - cross-component)

ELIF sub-item contains "commit" or "deployment" or "backward":
  phase = 5 (Git workflow)

ELSE:
  phase = 2 (default to implementation)
```

### Step 4: Infer Evidence Location

```
IF story_type == "CRUD":
  evidence = "src/{entity}/{endpoint}.{ext}"

ELIF story_type == "Refactoring":
  evidence = "wc -c/-l < {file being refactored}"

ELIF story_type == "Bug Fix":
  evidence = "tests/regression/test_{bug_id}.py"

ELIF story_type == "Feature":
  evidence = "tests/integration/test_{feature}.py"

Add test evidence:
  evidence += " + test_{item}.py passing"
```

---

## Template Insertion Point

**Location in story template:**
```markdown
## Edge Cases and Error Scenarios
...

---

## Acceptance Criteria Verification Checklist  ← INSERT HERE

**Purpose:** Real-time progress tracking...

---

## Definition of Done
...
```

**Rationale:** Place AFTER edge cases (part of specification) but BEFORE Definition of Done (implementation tracking)

---

## Workflow Integration Pattern

### Pattern: Incremental Edit Operations

**Phase Completion → Check AC Items → Edit Story File**

```
Phase {N} completes successfully
  ↓
Identify AC items mapped to Phase {N}
  ↓
FOR each item:
  Edit(
    file_path=story_file,
    old_string="- [ ] {item text}",
    new_string="- [x] {item text}"
  )
  ↓
Display: "✓ AC item checked: {item}"
  ↓
Continue TDD workflow
```

**Performance:** 1 Edit operation per AC sub-item (estimate 20-30 Edits per story = ~2-3 minutes overhead)

---

## Quality Considerations

### Benefits
✅ Real-time visibility (user sees progress as items check off)
✅ Prevents skipped items (explicit validation)
✅ Granular tracking (more detailed than phase-level TodoWrite)
✅ Evidence-linked (each item shows where to verify)
✅ Phase-mapped (clear when each item gets checked)

### Trade-offs
⚠️ Adds 20-30 Edit operations per story (~2-3 min overhead)
⚠️ Requires story file edits during workflow (more file I/O)
⚠️ Increases story file complexity (3 tracking mechanisms: TodoWrite, AC Checklist, DoD)
⚠️ Maintenance burden (keep phase mapping accurate)

### Mitigation
- Make checklist optional (can be disabled via config)
- Batch edits where possible (check multiple items per Edit)
- Clear documentation prevents confusion about which tracker to use

---

## Alternative: Simpler Approach

**Instead of real-time updates, update checklist at END of each phase:**

```
Phase 2 completes
  ↓
Batch update ALL Phase 2 items (single Edit with multiple replacements)
  ↓
Display phase summary with items checked
  ↓
Continue to Phase 3
```

**Benefit:** Reduces Edit operations from 20-30 to 5-6 (one per phase)
**Trade-off:** Not truly "real-time" (phase-level granularity)

---

## Recommendation

**Implement: End-of-Phase Batch Updates** (simpler approach)

**Rationale:**
- Achieves "real-time tracking" goal (visible progress)
- Reduces performance impact (6 Edits vs 30 Edits)
- Clearer workflow integration (one update step per phase)
- Easier to maintain (fewer conditional checks)

**User sees:**
- Phase 1 completes → 8 AC items checked ✓
- Phase 2 completes → 12 AC items checked ✓
- Phase 3 completes → 5 AC items checked ✓
- etc.

---

**Status:** Design complete, ready for implementation
