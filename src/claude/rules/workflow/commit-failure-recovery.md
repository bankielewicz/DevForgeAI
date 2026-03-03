# Commit Failure Recovery: DoD Validation

**Purpose:** Guide Claude through fixing DoD validation failures when `git commit` is blocked by the pre-commit hook.

**Reference:** RCA-010, RCA-014

---

## Trigger

When `git commit` returns exit code 1 with output containing ANY of:
- "VALIDATION FAILED"
- "DoD item marked [x] but missing from Implementation Notes"
- "COMMIT BLOCKED"
- "AUTONOMOUS DEFERRAL DETECTED"

---

## Recovery Workflow (MANDATORY)

### Step 1: Read the fix guide

```
Read('.claude/skills/devforgeai-development/references/dod-update-workflow.md')
```

This file contains the complete format specification, common errors, and correct examples.

### Step 2: Read the failing story file

Read the story file identified in the validator output (the `.story.md` path shown after "Validating:").

### Step 3: Diagnose the issue

<thinking>
**Reasoning steps to identify root cause:**

1. **Check for subsection nesting:**
   - Read Implementation Notes section
   - Look for `###` headers BEFORE DoD items
   - IF found → Diagnosis: "Items under subsection" (MOST COMMON)

2. **Check for missing items:**
   - Count DoD items marked `[x]` in DoD section
   - Count completion items in Implementation Notes
   - IF counts don't match → Diagnosis: "Items not added"

3. **Check for text mismatch:**
   - Extract DoD item text (without `- [x]` prefix)
   - Extract Implementation Notes item text (without `- [x]` and ` - Completed:` suffix)
   - IF texts don't match exactly → Diagnosis: "Text mismatch"

4. **Check for autonomous deferral:**
   - IF DoD shows `[x]` AND Implementation Notes shows `[ ]` AND no user approval marker
   - THEN Diagnosis: "Autonomous deferral"
</thinking>

Check these causes in order:

1. **DoD items under `###` subsection** — Items placed under `### Definition of Done Status` or similar `###` header inside `## Implementation Notes`. The `extract_section()` parser stops at the first `###` header, making items invisible to the validator.

2. **DoD items not added at all** — `## Implementation Notes` section exists but DoD completion items were never added to it.

3. **Text mismatch** — Item text in Implementation Notes doesn't exactly match the DoD section text (typos, rewording, missing backticks).

4. **Autonomous deferral** — DoD marked `[x]` but Implementation Notes shows `[ ]` without a user approval marker.

### Step 4: Fix the story file

<thinking>
**Fix strategy based on diagnosis:**

**IF diagnosis = "Items under subsection":**
1. Find `### Definition of Done Status` (or similar subsection)
2. Extract all `- [x]` items from under that subsection
3. Delete the `###` subsection header
4. Move items to appear directly under developer metadata
5. Ensure items are BEFORE any remaining `###` headers

**IF diagnosis = "Items not added":**
1. Read DoD section → Extract all `[x]` items
2. For each item: Create `- [x] {text} - Completed: {description}`
3. Insert items after developer metadata, before subsections

**IF diagnosis = "Text mismatch":**
1. Compare DoD text to Implementation Notes text character-by-character
2. Identify differences (typo, missing backticks, rewording)
3. Copy exact text from DoD section → Replace mismatched text

**IF diagnosis = "Autonomous deferral":**
1. HALT - Cannot fix autonomously
2. Report to user: "DoD marked complete but Implementation Notes shows deferred without approval"
</thinking>

- Ensure ALL DoD items marked `[x]` appear as a **flat list** directly under `## Implementation Notes`
- Items must appear AFTER developer metadata (`**Developer:**`, `**Implemented:**`), BEFORE any `###` subsections
- Format: `- [x] {exact DoD item text} - Completed: {what was done}`
- Do NOT place items under `### Definition of Done Status` or any other `###` header

### Step 5: Validate before retrying commit

<thinking>
**Validation decision logic:**

1. **Run validator:** `devforgeai-validate validate-dod {STORY_FILE}`
2. **Check exit code:**
   - IF exit code = 0 → Validation PASSED
     - THEN: Proceed to retry `git commit`
   - IF exit code ≠ 0 → Validation FAILED
     - THEN: HALT, read validator output
     - Identify remaining issues
     - Return to Step 3 (Diagnose)
3. **Never bypass:** Do NOT use `--no-verify` flag
</thinking>

```bash
devforgeai-validate validate-dod {STORY_FILE}
```

<decision>
**IF** validator exits with code 0:
  → **PROCEED:** Retry `git commit`

**IF** validator exits with non-zero code:
  → **HALT:** Read error output, return to Step 3

**NEVER:** Use `git commit --no-verify` to bypass validation
</decision>

---

## Correct Format (Validator PASSES)

```markdown
## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-12

- [x] Item 1 text - Completed: description of what was done
- [x] Item 2 text - Completed: description of what was done
- [x] Item 3 text - Completed: description of what was done

### TDD Workflow Summary   ← subsections OK AFTER items
...
```

## Wrong Format (Validator FAILS)

```markdown
## Implementation Notes

**Developer:** DevForgeAI AI Agent

### Definition of Done Status   ← PARSER STOPS HERE!
- [x] Item 1 - Completed: ...   ← NOT FOUND by validator
- [x] Item 2 - Completed: ...   ← NOT FOUND by validator
```

---

## HALT Trigger

Do NOT use `git commit --no-verify` to bypass validation. Fix the violations.
