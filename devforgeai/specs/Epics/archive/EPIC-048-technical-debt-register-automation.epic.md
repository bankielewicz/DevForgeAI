---
id: EPIC-048
title: Technical Debt Register Automation
business-value: Eliminate 100% of manual debt tracking - automate capture from /dev and /qa workflows
status: Planning
priority: High
complexity-score: 28
architecture-tier: Tier 2
created: 2026-01-20
estimated-points: 12
target-sprints: 1
source-brainstorm: BRAINSTORM-006
---

# Technical Debt Register Automation

## Business Goal

Automate the technical debt capture pipeline to eliminate manual tracking. Currently, the technical-debt-register.md claims to be "auto-updated" but requires 100% manual user intervention. This epic implements true automation.

**Success Metrics:**
- 100% of /dev Phase 06 deferrals auto-added to register
- 100% of /qa AC verification gaps auto-prompted for register addition
- Threshold alerts trigger at 5/10/15 debt items
- Blocking enforcement at 15 items prevents debt compounding

## Problem Statement

**Developers** experience **lost technical debt tracking** because **QA-discovered gaps have no automation hook**, resulting in **incomplete debt registers and compounding technical debt**.

**Root Cause:** The register update logic exists as pseudocode in Phase 06 reference but never executes unconditionally. The `/qa` workflow has NO code path to update the register.

## Features

### Feature 1: Register Format Standardization (FOUNDATION)
**Description:** Convert technical-debt-register.md to YAML frontmatter + structured markdown format, and establish hook infrastructure

**User Stories (high-level):**
1. YAML frontmatter with analytics section (counts, thresholds, source tracking)
2. Structured item format (table per DEBT-XXX entry)
3. Migration of existing 5 debt items to new format
4. technical-debt-analyzer subagent updated to parse YAML
5. Update source-tree.md v3.2 to add:
   - `.claude/hooks/` directory with naming rules
   - `.claude/skills/devforgeai-orchestration/assets/templates/` path
6. Update tech-stack.md v1.2 to add shell script exception for hooks:
   - `.claude/hooks/*.sh` - Hook scripts (exception to Markdown-only rule)
7. Create register template at documented location

**Estimated Effort:** Medium (4 points - increased for context file updates)
**Dependencies:** None - this is the foundation

### Feature 2: /dev Phase 06 Automation
**Description:** Make deferrals unconditionally update the register when user approves
**User Stories (high-level):**
1. ALL user-approved deferrals auto-added to register
2. Uses new YAML format from Feature 1
3. Source field = "dev_phase_06"

**Estimated Effort:** Small (2 points)
**Dependencies:** Feature 1

### Feature 3: QA Hook Integration
**Description:** Create post-qa-debt-detection hook for AC verification gaps
**User Stories (high-level):**
1. Gaps with PARTIAL/NOT_IMPLEMENTED status auto-prompted for addition
2. Uses new YAML format from Feature 1
3. Source field = "qa_discovery"

**Multiple Gaps Behavior:**
- When multiple gaps found: Display summary table of all gaps
- Single prompt: "Add these N gaps to technical debt register? [Y/n]"
- If confirmed: Add ALL gaps in single register update
- If declined: Skip all (user can manually add later)
- Rationale: Minimizes interruption, maintains workflow velocity

**Configuration:**
- Hook enabled by default
- Opt-out via `devforgeai/config/hooks.yaml`:
  ```yaml
  post-qa-debt-detection:
    enabled: false  # Disable for manual tracking preference
  ```

**Estimated Effort:** Small (2 points)
**Dependencies:** Feature 1

### Feature 4: Remediation Story Automation
**Description:** Offer to create follow-up stories when debt is added
**User Stories (high-level):**
1. AskUserQuestion prompt when debt item added
2. Pre-fills story from YAML debt item data
3. Links created story back to debt item

**Estimated Effort:** Medium (3 points)
**Dependencies:** Features 1, 2, 3

### Feature 5: Threshold Alerting System
**Description:** Warning and blocking alerts based on debt count
**User Stories (high-level):**
1. Warning displayed when total_open >= 5
2. Critical warning when >= 10
3. Blocking enforcement when >= 15 items

**Blocking Behavior:**
- Check: /dev pre-flight validates `total_open < blocking_threshold`
- If >= 15 items: HALT with message: "Technical debt exceeds threshold (15 items). Reduce debt before starting new work."
- Override: `--ignore-debt-threshold` flag (requires acknowledgment via AskUserQuestion)
- Exemptions: NONE - all /dev invocations blocked until debt reduced

**Override Prompt (AskUserQuestion):**
```yaml
Header: "Debt Override"
Question: "Technical debt threshold exceeded ({count} items). Override to proceed?"
Options:
  - "Yes, I accept increased technical debt risk"
  - "No, I'll reduce debt first"
```
- If override accepted: Log override in workflow state, proceed with warning
- If declined: HALT with remediation guidance (list oldest debt items)

**Estimated Effort:** Small (1 point)
**Dependencies:** Feature 1 (reads YAML thresholds)

### Feature 6: Command Extension (COULD HAVE)
**Description:** Add --add-to-debt and --create-stories flags to /review-qa-reports
**User Stories (high-level):**
1. --add-to-debt flag adds gaps to register
2. --create-stories flag creates remediation stories

