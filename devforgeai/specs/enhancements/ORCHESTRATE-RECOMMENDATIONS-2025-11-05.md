# Orchestrate Command & Orchestration Skill - Recommendations & Action Plan

**Date:** 2025-11-05
**Priority:** HIGH (budget violation + integration gaps)
**Effort:** 8-11 hours total (6-8 command refactoring + 2-3 skill documentation)
**Impact:** Framework completeness + budget compliance

---

## Executive Summary

Based on comprehensive audit findings, two parallel tracks of work are recommended:

**Track 1: /orchestrate Command Refactoring** (Priority: MEDIUM, Effort: 6-8 hours)
- Extract 234 lines of business logic to skill
- Reduce from 15,012 → ~11,000 chars (27% reduction)
- Achieve budget compliance (100% → 73% usage)

**Track 2: devforgeai-orchestration Skill Enhancement** (Priority: HIGH, Effort: 2-3 hours)
- Add 3 missing skill integrations (ideation, ui-generator, story-creation)
- Move QA retry logic from command to skill
- Achieve 100% skill coverage (5 of 7 → 7 of 7)

**Combined impact:** Complete framework integration + architectural compliance

---

## Track 1: /orchestrate Command Refactoring

### Current State

**Budget:**
- Lines: 599
- Characters: 15,012 ❌ (12 over 15K limit)
- Budget usage: 100%
- Status: OVER BUDGET

**Top-Heavy Sections:**
- Phase 3.5: QA Retry Loop (134 lines) ← Business logic
- Phase 1: Checkpoint Detection (47 lines) ← State management
- Phase 6: Finalization (53 lines) ← Workflow updates
- **Total:** 234 lines should move to skill

---

### Refactoring Strategy

#### Extraction 1: Phase 3.5 QA Retry Loop → devforgeai-orchestration Skill

**What to extract (134 lines):**
```markdown
Lines 199-332:
- QA report reading and failure detection
- Deferral failure specific handling
- Retry attempt counting
- Loop prevention (max 3 attempts)
- AskUserQuestion for user choice (3 options)
- Dev re-invocation for fixes
- QA re-invocation for retry
- Follow-up story creation
- Retry history tracking
```

**Move to skill as:**
```markdown
## Phase 3.5: QA Failure Recovery with Retry Loop

This phase handles QA validation failures with intelligent retry logic.

### Step 1: Detect QA Result
Read QA report, determine PASSED or FAILED

### Step 2: Analyze Failure Type
IF FAILED: Categorize (coverage, anti-pattern, deferral, compliance)

### Step 3: Count Retry Attempts
Parse story workflow history for "QA Attempt" entries

### Step 4: Loop Prevention
IF attempts >= 3: HALT with story split recommendation

### Step 5: Determine Recovery Strategy
Based on failure type and user input:
  - Return to dev for fixes (auto-retry)
  - Manual fix (halt orchestration)
  - Create follow-up stories (deferral resolution)

### Step 6: Execute Recovery
Re-invoke development or create stories as chosen

### Step 7: Track Retry History
Append workflow history with attempt details

Return: "QA_PASSED" | "QA_RETRY_IN_PROGRESS" | "QA_MAX_RETRIES" | "QA_USER_HALT"
```

**Command simplification:**
```markdown
Phase 3: QA Validation
  Skill(command="devforgeai-qa")

  # Skill handles result, including retries
  # Skill returns: QA_PASSED or QA_FAILED_FINAL

  IF QA_PASSED:
    → Proceed to Phase 4
  ELSE:
    → Display skill error message, halt
```

**Savings:** 134 → 5 lines (129 lines saved, ~3,500 chars)

---

#### Extraction 2: Phase 1 Checkpoint Detection → devforgeai-orchestration Skill

**What to extract (47 lines):**
```markdown
Lines 64-110:
- YAML frontmatter parsing
- Workflow history checkpoint search
- Starting phase determination
- Valid/invalid state checking
```

