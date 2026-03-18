# Reporting Workflow (SKILL.md Phase 5)

> **Phase mapping:** This file uses legacy step numbering (3.1-3.4). In SKILL.md v3.0, Reporting is **Phase 5** with steps 5.1-5.4. The step content is identical.

Contains complete implementation for reporting steps including ADR-010 coverage enforcement, RCA-002 gaps.json creation, and the Atomic Update Protocol (STORY-177).

---

### Step 3.1-3.3: Result Determination and Report Generation

**Purpose:** Determine QA result and generate reports.

**1. Determine Result:**

**CRITICAL (ADR-010):** Coverage below thresholds is a BLOCKING condition.
- Coverage gaps are NOT warnings - they trigger FAILED status
- test-automator WARN for coverage → escalates to FAILED here
- No deferral path exists for coverage gaps

```
# Coverage thresholds: Business 95%, Application 85%, Infrastructure 80%
# IMPORTANT: coverage < thresholds → FAILED (not PASS WITH WARNINGS)
IF any CRITICAL violations OR coverage < thresholds OR parallel < 66%:
    overall_status = "FAILED"
    # Coverage gap = FAILED (non-negotiable, per ADR-010)
ELIF any HIGH violations:
    overall_status = "PASS WITH WARNINGS"
    # HIGH violations (NOT coverage) allow approval with warnings
ELSE:
    overall_status = "PASSED"

Display: "Result determined: {overall_status}"
```

**2. Generate QA Report (Deep Mode Only):**
```
IF mode == "deep":
    Write(file_path="devforgeai/qa/reports/{STORY-ID}-qa-report.md",
          content=formatted_report)
    Display: "✓ QA report generated"
```

**3. Generate gaps.json (FAILED or PASS WITH WARNINGS):**

**MANDATORY if overall_status == "FAILED" OR "PASS WITH WARNINGS":**
```
Write(file_path="devforgeai/qa/reports/{STORY-ID}-gaps.json",
      content=JSON containing:
        - story_id
        - qa_result: overall_status  # "FAILED" or "PASS WITH WARNINGS"
        - coverage_gaps: [{file, layer, current, target, gap, suggested_tests}]
        - anti_pattern_violations: [{file, line, type, severity, remediation}]
        - deferral_issues: [{item, violation_type, severity, remediation}]
        - remediation_sequence: [{phase, name, target_files, gap_count}]
)

# Verify creation
Glob(pattern="devforgeai/qa/reports/{STORY-ID}-gaps.json")
IF NOT found:
    HALT: "gaps.json not created - required for /dev remediation mode"
```

### Step 3.3.5: MANDATORY gaps.json Creation BEFORE Status Transition [RCA-002]

**Purpose:** Ensure gaps.json exists BEFORE any status update to "QA Failed". This is a mandatory prerequisite for the atomic status update protocol.

**CRITICAL:** Create gaps.json BEFORE status update in Step 3.4. This ensures `/dev --fix` remediation mode has the required gap file regardless of how the failure was detected.

**Source:** RCA-002 discovered that gaps.json creation was conditional on deep mode, not status transition. This step links gaps.json creation to status="QA Failed" unconditionally.

**When overall_status == "FAILED":**
```
# MANDATORY: Write gaps.json BEFORE status Edit [RCA-002]
# Idempotent: Write() overwrites existing gaps.json (not append)

Write(file_path="devforgeai/qa/reports/{STORY-ID}-gaps.json",
      content=JSON containing:
        - story_id: "{STORY-ID}"
        - qa_timestamp: "{ISO_8601}"
        - overall_status: "FAILED"
        - violations: [
            {type, severity, message, remediation}
          ]
)

# Verify creation
Glob(pattern="devforgeai/qa/reports/{STORY-ID}-gaps.json")
IF NOT found:
    HALT: "gaps.json not created - cannot proceed to status update"

Display: "✓ gaps.json created (required for QA Failed status)"
```

**Idempotent Behavior:** Write() tool overwrites existing file. Each QA run produces fresh gaps.json with current violations only.

**Proceed to Step 3.4 only after gaps.json creation confirmed.**

### Step 3.4: Story File Update [Atomic Update Protocol - STORY-177]

**Purpose:** Update story YAML frontmatter status using atomic update protocol with QA results.

---

#### Atomic Update Protocol (STORY-177)

**CRITICAL:** Status updates MUST follow this 5-step atomic sequence to prevent YAML frontmatter divergence.

**Protocol Sequence:**
1. read current status from yaml frontmatter (capture for rollback)
2. edit yaml frontmatter status field (FIRST - before second edit)
3. grep verify new status in frontmatter (MANDATORY)
4. edit append record entry (ONLY after step 3 passes)
5. rollback: restore original status if verification fails (skip step 4)

---

