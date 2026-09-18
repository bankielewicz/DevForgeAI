# Phase 06: Deferral Challenge Checkpoint

**Skill Reference:** spec-driven-dev
**Phase:** Phase 06 (After Integration Testing, Before DoD Update Bridge)
**Loaded:** After Phase 05 completes, if story has any deferred DoD items
**Purpose:** Challenge ALL deferred DoD items to prevent autonomous deferrals and ensure user approval (RCA-006 enforcement).
**Trigger:** After Phase 05 completes successfully, before Phase 07

---

## Phase Progress Indicator

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 06/9: Deferral Challenge (56% -> 67% complete)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Display this indicator at the start of Phase 06. Progressive Disclosure: loaded ONLY if deferred DoD items exist.

---

## Skill Context Available

When loaded, the following context is available:
- **STORY_ID**, **STORY_FILE**, **Story Content** (loaded via @ reference)
- **Completion Status:** Phases 01-05 complete
- **Variables:** `$WORKFLOW_MODE`, `$GIT_AVAILABLE`, `$TEST_COMMAND`

---

## Two Validators (Different Purposes)

| Aspect | deferral-validator (AI) | devforgeai-validate validate-dod (CLI) |
|--------|------------------------|--------------------------------|
| **Type** | AI subagent | Python script (deterministic) |
| **Runs** | Phase 06 Step 3 | Pre-commit hook (Phase 08) |
| **Checks** | Semantic justification validity | Format compliance (DoD <-> Impl Notes) |
| **Validates** | Circular deferrals, blocker accuracy, story refs | DoD [x] items in Impl Notes, text match, format |
| **Can HALT** | No (advisory) | Yes (blocks git commit) |

### Workflow Handoff

1. **Phase 06:** deferral-validator validates semantic correctness (blockers real? circular? refs exist?)
2. **Phase 07:** Update DoD items in correct format (mark [x], add to Implementation Notes as FLAT LIST)
3. **Phase 08:** devforgeai-validate validate-dod validates format before commit (BLOCKS if fails)

Both validators must pass for successful Phase 08 completion.

---

## Checkpoint Workflow

### Step 1: Detect All Incomplete DoD Items [MANDATORY]

**CRITICAL (RCA-014):** Detect ANY unchecked DoD item, not just explicitly deferred items. Leaving work unchecked IS a deferral (implicit).

```
Grep(
  pattern="^- \[ \]",
  path="${STORY_FILE}",
  output_mode="content",
  -B=1,
  -A=3
)
```

**Parse results:**

```
incomplete_items = []
in_dod_section = false

FOR each match from Grep:
  item_text = line starting with "- [ ]"
  preceding_line = previous line (via -B=1)
  context_lines = next 3 lines (via -A=3)

  # Section filtering: Only process items in Definition of Done section
  IF preceding_line contains "## Definition of Done":
    in_dod_section = true
  IF preceding_line contains any of ["## Acceptance Criteria", "## Workflow Status",
     "## Implementation Notes", "### AC#", "Checklist"]:
    in_dod_section = false

  IF NOT in_dod_section: CONTINUE

  classification = classify_incomplete_item(context_lines)
  justification = extract_justification(context_lines)

  incomplete_items.append({
    text: item_text,
    classification: classification,
    justification: justification or "NONE",
    has_approval: check_for_approval(context_lines)
  })

FUNCTION classify_incomplete_item(context_lines):
  FOR each line in context_lines:
    IF line contains any of ["Deferred to STORY-", "Blocked by:", "Out of scope: ADR-",
       "Approved by user on"]:
      RETURN "explicit_deferral"
  RETURN "implicit_deferral"

FUNCTION extract_justification(context_lines):
  FOR each line in context_lines:
    IF line contains any of ["Deferred to", "Blocked by:", "Out of scope:", "Approved by user on"]:
      RETURN line.strip()
  RETURN null

FUNCTION check_for_approval(context_lines):
  FOR each line in context_lines:
    IF line contains "Approved by user on" AND line contains timestamp_pattern:
      RETURN true
  RETURN false
```

**Result:** `incomplete_items` = ALL incomplete DoD items (explicit + implicit deferrals)

---

### Step 2: Skip Checkpoint if No Incomplete Items

