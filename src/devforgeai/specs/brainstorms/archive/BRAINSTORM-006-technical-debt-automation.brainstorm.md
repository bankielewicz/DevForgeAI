# BRAINSTORM-006: Technical Debt Register Automation

**Session ID:** BRAINSTORM-006
**Date:** 2026-01-20
**Status:** Complete
**Confidence:** HIGH

---

## Executive Summary

The technical-debt-register.md claims to be "auto-updated by devforgeai-development skill" but technical debt discovered during QA requires MANUAL user intervention. This brainstorm explores automating the debt capture pipeline and adding "next steps" workflows to prevent debt compounding.

---

## Problem Statement

**Developers** experience **lost technical debt tracking** because **QA-discovered gaps have no automation hook**, resulting in **incomplete debt registers and compounding technical debt**.

### Evidence

From conversation log analysis (2026-01-19):
- User reviewed STORY-002, STORY-003, STORY-004 acceptance criteria against source code
- Claude identified schema gaps, missing columns, unimplemented features
- User had to MANUALLY ask Claude to update the register
- Register document claims "auto-updated" but wasn't

### Root Cause (CORRECTED - Worse Than Initially Thought)

**The technical-debt-register.md is NEVER automatically updated by ANY workflow.**

Investigation of `/dev` skill reveals:
1. **Phase 06 (Deferral Challenge):** Contains pseudocode to update register, but ONLY triggers when:
   - User selects "Update justification" AND provides "Blocked by:" text
   - User selects specific external blocker options
   - This is a **rare code path**, not automatic

2. **The register header LIES:** States "Maintained by: devforgeai-development skill (auto-updates when deferrals occur)" but no unconditional automation exists

3. **`/qa` workflow:** Has NO code path to update the register at all

**Root Cause:** The register update logic was written as pseudocode in reference documents but never implemented as unconditional automation. The "auto-update" claim is aspirational, not actual.

---

## Stakeholder Analysis

| Stakeholder | Role | Goals | Concerns |
|-------------|------|-------|----------|
| Developer | Primary User | Debt tracked automatically | Lost items, context switching |
| Claude AI | Executor | Clear triggers for updates | Ambiguous rules |
| Framework | System | Spec-driven integrity | Documentation mismatch |
| Future Maintainers | Secondary | Understand debt history | Incomplete records |

---

## Current State vs Desired State

### Current Flow (Bug - CORRECTED)

```
/dev (Phase 6 defers)    /qa (finds gaps)    User reviews    User manually asks    Register updated
        ↓                       ↓                  ↓                  ↓                   ↓
    NO auto-update         NO auto-update      User notices      User requests      Manual only
    (pseudocode only)      (no code path)      "Is this debt?"   "Add to register"  (100% manual)
```

**Reality:** NEITHER `/dev` NOR `/qa` automatically updates the register. The "auto-update" documented in the register header is false.

### Desired Flow (Fixed)

```
/dev (Phase 6 defers) → /qa (finds gaps) → AUTO: Register updated → AUTO: Next steps offered
        ↓                      ↓                     ↓                        ↓
    Auto-update           Hook triggers          Debt logged             Options:
    (works)               post-qa-debt-          with source,            - Create story
                          detection              severity                - Create epic
                                                                         - Schedule sprint
```

---

## Opportunities Identified

### O1a: Fix `/dev` Phase 06 Register Update [MUST HAVE]

**Description:** Make the existing pseudocode in Phase 06 actually execute unconditionally when deferrals are approved.

**Current State:** Pseudocode exists at lines 576-582 of `phase-06-deferral-challenge.md` but only triggers on specific "Blocked by:" user input path.

**Fix:** Add unconditional register update after ANY deferral is user-approved (Step 6, Option 2 "Keep deferred").

**Implementation Location:**
- `.claude/skills/devforgeai-development/references/phase-06-deferral-challenge.md` (fix Step 6)
- Add explicit Write() call after approval timestamp added

**Estimated Effort:** 2 points (increased to account for YAML format integration from O5)

---

### O1b: Add `post-qa-debt-detection` Hook [MUST HAVE]

**Description:** Create a hook in the `/qa` workflow that triggers when AC verification finds gaps between spec and implementation.

**Trigger Conditions:**
- AC verification shows "PARTIAL" or "NOT IMPLEMENTED" status
- Gap between spec requirement and actual code
- Coverage below thresholds (if not already blocking)