**Move to skill as:**
```markdown
## Phase 0: Story Loading and Checkpoint Detection (NEW)

### Step 1: Load Story Document
Read story file, extract YAML and workflow history

### Step 2: Detect Checkpoints
Search workflow history for:
  - "Checkpoint: DEV_COMPLETE"
  - "Checkpoint: QA_APPROVED"
  - "Checkpoint: STAGING_COMPLETE"

### Step 3: Determine Starting Phase
Based on status and checkpoints:
  - Backlog/Ready for Dev → Start from Phase 2 (Dev)
  - Dev Complete → Start from Phase 3 (QA)
  - QA Approved → Start from Phase 4 (Staging)
  - QA Failed → Restart from Phase 2 (Dev)
  - Checkpoints override status

### Step 4: Validate State
Check if orchestration can proceed:
  - ALLOW: Backlog, Ready for Dev, Dev Complete, QA Approved, QA Failed
  - BLOCK: In Development, QA In Progress, Releasing (manual process running)
  - COMPLETE: Released (already done)

Return: Starting phase number + checkpoint info
```

**Command simplification:**
```markdown
Phase 0: Argument Validation
  Validate story ID format
  Load story via @file

  # Skill determines starting phase internally
  # No checkpoint logic in command
```

**Savings:** 47 → 5 lines (42 lines saved, ~1,200 chars)

---

#### Extraction 3: Phase 6 Finalization → devforgeai-orchestration Skill

**What to extract (53 lines):**
```markdown
Lines 451-503:
- Workflow history updates
- YAML frontmatter status update
- Orchestration timeline documentation
- Checkpoint listing
```

**Move to skill as:**
```markdown
## Phase 6: Finalization (Enhanced from Command)

### Step 1: Calculate Orchestration Metrics
Duration, phase timings, test counts, coverage

### Step 2: Update Workflow History
Append orchestration summary:
  - Timeline (start, end, duration)
  - Phase results (all with durations)
  - Final status
  - Checkpoints reached

### Step 3: Update Story Status
Edit YAML frontmatter:
  - status: "Released"
  - completed_date: {timestamp}

### Step 4: Generate Completion Summary
Return celebratory message with metrics

Return: Completion summary for command to display
```

**Command simplification:**
```markdown
Phase 6: Completion
  # Skill handles all finalization
  Display: skill_result.completion_message
```

**Savings:** 53 → 3 lines (50 lines saved, ~1,500 chars)

---

### Total Refactoring Impact

| Extraction | Lines Saved | Chars Saved |
|------------|-------------|-------------|
| Phase 3.5 (Retry loop) | 129 | ~3,500 |
| Phase 1 (Checkpoints) | 42 | ~1,200 |
| Phase 6 (Finalization) | 50 | ~1,500 |
| **Total** | **221** | **~6,200** |

**Projected command after refactoring:**
- Lines: 599 - 221 = ~378 lines
- Characters: 15,012 - 6,200 = ~8,800 chars
- Budget usage: 8,800 / 15,000 = 59%
- **Status:** ✅ Within budget with 41% headroom

---

## Track 2: devforgeai-orchestration Skill Enhancement

### Current State

**Skill size:** 2,351 lines (70K chars)
**Skill coverage:** 5 of 7 DevForgeAI skills (71%)
**Integration section:** Lines 2225-2251 (26 lines for 4 skills)

---

### Enhancement 1: Add devforgeai-ideation Integration

**Add to "Integration with Other Skills" section (after devforgeai-release):**

