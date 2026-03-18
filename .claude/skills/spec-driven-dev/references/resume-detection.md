# Resume Detection and Pre-Flight Validation

**Purpose:** Contains all resume-specific business logic extracted from `/resume-dev` command per lean orchestration pattern (STORY-459). Loaded on demand by spec-driven-dev skill when resume mode is detected.

**Origin:** Extracted from `.claude/commands/resume-dev.md` (676 lines -> reference file + lean command)

---

## Resume Pre-Flight Validation

### Step 1.1: Validate Context Files Exist

```
devforgeai-validate validate-context

IF validation fails:
  Display: "  Context files missing or invalid"
  Display: "   Run: /create-context to generate context files"
  HALT

Display: "✓ Context files validated (6/6 present)"
```

### Step 1.2: Validate Technology Stack

```
Task(
  subagent_type="tech-stack-detector",
  description="Validate technology stack for resumed story",
  prompt="Detect and validate project technology stack against tech-stack.md.
  This is a RESUME operation - story was previously started, now resuming.
  Validate:
  1. Project technologies match tech-stack.md (no drift)
  2. No unapproved dependencies added since last run
  3. No library substitutions
  Return validation result (PASS/FAIL) and any conflicts."
)

IF validation fails:
  Display: "  Tech stack conflicts detected"
  Display: "   Conflicts: {conflicts from subagent}"
  Display: "   Resolve conflicts before resuming development"
  HALT

Display: "✓ Technology stack validated"
```

### Step 1.3: Validate Spec vs Context Files

```
Read story Technical Specification section

IF technical_spec contains technology NOT in tech-stack.md:
  Display: "  Spec-Context conflict detected"
  Display: "   Spec requires: {technology}"
  Display: "   tech-stack.md locked: {locked_technologies}"
  # NOTE: User interaction (spec conflict prompt) handled by command, not reference
  # Command handles user interaction for spec conflict resolution

Display: "✓ Spec validated against context files"
```

**Why these validations are essential:**
1. **Context files:** Story implementation depends on architectural constraints
2. **Tech stack:** Ensures no technology drift since story started
3. **Spec vs Context:** Prevents implementing features that violate locked decisions
4. **Git validation skipped:** Not needed for resumption (already initialized)

---

## Session Checkpoint Detection

**Execute FIRST if RESUME_MODE == "auto" (before DoD analysis):**

```
IF RESUME_MODE == "auto":
  checkpoint_path = "devforgeai/sessions/$STORY_ID/checkpoint.json"

  result = read_checkpoint($STORY_ID)

  IF result starts with "CHECKPOINT_FOUND":
    CHECKPOINT_PHASE = parsed[1]
    PHASE_NAME = parsed[2]
    PROGRESS = parsed[3]
    PHASE_NUM = CHECKPOINT_PHASE + 1

    Display: ""
    Display: "                                                           "
    Display: "    SESSION CHECKPOINT DETECTED"
    Display: "                                                           "
    Display: ""
    Display: "  Last checkpoint: Phase {CHECKPOINT_PHASE} ({PHASE_NAME})"
    Display: "  Progress: {PROGRESS}%"
    Display: "  Resuming from: Phase {PHASE_NUM}"
    Display: ""

    SKIP: "DoD Analysis"
    GOTO: "Set Resume Context Markers"

  ELSE IF result contains "error" or "corrupt":
    Display: "  Checkpoint corrupted - falling back to DoD analysis"
    Continue to DoD analysis

  ELSE:
    Display: "  No session checkpoint found - analyzing DoD for resumption point"
    Continue to DoD analysis
```

**Why checkpoint-first:** Checkpoints are precise (exact phase number); DoD analysis is approximate (infers phase from incomplete items).

---

## DoD-Based Resumption Point Detection

**Execute if RESUME_MODE == "auto" AND no checkpoint detected:**

