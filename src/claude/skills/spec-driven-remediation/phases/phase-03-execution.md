# Phase 03: Fix Execution

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=remediation --from=02 --to=03
# Exit 0: proceed | Exit 1: Phase 02 incomplete
```

## Contract

PURPOSE: Apply fixes to files based on classification — automated fixes first, then interactive, then ADR-required.
REQUIRED SUBAGENTS: None (fixes are applied inline via Edit/Write; user decisions via AskUserQuestion)
REQUIRED ARTIFACTS: Modified files, per-finding status in checkpoint
STEP COUNT: 3 mandatory steps (Steps 2 and 3 are conditional on AUTO_ONLY flag)

**Safety principle:** Every file modification uses Edit() with explicit old_string/new_string. No blind overwrites.

---

## Mandatory Steps

### Step 1: Automated Fixes

EXECUTE: Load fix-actions-catalog.md fresh for this phase (per-phase reference loading). Then apply each automated fix.
```
Read(file_path="{SKILL_DIR}/references/fix-actions-catalog.md")
```

For each automated finding, ordered by priority from audit Section 7 (Remediation Priority Order):
```
FOR each finding WHERE classification == "automated":

    IF USER_APPROVAL_MODE == "skip_auto":
        Mark finding as status = "skipped"
        Display: "- Skipped {finding_id} (user chose skip automated)"
        CONTINUE

    IF USER_APPROVAL_MODE == "review_each":
        Display the fix preview for this finding
        AskUserQuestion:
            Question: "Apply this fix for {finding_id}?"
            Header: "Confirm Fix"
            Options:
                - label: "Apply"
                  description: "{change_summary}"
                - label: "Skip"
                  description: "Do not apply this fix"
        IF user chose "Skip":
            Mark finding as status = "skipped"
            CONTINUE

    # Extract fix parameters
    Use the appropriate fix procedure from fix-actions-catalog.md:
    - fix_broken_file_reference for quality/broken_file_reference
    - fix_missing_frontmatter_field for provenance/missing_*
    - fix_stale_status_label for quality/stale_status_label
    - fix_api_contract_error for coherence/api_contract_error
    - fix_naming_inconsistency for coherence/naming_inconsistency

    # Apply the fix
    Edit(
        file_path = {target_file_path},
        old_string = {old_string},
        new_string = {new_string}
    )

    # Record result
    Mark finding as status = "applied", change_summary = "{description}"
    Display: "Applied {finding_id}: {change_summary}"
```

VERIFY: For each applied automated fix, confirm the change was made.
```
FOR each finding WHERE status == "applied" AND classification == "automated":
    Grep(pattern="{new_string_pattern}", path="{target_file_path}")
    # Must return a match — the new value is present in the file
```

RECORD:
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=remediation --phase=03 --step=auto-fixes
```

**Checkpoint (mid-phase):** After all automated fixes, write partial results to checkpoint for session resilience.
```
Update checkpoint:
  current_phase: 3
  findings:
    - finding_id: "F-001"
      status: "applied"
      file_changed: "{path}"
      change_summary: "{description}"
```

---

### Step 2: Interactive Fixes

**SKIP if AUTO_ONLY == true.** Display: "Auto-only mode — skipping {count_interactive} interactive findings."