```markdown
### devforgeai-ideation
**When:** Project initiation, transforming business ideas into structured requirements (entry point for greenfield projects)
**Invocation:** `Skill(command="devforgeai-ideation")`
**Process:** 6-phase discovery workflow
  - Phase 1-2: Discovery & Requirements Elicitation (interactive, 10-60 questions)
  - Phase 3: Complexity Assessment (0-60 score determines architecture tier)
  - Phase 4: Epic Decomposition (break initiative into epics)
  - Phase 5: Feasibility Analysis (technical assessment, risk evaluation)
  - Phase 6: Documentation, Self-Validation, Next Action
**Output:** Epic documents in `devforgeai/specs/Epics/`, requirements specs in `devforgeai/specs/requirements/`
**Result:** Auto-transitions to devforgeai-architecture for context file creation
**Workflow position:** Entry point (before epics)
**When to skip:** Brownfield projects with well-defined epics, small features

**Orchestration use case:**
When creating new project or major initiative:
1. User runs: /ideate [business-idea]
2. devforgeai-ideation generates epics
3. Auto-transitions to devforgeai-architecture
4. Then devforgeai-orchestration for sprint/story planning
```

**Effort:** 30 minutes (copy from ideation skill, adapt for orchestration context)

---

### Enhancement 2: Add devforgeai-ui-generator Integration

**Add to "Integration with Other Skills" section:**

```markdown
### devforgeai-ui-generator
**When:** Story has UI requirements (optional phase after architecture, before or during development)
**Invocation:** `Skill(command="devforgeai-ui-generator")`
**Process:** 7-phase UI specification workflow
  - Phase 1: Context validation (requires all 6 context files)
  - Phase 2: Story analysis (extract UI requirements from acceptance criteria)
  - Phase 3: Interactive discovery (Web/GUI/Terminal, tech stack, styling)
  - Phase 4: Template loading (framework-specific templates)
  - Phase 5: Code generation (production-ready components)
  - Phase 6: Documentation & story update
  - Phase 7: Specification validation (completeness, placeholders, framework compliance)
**Output:** UI component code in `devforgeai/specs/ui/`, UI-SPEC-SUMMARY.md, story updated with UI references
**Result:** Story has complete UI specification ready for development implementation
**Prerequisites:** devforgeai-architecture must run first (6 context files required)
**Workflow position:** Between architecture and development (optional)
**When to skip:** Backend-only stories, API-only stories, CLI-only features (no UI components)

**Orchestration integration:**
Detection logic for when to invoke UI generator:
  - Story acceptance criteria mention: "UI", "form", "dashboard", "page", "component", "interface"
  - Story has UI specification section with placeholders
  - Explicit user request: /create-ui [STORY-ID]

Invocation timing:
  - After: devforgeai-architecture complete (context files validated)
  - Before: devforgeai-development starts (UI specs inform TDD)
  - Or during: Developer requests UI spec mid-development

Coordination:
  - Ask user: "Story has UI requirements. Generate UI specs now?" (Yes/Skip/After dev)
  - If Yes: Invoke devforgeai-ui-generator
  - If Skip: Proceed to development (can run /create-ui manually later)
  - If After dev: Continue, remind after dev complete
```

**Effort:** 45 minutes (copy from ui-generator skill, add orchestration coordination logic)

---

### Enhancement 3: Complete devforgeai-story-creation Documentation

**Add to "Integration with Other Skills" section:**

```markdown
### devforgeai-story-creation
**When:** Creating stories from feature descriptions, decomposing epics, generating follow-up stories for deferred work
**Invocation:** `Skill(command="devforgeai-story-creation")`
**Process:** 8-phase complete story generation workflow
  - Phase 1: Story Discovery (generate ID, epic/sprint context, metadata)
  - Phase 2: Requirements Analysis (requirements-analyst subagent, user story + AC)
  - Phase 3: Technical Specification (api-designer subagent, data models, business rules)
  - Phase 4: UI Specification (components, mockups, accessibility - if UI detected)
  - Phase 5: Story File Creation (YAML frontmatter + markdown sections)
  - Phase 6: Epic/Sprint Linking (update parent documents)
  - Phase 7: Self-Validation (quality checks, self-healing)
  - Phase 8: Completion Report (summary, next actions)
**Output:** Complete story document in `devforgeai/specs/Stories/{STORY-ID}.story.md` with all sections
**Result:** Story created in Backlog status, linked to epic/sprint, fully specified, ready for development
**Workflow position:** Story creation phase (after sprint planning, before development)

**When orchestration invokes story-creation:**
- Epic decomposition into stories (Phase 4A: Epic Creation, Step 6)
- Deferral tracking (Phase 4.5: Deferred Work Tracking, creating follow-up stories)
- Automated story generation from feature list

**Subagents used by story-creation:**
- requirements-analyst (Phase 2) - User story and acceptance criteria
- api-designer (Phase 3, conditional) - API contracts if endpoints detected

**Reusability:** Also invoked by /create-story command, development skill (deferral follow-ups)
```