```
Extract DoD items by category:
  implementation_unchecked = count(Implementation section "[ ]" items)
  quality_unchecked = count(Quality section "[ ]" items)
  testing_unchecked = count(Testing section "[ ]" items)
  documentation_unchecked = count(Documentation section "[ ]" items)

  total_unchecked = sum(all categories)
  total_items = count(all DoD checkbox items)
  completion_pct = ((total_items - total_unchecked) / total_items) * 100

Display: ""
Display: "DoD Analysis:"
Display: "  Completion: {completion_pct}% ({total_unchecked} items remaining)"
Display: "  Implementation: {implementation_unchecked} incomplete"
Display: "  Quality: {quality_unchecked} incomplete"
Display: "  Testing: {testing_unchecked} incomplete"
Display: "  Documentation: {documentation_unchecked} incomplete"
Display: ""

IF total_unchecked == 0:
  Display: "  DoD 100% complete - no resumption needed"
  Display: "  Story appears finished. Run /qa instead?"
  HALT

IF implementation_unchecked > 0:
  PHASE_NUM=2
  PHASE_NAME="Phase 2: Implementation (Green Phase)"
  REASON="Implementation items incomplete"

ELSE IF quality_unchecked > 0:
  PHASE_NUM=3
  PHASE_NAME="Phase 3: Refactoring & Quality"
  REASON="Quality validations incomplete"

ELSE IF testing_unchecked > 0:
  PHASE_NUM=4
  PHASE_NAME="Phase 4: Integration Testing"
  REASON="Test coverage gaps"

ELSE IF documentation_unchecked > 0:
  PHASE_NUM=3
  PHASE_NAME="Phase 3: Documentation"
  REASON="Documentation incomplete"

Display: "Auto-detected resumption point: {PHASE_NAME}"
Display: "Reason: {REASON}"
```

---

## Context Isolation Compliance

**Architecture Constraint:** architecture-constraints.md (lines 38-40) states skills MUST NOT assume state from previous invocations.

**How resume detection complies:** Resume detection reads ALL state explicitly via `Read()` tool calls:
- Checkpoint file read via `Read(file_path="devforgeai/sessions/$STORY_ID/checkpoint.json")`
- Story file DoD section via `Read(file_path="${STORY_FILE}")`
- Context files via `devforgeai-validate validate-context`

No implicit state assumptions. All file reads are explicit. Missing files trigger graceful fallback (checkpoint -> DoD -> error).

---

## Use Cases

### Use Case 1: Fix Test Failures

**Scenario:** `/dev STORY-057` completed but 8 tests failing
**Command:** `/resume-dev STORY-057 4`
**Behavior:** Skips Phase 0-3, starts at Phase 4 (Integration Testing), runs integration-tester with fixed code

### Use Case 2: Complete Documentation

**Scenario:** Implementation and tests done, only documentation items remain
**Command:** `/resume-dev STORY-057 3`
**Behavior:** Skips Phase 0-2, starts at Phase 3 (Refactoring & Quality), code-reviewer validates documentation

### Use Case 3: Auto-Detect Resumption

**Scenario:** User doesn't know which phase to resume
**Command:** `/resume-dev STORY-057`
**Behavior:** Analyzes DoD (60% complete), finds implementation items unchecked, auto-detects Phase 2

### Use Case 4: Second Run After Incomplete

**Scenario:** User ran `/dev STORY-057`, stopped at 87%
**Command:** `/resume-dev STORY-057 2`
**Behavior:** More explicit than re-running `/dev`, skips pre-flight and test generation, starts at Phase 2

---

## Examples

### Example 1: Resume from Implementation

```
$ /resume-dev STORY-057 2

  Story loaded: STORY-057
  Manual resumption: Phase 2

  DevForgeAI Development Workflow (RESUME MODE)

**Story ID:** STORY-057
**Resume from Phase:** 2
**Resume Mode:** manual

Resuming TDD workflow from Phase 2...

[Skill executes Phase 2 -> 3 -> 4 -> 4.5 -> 5 -> 6 -> 7]
[Story reaches 100%, commits]
```

### Example 2: Auto-Detect Resumption

```
$ /resume-dev STORY-057

  Story loaded: STORY-057
Auto-detecting resumption point from DoD status...

DoD Analysis:
  Completion: 87% (7/30 complete, 23 remaining)
  Implementation: 6 incomplete
  Quality: 8 incomplete
  Testing: 7 incomplete
  Documentation: 2 incomplete

Auto-detected resumption point: Phase 2: Implementation (Green Phase)
Reason: Implementation items incomplete

  DevForgeAI Development Workflow (RESUME MODE)

**Story ID:** STORY-057
**Resume from Phase:** 2
**Resume Mode:** auto

**Auto-Detection Results:**
  DoD Completion: 87%
  Remaining Work: 23 items
  Resumption Point: Phase 2: Implementation (Green Phase)

Resuming TDD workflow from Phase 2...

[Skill executes, completes remaining work]
```

---

## Error Handling