**IF incomplete_items is empty:**
```
Display: "All DoD items complete (100%) - no deferrals detected"
Display: "Skipping Phase 06 - Proceeding to Phase 07 (DoD Update)..."
Exit checkpoint, return control to skill for Phase 07
```

**OTHERWISE:** Continue to Step 3

---

### Step 3: Invoke deferral-validator Subagent [MANDATORY IF deferrals exist]

**Display checkpoint notice:**
```
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Phase 06: DEFERRAL CHALLENGE CHECKPOINT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Found {len(deferred_items)} deferred Definition of Done items:
{FOR each item}: {index}. {item.text} — Justification: {item.justification}

Validating blockers with deferral-validator subagent..."
```

**Invoke:**
```
Task(
  subagent_type="deferral-validator",
  description="Validate deferred items for ${STORY_ID}",
  prompt="""
Validate the following deferred items:

Story: ${STORY_ID}
Deferred Items:
{FOR each item}: - {item.text} / {item.justification}

For each deferral:
1. Deferred to story: Check git log + story file status. Is dependency complete?
2. Blocked by toolchain: Check toolchain availability (rustup/npm/dotnet). Available?
3. Blocked by artifacts: Check if expected artifacts exist.
4. Out of scope (ADR): Check if ADR file exists.

Return JSON:
{
  "can_resolve_now": [{ "item": "...", "reason": "...", "command": "..." }],
  "must_stay_deferred": [{ "item": "...", "reason": "...", "blocker": "..." }],
  "violations": [{ "item": "...", "severity": "CRITICAL|HIGH|MEDIUM", "issue": "..." }]
}
""")
```

---

### Step 4: Handle Validation Results [MANDATORY]

```
can_resolve_count = len(validation_result.can_resolve_now)
must_defer_count = len(validation_result.must_stay_deferred)
violation_count = len(validation_result.violations)
```

**Display:**
```
"DEFERRAL VALIDATION RESULTS:

Resolvable Deferrals: {can_resolve_count}
{FOR each}: - {item.item} — Reason: {item.reason} — Action: {item.command}

Valid Deferrals: {must_defer_count}
{FOR each}: - {item.item} — Blocker: {item.blocker}

{IF violation_count > 0}:
VIOLATIONS DETECTED: {violation_count}
{FOR each}: - {violation.item} — Severity: {violation.severity} — Issue: {violation.issue}"
```

---

### Step 5: Handle Violations [MANDATORY IF violations detected]

**IF CRITICAL violations:**
```
Display: "CRITICAL DEFERRAL VIOLATIONS - MUST be resolved:
{FOR each CRITICAL violation}: - {violation.item}: {violation.issue}

Common: Circular chains, missing target stories/ADRs, invalid justification format.

WORKFLOW HALTED - Fix issues and re-run: /dev ${STORY_ID}"

HALT execution. Exit Phase 06.
```

**IF HIGH violations (non-critical):**
```
AskUserQuestion:
  Question: "HIGH-severity deferral violations detected. How should we proceed?"
  Header: "Deferral Violations"
  Options:
    - "Fix violations now (I'll update deferrals)"
    - "Override and proceed (I'll provide justification)"
  multiSelect: false

IF "Fix violations now": Display fix list, HALT execution.
IF "Override and proceed":
  AskUserQuestion for justification text.
  Log override to story file with timestamp.
  Proceed to Step 6.
```

---

### Step 6: Challenge ALL Incomplete Items with User Approval [MANDATORY]

**Policy:** ZERO autonomous deferrals. AskUserQuestion for EVERY incomplete DoD item (RCA-006, RCA-014).

**FOR EACH incomplete item:**

```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 DEFERRAL #{index}/{total_deferrals}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Item: {item.text}
Current Justification: {item.justification}

{IF item in can_resolve_now}: BLOCKER RESOLVED: {item.reason} — Recommended: {item.command}
{ELSE IF item in must_stay_deferred}: BLOCKER VALID: {item.reason} — Blocker: {item.blocker}"

AskUserQuestion:
  Question: "How should we handle: '{item.text}'?"
  Header: "Deferral Decision"
  Options:
    - "HALT and implement NOW"
    - "Keep deferred (blocker is valid)"
    - "Update justification (blocker changed)"
    - "Remove from DoD (not needed)"
  multiSelect: false
```