**Effort:** 30 minutes (extract from story-creation skill, add orchestration context)

---

### Enhancement 4: Add Phase 3.5 QA Retry Logic to Skill

**Add new phase to devforgeai-orchestration skill:**

```markdown
## Phase 3.5: QA Failure Recovery with Retry Loop (NEW - Moved from Command)

**Purpose:** Handle QA validation failures with intelligent retry logic, loop prevention, and automated recovery.

**This phase moves 134 lines of business logic FROM /orchestrate command TO skill for proper layer separation.**

---

### Step 1: Load QA Report and Detect Failure

```
Read(file_path="devforgeai/qa/reports/{STORY_ID}-qa-report.md")

Parse report:
  - Overall status: PASSED or FAILED
  - Failure type: coverage, anti-pattern, deferral, compliance
  - Violations: CRITICAL, HIGH, MEDIUM, LOW counts
  - Specific issues: List of violations with remediation
```

---

### Step 2: Count Retry Attempts

```
Read(file_path="devforgeai/specs/Stories/{STORY_ID}.story.md")

Grep(pattern="QA Attempt [0-9]+", path=story_file)

qa_attempts = count of "QA Attempt" entries in workflow history

Display: "QA attempt {qa_attempts} failed"
```

---

### Step 3: Loop Prevention

```
IF qa_attempts >= 3:
    # Max retries exceeded - suggest story split

    Return structured result:
    {
      "status": "QA_MAX_RETRIES_EXCEEDED",
      "attempts": qa_attempts,
      "last_failure": failure_type,
      "violations": violations_list,
      "recommendation": "Story scope too large - split into smaller stories",
      "actions": [
        "Review DoD items for proper estimation",
        "Split story into 2-3 smaller stories",
        "Escalate blockers to leadership",
        "Manual fix: /dev {STORY_ID}"
      ]
    }

    HALT orchestration
```

---

### Step 4: Determine Recovery Strategy Based on Failure Type

```
IF failure_type == "deferral":
    # Specific handling for deferral violations

    AskUserQuestion:
        Question: "QA failed due to deferral violations (attempt {qa_attempts}/3). How to proceed?"
        Header: "QA Deferral Failure"
        Options:
            - "Fix deferrals and retry (return to development)"
            - "Create follow-up stories for deferred items"
            - "Manual resolution (halt orchestration)"
        multiSelect: false

    user_choice = response

ELSE IF failure_type IN ["coverage", "anti-pattern", "compliance"]:
    # Standard QA failures

    AskUserQuestion:
        Question: "QA failed: {failure_type} ({qa_attempts}/3 attempts). Fix and retry?"
        Header: "QA Failure"
        Options:
            - "Yes - return to development to fix issues"
            - "No - halt orchestration, manual fix"
        multiSelect: false

    user_choice = response
```

---

### Step 5: Execute Recovery Action

```
IF user_choice == "Fix deferrals and retry" OR user_choice == "Yes":
    Display: "Returning to development to fix {failure_type} issues..."

    # Set context for development skill
    **Development Mode:** retry_after_qa_failure
    **QA Failure Type:** {failure_type}
    **Issues to Fix:** {violations_summary}

    # Re-invoke development
    Skill(command="devforgeai-development")

    # After dev completes, automatically retry QA
    Display: "Development fixes complete. Retrying QA validation (attempt {qa_attempts + 1})..."

    **Validation Mode:** deep

    # Re-invoke QA
    Skill(command="devforgeai-qa")

    # Check QA result
    IF QA now PASSED:
        Return: "QA_PASSED_AFTER_RETRY"
    ELSE:
        # Recursive: Go back to Step 2 (count attempts again)
        # Loop continues until PASS or max attempts