**Step 1: Read Current Status (capture for rollback):**
```
Read(file_path="devforgeai/specs/Stories/{STORY-ID}.story.md")

# Extract and store original status for potential rollback
original_status = extract_status_from_yaml(file_content)
# Example: original_status = "Dev Complete"

Display: "✓ Original status captured: {original_status}"
```

**Step 2: Edit YAML Frontmatter Status (FIRST - yaml first):**
```
# Determine target status
IF overall_status == "PASSED" OR overall_status == "PASS WITH WARNINGS":
    target_status = "QA Approved"
ELSE:
    target_status = "QA Failed"

# Edit YAML frontmatter status FIRST (before Step 4)
Edit(
    file_path="devforgeai/specs/Stories/{STORY-ID}.story.md",
    old_string="status: {original_status}",
    new_string="status: {target_status}"
)

Display: "✓ YAML status edited: {original_status} → {target_status}"
```

**Step 3: Grep Verify New Status (MANDATORY):**
```
# Verify the status update succeeded using Grep
Grep(
    pattern="^status: {target_status}",
    path="devforgeai/specs/Stories/{STORY-ID}.story.md",
    output_mode="content"
)

IF grep_result.found == false:
    # ROLLBACK TRIGGERED - verification failed
    GOTO Step 5 (Rollback)
ELSE:
    # status before history - Grep verification complete, proceed to history
    Display: "✓ Status verification passed: {target_status} confirmed in frontmatter"
    # Proceed to Step 4
```

**Step 4: Edit Append History Entry (ONLY after verification succeeds):**
**Reference:** `.claude/references/changelog-update-guide.md`
    Read(file_path=".claude/references/changelog-update-guide.md")

```
# IF verification succeeds THEN append history
# do not append if fail - skip history on fail
# 3-step sequence: Edit status -> Grep verify -> Edit history
# This step executes ONLY if Step 3 verification passed
# History entry is CONDITIONAL on successful status update

Author: `.claude/qa-result-interpreter`
Phase/Action: `QA Light` or `QA Deep`
Change: `{result}: Coverage {pct}%, {violations} violations`

# Append changelog entry using Edit tool
Edit(
    file_path="devforgeai/specs/Stories/{STORY-ID}.story.md",
    old_string="| {last_date} | {last_author} | {last_action} | {last_change} | {last_files} |",
    new_string="| {last_date} | {last_author} | {last_action} | {last_change} | {last_files} |\n| {current_timestamp} | .claude/qa-result-interpreter | QA {MODE} | {overall_status}: Coverage {coverage}%, {violations} violations | - |"
)

# Update Current Status display
Edit(
    file_path="devforgeai/specs/Stories/{STORY-ID}.story.md",
    old_string="**Current Status:** {original_status}",
    new_string="**Current Status:** {target_status}"
)

Display: "✓ Change Log entry appended"
$STORY_FILE_UPDATED = true
```

**Step 5: Rollback Restore Original on Verification Failure:**
```
# This step executes ONLY if Step 3 verification FAILED
# Restores original status, no history append on rollback
# Use Edit to restore original value

Edit(
    file_path="devforgeai/specs/Stories/{STORY-ID}.story.md",
    old_string="status: {target_status}",
    new_string="status: {original_status}"
)
# Edit restores original value - rollback complete

Display: "❌ Status verification FAILED - rolled back to: {original_status}"
Display: "   No history entry appended (rollback scenario)"
Display: "   Manual intervention required"

HALT: "Atomic status update failed - divergence prevented by rollback"
```

---

#### Single Edit Sequence Optimization (AC#4)

**when possible use single Edit to combine YAML update and append in one sequence.**
**Use single Edit when:** file structure allows, both updates in proximity.
**Fallback to separate edits when:** file structure prevents combined edit.
**Optimization rationale:** token efficiency - reduces tool calls.
```
# Optimized: Single Edit for both status and history (reduces tool calls)
# Use when story file structure allows combined edit

Edit(
    file_path="devforgeai/specs/Stories/{STORY-ID}.story.md",
    old_string="status: {original_status}\n...\n| {last_changelog_row} |",
    new_string="status: {target_status}\n...\n| {last_changelog_row} |\n| {new_changelog_row} |"
)

# Still require Grep verification after combined edit
Grep(pattern="^status: {target_status}", path="...")
```

**Fallback:** Use separate Edits (Steps 2 and 4) when single Edit not possible due to file structure.

---

**Validation Checkpoint (Atomic Update):**
- [ ] Original status captured (Step 1)?
- [ ] YAML frontmatter Edit executed FIRST (Step 2)?
- [ ] Grep verification executed (Step 3)?
- [ ] Verification passed (no rollback triggered)?
- [ ] History entry appended AFTER verification (Step 4)?
- [ ] Change Log entry has `.claude/qa-result-interpreter` author?

IF any checkbox unchecked: HALT with "Atomic update incomplete"
IF rollback triggered: HALT with "Atomic update failed - rolled back"

**This step is ATOMIC - do NOT proceed to Phase 4 until story file verified.**