**Option 1: "HALT and implement NOW"**
```
# Remove deferral justification from story file
Edit(file_path="${STORY_FILE}",
  old_string="- [ ] {item.text}\n    {item.justification}",
  new_string="- [ ] {item.text}")

items_to_implement.append(item.text)

# After ALL items processed, if items_to_implement not empty:
Display: "Returning to Phase 03 to implement {len(items_to_implement)} items."
HALT Phase 06. Return to skill: "Resume Phase 03 for items: {items_to_implement}"
```

**Option 2: "Keep deferred"**
```
current_timestamp = $(date -u +"%Y-%m-%d %H:%M:%S UTC")

Edit(file_path="${STORY_FILE}",
  old_string="{item.justification}",
  new_string="{item.justification}\n    User approved: {current_timestamp}")

approved_deferrals.append({ item: item.text, justification: item.justification, timestamp: current_timestamp })
```

**Option 3: "Update justification"**
```
AskUserQuestion:
  Question: "Provide updated justification for deferring '{item.text}'"
  Header: "New Justification"

new_justification = user_input

# Validate references in new justification
IF "Deferred to STORY-" in new_justification:
  Glob(pattern="devforgeai/specs/Stories/{target_story}*.story.md")
  IF not found: Display warning about missing story.

ELSE IF "Blocked by:" in new_justification:
  Append to technical debt register.

ELSE IF "Out of scope: ADR-" in new_justification:
  Glob(pattern="devforgeai/specs/adrs/{adr_reference}*.md")
  IF not found: Display warning about missing ADR.

# Update story file
Edit(file_path="${STORY_FILE}",
  old_string="- [ ] {item.text}\n    {item.justification}",
  new_string="- [ ] {item.text}\n    {new_justification}\n    User approved: {current_timestamp}")
```

**Option 4: "Remove from DoD"**
```
AskUserQuestion:
  Question: "Why is '{item.text}' no longer needed? (Logged as scope change)"
  Header: "Removal Reason"

removal_reason = user_input

Edit(file_path="${STORY_FILE}",
  old_string="- [ ] {item.text}\n    {item.justification}",
  new_string="")

# Log scope change in Workflow History section
Append: "### Scope Changes\n- **Removed:** {item.text}\n  - **Reason:** {removal_reason}\n  - **Date:** {current_timestamp}\n  - **Approved by:** User"

removed_items.append({ item: item.text, reason: removal_reason })
```

---

### Step 6.5: Mandatory HALT Verification [CANNOT BE SKIPPED]

Defends against autonomous approval bypass (RCA-006).

#### 6.5.1 Verify User Approval for ALL Deferrals

```
unapproved_deferrals = []

FOR each deferral in all_deferrals:
  IF deferral.status in ["kept", "deferred"] AND deferral.user_approval_timestamp IS EMPTY:
    unapproved_deferrals.append(deferral)

IF unapproved_deferrals is NOT empty:
  HALT with message:
  "AUTONOMOUS DEFERRAL DETECTED - WORKFLOW HALTED
   {len(unapproved_deferrals)} deferral(s) approved WITHOUT user consent (RCA-006 violation).
   Missing user approval timestamp for:
   {FOR each}: - {deferral.text} / {deferral.justification}"

  # Force user decision for each unapproved deferral
  FOR each deferral in unapproved_deferrals:
    AskUserQuestion:
      Question: "Deferral '{deferral.text}' was auto-approved. What should happen?"
      Header: "MANDATORY Approval"
      Options:
        - "HALT and implement NOW (reject deferral)"
        - "Approve deferral (I explicitly consent)"
        - "Remove from DoD (not needed)"
      multiSelect: false

    IF "Approve deferral":
      Edit to add "User approved: {timestamp}" to story file.
    ELIF "HALT and implement NOW":
      items_to_implement.append(deferral.text)
      HALT: return to Phase 03.
    ELIF "Remove from DoD":
      Edit to remove item from story file.
```

#### 6.5.2 Audit Trail Requirement

Every kept deferral MUST have this format:
```markdown
- [ ] {deferral_text}
  Blocker: {blocker_type}
  Justification: {detailed_reason}
  User approved: {YYYY-MM-DD HH:MM:SS UTC}  <- MANDATORY
```

Deferrals WITHOUT "User approved:" timestamp are INVALID and fail Phase 06.

#### 6.5.3 Final Checkpoint Verification

