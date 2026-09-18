---
name: story-discovery-batch
description: Batch mode (EPIC_BATCH) flow for Phase 01 — extract features from epic, select, configure batch loop
version: "3.0"
---

# Story Discovery — Batch Mode (EPIC_BATCH)

Triggered when `/create-story EPIC-NNN` is invoked. The `story-preflight` CLI already validated the epic exists and provided `next_session_id`.

## Frontmatter Defaults for New Stories

**Sprint field rule (no Glob required):**
- If `**Sprint ID:**` context marker is set (passed from `/create-sprint`): use that value
- Otherwise: `sprint: Backlog` — ALWAYS the default for new stories
- **NEVER** reverse-engineer sprint values by searching sibling stories via Glob

**Status field rule:**
- Always `status: Backlog` for new stories created by `/create-story`
- `/dev` will update to `In Development` when implementation begins

---

## Step 0.1: Batch Mode Detection

```
IF conversation contains "**Mode:** EPIC_BATCH" AND "**Epic ID:** EPIC-":
    BATCH_MODE = "epic_batch"
    EPIC_ID = from context marker
    Display: "EPIC_BATCH mode detected for {EPIC_ID}"
    → Proceed to Step 0.2
ELSE:
    → Load story-discovery-interactive.md instead
```

---

## Step 0.2: Extract Features from Epic

**TRUST THE CLI — The `story-preflight` JSON already contains everything you need.** Do NOT re-read the epic file. Do NOT Glob for existing stories to verify coverage.

The CLI has already:
1. Parsed the epic's Stories table (canonical `## Stories` or variant `## Story Summary`)
2. Mapped each feature to its covering story (or `null` if uncovered)
3. Pre-allocated next story IDs for uncovered features
4. Scanned both active stories and archive for the true `next_story_id`

**Use the preflight JSON directly:**

```
# All data from the story-preflight CLI result (already in conversation context):
epic_features = result.epic_features              # Full feature list with coverage
features_covered = result.features_covered        # e.g., 6
features_uncovered = result.features_uncovered    # e.g., 2
uncovered_feature_ids = result.uncovered_feature_ids  # e.g., ["F-07", "F-08"]
preallocated_story_ids = result.preallocated_story_ids  # e.g., {"F-07": "STORY-628", "F-08": "STORY-629"}

Display feature table from epic_features:
  | Feature | Title | Points | Priority | Status |
  Mark covered features (covered_by != null) with the assigned STORY-NNN
  Mark uncovered features (covered_by == null) with "NEW"
```

**FORBIDDEN in Step 0.2:**
- ❌ `Read(epic_file)` — CLI already parsed it
- ❌ `Glob(pattern="devforgeai/specs/Stories/STORY-*.story.md")` — CLI already scanned disk
- ❌ `Grep(pattern="STORY-6[0-9]+", ...)` — CLI already cross-referenced
- ❌ Reverse-engineering the next story ID from existing stories — use `preallocated_story_ids`

The CLI is the source of truth. Do not verify its output.

---

## Step 0.3: Multi-Select Features

```
AskUserQuestion(
  question: "Select features to create stories for ({count} available)",
  header: "Feature selection",
  options: [feature list + "All features" option],
  multiSelect: true
)
```

---

## Step 0.4: Batch Metadata Collection

Collect defaults for the batch via 3 AskUserQuestions:

1. **Sprint**: Backlog (default) or select from available sprints
2. **Priority**: Use epic values per-feature (default) or single default
3. **Points**: Use epic values per-feature (default) or single default

---

## Step 0.4.5: Reference Loading Note

Do NOT pre-load reference files here. Each phase file has its own "Reference Loading [MANDATORY]" section that loads the specific references it needs. Pre-loading causes token limit failures on large files. Note: `acceptance-criteria-patterns.md` has been split into `acceptance-criteria-core.md`, `acceptance-criteria-domains.md`, and `acceptance-criteria-refactor.md` (conditional) — each now fits within the Read budget.

Proceed directly to Step 0.4.6.

---

## Step 0.4.6: Complete Phase 01 via CLI

```bash
# Record Phase 01 steps that batch setup covered:
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=01 --step=1.2 --project-root=.
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=01 --step=1.3 --project-root=.
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=01 --step=1.4 --project-root=.
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=01 --step=1.5 --project-root=.
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=01 --step=1.6 --project-root=.
devforgeai-validate phase-complete ${SESSION_ID} --workflow=stories --phase=01 --checkpoint-passed --project-root=.
```

---

## Step 0.5: Batch Loop

