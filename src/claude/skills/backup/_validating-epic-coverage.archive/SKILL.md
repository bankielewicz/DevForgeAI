---
name: validating-epic-coverage
description: >
  **HALT — do not use. Absorbed into spec-driven-coverage (2026-03-18).**
  Use Skill(command="spec-driven-coverage") instead.
  Original: Validates epic-to-story coverage, detects gaps, formats display output, and
  orchestrates batch story creation for coverage gaps. Extracted from
  /validate-epic-coverage and /create-missing-stories commands per lean
  orchestration pattern. Delegates display formatting to
  epic-coverage-result-interpreter subagent.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(devforgeai/traceability/gap-detector.sh:*)
  - Bash(devforgeai/epic-coverage/generate-report.sh:*)
  - Task
  - Skill
model: claude-opus-4-6
---

# Validating Epic Coverage

Validate epic-to-story coverage gaps and orchestrate batch story creation.

**This skill expands inline. YOU execute each phase sequentially after invocation.**

---

## Execution Model

After invocation, read context markers to determine mode:

- **Mode: validate** — Run gap detection + coverage report + display formatting
- **Mode: detect** — Run gap detection only, return structured gap data
- **Mode: create** — Run batch story creation from provided gap data

---

## Phase 1: Gap Detection

**Purpose:** Execute gap detection scripts and collect raw coverage data.

```
# Step 1.1: Verify prerequisites
epic_files = Glob(pattern="devforgeai/specs/Epics/*.epic.md")

IF no epic files found:
    Display: "ℹ️ No epics found in devforgeai/specs/Epics/"
    Display: "To create epics, run: /create-epic"
    RETURN {status: "no_epics", gaps: []}

# Step 1.2: Run coverage report generator
IF Mode == "validate" OR Mode == "all":
    Bash(command="devforgeai/epic-coverage/generate-report.sh")
    Parse coverage statistics from output

# Step 1.3: Run gap detector
IF Epic ID provided (single epic mode):
    Bash(command="devforgeai/traceability/gap-detector.sh ${EPIC_ID}")
ELSE:
    Bash(command="devforgeai/traceability/gap-detector.sh")

# Step 1.4: Parse JSON output
gaps = parse_json_output(gap_detector_output)
```

**Edge Cases:**

```
# Empty epic (no features defined)
IF gaps.total_features == 0:
    Display: "ℹ️ No features defined in ${EPIC_ID}"
    Display: "To define features, edit: devforgeai/specs/Epics/${EPIC_ID}*.epic.md"
    Display: "Or run /ideate to generate features from a business idea."
    RETURN {status: "no_features", gaps: []}

# 100% coverage (no gaps)
IF gaps.missing_features.length == 0:
    Display: "✅ ${EPIC_ID} has 100% coverage!"
    Display: "All ${gaps.total_features} features have stories."
    RETURN {status: "full_coverage", gaps: []}
```

**Coverage Counting Rules (BR-002):**
Only stories with status >= "Dev Complete" count toward coverage.
Backlog stories show as "Planned" but don't contribute to percentage.

---

## Phase 2: Display Formatting

**Purpose:** Delegate all display output to epic-coverage-result-interpreter subagent.

```
IF Mode == "detect":
    # Return structured data only, no display
    RETURN {
        status: "gaps_found",
        epic_id: EPIC_ID,
        total_features: gaps.total_features,
        covered_features: gaps.covered_features,
        missing_features: gaps.missing_features,
        coverage_percentage: gaps.coverage_percentage
    }

# Determine display template based on context
IF EPIC_ID provided:
    template = "single-epic"
ELSE:
    template = "all-epics"

# Delegate to subagent for display formatting
Task(
    subagent_type="epic-coverage-result-interpreter",
    description="Format ${template} coverage display",
    prompt="""
    Generate coverage display using template: ${template}

    Data:
    - Epic ID: ${EPIC_ID}
    - Total features: ${gaps.total_features}
    - Covered features: ${gaps.covered_features}
    - Coverage: ${gaps.coverage_percentage}%
    - Missing features: ${JSON.stringify(gaps.missing_features)}

    Visual indicators:
    - ✅ GREEN: 100% coverage
    - ⚠️ YELLOW: 50-99% coverage
    - ❌ RED: <50% coverage

    Include actionable gap list with shell-safe /create-story commands (top 10).
    If >10 gaps, show overflow count and batch creation hint.
    """
)
```

**Shell-Safe Escaping (BR-003):**
Feature descriptions containing quotes, backticks, or `$` must be escaped
in /create-story command suggestions. Use single-quote wrapping with interior
escaping per POSIX shell conventions.

---

## Phase 3: Batch Story Creation

**Purpose:** Create stories for all detected gaps with failure isolation.