**Implementation Location:**
- `.claude/hooks/post-qa-debt-detection.md` (new hook)
- `.claude/skills/devforgeai-qa/SKILL.md` (invoke hook at Phase 3)

**Estimated Effort:** 2 points

---

### O2: Extend `/review-qa-reports` for Debt Actions [COULD HAVE]

**Description:** Add debt management options to existing command.

**New Options:**
```bash
/review-qa-reports --add-to-debt    # Add gaps to register
/review-qa-reports --create-stories # Create remediation stories
```

**Estimated Effort:** 1 point

---

### O3: Threshold-Based Alerts [SHOULD HAVE]

**Description:** When debt count exceeds thresholds, automatically suggest actions.

**Thresholds:**
- 5 items → Warning in QA output
- 10 items → Suggest debt reduction sprint
- 15 items → Block new feature work until addressed

**Implementation:** Update `technical-debt-analyzer` subagent

**Estimated Effort:** 1 point

---

### O4: Auto-Create Remediation Stories/Epic [MUST HAVE]

**Description:** When debt is added, offer to create follow-up work items.

**Workflow:**
```
Debt Item Added → AskUserQuestion: "Create remediation story?"
                         ↓
              Yes: /create-story with pre-filled data
              No: Just log to register

Debt > 5 items → AskUserQuestion: "Create remediation epic?"
                         ↓
              Yes: /create-epic grouping related debt
              No: Individual stories remain
```

**Estimated Effort:** 3 points

---

### O5: Standardize Register Format (YAML Frontmatter + Structured Markdown) [MUST HAVE]

**Description:** Redesign the technical-debt-register.md to use the same YAML frontmatter + Markdown pattern as research documents, stories, and epics. This enables machine-parseable metadata while maintaining human readability.

**Current Problem:**
- Current register is pure markdown with ad-hoc structure
- Counts are inline text that requires regex to parse
- Analysis section is unstructured prose
- No standardized entry format for automation

**Proposed Format:**

```yaml
---
id: "DEBT-REGISTER"
version: "2.0"
last_updated: "2026-01-20"
last_analyzed: "2026-01-20"

# Machine-parseable analytics
analytics:
  total_open: 5
  total_in_progress: 0
  total_resolved: 0
  average_age_days: 4
  oldest_item: "STORY-002"
  by_type:
    story_split: 0
    scope_change: 5
    external_blocker: 0
  by_priority:
    high: 1
    medium: 2
    low: 2
  by_source:
    dev_phase_06: 0
    qa_discovery: 5  # NEW - tracks QA-discovered debt

# Threshold alerts (for automated warnings)
thresholds:
  warning_count: 5
  critical_count: 10
  blocking_count: 15
  stale_days: 90

# Related documents
related_stories: []
related_epics: ["EPIC-XXX"]
related_adrs: []
---

# Technical Debt Register

## Open Debt Items

<!-- Each item follows this structured format for automation -->

### DEBT-001: STORY-002 - Imports Table Schema Missing Columns

| Field | Value |
|-------|-------|
| **Date Added** | 2026-01-13 |
| **Source** | dev_phase_06 |
| **Type** | scope_change |
| **Priority** | medium |
| **Status** | open |
| **Resolution Target** | Before STORY-003 |
| **Estimated Effort** | 2 points |
| **Follow-up** | TBD |

**Description:** Implementation simplified schema for MVP...

**Impact:** Minor - basic import tracking works...

---

### DEBT-002: ...
```

**Benefits:**
1. **YAML frontmatter** provides structured analytics for automated analysis
2. **Table format** per item enables consistent parsing
3. **Source field** tracks where debt originated (dev vs qa)
4. **Thresholds section** enables automated alerting
5. **Compatible** with existing DevForgeAI patterns (research, stories)

**Implementation Impact:**
- ALL code that reads/writes the register must be updated
- Phase 06 pseudocode → real implementation using new format
- QA hook → writes in new format
- `technical-debt-analyzer` subagent → parses YAML frontmatter

**Estimated Effort:** 3 points (includes updating all touchpoints)

---

### O6: Debt Source Tracking [INCLUDED IN O5]

**Description:** Track whether debt came from /dev (Phase 6) or /qa (AC verification).

**Rationale:** Now included in O5 as the `source` field in YAML format. Not a separate story.