```
IF count_deferrals_without_timestamp() > 0:
  HALT: "Cannot proceed. {count} deferral(s) lack user approval timestamp."

ELSE:
  Display: "Step 6.5 Complete: All deferrals have user approval timestamps
    - {len(approved_deferrals)} approved
    - {len(items_to_implement)} rejected (will implement)
    - {len(removed_items)} removed from DoD"

  IF items_to_implement is NOT empty: GOTO Phase 03 (Step 7)
  ELSE: PROCEED to Step 7
```

---

### Step 6.6: Technical Debt Register Update [MANDATORY - UNCONDITIONAL]

See: [technical-debt-register-workflow.md](technical-debt-register-workflow.md) (Step 6.6)

When user approves a deferral: sequential DEBT-NNN ID, entry with 8 required fields, analytics counter updates.

```
Read(file_path="references/technical-debt-register-workflow.md")
```

---

### Step 7: Immediate Resumption Decision [MANDATORY - RCA-014]

Resumption happens IMMEDIATELY in Phase 06 (not separate Phase 06-R), eliminating circular dependency.

```
attempt_now_count = count(items where user selected "Attempt now")
approved_count = count(items where user selected "Keep deferred")
removed_count = count(items where user selected "Remove from DoD")

IF attempt_now_count > 0:
  Display: "RESUMPTION TRIGGERED - Implement {attempt_now_count} deferred items"
  Display items list.

  # Analyze items to determine resumption phase
  needs_implementation = any item contains "feature|implemented|code written|functionality"
  needs_refactoring = any item contains "refactor|code quality|complexity|review"
  needs_integration = any item contains "integration test|end-to-end|e2e|cross-component"

  # Determine earliest phase needed
  IF needs_implementation:
    resumption_phase = Phase 03 (Green)
  ELSE IF needs_refactoring:
    resumption_phase = Phase 04 (Refactor)
  ELSE IF needs_integration:
    resumption_phase = Phase 05 (Integration)
  ELSE:
    AskUserQuestion:
      Question: "Which TDD phase to resume from?"
      Options: ["Phase 03 (Implementation)", "Phase 04 (Refactoring)", "Phase 05 (Integration)"]

  iteration_count += 1
  Display: "TDD Iteration: {iteration_count}/5"

  # Check iteration limit
  IF iteration_count >= 5:
    AskUserQuestion:
      Question: "Story has required 5 TDD iterations. How should we proceed?"
      Options:
        - "Continue anyway (allow iteration 6+)"
        - "Commit current progress with documented deferrals"
        - "Review what's blocking completion (investigate)"

    IF "Continue anyway": GOTO resumption_phase
    IF "Commit current progress": GOTO Phase 07
    IF "Review": Display "/rca suggestion", HALT workflow.

  GOTO resumption_phase

ELSE IF approved_count > 0:
  Display: "All {approved_count} incomplete items approved for deferral"
  GOTO Phase 07

ELSE:
  Display: "All {removed_count} items removed from DoD"
  GOTO Phase 07
```

---

### Step 8: Final Summary Display [MANDATORY]

