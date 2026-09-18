# Phase 04: Post-Fix Verification

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=remediation --from=03 --to=04
# Exit 0: proceed | Exit 1: Phase 03 incomplete
```

## Contract

PURPOSE: Verify every applied fix using the finding's Verification field and per-type verification procedures. Provide feedback loop on failures.
REQUIRED SUBAGENTS: None
REQUIRED ARTIFACTS: Per-finding verification status in checkpoint
STEP COUNT: 2 mandatory steps

**Verification principle:** Never trust that a fix worked because you applied it. Always verify independently using the finding's Verification field.

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-remediation/references/fix-verification-workflow.md")
```

IF Read fails: HALT -- "Phase 04 reference files not loaded."

---

## Mandatory Steps

### Step 1: Load Reference — fix-verification-workflow.md (Fresh Per-Phase Load)

EXECUTE: Load the verification workflow reference fresh for this phase. Do NOT rely on any previously loaded version.
```
Read(file_path="{SKILL_DIR}/references/fix-verification-workflow.md")
```

VERIFY: Content loaded and contains "Per-Type Verification Procedures" heading.
```
Grep(pattern="## Per-Type Verification Procedures", path="{SKILL_DIR}/references/fix-verification-workflow.md")
# Must return a match
```

RECORD: Reference load confirmed.

---

### Step 2: Verify Each Applied Fix

EXECUTE: For each fix with status == "applied", run the verification check specified in the finding's Verification field and the per-type procedures from fix-verification-workflow.md.

```
FOR each finding WHERE status == "applied":

    # Determine verification method from finding.Verification field
    # Cross-reference with per-type procedure in fix-verification-workflow.md

    verification_result = RUN verification check:
        - For file reference fixes: Glob/Grep to confirm file exists at new path
        - For frontmatter fixes: Grep to confirm field present in frontmatter
        - For status fixes: Grep to confirm new status value
        - For path fixes: Read target file to confirm it exists
        - For naming fixes: Grep to confirm new name present, old name absent

    <verification>
      <finding_id>{finding_id}</finding_id>
      <method>{verification_command}</method>
      <passed>{true|false}</passed>
      <error>{error_message if failed}</error>
    </verification>

    IF verification_result.passed:
        Display: "Verified {finding_id}"
        Mark finding as verification = "passed"

    ELSE:
        Display: "Failed {finding_id}: {error_message}"
        Mark finding as verification = "failed"

        # FEEDBACK LOOP
        IF finding.retry_count < 2:
            AskUserQuestion:
                Question: "Verification failed for {finding_id}. How to proceed?"
                Header: "Fix Failed"
                Options:
                    - label: "Retry fix"
                      description: "Re-apply the fix and verify again (attempt {retry_count + 1} of 2)"
                    - label: "Try manual approach"
                      description: "I'll provide the correct edit"
                    - label: "Defer"
                      description: "Mark as AUDIT-DEFERRED, fix later"

            IF user chose "Retry fix":
                finding.retry_count += 1
                Re-apply fix using same procedure
                Re-run verification
                IF passes: Mark verification = "passed"
                ELSE: Continue to next iteration of feedback loop

            ELIF user chose "Try manual approach":
                # User will provide the correct edit — wait for input
                AskUserQuestion:
                    Question: "What should the correct edit be for {finding_id}?"
                    Header: "Manual Fix"
                    Options:
                        - label: "I'll describe the fix"
                          description: "Tell me what to change and I'll apply it"
                        - label: "Defer instead"
                          description: "Mark as AUDIT-DEFERRED"
                Apply user-provided fix
                Re-run verification

            ELIF user chose "Defer":
                Add AUDIT-DEFERRED marker to target file
                Mark finding as status = "deferred", verification = "deferred"

        ELSE:
            # Max retries reached (2)
            Display: "Max retries reached for {finding_id}. Deferring."
            AskUserQuestion:
                Question: "Max 2 retries reached for {finding_id}. Defer or provide manual fix?"
                Header: "Max Retries"
                Options:
                    - label: "Defer"
                      description: "Mark as AUDIT-DEFERRED"
                    - label: "I'll provide the fix manually"
                      description: "Tell me the exact edit to make"
```

VERIFY: Every applied finding has a final verification status of "passed" or "deferred".
```
FOR each finding WHERE status == "applied":
    ASSERT finding.verification in ["passed", "deferred"]
    # No finding should be left with verification = "failed" — it must be resolved
    # via retry, manual fix, or deferral
```

---

### AC-Count Preservation Heuristic (template/legacy_format fixes)

**Trigger:** For any story that had at least one finding with `type == "template/legacy_format"` applied (or deferred) in Phase 03 Step 2.

**Purpose:** Markdown→XML AC conversion (Phase 03 procedure P6) must NEVER drop or merge AC blocks. This heuristic counts AC headers before and after the edits and fails verification on mismatch.

```
FOR each story_id WHERE checkpoint.template_legacy_format_pre_ac_count[story_id] is set:

    pre_count = checkpoint.template_legacy_format_pre_ac_count[story_id]

    Read(file_path=target_file_for(story_id)) -> content

    post_count_xml = number of matches of regex r'<acceptance_criteria id="AC[0-9]+"' in content
    post_count_deferred = number of `^### AC#?\d+:` headers in content that are immediately followed
                          by a line matching `AUDIT-DEFERRED: template/legacy_format`

    total_post = post_count_xml + post_count_deferred

    IF total_post != pre_count:
        # AC count mismatch — silent loss detected
        FOR each finding WHERE finding.affected == [story_id] AND finding.type == "template/legacy_format":
            Mark finding verification = "failed"

        Display: f"AC count mismatch for {story_id}: pre={pre_count}, post={total_post} (xml={post_count_xml} + deferred={post_count_deferred}). Manual review required."

        # Surface to user via AskUserQuestion using the standard Step 2 feedback loop
        AskUserQuestion:
            Question: f"AC-count preservation failed for {story_id}. The markdown→XML conversion lost or merged AC blocks. How to proceed?"
            Header: "AC Count"
            Options:
                - label: "Show diff and let me decide"
                  description: "Display pre/post AC headers and proceed with user-guided correction"
                - label: "Re-run P6 fixes for this story"
                  description: "Reset all template/legacy_format findings for this story to status='pending' and re-execute"
                - label: "Defer all P6 findings for this story"
                  description: "Mark all template/legacy_format findings as deferred with AUDIT-DEFERRED markers"

    ELSE:
        # Count preserved — all P6 fixes retain their existing status (applied or deferred)
        Display: f"AC count preserved for {story_id}: pre={pre_count}, post={total_post}. ✓"
```

This heuristic supplements the standard per-finding Grep verification. It catches the failure mode where individual `<acceptance_criteria>` blocks are syntactically correct but the AC count diverges (e.g., two markdown ACs merged into one XML AC, or one markdown AC dropped entirely during the Edit).

RECORD:
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=remediation --phase=04 --step=verify-fixes
```

Update checkpoint with verification results:
```
Update checkpoint:
  current_phase: 4
  findings:
    - finding_id: "F-001"
      verification: "passed"
      retry_count: 0
    - finding_id: "F-002"
      verification: "passed"
      retry_count: 1
    - finding_id: "F-003"
      verification: "deferred"
      retry_count: 2
  phase_completion:
    phase_04: true
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=remediation --phase=04 --checkpoint-passed
# Exit 0: proceed to Phase 05 | Exit 1: phase incomplete
```
