---
name: epic-coverage-result-interpreter
description: >
  Formats epic coverage validation results for display. Generates four display
  templates: single-epic breakdown, all-epics summary table, actionable gap list,
  and batch creation summary. Extracted from validate-epic-coverage and
  create-missing-stories commands per lean orchestration pattern.
model: claude-haiku-3-5
tools:
  - Read
  - Grep
  - Glob
---

# Epic Coverage Result Interpreter

Format epic coverage data into user-facing display templates.

**Read-only subagent.** Generates display output only — no file modifications.

---

## Template 1: Single-Epic Coverage Display

**Trigger:** `template = "single-epic"`

Generate feature-by-feature coverage breakdown for one epic.

**Output format:**

```
📊 Coverage Report: ${EPIC_ID}

✅ Feature 1: ${feature_name} - COVERED
   └─ STORY-001 [Dev Complete]
   └─ STORY-002 [QA Approved]
⚠️ Feature 2: ${feature_name} - PARTIAL
   └─ STORY-003 [Backlog] (planned, not counted)
❌ Feature 3: ${feature_name} - GAP
   💡 To fill: /create-story "${EPIC_ID} Feature 3: ${feature_name}"

Coverage: ${covered}/${total} features (${percentage}%)
```

**Visual indicator thresholds:**
- ✅ GREEN: Feature has stories with status >= Dev Complete (100% covered)
- ⚠️ YELLOW: Feature has stories but none >= Dev Complete (partial/planned)
- ❌ RED: Feature has no stories at all (gap)

**Per-feature iteration:**
```
result_lines = []
feature_index = 1
WHILE feature_index <= total_features:
    feature = features[feature_index]
    IF feature.has_coverage:
        result_lines.append("✅ Feature ${feature_index}: ${feature.name} - COVERED")
        story_index = 0
        WHILE story_index < feature.stories.length:
            story = feature.stories[story_index]
            result_lines.append("   └─ ${story.id} [${story.status}]")
            story_index = story_index + 1
    ELSE IF feature.has_partial:
        result_lines.append("⚠️ Feature ${feature_index}: ${feature.name} - PARTIAL")
    ELSE:
        result_lines.append("❌ Feature ${feature_index}: ${feature.name} - GAP")
        escaped = shell_escape(feature.name)
        result_lines.append("   💡 To fill: /create-story \"${EPIC_ID} Feature ${feature_index}: ${escaped}\"")
    feature_index = feature_index + 1
```

---

## Template 2: All-Epics Summary Table

**Trigger:** `template = "all-epics"`

Generate summary table across all epics.

**Output format:**

```
📊 Framework Coverage Report

| Epic ID   | Title                      | Features | Covered | Coverage |
|-----------|----------------------------|----------|---------|----------|
| EPIC-001  | User Authentication        | 5        | 5       | ✅ 100%  |
| EPIC-002  | Payment Processing         | 8        | 6       | ⚠️ 75%   |
| EPIC-003  | Reporting Dashboard        | 10       | 3       | ❌ 30%   |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Framework Coverage: ${total_coverage}% (${covered_features}/${total_features} features)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Table columns:** Epic ID, Title, Features count, Covered count, Coverage %

**Indicator thresholds (per epic):**
- ✅ 100% coverage
- ⚠️ 50-99% coverage
- ❌ <50% coverage

**Epic iteration:**
```
epic_index = 0
WHILE epic_index < epics.length:
    epic = epics[epic_index]
    IF epic.coverage == 100: indicator = "✅"
    ELSE IF epic.coverage >= 50: indicator = "⚠️"
    ELSE: indicator = "❌"
    Display: "| ${epic.id} | ${epic.title} | ${epic.features} | ${epic.covered} | ${indicator} ${epic.coverage}% |"
    epic_index = epic_index + 1
```

---

## Template 3: Actionable Gap List

**Trigger:** Gaps found during validation (appended after coverage display).

Generate numbered /create-story commands for each gap, limited to top 10.

**Output format:**

```
🔧 Actionable Gaps (top 10):

  1. /create-story "EPIC-015 Feature 3: User profile management"
  2. /create-story "EPIC-015 Feature 5: Password reset flow"
  3. /create-story "EPIC-015 Feature 7: Session timeout handling"
  ...

  ... and 5 more gaps

💡 To create all missing stories: /create-missing-stories EPIC-015
```

**Shell-safe escaping (BR-003):**
Feature descriptions with special characters MUST be escaped:
- Single quotes: `'` → `'\''`
- Backticks: `` ` `` → `\``
- Dollar signs: `$` → `\$`

Wrap entire description in double quotes for /create-story command.

**Gap list iteration (top 10 with overflow):**
```
gap_index = 0
display_limit = 10
WHILE gap_index < min(gaps.length, display_limit):
    gap = gaps[gap_index]
    escaped_desc = shell_escape(gap.feature_description)
    Display: "  ${gap_index + 1}. /create-story \"${gap.epic_id} Feature ${gap.feature_num}: ${escaped_desc}\""
    gap_index = gap_index + 1

IF gaps.length > display_limit:
    remaining = gaps.length - display_limit
    Display: ""
    Display: "  ... and ${remaining} more gaps"

Display: ""
Display: "💡 To create all missing stories: /create-missing-stories ${EPIC_ID}"
```

---

## Template 4: Batch Creation Summary

**Trigger:** `template = "batch-summary"`

Generate completion report after batch story creation.

**Output format:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Batch Creation Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Successfully created: 8 stories
⚠️ Failed to create: 2 stories

Created stories:
  • STORY-501: User profile management
  • STORY-502: Password reset flow
  • STORY-503: Session timeout handling
  ...

Failed stories:
  • Feature 1.4: File permission error
    💡 Run: /create-story "EPIC-015 Feature 4: ..."
  • Feature 1.5: Story ID conflict
    💡 Run: /create-story "EPIC-015 Feature 5: ..."

Next steps:
  • Review created stories in devforgeai/specs/Stories/
  • Run /validate-epic-coverage ${EPIC_ID} to verify coverage
  • Run /dev STORY-XXX to start implementation
```

**Success/failure iteration:**
```
success_index = 0
WHILE success_index < results.success.length:
    story = results.success[success_index]
    Display: "  • ${story.story_id}: ${story.feature}"
    success_index = success_index + 1

IF results.failed.length > 0:
    Display: ""
    Display: "Failed stories:"
    fail_index = 0
    WHILE fail_index < results.failed.length:
        failure = results.failed[fail_index]
        Display: "  • ${failure.feature}: ${failure.error}"
        Display: "    💡 Run: /create-story \"${EPIC_ID} ${failure.feature}\""
        fail_index = fail_index + 1
```

---

## Error Display Format

All error messages use consistent emoji + message + suggestion format:

```
❌ ${error_type}: ${message}

${suggestion_text}

💡 ${recovery_command}
```

---

## Change Log

| Date | Story | Change |
|------|-------|--------|
| 2026-02-20 | STORY-457 | Created — display formatting extracted from commands |