ELIF user_choice == "Create follow-up stories":
    Display: "Creating follow-up stories for deferred DoD items..."

    # Extract deferred items from story
    Read story DoD section
    deferred_items = parse items marked [ ] with deferral reasons

    created_stories = []
    FOR each deferred_item in deferred_items:
        AskUserQuestion:
            Question: "Create follow-up story for: '{deferred_item.description}'?"
            Header: "Follow-up Story"
            Options: ["Yes", "Skip"]
            multiSelect: false

        IF "Yes":
            # Set context for story creation
            **Feature Description:** {deferred_item.description}
            **Parent Story:** {STORY_ID} (deferred from)
            **Epic:** {current_story.epic}
            **Sprint:** {next_sprint or current_sprint}

            # Invoke story creation skill
            Skill(command="devforgeai-story-creation")

            created_stories.append(story_id)

    # Update original story with follow-up references
    Edit story:
        Append to DoD section:
        "{deferred_item}: Tracked in {STORY-XXX}"

    Return: "FOLLOW_UP_STORIES_CREATED" + list of created_stories

ELIF user_choice == "Manual resolution" OR user_choice == "No":
    Display: "Orchestration halted. QA report: devforgeai/qa/reports/{STORY_ID}-qa-report.md"

    Return: "QA_FAILED_USER_HALT"
```

---

### Step 6: Track Retry Iteration in Workflow History

```
Edit(file_path="devforgeai/specs/Stories/{STORY_ID}.story.md")

Append to workflow history:
  "QA Attempt {qa_attempts}: FAILED - {failure_type}"
  "{recovery_action}"
  "QA Attempt {qa_attempts + 1}: {PASSED/FAILED/IN_PROGRESS}"

Return: Updated workflow history entry
```

---

### Step 7: Return Result to Command

```json
{
  "status": "QA_PASSED" | "QA_PASSED_AFTER_RETRY" | "QA_FAILED_USER_HALT" | "QA_MAX_RETRIES_EXCEEDED" | "FOLLOW_UP_STORIES_CREATED",
  "attempts": qa_attempts,
  "recovery_action": "retry" | "follow_ups" | "manual" | "max_retries",
  "created_stories": [...] (if follow-ups created),
  "next_phase": "staging" | "halt" | "retry_qa",
  "display_message": "..." (celebration or error message)
}
```

**Command receives result and displays:**
- If QA_PASSED: Proceed to Phase 4 (staging)
- If QA_FAILED_*: Display message, halt orchestration
- If FOLLOW_UP_STORIES_CREATED: Display created stories, halt
```

**Effort:** 3-4 hours (complex logic, requires careful extraction and testing)

---

## Combined Refactoring Plan

### Option A: Sequential (Recommended)

**Week 1: Skill Enhancement** (2-3 hours)
- Add missing skill integrations (ideation, ui-generator, story-creation)
- Establish complete framework integration picture
- No code changes, low risk

**Week 2: Command Refactoring** (6-8 hours)
- Extract Phase 3.5, 1, 6 to skill
- Skill already enhanced with missing integrations
- Test comprehensive (30+ test cases)

**Total:** 8-11 hours over 2 weeks

**Benefits:**
- Skill complete first (provides foundation)
- Command refactoring references complete skill
- Lower risk (skill changes validate before command refactor)

---

### Option B: Parallel (Faster but Higher Risk)

**Simultaneously:**
- Track 1: Command refactoring (1 person, 6-8 hours)
- Track 2: Skill enhancement (1 person, 2-3 hours)

**Total:** 6-8 hours (if parallelized)

**Risks:**
- Coordination needed (both touch orchestration skill)
- Integration testing more complex
- Merge conflicts possible

**Not recommended unless time-critical**