### Error: Story already complete (DoD 100%)

```
Display: "Story {STORY_ID} appears complete (DoD 100%)"
Display: "Status: {story_status}"
Display: ""
Display: "If you need to:"
Display: "  - Re-run tests: pytest tests/..."
Display: "  - Re-run QA: /qa {STORY_ID}"
Display: "  - Make changes: Edit files manually, then /dev {STORY_ID}"
HALT
```

### Error: Story not started (status: Backlog)

```
Display: "Story {STORY_ID} not started (status: Backlog)"
Display: ""
Display: "Use: /dev {STORY_ID} to start development"
Display: "(Cannot resume what hasn't started)"
HALT
```

### Error: Invalid phase number

```
Display: "Invalid phase: {PHASE_NUM}"
Display: "Valid: 0-7"
Display: "Use: /resume-dev {STORY_ID} [0-7]"
HALT
```

---

## Integration with spec-driven-dev Skill

**Skill changes required** (already implemented in REC-1):

1. **Parameter Extraction** enhanced to detect resume markers
2. **Phase skip logic** implemented (mark phases 0 through N-1 as "skipped")
3. **GOTO Phase N** capability (start execution at specified phase)

**No changes needed in:**
- Individual phase implementations (Phases 0-7 unchanged)
- Subagent invocations (work same in resume mode)
- Quality gates (still enforced)

---

## Integration Pattern

**Typical workflow:**

```
1. User starts story
   $ /dev STORY-057

2. Workflow reaches 87%, user rejects deferrals

3a. AUTOMATIC (REC-1): Phase 4.5-R resumes automatically
    [Loop back to Phase 2, continue to 100%]

3b. MANUAL (REC-2): User uses rewind command
   $ /resume-dev STORY-057 2
   [Skip Phase 0-1, resume from Phase 2]
```

**Both paths work:**
- REC-1 (automatic): No user action needed, workflow self-corrects
- REC-2 (manual): User control, faster (skips phases), explicit

---

## Comparison with /dev Command

| Aspect | /dev STORY-ID | /resume-dev STORY-ID 2 |
|--------|---------------|------------------------|
| **Phases executed** | 0-7 (all phases) | 2-7 (skips 0-1) |
| **Time** | ~20-30 minutes | ~15-20 minutes |
| **Use when** | Starting new story | Continuing incomplete story |
| **Skips** | None | Phases 0 through N-1 |
| **Token cost** | ~80-120K | ~60-90K (saves 20-30K) |

---

## Related Commands

**Development workflow:**
- `/dev STORY-ID` - Full TDD workflow (Phase 0-7)
- `/resume-dev STORY-ID [phase]` - Resume from specific phase
- `/qa STORY-ID [mode]` - Quality validation only
- `/orchestrate STORY-ID` - Full lifecycle (dev + qa + release)

**Framework analysis:**
- `/rca [issue]` - Root cause analysis
- `/audit-deferrals` - Audit deferred work

---

## Success Indicators

**When /resume-dev works correctly:**

1. User can manually resume from any phase (0-7)
2. Auto-detect correctly identifies resumption point
3. Phases 0 through N-1 skipped (marked "skipped")
4. Phase N starts fresh with prior implementation state loaded
5. Workflow proceeds normally after resumption
6. Iteration counter tracks multiple resumptions
7. Story completes to 100% after resumption

**UX Before/After:**
- **Before:** Run `/dev STORY-057` -> 87% -> frustrated -> run again -> 87% again
- **After:** Run `/dev STORY-057` -> 87% -> run `/resume-dev STORY-057` -> 100%

---

## Performance

**Token Budget:**
- Command overhead: ~2K tokens (parameter validation, context markers)
- Skill execution: Same as normal /dev (depends on phases executed)
- **Savings from skipping phases:** ~5-15K tokens

**Execution Time:**
- Manual mode: Immediate (no auto-detection)
- Auto mode: +30 seconds (DoD analysis)
- **Time saved:** Skipping Phase 0-1 saves ~3-5 minutes

---

## Character Budget Analysis

**Post-refactoring:**
- Command: ~100 lines, ~3,500 characters
- Reference: ~290 lines (loaded on demand by skill)
- **Net savings:** ~8,500 characters removed from main conversation context

---

**End of resume-detection.md**
**Created:** 2026-02-20 (STORY-459)
**Origin:** Extracted from resume-dev.md (676 lines -> lean command + this reference)