```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PHASE 06 COMPLETE: Deferral Challenge Checkpoint
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Incomplete Items Challenged: {total}
- Explicit deferrals: {count}
- Implicit deferrals: {count} (RCA-014)

User Decisions:
- Attempt now: {attempt_now_count}
- Approved (deferred): {approved_count}
- Removed from DoD: {removed_count}

{IF attempt_now_count > 0}: RESUMING AT: {resumption_name} — Items: {list}
{IF approved_count > 0}: Approved Deferrals: {list with timestamps}
{IF removed_count > 0}: Removed: {list with reasons}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

---

### Step 9: Update AC Verification Checklist [RCA-011]

```
Read(file_path="references/ac-checklist-update-workflow.md")
Grep(pattern="Phase.*: 4.5", path="${STORY_FILE}", output_mode="content", -B=1)
```

Common Phase 06 AC items: deferrals user-approved, no circular chains, follow-up stories created, timestamps recorded, debt register updated.

Batch-update all complete Phase 06 items. Display: "Phase 06 AC Checklist: {count} items checked | AC Progress: {X}/{Y}"

**Graceful Skip:** If AC Verification Checklist section not found, skip and continue.

---

## Success Criteria

- [ ] All incomplete DoD items detected (explicit + implicit)
- [ ] Section filtering applied (only DoD, not AC Checklist)
- [ ] deferral-validator invoked for explicit deferrals
- [ ] CRITICAL violations halted workflow
- [ ] HIGH violations handled (fixed or overridden)
- [ ] User interaction completed for EVERY incomplete item
- [ ] Story file updated with approval timestamps
- [ ] Items to implement flagged, resumption phase determined
- [ ] Removed items logged in Workflow History
- [ ] Immediate resumption decision made (no delay)

**On success (all approved):** Proceed to Phase 07
**On success (attempt now):** IMMEDIATE loop back to Phase 03/04/05
**On success (removed):** Proceed to Phase 07
**On failure (CRITICAL):** HALT, user must fix and re-run /dev

---

## Integration Notes

**Invoked by:** spec-driven-dev skill (after Phase 05, before Phase 08)

**Invokes:** deferral-validator, requirements-analyst (follow-up stories), architect-reviewer (ADRs)

**Updates:** Story file (approvals, justifications, scope changes), Technical debt register

**References:** `.claude/agents/deferral-validator.md`, `references/dod-validation-checkpoint.md`, RCA-006

---

## Error Handling

**Story File Not Loaded:**
Verify /dev includes @story reference. Check file exists via Glob. Re-run /dev.

**deferral-validator Fails:**
Review error output. Fix environment (git, toolchains). Fallback: manual user review of each deferral.

**Story File Update Fails:**
Re-read story file, verify exact text match for Edit, use unique context if needed.

**User Cancels:**
Cannot proceed without approvals. Re-run /dev when ready.

---

## Phase 06 vs Phase 08 DoD Validation

| Aspect | Phase 06 (This) | Phase 08 |
|--------|-----------------|----------|
| Purpose | Challenge ALL deferrals | Handle items WITHOUT justifications |
| Scope | Items with justifications | New incomplete items |
| Timing | After TDD, before commit | During commit prep |
| Validator | deferral-validator (semantic) | devforgeai-validate (format) |

No duplication: Phase 06 processes items WITH justifications. Phase 08 processes items WITHOUT.

---

## PHASE 06 COMPLETION CHECKPOINT

**Before proceeding to Phase 07, verify ALL steps executed:**

- [ ] **Step 1:** Grep scan complete, all deferred DoD items identified
- [ ] **Step 2:** Skip/continue decision made
- [ ] **Step 3:** deferral-validator invoked (if deferrals exist)
- [ ] **Step 4:** Validation results parsed and categorized
- [ ] **Step 5:** All deferrals displayed with validation results to user
- [ ] **Step 6:** User decisions captured for ALL deferrals (AskUserQuestion)
- [ ] **Step 6.5:** HALT verification passed (no autonomous approvals)
- [ ] **Step 7:** Story file updated with approval timestamps
- [ ] **Step 9:** AC Verification Checklist updated (or gracefully skipped)

**IF ANY UNCHECKED:** DO NOT PROCEED. Most common miss: Step 6 user approval.

**IF ALL CHECKED:**
```
PHASE 06 COMPLETE - Deferral Challenge Checkpoint Done

Deferrals: {count} | Approved: {count} | Implement: {count} | Removed: {count}
Zero autonomous deferrals. Ready for DoD format update.

**Next:** Load dod-update-workflow.md and execute Phase 07
```

**See Also:**
- `dod-update-workflow.md` - DoD formatting (MUST execute before Phase 08)
- `git-workflow-conventions.md` - Git commit workflow
- `dod-validation-checkpoint.md` - Phase 08 Step 1.7
- `deferral-budget-enforcement.md` - Phase 08 Step 1.6

---

## Handoff to Phase 07: DoD Update Workflow

Load and execute:
```
Read(file_path="references/dod-update-workflow.md")
```

Phase 07 does: mark completed DoD items [x], add to Implementation Notes (FLAT LIST), validate format via `devforgeai-validate validate-dod`, update Workflow Status.

**Pre-Phase-07 Checklist:**
- [ ] All deferred items have user approval (Phase 06)
- [ ] DoD items marked [x] in Definition of Done
- [ ] Items added to Implementation Notes (flat list, no ### subsection)
- [ ] Workflow Status updated
- [ ] devforgeai-validate validate-dod passes (exit code 0)

If ANY unchecked: DO NOT proceed to Phase 08.