---

### Option C: Skill Enhancement Only (Quick Win)

**Just add missing skill integrations** (2-3 hours)
- No command refactoring
- Command stays over budget
- But skill documentation complete

**Benefits:**
- Quick completion (1 day)
- Low risk (documentation only)
- Framework integration knowledge complete

**Drawbacks:**
- Command still over budget (violated protocol)
- Architectural issues remain (business logic in command)
- Technical debt not addressed

**Use when:** Need quick documentation improvement, can defer command refactoring

---

## Effort Breakdown

### Track 1: /orchestrate Command Refactoring (6-8 hours)

| Phase | Task | Duration |
|-------|------|----------|
| **Analysis** | Line-by-line phase review | 1 hour |
| **Extraction** | Move Phase 3.5 to skill | 2 hours |
| **Extraction** | Move Phase 1 to skill | 1 hour |
| **Extraction** | Move Phase 6 to skill | 1 hour |
| **Integration** | Update skill phases | 1 hour |
| **Testing** | 30+ test cases | 2 hours |
| **Documentation** | Update references, create summary | 1 hour |
| **TOTAL** | | **8-9 hours** |

### Track 2: devforgeai-orchestration Skill Enhancement (2-3 hours)

| Phase | Task | Duration |
|-------|------|----------|
| **Documentation** | Add devforgeai-ideation integration | 30 min |
| **Documentation** | Add devforgeai-ui-generator integration | 45 min |
| **Documentation** | Complete devforgeai-story-creation docs | 30 min |
| **Skill Logic** | Add Phase 3.5 QA retry logic | 1 hour |
| **Testing** | Verify skill still works, integration tests | 30 min |
| **TOTAL** | | **3 hours** |

### Combined Total: 11 hours (conservative estimate)

---

## Testing Strategy

### For /orchestrate Command Refactoring

**Unit Tests (12 cases):**
1. Argument validation (valid, invalid, missing)
2. Story file loading (exists, missing, multiple)
3. Skill invocation (context markers set correctly)
4. Checkpoint detection (DEV_COMPLETE, QA_APPROVED, STAGING_COMPLETE, none)
5. QA retry scenarios (first failure, second retry, max retries)
6. Finalization (workflow history, status update)

**Integration Tests (10 cases):**
1. Full orchestration (Backlog → Released)
2. Resume from DEV_COMPLETE checkpoint
3. Resume from QA_APPROVED checkpoint
4. QA failure → retry → pass
5. QA failure → retry → retry → pass
6. QA failure 3 times → max retries halt
7. Staging failure → manual fix → resume
8. Production failure → rollback → fix → resume

**Regression Tests (8 cases):**
1. Checkpoint resume still works
2. Quality gates still enforced
3. Skill invocations unchanged
4. Status transitions preserved
5. Workflow history format same
6. Error messages preserved

**Performance Tests:**
- Command overhead <2.5K tokens (down from ~4K)
- Character budget 59% usage (down from 100%)
- Execution time unchanged (~60-90 min total)

---

### For devforgeai-orchestration Skill Enhancement

**Validation Tests (6 cases):**
1. Ideation integration documented correctly
2. UI-generator integration documented correctly
3. Story-creation integration completed
4. Phase 3.5 QA retry logic works
5. All 7 skills referenced in integration section
6. No regressions in existing phases

**Documentation Tests:**
- [ ] All skills have When/Invocation/Process/Result sections
- [ ] Workflow position clear for each skill
- [ ] Prerequisites documented
- [ ] When to skip documented
- [ ] Integration section complete (7 of 7 skills)

---

## Risk Assessment

### Risks for Command Refactoring

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Breaking checkpoint resume | High | Comprehensive regression tests (8 cases) |
| QA retry loop errors | High | Extract carefully, test all 3 user choice paths |
| Workflow history corruption | Medium | Backup stories before testing |
| Token budget breach | Low | Extract reduces overhead (measured improvement) |

**Overall risk:** 🟡 MEDIUM (complex logic but proven pattern)