---

## Prioritization

### MoSCoW

| Priority | Opportunities |
|----------|---------------|
| **MUST** | O5 (Register Format - FOUNDATION), O1a (Fix /dev), O1b (QA Hook), O4 (Auto-stories) |
| **SHOULD** | O3 (Thresholds - built into O5 format) |
| **COULD** | O2 (Extend command) |

### Recommended Implementation Order

1. **O5: Register Format** - FOUNDATION - must be done FIRST so other stories write to correct format
2. **O1a: Fix /dev Phase 06** - Update to use new format
3. **O1b: QA Hook** - Writes to new format
4. **O4: Auto-stories** - Uses new format for story creation
5. **O3: Thresholds** - Already in YAML frontmatter, just needs alerting logic
6. **O2: Command extension** - UX polish

**CRITICAL DEPENDENCY:** O5 (Register Format) must complete before O1a, O1b, O4 can be implemented.

---

## Constraints

| Constraint | Type | Mitigation |
|------------|------|------------|
| Must use existing hook system | Technical | Use `post-qa-*` pattern |
| Must work in Claude Code terminal | Technical | No external services |
| Register format v2.0 immutable after migration | Technical | Future changes require migration story |
| Existing `/review-qa-reports` exists | Technical | Extend rather than replace |

---

## Hypotheses to Validate

| ID | Hypothesis | Success Criteria | Validation Method |
|----|------------|------------------|-------------------|
| H1 | Hook catches all QA-discovered debt | 100% of AC gaps logged | Test with STORY-002-006 |
| H2 | Threshold alerts prevent compounding | Debt stays <10 avg | Monitor over 5 sprints |
| H3 | Auto-story creation is used | >80% of debt gets stories | Usage analytics |

---

## Technical Specification Preview

### New Register Format (YAML Frontmatter + Markdown)

**File:** `devforgeai/technical-debt-register.md`

```yaml
---
id: "DEBT-REGISTER"
version: "2.0"
last_updated: "2026-01-20T14:30:00Z"
last_analyzed: "2026-01-20T14:30:00Z"

analytics:
  total_open: 5
  total_in_progress: 0
  total_resolved: 0
  average_age_days: 4
  oldest_item:
    id: "DEBT-001"
    story: "STORY-002"
    age_days: 7
  by_type:
    story_split: 0
    scope_change: 5
    external_blocker: 0
  by_priority:
    high: 1
    medium: 2
    low: 2
  by_source:
    dev_phase_06: 0
    qa_discovery: 5

thresholds:
  warning_count: 5
  critical_count: 10
  blocking_count: 15
  stale_days: 90

related_epics: []
related_adrs: []
---

# Technical Debt Register

## Open Debt Items

### DEBT-001: STORY-002 - Imports Table Schema Missing Columns

| Field | Value |
|-------|-------|
| **ID** | DEBT-001 |
| **Date Added** | 2026-01-13 |
| **Source** | qa_discovery |
| **Type** | scope_change |
| **Priority** | medium |
| **Status** | open |
| **Resolution Target** | Before STORY-003 |
| **Estimated Effort** | 2 points |
| **Follow-up Story** | TBD |

**Description:** Implementation simplified schema for MVP. Technical specification defined `imported_names` (JSON array) and `is_relative` (Boolean) columns which were not implemented.

**Impact:** Minor - basic import tracking works, but dependency queries may need richer data.

---

### DEBT-002: ...
```

### New Hook: `post-qa-debt-detection`

```yaml
# .claude/hooks.yaml addition
hooks:
  post-qa-debt-detection:
    trigger: "qa-validation-complete"
    condition: "gaps_found > 0"
    action: "update-technical-debt-register"
    parameters:
      source: "qa_discovery"
      auto_create_story: "ask"  # ask | always | never
```

### Register Update Logic (Updated for YAML Format)

