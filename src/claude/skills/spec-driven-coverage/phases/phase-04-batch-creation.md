# Phase 04: Batch Story Creation

**Purpose:** Create stories for all detected gaps with failure isolation (BR-004). Each story creation is independent — failure on item N does not affect item N+1.

**Mode:** create only (skip this phase for validate and detect modes)

**Pre-Flight:** Verify Phase 01 completed and gap_data is available.

---

## Step 4.1: Verify Phase 01 Completion

**EXECUTE:**
Check that gap_data from Phase 01 is available in working memory.

**VERIFY:**
- gap_data object exists
- gap_data.missing_features is a non-empty array
- If missing_features is empty: Display "No gaps to create stories for" and skip to Phase 05

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=04 --step=4.1 --project-root=. 2>&1")
```

---

## Step 4.2: Load Story Quality Gates Reference

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-coverage/references/story-quality-gates.md")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-coverage/references/story-quality-gates.md")
```

This reference documents evidence verification requirements from RCA-020. All batch-created stories must include verified_violations sections with actual file paths and line numbers — no placeholders allowed.

**VERIFY:**
- File content loaded into context
- Content contains "RCA-020" and "verified_violations"

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=04 --step=4.2 --project-root=. 2>&1")
```

---

## Step 4.3: Load Business Rules Reference (BR-004)

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-coverage/references/business-rules.md")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-coverage/references/business-rules.md")
```

Review BR-004 (Batch Failure Isolation) before starting the batch loop.

**VERIFY:**
- File content loaded into context
- Content contains "BR-004" and "failure isolation"

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=04 --step=4.3 --project-root=. 2>&1")
```

---

## Step 4.4: Collect Batch Context Markers

**EXECUTE:**
Extract batch metadata from context markers set by the invoking command:

```
EPIC_ID = context["Epic ID"]
SPRINT = context["Sprint"]
PRIORITY = context["Priority"]
POINTS = context["Points"]
INDIVIDUAL_PRIORITY = context["Individual Priority"]  # true/false
INDIVIDUAL_POINTS = context["Individual Points"]      # true/false
BATCH_TOTAL = context["Batch Total"]
```

**VERIFY:**
- EPIC_ID is populated
- BATCH_TOTAL matches gap_data.missing_features.length
- SPRINT, PRIORITY, POINTS have valid values

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=04 --step=4.4 --project-root=. 2>&1")
```

---

## Step 4.5: Initialize Batch Tracking

**EXECUTE:**
```
results = {
    success: [],   # Array of {story_id, feature_title}
    failed: []     # Array of {feature_title, error}
}
index = 0

Display: ""
Display: "Creating ${gap_data.missing_features.length} stories..."
Display: ""
```

**VERIFY:**
- results.success is an empty array
- results.failed is an empty array
- index == 0

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=04 --step=4.5 --project-root=. 2>&1")
```

---

## Step 4.6: Execute Batch Creation Loop (BR-004: Failure Isolation)

**EXECUTE:**

For each gap in gap_data.missing_features, execute the following loop. Each iteration is isolated — failure on one does NOT prevent the next from executing.

```
WHILE index < gap_data.missing_features.length:
    gap = gap_data.missing_features[index]
    next_story_id = get_next_story_id()

    # Determine per-story priority/points
    gap_priority = PRIORITY if not INDIVIDUAL_PRIORITY else omit
    gap_points = POINTS if not INDIVIDUAL_POINTS else omit

    Display: "[${index + 1}/${BATCH_TOTAL}] Creating: ${gap.feature_title}"

    # Set batch context markers for spec-driven-stories skill
    **Story ID:** ${next_story_id}
    **Epic ID:** ${EPIC_ID}
    **Feature Number:** ${gap.feature_number}
    **Feature Name:** ${gap.feature_title}
    **Feature Description:** ${gap.feature_title} - ${gap.feature_description}. Implements ${EPIC_ID} Feature ${gap.feature_number}.
    **Priority:** ${gap_priority}
    **Points:** ${gap_points}
    **Sprint:** ${SPRINT}
    **Batch Mode:** true
    **Batch Index:** ${index}
    **Batch Total:** ${BATCH_TOTAL}
    **Created From:** /create-missing-stories

    TRY:
        Skill(command="spec-driven-stories")

        # Verify story file was created
        story_file = Glob(pattern="devforgeai/specs/Stories/${next_story_id}*.story.md")
        IF story_file exists:
            results.success.push({story_id: next_story_id, feature: gap.feature_title})
            Display: "  Created ${next_story_id}"
        ELSE:
            RAISE "Story file not created"

    CATCH Exception as e:
        results.failed.push({feature: gap.feature_title, error: str(e)})
        Display: "  Failed: ${e}"
        Display: "     Continuing to next story..."

    index = index + 1
```

**VERIFY:**
- index == gap_data.missing_features.length (all gaps processed)
- results.success.length + results.failed.length == BATCH_TOTAL
- Each failed item has an error message

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=04 --step=4.6 --project-root=. 2>&1")
```

---

## Phase 04 Completion

**EXECUTE:**
```
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} --phase=04 --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0 or 2 (backward compatibility)

**NEXT:** Proceed to Phase 05 (Completion Summary)