### Risks for Skill Enhancement

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Documentation errors | Low | Copy from source skills, verify accuracy |
| Integration logic errors | Low | Documentation only (no code changes) |
| Skill file too large | Low | Already 2,351 lines, +100 lines acceptable |

**Overall risk:** 🟢 LOW (documentation updates only)

---

## Success Criteria

### For /orchestrate Command Refactoring

- [ ] Character count <15K (currently 15,012)
- [ ] Business logic moved to skill (234 lines extracted)
- [ ] Checkpoint resume functionality preserved
- [ ] QA retry loop preserved (but in skill)
- [ ] All quality gates intact
- [ ] Token overhead reduced 37% (~4K → ~2.5K)
- [ ] 100% backward compatible
- [ ] 30+ test cases pass

### For devforgeai-orchestration Skill Enhancement

- [ ] All 7 DevForgeAI skills documented in integration section
- [ ] devforgeai-ideation: When/Invocation/Process/Result complete
- [ ] devforgeai-ui-generator: When/Invocation/Process/Result complete
- [ ] devforgeai-story-creation: Integration documentation complete
- [ ] Phase 3.5 QA retry logic added to skill
- [ ] Skill coverage: 100% (7 of 7)
- [ ] No regressions in existing functionality

---

## Action Plan

### Immediate Actions (Recommended Sequence)

**Step 1: Skill Enhancement FIRST** (Priority: HIGH, Effort: 2-3 hours)

**Why first:**
- Lower risk (documentation only)
- Provides foundation for command refactoring
- Quick win (completes framework integration)
- No code changes (just add missing sections)

**Tasks:**
1. Add devforgeai-ideation to integration section (30 min)
2. Add devforgeai-ui-generator to integration section (45 min)
3. Complete devforgeai-story-creation documentation (30 min)
4. Add Phase 3.5 QA retry logic to skill (1 hour)
5. Test skill enhancements (30 min)

**Deliverable:** Complete orchestration skill with 100% framework integration

---

**Step 2: Command Refactoring SECOND** (Priority: MEDIUM, Effort: 6-8 hours)

**Why second:**
- Skill now complete (provides context for extraction)
- Can reference skill phases in command
- Proven pattern from /qa refactoring

**Tasks:**
1. Backup command: `cp orchestrate.md orchestrate.md.backup`
2. Extract Phase 3.5 to skill (2 hours)
3. Extract Phase 1 to skill (1 hour)
4. Extract Phase 6 to skill (1 hour)
5. Test extractions (30 test cases, 2 hours)
6. Update memory references (30 min)
7. Deploy and monitor (1 hour)

**Deliverable:** Lean /orchestrate command within budget (59% usage)

---

### Timeline

**Option A (Sequential - Recommended):**
```
Week 1:
  Mon-Tue: Skill enhancement (2-3 hours)
  Wed: Skill testing and validation (1 hour)
  Thu-Fri: Command refactoring planning (1 hour)

Week 2:
  Mon-Tue: Command refactoring (6-8 hours)
  Wed-Thu: Comprehensive testing (2 hours)
  Fri: Deploy, monitor, document (1 hour)

Total: 2 weeks, 12-15 hours
```

**Option B (Skill Enhancement Only):**
```
Week 1:
  Mon: Skill enhancement (2-3 hours)
  Tue: Testing and deployment (30 min)

Total: 1 day, 3 hours
```

**Option C (Command Refactoring Only):**
```
Week 1-2:
  Command refactoring (6-8 hours)
  Testing (2 hours)
  Deploy (1 hour)

Total: 9-11 hours (but skill still incomplete)
```

---

## Recommended Approach

### Phase 1: Skill Enhancement (This Week)

**Priority:** ✅ DO THIS FIRST

**Rationale:**
1. Quick win (2-3 hours)
2. Low risk (documentation only)
3. High value (100% skill coverage)
4. Provides foundation for command refactoring