EXECUTE: For each interactive finding, present the issue and resolution options to the user.
```
FOR each finding WHERE classification == "interactive":

    # Display finding details
    Display:
    [{severity}] {finding_id}: {type}
    Summary: {summary}
    Affected: {affected files/stories}
    Evidence: {evidence}
    Remediation options: {remediation}

    # Present resolution via AskUserQuestion
    AskUserQuestion:
        Question: "How to resolve {finding_id}?"
        Header: "Resolution"
        Options:
            - label: "Apply recommended fix"
              description: "{recommended_fix_from_remediation_field}"
            - label: "Defer"
              description: "Add AUDIT-DEFERRED marker, fix later"

    IF user chose "Apply recommended fix":
        # Apply the fix using the procedure from fix-actions-catalog.md
        # The interactive fix procedures in the catalog describe exactly how
        Apply fix per fix-actions-catalog.md Interactive Fix Procedures section
        Mark finding as status = "applied"
        Display: "Applied {finding_id}: {change_summary}"

    ELIF user chose "Defer":
        # Add deferral marker to target file
        Edit(
            file_path = {target_file},
            old_string = {appropriate_anchor_text},
            new_string = {anchor_text + "\n<!-- AUDIT-DEFERRED: {finding_id} - {user_reason} -->"}
        )
        Mark finding as status = "deferred"
        Display: "Deferred {finding_id}: {reason}"

    # Record user decision in checkpoint
    Update checkpoint user_decisions:
        - timestamp: {current_timestamp}
          finding_id: "{finding_id}"
          decision: "{user_choice}"
```

**Batch finding handling** (affects >3 files with same fix type):
```
IF finding affects > 3 files with identical fix type:
    AskUserQuestion:
        Question: "Apply same resolution to all {N} affected files?"
        Header: "Batch Fix"
        Options:
            - label: "Yes, apply uniformly"
              description: "Same change in all {N} files"
            - label: "No, review each file"
              description: "Walk through files individually"

    IF "Yes, apply uniformly":
        Apply to all files in batch
    ELSE:
        Walk through each file with individual AskUserQuestion
```

VERIFY: Each interactive finding has a final status of "applied" or "deferred".
```
FOR each finding WHERE classification == "interactive":
    ASSERT finding.status in ["applied", "deferred"]
    IF finding.status == "applied":
        # Verify the change exists in the target file
        Grep(pattern="{verification_pattern}", path="{target_file}")
    IF finding.status == "deferred":
        # Verify the AUDIT-DEFERRED marker was added
        Grep(pattern="AUDIT-DEFERRED: {finding_id}", path="{target_file}")
```

RECORD:
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=remediation --phase=03 --step=interactive-fixes
```

---

### Step 3: ADR-Required Fixes

**SKIP if AUTO_ONLY == true.** Display: "Auto-only mode — skipping {count_adr} ADR-required findings."

EXECUTE: For each ADR-required finding, read the referenced ADR (if any) and present resolution options.
```
FOR each finding WHERE classification == "adr_required":

    # Read referenced ADR if available
    IF finding.Evidence or finding.Remediation references an ADR ID (e.g., ADR-NNN):
        adr_path = "devforgeai/specs/adrs/ADR-{NNN}-*.md"
        adr_files = Glob(pattern=adr_path)
        IF adr_files:
            Read(file_path=adr_files[0])

    AskUserQuestion:
        Question: "Does existing ADR cover this case for {finding_id}?"
        Header: "ADR Review"
        Options:
            - label: "Yes, cite existing ADR"
              description: "Update note to reference ADR-{NNN}"
            - label: "No, needs new ADR"
              description: "Defer fix — run /create-story for ADR first"
            - label: "Defer"
              description: "Mark as AUDIT-DEFERRED"

    IF "Yes, cite existing ADR":
        Apply fix with ADR citation
        Mark finding as status = "applied"

    ELIF "No, needs new ADR":
        Display: "Deferring {finding_id} — create ADR story first, then re-run /fix-story"
        Mark finding as status = "deferred"
        Add AUDIT-DEFERRED marker

    ELIF "Defer":
        Add AUDIT-DEFERRED marker
        Mark finding as status = "deferred"
```

VERIFY: Each ADR-required finding has a final status.
```
FOR each finding WHERE classification == "adr_required":
    ASSERT finding.status in ["applied", "deferred"]
```

RECORD:
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=remediation --phase=03 --step=adr-fixes
```

Update checkpoint with complete fix execution results:
```
Update checkpoint:
  current_phase: 3
  phase_completion:
    phase_03: true
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=remediation --phase=03 --checkpoint-passed
# Exit 0: proceed to Phase 04 | Exit 1: phase incomplete
```