```python
# Pseudocode for debt update using new YAML format
def add_debt_item(gap, source):
    # 1. Read register and parse YAML frontmatter
    register = Read("devforgeai/technical-debt-register.md")
    frontmatter, body = parse_yaml_frontmatter(register)

    # 2. Generate next DEBT-ID
    existing_ids = extract_debt_ids(body)
    next_id = f"DEBT-{max(existing_ids) + 1:03d}"

    # 3. Create structured debt entry
    debt_entry = f"""
### {next_id}: {gap.story_id} - {gap.description[:50]}

| Field | Value |
|-------|-------|
| **ID** | {next_id} |
| **Date Added** | {today()} |
| **Source** | {source} |
| **Type** | {gap.type} |
| **Priority** | {map_severity_to_priority(gap.severity)} |
| **Status** | open |
| **Resolution Target** | TBD |
| **Estimated Effort** | TBD |
| **Follow-up Story** | TBD |

**Description:** {gap.description}

**Impact:** {gap.impact}

---
"""

    # 4. Update YAML analytics
    frontmatter['analytics']['total_open'] += 1
    frontmatter['analytics']['by_source'][source] += 1
    frontmatter['analytics']['by_priority'][gap.priority] += 1
    frontmatter['last_updated'] = now_iso8601()

    # 5. Insert debt entry into body
    updated_body = insert_after_marker(body, "## Open Debt Items", debt_entry)

    # 6. Write updated register
    updated_register = render_yaml_frontmatter(frontmatter) + updated_body
    Write("devforgeai/technical-debt-register.md", updated_register)

    # 7. Offer story creation
    IF config.auto_create_story == "ask":
        AskUserQuestion("Create remediation story for {next_id}?")
```

---

## Recommended Epic Structure

```
EPIC-XXX: Technical Debt Automation Enhancement
│
├── STORY-A: Standardize Register Format (YAML Frontmatter) [FOUNDATION - DO FIRST]
│   ├── AC1: YAML frontmatter with analytics section (counts, thresholds, source tracking)
│   ├── AC2: Structured item format (table per item)
│   ├── AC3: Migration of existing 5 debt items to new format
│   ├── AC4: technical-debt-analyzer updated to parse YAML
│   └── Effort: 3 points
│
├── STORY-B: Fix /dev Phase 06 unconditional register update
│   ├── AC1: ALL user-approved deferrals auto-added to register
│   ├── AC2: Uses new YAML format (depends on STORY-A)
│   ├── AC3: Source field = "dev_phase_06"
│   └── Effort: 2 points (increased due to format change)
│
├── STORY-C: Implement post-qa-debt-detection hook
│   ├── AC1: Gaps found during QA auto-added to register
│   ├── AC2: Uses new YAML format (depends on STORY-A)
│   ├── AC3: Source field = "qa_discovery"
│   └── Effort: 2 points
│
├── STORY-D: Add "create story from debt" workflow
│   ├── AC1: User offered to create story when debt added
│   ├── AC2: Pre-fills story from YAML debt item
│   └── Effort: 3 points
│
├── STORY-E: Implement threshold alerts (uses YAML thresholds)
│   ├── AC1: Warning displayed when total_open >= thresholds.warning_count
│   ├── AC2: Blocking suggestion when >= thresholds.critical_count
│   └── Effort: 1 point
│
└── STORY-F: Extend /review-qa-reports command (COULD HAVE)
    ├── AC: --add-to-debt and --create-stories flags work
    └── Effort: 1 point
```

**Total Estimated Effort:** 12-14 points

**Dependency Graph:**
```
STORY-A (Format) ─────┬──────────────────────────────────┐
                      │                                  │
                      ▼                                  ▼
              STORY-B (/dev fix)              STORY-C (QA hook)
                      │                                  │
                      └──────────┬───────────────────────┘
                                 │
                                 ▼
                      STORY-D (Auto-stories)
                                 │
                                 ▼
                      STORY-E (Thresholds)
                                 │
                                 ▼
                      STORY-F (/review-qa-reports)
```

---

## Next Steps

1. **Review** this brainstorm for accuracy
2. **Run** `/ideate` to transform into formal requirements
3. **Create** epic and stories via `/create-epic`
4. **Implement** starting with O1 (hook) as foundation

---

## Appendix: Conversation Evidence

Source: `/mnt/c/Projects/DevForgeAI2/tmp/2026-01-19-local-command-caveatcaveat-the-messages-below-w.txt`

Key excerpts showing manual intervention required:
- Line 418-506: User asks "is this technical debt?" → Claude confirms → User asks to add to register
- Line 507-637: Claude manually updates register (not automatic)
- Line 861-968: Process repeats for STORY-003

This pattern repeated for each story review, demonstrating the automation gap.

---

**Created:** 2026-01-20
**Template Version:** 1.0