**Deliverable:**
- devforgeai-orchestration skill with all 7 framework skills integrated
- Phase 3.5 QA retry logic in skill (where it belongs)
- Complete framework workflow documentation

---

### Phase 2: Command Refactoring (Next Week)

**Priority:** ⚠️ DEFER UNTIL SKILL COMPLETE

**Rationale:**
1. Can reference complete skill phases
2. Extraction targets clear
3. Proven pattern from /qa refactoring
4. Skill provides all logic (command just delegates)

**Deliverable:**
- /orchestrate command within budget (~11K chars, 59% usage)
- Lean orchestration pattern applied
- 234 lines extracted to skill
- Token efficiency improved 37%

---

## Metrics Targets

### /orchestrate Command (After Refactoring)

| Metric | Before | Target | Improvement |
|--------|--------|--------|-------------|
| **Lines** | 599 | ~380 | 37% reduction |
| **Characters** | 15,012 | ~11,000 | 27% reduction |
| **Budget Usage** | 100% | 73% | 27% more headroom |
| **Token Overhead** | ~4K | ~2.5K | 37% reduction |
| **Phases** | 8 | 5 | Simpler structure |

### devforgeai-orchestration Skill (After Enhancement)

| Metric | Before | Target | Change |
|--------|--------|--------|--------|
| **Lines** | 2,351 | ~2,550 | +200 lines |
| **Skill Coverage** | 71% (5 of 7) | 100% (7 of 7) | +29% coverage |
| **Integration Section** | 4 skills | 7 skills | Complete |
| **Phase 3.5** | Missing | Added | Retry logic in skill |

---

## Deliverables

### Documentation

**This report:**
- `devforgeai/specs/enhancements/ORCHESTRATE-AUDIT-FINDINGS-2025-11-05.md` ✅
- `devforgeai/specs/enhancements/ORCHESTRATE-RECOMMENDATIONS-2025-11-05.md` (this file) ✅

**To create:**
- `devforgeai/specs/enhancements/ORCHESTRATE-REFACTORING-PLAN.md` (detailed plan)
- `devforgeai/specs/enhancements/ORCHESTRATE-SKILL-ENHANCEMENT-CHECKLIST.md` (implementation guide)

### Code Changes (When Implemented)

**Phase 1 (Skill Enhancement):**
1. `.claude/skills/devforgeai-orchestration/SKILL.md` (add 3 integrations + Phase 3.5)

**Phase 2 (Command Refactoring):**
2. `.claude/commands/orchestrate.md` (extract 234 lines → ~380 lines final)
3. `.claude/memory/commands-reference.md` (update /orchestrate entry)

---

## Quick Decision Matrix

**If you have limited time:**
→ **Do skill enhancement only** (2-3 hours, complete framework integration)

**If you want budget compliance:**
→ **Do command refactoring** (6-8 hours, lean orchestration)

**If you want complete solution:**
→ **Do both sequentially** (11 hours, skill first then command)

**If you want perfect:**
→ **Do both + comprehensive testing** (15 hours, full validation)

---

## Final Recommendations

### Immediate (Priority: HIGH)

✅ **Enhance devforgeai-orchestration skill** (2-3 hours)
- Add 3 missing skill integrations
- Move QA retry logic from command to skill
- Achieve 100% framework skill coverage

**Rationale:**
- Quick completion
- Low risk
- High value (framework completeness)
- Foundation for command refactoring

---

### Near-Term (Priority: MEDIUM)

⏸️ **Refactor /orchestrate command** (6-8 hours)
- Extract 234 lines to skill
- Achieve budget compliance (100% → 73%)
- Apply lean orchestration pattern

**Rationale:**
- Budget violation (even if minor)
- Architectural alignment
- Token efficiency (37% improvement)
- But can defer until skill complete

---

### Long-Term (Priority: LOW)

📊 **Monitor and maintain**
- Quarterly budget audits (/audit-budget)
- Track command growth
- Update protocol with lessons learned

---

**Status:** ✅ Recommendations complete - Clear action plan with priorities