**Entry condition:** Mode == "create" with context markers from command.

```
# Step 3.1: Collect context markers
EPIC_ID = context["Epic ID"]
SPRINT = context["Sprint"]
PRIORITY = context["Priority"]
POINTS = context["Points"]
INDIVIDUAL_PRIORITY = context["Individual Priority"]
INDIVIDUAL_POINTS = context["Individual Points"]
BATCH_TOTAL = context["Batch Total"]

# Step 3.2: Re-run gap detection if needed
IF no cached gap data:
    Bash(command="devforgeai/traceability/gap-detector.sh ${EPIC_ID}")
    gaps = parse_json_output(output)

# Step 3.3: Initialize tracking
results = {success: [], failed: []}

Display: ""
Display: "🚀 Creating ${gaps.missing_features.length} stories..."
Display: ""
```

**Batch Creation Loop (BR-004: Failure Isolation):**

```
# Each story creation is isolated - failure on item N
# does NOT affect item N+1.

index = 0
WHILE index < gaps.missing_features.length:
    gap = gaps.missing_features[index]
    next_story_id = get_next_story_id()

    # Determine per-story priority/points
    # If INDIVIDUAL_PRIORITY/POINTS: story-creation skill prompts user
    gap_priority = PRIORITY if not INDIVIDUAL_PRIORITY else omit
    gap_points = POINTS if not INDIVIDUAL_POINTS else omit

    Display: "[${index + 1}/${BATCH_TOTAL}] Creating: ${gap.feature_title}"

    # Set batch context markers per story
    # All markers required by spec-driven-stories skill:
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

        IF story file exists:
            results.success.append({story_id: next_story_id, feature: gap.feature_title})
            Display: "  ✅ Created ${next_story_id}"
        ELSE:
            RAISE "Story file not created"

    CATCH Exception as e:
        results.failed.append({feature: gap.feature_title, error: str(e)})
        Display: "  ❌ Failed: ${e}"
        Display: "     Continuing to next story..."

    index = index + 1
```

**Story Quality Gates (RCA-020):**
See `references/story-quality-gates.md` for evidence verification requirements
applied to each story created during batch mode.

---

## Phase 4: Completion Summary

**Purpose:** Display batch results via subagent.

```
Task(
    subagent_type="epic-coverage-result-interpreter",
    description="Format batch completion summary",
    prompt="""
    Generate batch summary display.

    Data:
    - Success count: ${results.success.length}
    - Failed count: ${results.failed.length}
    - Success list: ${JSON.stringify(results.success)}
    - Failed list: ${JSON.stringify(results.failed)}
    - Epic ID: ${EPIC_ID}

    Include:
    - Success/fail counts
    - Per-story status (story ID + feature name)
    - Failure details with error messages
    - Recovery commands for failed stories
    - Next steps (review stories, validate coverage, start dev)
    """
)
```

---

## Business Rules

| ID | Rule | Enforcement |
|----|------|-------------|
| BR-001 | Epic ID: case-insensitive, normalized to EPIC-NNN | Command Phase 0 |
| BR-002 | Coverage: only status >= Dev Complete counts | Phase 1 gap detection |
| BR-003 | Shell-safe escaping for feature descriptions | Phase 2 display + subagent |
| BR-004 | Batch failure isolation: item N failure ≠ item N+1 | Phase 3 TRY/CATCH |

---

## Mode Router

```
READ context markers from command invocation
PROMPT_MODE = context["Prompt Mode"]  # interactive, quiet, or ci

SWITCH on Mode:
    "validate":
        Phase 1 (gap detection + report)
        IF PROMPT_MODE != "quiet" AND PROMPT_MODE != "ci":
            Phase 2 (display via subagent - interactive mode)
        ELSE:
            Phase 2 (display via subagent - quiet/CI mode, no prompts)
        RETURN structured gap data

    "detect":
        Phase 1 (gap detection only)
        RETURN structured gap data (no display)

    "create":
        Phase 1 (gap detection if not cached)
        Phase 3 (batch creation)
        Phase 4 (completion summary)
        RETURN batch results
```

---

## Performance Targets

- Single epic validation: < 500ms
- All epics (20 epics, 200 stories): < 3 seconds
- Batch story creation: ~3 seconds per story
- Batch of 10 stories: < 30 seconds total

---

## References

| File | Purpose |
|------|---------|
| `references/story-quality-gates.md` | RCA-020 evidence verification (verbatim) |

---

## Change Log

| Date | Story | Change |
|------|-------|--------|
| 2026-02-20 | STORY-457 | Created — extracted from validate-epic-coverage + create-missing-stories |

---

**Created:** 2026-02-20 (STORY-457)
**Pattern:** Lean orchestration skill (extracted business logic)
**ADR:** ADR-020 (Structural Changes Authorization)
