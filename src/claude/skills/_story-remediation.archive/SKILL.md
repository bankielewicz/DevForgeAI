---
name: story-remediation
description: |
  Apply automated and guided fixes to story, epic, and context files based on
  validate-stories audit findings. Classifies findings by fix complexity, applies
  safe automated fixes, guides interactive fixes with user confirmation, verifies
  all changes, and produces a fix report. Use when /fix-story is invoked, when
  audit findings need remediation, or when custody chain validation produces
  findings requiring correction.
metadata:
  author: DevForgeAI
  version: "1.0.0"
  category: story-lifecycle
  agent-skills-spec-version: "1.0"
  last-updated: "2026-02-17"
allowed-tools: Read Write Edit Glob Grep AskUserQuestion
---

# Story Remediation

You are a story remediation specialist that fixes story, epic, and context files based on structured audit findings from `/validate-stories`. You classify findings by fix complexity, apply safe automated fixes, guide interactive fixes with user confirmation, verify all changes, and produce a fix report.

## EXECUTION MODEL: This Skill Expands Inline

After invocation via `/fix-story` command, YOU (Claude) execute these phases sequentially. Do not wait passively after skill invocation. Execute Phase 0 through Phase 5 in order.

---

## Phase 0: Context Loading + Finding Extraction

### Step 0.1: Read Context Markers

Read the context markers set by the `/fix-story` command in the conversation:

- **Fix Mode:** audit_file | story_id | epic_id
- **Audit File:** path to audit file
- **Dry Run:** true | false
- **Auto Only:** true | false
- **Finding Filter:** F-NNN | all

### Step 0.2: Load Audit File + Parse Findings

```
audit_content = Read(file_path=AUDIT_FILE)

Parse findings from "## 4. Findings Detail" section.
Each finding is a table with fields:
  - Finding ID (e.g., F-001)
  - Severity (CRITICAL | HIGH | MEDIUM | LOW)
  - Type (e.g., quality/broken_file_reference)
  - Affected (comma-separated story/epic IDs)
  - Phase (audit phase that detected it)
  - Summary (description of issue)
  - Evidence (proof of issue with file/line references)
  - Remediation (fix instructions)
  - Verification (how to confirm fix worked)
```

### Step 0.3: Load Reference Files in PARALLEL

```
Read(file_path="references/fix-actions-catalog.md")
Read(file_path="references/fix-verification-workflow.md")
Read(file_path=".claude/skills/spec-driven-stories/references/context-validation.md")
```

### Step 0.4: Apply Finding Filter

```
IF Finding Filter != "all":
    findings = [f for f in findings if f.finding_id == FINDING_FILTER]
    IF findings is empty:
        HALT: "Finding {FINDING_FILTER} not found in audit file"
```

### Step 0.5: Resume Detection

```
IF audit_content contains "## 9. Fix Session":
    Parse previously fixed finding IDs from fix session records
    Mark those findings as "previously_fixed"
    Display: "Resuming: {K} findings already fixed in prior session"
```

Display: "**{N} findings loaded** ({M} new, {K} previously fixed)"

---

## Phase 1: Finding Triage + Classification

**For detailed classification procedures:** → Load `references/fix-actions-catalog.md`

<thinking>
For each finding, classify by evaluating three safety conditions:
1. Is the fix deterministic? (old/new values derivable from evidence and remediation fields)
2. Is it a single file affected? (or batch of identical single-file edits)
3. Is the target file NOT a context file? (context files are LOCKED — require interactive confirmation)

IF all three conditions met → "automated"
IF target is a context file → "interactive" (context files are immutable without user approval)
IF finding mentions ADR → "adr_required"
IF no fix procedure available → "advisory"
</thinking>

FOR each finding (skip previously_fixed):

```
classification = classify_finding(finding)
  → "automated"     — deterministic fix, single file, not a context file
  → "interactive"   — multi-file, context file edit, or requires judgment
  → "adr_required"  — needs ADR creation/reference before fix
  → "advisory"      — informational only, no automated fix possible
```

Display fix plan summary:

```
╔══════════════════════════════════════════╗
║           Fix Plan Summary               ║
╠══════════════════════════════════════════╣
║  Automated (safe):   {count_auto}        ║
║  Interactive:        {count_interactive}  ║
║  Requires ADR:       {count_adr}         ║
║  Advisory only:      {count_advisory}    ║
║  Previously fixed:   {count_fixed}       ║
╚══════════════════════════════════════════╝
```

---

## Phase 2: Safety Preview

FOR each automated finding, generate and display a preview:

<fix_preview>
  <finding_id>{finding_id}</finding_id>
  <severity>{severity}</severity>
  <file>{target_file_path}</file>
  <before>{old_string}</before>
  <after>{new_string}</after>
</fix_preview>

Display all previews to user.

### Dry Run Exit Point

```
IF Dry Run == true:
    Display: "✅ Dry run complete. No files were modified."
    Display: "Re-run without --dry-run to apply fixes."
    → GOTO Phase 5 (report only, no session record)
```

### User Confirmation

```
IF count_auto > 0:
    AskUserQuestion:
        Question: "Apply {count_auto} automated fixes now?"
        Header: "Fix Mode"
        Options:
            - label: "Apply all automated fixes (Recommended)"
              description: "Safe, non-structural changes with post-fix verification"
            - label: "Review each fix individually"
              description: "Walk through each automated fix one at a time"
            - label: "Skip automated, do interactive only"
              description: "Manual control for all changes"
```

---

## Phase 3: Fix Execution

### Step 3.1: Automated Fixes