```
FOR each feature in selected_features:
    # Get next story ID from CLI (no Glob needed — CLI scans instantly)
    result = Bash(command="devforgeai-validate story-preflight ${EPIC_ID} --project-root=. --format=json 2>&1")
    story_id = parse result.next_story_id from JSON

    # --- Phase 02: Requirements Analysis ---
    devforgeai-validate phase-check ${SESSION_ID} --workflow=stories --from=01 --to=02 --project-root=.
    Invoke story-requirements-analyst subagent with feature description
    devforgeai-validate phase-record ... --step=2.1, 2.2, 2.3, 2.4
    devforgeai-validate phase-complete ... --phase=02

    # --- Phase 03: Technical Specification (INLINE) ---
    devforgeai-validate phase-check ... --from=02 --to=03
    Execute inline: evidence pre-flight, API detection, YAML v2.0 assembly, embedding mandate
    devforgeai-validate phase-record ... --step=3.1, 3.2, 3.3, 3.4, 3.5
    devforgeai-validate phase-complete ... --phase=03

    # --- Phase 04: UI Specification (INLINE, often N/A for CLI) ---
    devforgeai-validate phase-check ... --from=03 --to=04
    Determine UI applicability. Document N/A if no UI.
    devforgeai-validate phase-record ... --step=4.1, 4.2, 4.3
    devforgeai-validate phase-complete ... --phase=04

    # --- Phase 05: Story File Creation (INLINE — Write allowed by hook) ---
    devforgeai-validate phase-check ... --from=04 --to=05
    Validate output dir, load template, parse SECTION_MANIFEST, assemble, write file
    devforgeai-validate phase-record ... --step=5.1, 5.2, 5.3, 5.4, 5.5
    devforgeai-validate phase-complete ... --phase=05

    # --- Phase 06: Epic/Sprint Linking (INLINE) ---
    devforgeai-validate phase-check ... --from=05 --to=06
    Update epic file with story reference. Update sprint if assigned.
    devforgeai-validate phase-record ... --step=6.1, 6.2, 6.3
    devforgeai-validate phase-complete ... --phase=06

    # --- Phase 07: Self-Validation (INLINE) ---
    devforgeai-validate phase-check ... --from=06 --to=07
    Validate frontmatter, AC format, SECTION_MANIFEST, self-containment
    devforgeai-validate phase-record ... --step=7.1, 7.2, 7.3, 7.4
    devforgeai-validate phase-complete ... --phase=07

    # --- Reset for next story ---
    devforgeai-validate phase-init ${SESSION_ID} --workflow=stories --reset --project-root=.
```

---

## Step 0.6: Batch Summary

```
Display:
  Total Attempted: {batch_total}
  Created: {count} stories
  Failed: {count}

  Created Stories:
    - STORY-NNN: Feature Name (file path)

  Suggested Next Actions:
    - /dev STORY-NNN to implement first story
    - /create-sprint to organize into sprints
```

---

## Step 0.7: Post-Batch Structural Validation

For each story in `$BATCH_CREATED_LIST`:

```
# Check 1 (CLI-enforced, ADR-090): Required H2 sections from SECTION_MANIFEST
# Closes the prose-only structural gate via validate-story-sections --story-file
# (extension shipped by ADR-090 / closes ADR-080 §FU#4 H8-CLI). Deterministic
# Python regex replaces orchestrator-side Grep loops that were unreliable
# under token pressure for framework consumers.
cli_result = Bash(f"devforgeai-validate validate-story-sections \
    --template-file=$TEMPLATE_FILE_PATH \
    --story-file={story_path} \
    --format=json")

IF cli_result.exit_code == 1:
    parsed = json_parse(cli_result.stdout)
    Display: f"  FAIL {story_path}: missing required H2 sections {parsed.missing_sections}"
    failed_list.append({"story": story_path, "missing_sections": parsed.missing_sections})
    continue   # skip remaining checks for this story
ELIF cli_result.exit_code == 2:
    Display: f"  FAIL {story_path}: IO error during section validation"
    failed_list.append({"story": story_path, "error": "io_error"})
    continue
ELIF cli_result.exit_code == 127:
    Display: "WARNING: validate-story-sections CLI not installed — falling back to inline Grep for this batch"
    # Inline Grep fallback (preserves the pre-ADR-090 behavior on installs
    # missing the extended CLI). The Grep loop pattern matches Phase 05
    # Step 5.5's existing in-phase logic.

# Checks 2-5 (orchestrator-side, lower-impact structural):
2. Implementation Guide present for >= 5pt stories
3. Tech spec has `format_version` and `COMP-NNN` IDs
4. Frontmatter has `template_version`
5. Provenance has >= 2 `<origin>` tags for epic-linked stories
```

If any check fails: remove from created list, add to failed list with specific missing elements. Re-validation of a failed story requires re-running the per-story creation phases.

---

## Gap-Aware Story ID Generation

Story IDs are generated by the `story-preflight` CLI command (`next_story_id` in JSON response).
The CLI scans `devforgeai/specs/Stories/STORY-*.story.md` instantly — no Glob needed.
For each story in the batch, re-call the CLI to get the updated next ID (accounts for just-created stories).