**Estimated Effort:** Small (1 point)
**Dependencies:** Features 3, 4

## Requirements Summary

### Functional Requirements
- FR-01: Unconditional register update on /dev Phase 06 deferrals
- FR-02: Post-QA hook triggers when AC verification finds gaps
- FR-03: YAML frontmatter + structured markdown register format
- FR-04: Auto-create remediation stories from debt items (always ask)
- FR-05: Threshold-based alerts (5/10/15 item triggers)
- FR-06: /review-qa-reports command extension (COULD HAVE)

### Data Model
**Entities:**
- DEBT-XXX: Individual debt entries with ID, Date, Source, Type, Priority, Status, Effort, Follow-up
- Analytics: YAML frontmatter counters (total_open, by_type, by_priority, by_source)
- Thresholds: warning_count, critical_count, blocking_count, stale_days

**Relationships:**
- DEBT-XXX → STORY-XXX: Follow-up story link
- DEBT-XXX → Source: dev_phase_06 | qa_discovery

**ID Format:**
- Pattern: `DEBT-NNN` (3-digit zero-padded)
- Initial value: `DEBT-001` (if register empty)
- Sequence: `max(existing IDs) + 1`
- Example sequence: DEBT-001, DEBT-002, ..., DEBT-999

### Integration Points

**Register Location:** `devforgeai/technical-debt-register.md`
**Template:** `.claude/skills/devforgeai-orchestration/assets/templates/technical-debt-register-template.md`

1. **Hook file:** `.claude/hooks/post-qa-debt-detection.sh`
   - **Format:** Shell script (documented exception in tech-stack.md v1.2)
   - **Naming convention:** `post-{workflow}-{action}.sh`
   - Registration: `devforgeai/config/hooks.yaml`
   - Invocation: IF EXISTS check in /qa Phase 3
   - Exit codes:
     - `0` = No gaps found OR user declined to add (proceed)
     - `1` = Gaps added successfully (warn: debt count increased)
     - `2` = User cancelled OR error during update (halt)
2. **/dev skill:** Phase 06 deferral workflow (unconditional update)
3. **/qa skill:** Phase 3 report generation (triggers hook)
4. **technical-debt-analyzer subagent:** YAML parsing, auto-creates register from template if missing

**Context File Updates Required (Feature 1):**
- source-tree.md v3.2: Add `.claude/hooks/` directory and `assets/templates/` path
- tech-stack.md v1.2: Add shell script exception for hooks

### Non-Functional Requirements

**Performance:**
- Hook execution: <500ms additional workflow time
- Register parsing: <100ms for <100 items

**Availability:**
- Register updates must be atomic (no partial writes)

**Maintainability:**
- New format parseable by Grep/YAML tools

## Architecture Considerations

**Complexity Tier:** 2 (Moderate Application)

**Recommended Architecture:**
- Pattern: Hook-based event system (IF EXISTS invocation)
- Layers: Command → Skill → Hook → Register
- Database: File-based (`devforgeai/technical-debt-register.md`)
- Hook Config: `devforgeai/config/hooks.yaml`
- Deployment: In-place file updates (atomic writes)

**Technology:**
- YAML frontmatter for structured metadata
- Markdown for human-readable content
- Grep patterns for machine parsing

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Register format migration breaks existing parsers | MEDIUM | Test with existing 5 items before go-live |
| Hook system doesn't trigger correctly | MEDIUM | Add fallback manual command |
| Blocking threshold too aggressive | MEDIUM | Configurable thresholds in YAML |
| Auto-story creation overwhelms user | LOW | Always-ask behavior (configurable) |

## Dependencies

**Prerequisites:**
- None (framework internal enhancement)

**Dependents:**
- Future debt metrics dashboard
- Future debt aging alerts

## Implementation Order

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

**Critical Path:** STORY-A → STORY-B/C → STORY-D

## Stories

| Story ID | Feature | Title | Status | Points |
|----------|---------|-------|--------|--------|
| STORY-285 | Feature 1 | Register Format Standardization - Technical Debt v2.0 | Backlog | 4 |
| STORY-286 | Feature 2 | /dev Phase 06 Automation - Unconditional Register Update | Backlog | 2 |
| STORY-287 | Feature 3 | QA Hook Integration - Post-QA Technical Debt Detection | Backlog | 2 |
| STORY-288 | Feature 4 | Remediation Story Automation - Follow-up Story Creation | Backlog | 3 |
| STORY-289 | Feature 5 | Threshold Alerting System - Warning and Blocking Enforcement | Backlog | 1 |
| STORY-290 | Feature 6 | Command Extension - /review-qa-reports --add-to-debt and --create-stories | Backlog | 1 |

## Next Steps

1. **Story Creation:** ✅ All 6 features now have stories created
2. **Sprint Planning:** Run `/create-sprint` to assign stories to sprint
3. **Development:** Run `/dev STORY-XXX` to implement each story

---

**Epic Template Version:** 2.0
**Source:** BRAINSTORM-006 (Technical Debt Register Automation)
**Ideation Date:** 2026-01-20