FOR each automated finding (ordered by priority from audit §7 Remediation Priority Order):

1. Extract fix parameters from finding evidence and remediation fields
2. Apply fix using procedure from `references/fix-actions-catalog.md`
3. Record result:

<fix_result>
  <finding_id>{finding_id}</finding_id>
  <status>applied</status>
  <file>{file_path}</file>
  <change_summary>{description of change}</change_summary>
</fix_result>

4. Display: "✓ Fixed {finding_id}: {change_summary}"

**Checkpoint:** After all automated fixes, write partial results summary to conversation for session resilience.

### Step 3.2: Interactive Fixes

**Skip if Auto Only == true.**

FOR each interactive finding:

1. Display finding details:
   ```
   [{severity}] {finding_id}: {type}
   Summary: {summary}
   Affected: {affected files/stories}
   Remediation options: {remediation}
   ```

2. Present resolution:
   ```
   AskUserQuestion:
       Question: "How to resolve {finding_id}?"
       Header: "Resolution"
       Options:
           - label: "Apply recommended fix"
             description: "{recommended_fix_description}"
           - label: "Defer"
             description: "Add AUDIT-DEFERRED marker, fix later"
   ```

3. **Batch finding handling** (affects >3 files):
   ```
   AskUserQuestion:
       Question: "Apply same resolution to all {N} affected files?"
       Header: "Batch Fix"
       Options:
           - label: "Yes — apply uniformly"
             description: "Same change in all {N} files"
           - label: "No — review each file"
             description: "Walk through files individually"
   ```

4. Apply chosen resolution or add deferral marker:
   ```
   IF deferred:
       Edit target file to add: <!-- AUDIT-DEFERRED: {finding_id} - {reason} -->
   ```

### Step 3.3: ADR-Required Fixes

**Skip if Auto Only == true.**

FOR each adr_required finding:

1. Read referenced ADR file (if ADR ID provided in evidence)
2. Present options:
   ```
   AskUserQuestion:
       Question: "Does existing ADR cover this case?"
       Header: "ADR Review"
       Options:
           - label: "Yes, cite existing ADR"
             description: "Update note to reference ADR-{NNN}"
           - label: "No, needs new ADR"
             description: "Defer fix — run /create-story for ADR first"
           - label: "Defer"
             description: "Mark as AUDIT-DEFERRED"
   ```
3. Apply chosen resolution

---

## Phase 4: Post-Fix Verification (Feedback Loop)

**For detailed verification procedures:** → Load `references/fix-verification-workflow.md`

FOR each applied fix:

1. Run the verification check from the finding's "Verification" field:

<verification>
  <finding_id>{finding_id}</finding_id>
  <method>{verification_command}</method>
  <passed>{true|false}</passed>
  <error>{error_message if failed}</error>
</verification>

2. Display result:
   - ✓ "Verified {finding_id}" (if passed)
   - ✗ "Failed {finding_id}: {error}" (if failed)

### Feedback Loop on Verification Failure

```
IF any verification fails:
    AskUserQuestion:
        Question: "Verification failed for {finding_id}. How to proceed?"
        Header: "Fix Failed"
        Options:
            - label: "Retry fix"
              description: "Re-apply the fix and verify again (max 2 retries)"
            - label: "Try manual approach"
              description: "I'll provide the correct edit"
            - label: "Defer"
              description: "Mark as AUDIT-DEFERRED, fix later"

    IF retry: re-apply fix → re-verify (max 2 retries total)
    Only proceed when verification passes OR user explicitly defers.
```

---

## Phase 5: Fix Report + Session Record

### Generate Report

<report>

```
## Fix Session Report

**Audit Source:** {AUDIT_FILE}
**Session Date:** {current_date}
**Mode:** {Dry Run | Auto Only | Full}

### Results Summary

| Outcome | Count |
|---------|-------|
| Applied (automated) | {count_auto_applied} |
| Applied (interactive) | {count_interactive_applied} |
| Deferred | {count_deferred} |
| Skipped | {count_skipped} |
| Failed verification | {count_failed} |
| Previously fixed | {count_previously_fixed} |

### Applied Fixes

{FOR each applied fix:}
- [✓] {finding_id} ({type}): {change_summary} — verified

### Deferred Items

{FOR each deferred:}
- [ ] {finding_id} ({severity}): {reason}

### Remaining Findings

{FOR each not_fixed:}
- {finding_id} ({severity}): {summary}

### Next Steps

{IF all fixed: "Run /validate-stories to confirm clean audit."}
{IF remaining: "Re-run /fix-story to address remaining findings."}
{IF deferred: "Address deferred items in a future session."}
```

</report>

### Append Session Record to Audit File

```
IF AUDIT_FILE exists AND Dry Run == false:
    Append to audit file:

    ## 9. Fix Session: {current_date}

    **Applied:** {count_applied} | **Deferred:** {count_deferred} | **Skipped:** {count_skipped}

    | Finding | Status | Verification |
    |---------|--------|-------------|
    {FOR each finding: | {id} | {status} | {verified/deferred/skipped} |}
```

This enables resume detection on re-run (Phase 0, Step 0.5).

Display report to user.

---

## Success Criteria

This skill succeeds when:
- [ ] All findings loaded and classified correctly
- [ ] Automated fixes applied only after user confirmation
- [ ] Interactive fixes presented with clear resolution options
- [ ] All applied fixes pass post-fix verification
- [ ] Fix report generated with accurate summary
- [ ] Session record appended to audit file for resume capability
- [ ] No files modified without user approval (--dry-run respected)
- [ ] Deferred items properly marked with AUDIT-DEFERRED comments
