# Fix Verification Workflow

Post-fix verification procedures for each finding type. Every applied fix MUST be verified before marking as complete.

---

## Table of Contents

1. [Verification Principles](#verification-principles)
2. [Per-Type Verification Procedures](#per-type-verification-procedures)
3. [Failure Handling](#failure-handling)
4. [Verification Report Format](#verification-report-format)

---

## Verification Principles

1. **Every fix gets verified.** No fix is marked "applied" without passing verification.
2. **Use the finding's Verification field.** Each audit finding includes a specific verification command — use it.
3. **Fail fast, don't fail silently.** If verification fails, report it immediately.
4. **Feedback loop.** On failure: retry → manual → defer. Max 2 retries.

---

## Per-Type Verification Procedures

### quality/broken_file_reference

**Method:** Confirm the corrected path/filename exists on disk AND the old (broken) string no longer exists in the target file.

```
Step 1: Verify correct file exists
    result = Glob(pattern="{correct_file_path}")
    IF no match: FAIL "Corrected file not found on disk: {correct_file_path}"

Step 2: Verify old string removed from target
    result = Grep(pattern="{old_string}", path="{target_story_file}")
    IF match found: FAIL "Old string still present in {target_story_file}"

→ Both pass: PASS ✓
```

### provenance/missing_brainstorm_frontmatter

**Method:** Confirm the new YAML field exists in the file's frontmatter.

```
Step 1: Grep for the field
    result = Grep(pattern="{field_name}:", path="{target_file}")
    IF no match: FAIL "Field '{field_name}' not found in {target_file}"

Step 2: Verify value is correct
    result = Grep(pattern="{field_name}: {expected_value}", path="{target_file}")
    IF no match: FAIL "Field exists but value is wrong"

→ Both pass: PASS ✓
```

### provenance/missing_frontmatter

**Method:** Same as `missing_brainstorm_frontmatter` — verify field and value present.

```
Step 1: Grep for the field
    result = Grep(pattern="{field_name}:", path="{target_file}")
    IF no match: FAIL "Field '{field_name}' not found in {target_file}"

Step 2: Verify value
    result = Grep(pattern="{field_name}: {expected_value}", path="{target_file}")
    IF no match: FAIL "Field exists but value is wrong"

→ Both pass: PASS ✓
```

### quality/stale_status_label

**Method:** Confirm the new status value is present and the old value is gone.

```
Step 1: Verify new status
    result = Grep(pattern="status: {new_status}", path="{target_file}")
    IF no match: FAIL "New status not found"

Step 2: Verify old status removed
    result = Grep(pattern="status: {old_status}", path="{target_file}")
    IF match found: FAIL "Old status still present"

→ Both pass: PASS ✓
```

### context/invalid_path

**Method:** Depends on resolution chosen by user.

**IF resolution = "Add path to source-tree.md":**
```
Step 1: Verify path in source-tree.md
    result = Grep(pattern="{new_path}", path="devforgeai/specs/context/source-tree.md")
    IF no match: FAIL "Path not found in source-tree.md"

→ PASS ✓
```

**IF resolution = "Redirect outputs to documented directory":**
```
Step 1: Verify ALL affected story files updated
    FOR each affected_story in finding.Affected:
        story_path = resolve_story_path(affected_story)
        result = Grep(pattern="{old_path}", path=story_path)
        IF match found: FAIL "Old path still present in {affected_story}"

Step 2: Verify new path used
    FOR each affected_story in finding.Affected:
        story_path = resolve_story_path(affected_story)
        result = Grep(pattern="{new_path}", path=story_path)
        IF no match: FAIL "New path not found in {affected_story}"

→ All pass: PASS ✓
```

### adr/implicit_adr_need

**Method:** Confirm the note has been updated with explicit ADR reference OR deferred.

```
IF resolution = "Cite existing ADR":
    result = Grep(pattern="ADR-\\d+", path="{target_file}")
    IF no match: FAIL "No explicit ADR reference found"

    result = Grep(pattern="Will require ADR", path="{target_file}")
    IF match found: FAIL "Ambiguous 'Will require ADR' text still present"

IF resolution = "Deferred":
    result = Grep(pattern="AUDIT-DEFERRED", path="{target_file}")
    IF no match: FAIL "Deferral marker not found"

→ PASS ✓
```

### provenance/broken_brainstorm_ref

**Method:** Confirm brainstorm reference is valid and points to existing file.

```
Step 1: Extract brainstorm reference
    result = Grep(pattern="brainstorm.*:", path="{target_file}")
    brainstorm_id = extract BRAINSTORM-NNN from result

Step 2: Verify brainstorm file exists
    result = Glob(pattern="devforgeai/specs/brainstorms/{brainstorm_id}*.md")
    IF no match: FAIL "Referenced brainstorm file not found"

→ PASS ✓
```

### coherence/api_contract_error

**Method:** Confirm the incorrect field name no longer appears in the story file.

```
Step 1: Verify old field name removed
    result = Grep(pattern="{old_field_name}", path="{target_story_file}")
    IF match found: FAIL "Old API field name '{old_field_name}' still present"

Step 2: Verify new field name present
    result = Grep(pattern="{new_field_name}", path="{target_story_file}")
    IF no match: FAIL "New API field name '{new_field_name}' not found"

→ Both pass: PASS ✓
```

### coherence/naming_inconsistency

**Method:** Confirm the old artifact name no longer appears in the story file.

```
Step 1: Verify old name removed
    result = Grep(pattern="{old_artifact_name}", path="{target_story_file}")
    IF match found: FAIL "Old artifact name '{old_artifact_name}' still present"

Step 2: Verify new name present
    result = Grep(pattern="{new_artifact_name}", path="{target_story_file}")
    IF no match: FAIL "New artifact name '{new_artifact_name}' not found"

→ Both pass: PASS ✓
```

### coherence/schema_mismatch

**Method:** Re-run cross-story schema validation on affected stories to confirm alignment.

```
Step 1: Re-validate schema consistency
    findings = validate_cross_story_schema(affected_stories)
    relevant = [f for f in findings if f.target_file == "{target_file}"]
    IF len(relevant) > 0: FAIL "Schema still mismatched after fix"

→ No findings: PASS ✓
```

### coherence/plan_story_drift

**Method:** Re-run plan-story drift validation for the specific spec category.

```
Step 1: Re-validate drift
    findings = validate_plan_story_drift(story, plan_file)
    relevant = [f for f in findings if f.spec_category == "{category}"]
    IF len(relevant) > 0: FAIL "Drift still present for '{category}'"

→ No findings: PASS ✓
```

### coherence/format_inconsistency

**Method:** Confirm all affected stories now use the canonical format.

```
Step 1: Verify old format removed from all stories
    FOR each affected_story in finding.Affected:
        result = Grep(pattern="{old_format_pattern}", path="{story_file}")
        IF match found: FAIL "Old format still present in {affected_story}"

Step 2: Verify new format present
    FOR each affected_story in finding.Affected:
        result = Grep(pattern="{new_format_pattern}", path="{story_file}")
        IF no match: FAIL "New format not found in {affected_story}"

→ All pass: PASS ✓
```

### coherence/instruction_contradiction

**Method:** Confirm contradictory instruction resolved — only one placement remains.

```
Step 1: Extract placement instructions from both stories
    placements = extract_placement_instructions(story_A, story_B)
    unique_placements = set(placements)
    IF len(unique_placements) > 1: FAIL "Contradiction still exists"

→ Single placement: PASS ✓
```

### coherence/dependency_assumption_mismatch

**Method:** Re-run dependency assumption validation on affected story pair.

```
Step 1: Re-validate assumptions
    findings = validate_dependency_assumptions(affected_stories)
    relevant = [f for f in findings if f.affected == [story_id, dep_id]]
    IF len(relevant) > 0: FAIL "Assumption mismatch still present"

→ No findings: PASS ✓
```

---

## Failure Handling

When verification fails for any fix:

### Feedback Loop Protocol

```
retry_count = 0
MAX_RETRIES = 2

WHILE verification fails AND retry_count < MAX_RETRIES:
    AskUserQuestion:
        Question: "Verification failed for {finding_id}: {error}. How to proceed?"
        Header: "Fix Failed"
        Options:
            - label: "Retry fix"
              description: "Re-apply the fix and verify again ({MAX_RETRIES - retry_count} retries remaining)"
            - label: "Try manual approach"
              description: "I'll provide the correct edit parameters"
            - label: "Defer"
              description: "Mark as AUDIT-DEFERRED, fix in a later session"

    IF "Retry fix":
        Re-apply the fix procedure
        Re-run verification
        retry_count += 1

    IF "Try manual approach":
        Prompt user for correct old_string and new_string
        Apply user-provided edit
        Run verification
        BREAK

    IF "Defer":
        Edit target file to add: <!-- AUDIT-DEFERRED: {finding_id} - Verification failed: {error} -->
        Mark fix as "deferred"
        BREAK

IF retry_count >= MAX_RETRIES AND still failing:
    Display: "Fix for {finding_id} failed after {MAX_RETRIES} retries."
    Mark fix as "failed"
```

### Never Fail Silently

- NEVER mark a fix as "applied" if verification fails
- ALWAYS report the specific verification error message
- ALWAYS offer the user a choice: retry, manual, or defer
- Deferred fixes are tracked with AUDIT-DEFERRED markers in the file

---

## Verification Report Format

After all verifications complete, produce a summary:

```
### Verification Results

| Finding | Fix Status | Verification | Error |
|---------|-----------|-------------|-------|
| F-002 | applied | ✓ PASS | — |
| F-003 | applied | ✓ PASS | — |
| F-001 | applied | ✓ PASS | — |
| F-004 | deferred | — | Deferred by user |

**Verified:** {count_passed}/{count_total} fixes passed verification
```

This summary is included in the Phase 5 fix report.
