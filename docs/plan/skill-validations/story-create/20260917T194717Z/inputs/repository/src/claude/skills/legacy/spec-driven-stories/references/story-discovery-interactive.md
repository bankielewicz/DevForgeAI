---
name: story-discovery-interactive
description: Interactive mode (SINGLE_STORY) flow for Phase 01 — capture feature description, generate story ID, collect metadata
version: "3.0"
---

# Story Discovery — Interactive Mode (SINGLE_STORY)

Triggered when `/create-story "feature description text"` is invoked with 10+ words.

## Frontmatter Defaults for New Stories

**Sprint field rule (no Glob required):**
- Default: `sprint: Backlog` for all new stories
- Only override if user explicitly specifies a Sprint-NN during metadata collection (Step 1.4)
- **NEVER** reverse-engineer sprint values from sibling stories via Glob

**Status field rule:**
- Always `status: Backlog` for new stories
- `/dev` will update to `In Development` when implementation begins

---

## Step 1.1: Feature Description Capture

```
IF $FEATURE_DESCRIPTION from context marker:
    Validate: >= 10 words, describes WHAT users will do (not HOW to implement)
    IF < 10 words: AskUserQuestion for more detail
ELSE:
    AskUserQuestion(
      question: "Describe the feature (minimum 10 words, describe WHAT users will do)",
      header: "Feature description",
      options: ["CRUD operation", "Authentication/Authorization", "Workflow/Process", "Reporting/Analytics"]
    )
    Then ask for detailed description of the selected type
```

---

## Step 1.2: Generate Story ID (Gap-Aware)

```
story_files = scan devforgeai/specs/Stories/STORY-*.story.md
story_numbers = extract numbers, sort

IF gaps exist in sequence:
    next_number = first gap
ELSE:
    next_number = max + 1

STORY_ID = f"STORY-{next_number:03d}"
```

---

## Step 1.3: Discover Epic Context

```
AskUserQuestion(
  question: "Which epic does this story belong to?",
  header: "Epic association",
  options: [list of EPIC-NNN from devforgeai/specs/Epics/*.epic.md] + ["None - standalone story"]
)
EPIC_ID = selection or null
```

---

## Step 1.4: Discover Sprint Context

```
AskUserQuestion(
  question: "Assign to sprint?",
  header: "Sprint",
  options: [list of Sprint-N from devforgeai/specs/Sprints/*.md] + ["Backlog"]
)
SPRINT_ID = selection or "Backlog"
```

---

## Step 1.5: Collect Story Metadata

```
# Priority
AskUserQuestion(question: "Story priority?", header: "Priority",
  options: ["Critical", "High", "Medium", "Low"])

# Story Type
AskUserQuestion(question: "Story type?", header: "Type",
  options: ["feature (full TDD)", "documentation (skip integration)", "bugfix (skip refactor)", "refactor (skip red)"])

# Story Points (Fibonacci)
AskUserQuestion(question: "Complexity estimate?", header: "Points",
  options: ["1 (trivial)", "2 (simple)", "3 (standard)", "5 (complex)", "8 (very complex)", "13 (consider splitting)"])
```

---

## Step 1.6: Collect Dependencies (Optional)

```
AskUserQuestion(question: "Dependencies on other stories?", header: "Dependencies",
  options: ["No dependencies (Recommended)", "Has dependencies"])

IF "Has dependencies":
    Ask for STORY-NNN IDs (comma-separated)
    Validate format: ^STORY-\d{3,4}$
    Warn if referenced story file not found
```

---

## Phase 01 CLI Completion

```bash
# Record all steps
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=01 --step=1.1 --project-root=.
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=01 --step=1.2 --project-root=.
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=01 --step=1.3 --project-root=.
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=01 --step=1.4 --project-root=.
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=01 --step=1.5 --project-root=.
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=01 --step=1.6 --project-root=.
devforgeai-validate phase-complete ${SESSION_ID} --workflow=stories --phase=01 --checkpoint-passed --project-root=.
```

---

## Output

Phase 01 produces:
- `$STORY_ID`: STORY-NNN format
- `$EPIC_ID`: EPIC-NNN or null
- `$SPRINT_ID`: Sprint-N or "Backlog"
- `$PRIORITY`: Critical/High/Medium/Low
- `$POINTS`: 1/2/3/5/8/13
- `$TYPE`: feature/documentation/bugfix/refactor
- `$DEPENDS_ON`: Array of STORY-IDs or []
- `$FEATURE_DESCRIPTION`: User-provided text

→ Proceed to Phase 02: Requirements Analysis
