# EPIC-048: Technical Debt Register Automation - Requirements Specification

**Version:** 1.0
**Date:** 2026-01-20
**Status:** Approved
**Author:** DevForgeAI Ideation Skill
**Complexity Score:** 28/60 (Tier 2: Moderate)
**Source:** BRAINSTORM-006

---

## 1. Project Overview

### 1.1 Project Context

| Attribute | Value |
|-----------|-------|
| **Type** | Brownfield (Framework Enhancement) |
| **Domain** | Developer Tooling / Workflow Automation |
| **Timeline** | 1 sprint (~2 weeks) |
| **Team** | Solo framework development |
| **Estimated Effort** | 12 story points |

### 1.2 Problem Statement

**Developers** experience **lost technical debt tracking** because **QA-discovered gaps have no automation hook**, resulting in **incomplete debt registers and compounding technical debt**.

**Evidence (from BRAINSTORM-006):**
- User reviewed STORY-002, STORY-003, STORY-004 acceptance criteria against source code
- Claude identified schema gaps, missing columns, unimplemented features
- User had to MANUALLY ask Claude to update the register
- Register document claims "auto-updated by devforgeai-development skill" but this is FALSE

**Root Cause Analysis:**
1. `/dev` Phase 06 has pseudocode for register update but only triggers on rare "Blocked by:" code path
2. `/qa` workflow has NO code path to update the register at all
3. The "auto-update" claim in register header is aspirational, not actual

### 1.3 Solution Overview

Implement true automation for technical debt capture:

1. **Standardize register format** - YAML frontmatter + structured markdown for machine parsing
2. **Fix /dev automation** - Unconditional register update on ALL user-approved deferrals
3. **Add /qa automation** - Hook triggers when AC verification finds gaps
4. **Enable remediation workflow** - Prompt to create follow-up stories from debt items
5. **Prevent debt compounding** - Threshold-based alerts and blocking

### 1.4 Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| /dev Phase 06 deferrals auto-added | 100% | Test with sample deferrals |
| /qa gaps auto-prompted | 100% | Test with AC verification |
| Threshold alerts functional | 5/10/15 triggers | Test with debt count simulation |
| Blocking at 15 items | Enforced | Test prevents new feature work |

---

## 2. User Roles & Personas

### 2.1 Primary Users

| Role | Description | Usage Frequency |
|------|-------------|-----------------|
| Developer | Uses /dev and /qa workflows | Daily |
| Claude AI | Executes workflows, updates register | Per workflow invocation |
| Framework Maintainer | Reviews debt trends, creates remediation stories | Weekly |

### 2.2 User Personas

**Persona 1: Solo Developer (Bryan)**
- **Role:** Primary DevForgeAI user
- **Goals:** Zero manual tracking, automated debt capture
- **Needs:** Clear prompts, easy story creation from debt
- **Pain Points:** Forgetting to add debt items, lost context between sessions

**Persona 2: Claude AI Agent**
- **Role:** Workflow executor
- **Goals:** Clear triggers for register updates, unambiguous rules
- **Needs:** Structured format for reliable parsing
- **Pain Points:** Pseudocode that doesn't execute, ambiguous conditions

**Persona 3: Future Maintainer**
- **Role:** Inherits codebase
- **Goals:** Understand debt history, prioritize remediation
- **Needs:** Complete debt records with timestamps and sources
- **Pain Points:** Incomplete or inconsistent debt tracking

---

## 3. Functional Requirements

### 3.1 User Stories

#### FR-01: Register Format Standardization

**As a** framework maintainer,
**I want** the technical-debt-register.md to use YAML frontmatter with structured item format,
**So that** automation can reliably parse, query, and update debt items.

**Acceptance Criteria:**
- AC1: YAML frontmatter contains `analytics` section with counts (total_open, by_type, by_priority, by_source)
- AC2: YAML frontmatter contains `thresholds` section (warning_count: 5, critical_count: 10, blocking_count: 15)
- AC3: Each debt item uses structured table format with fields: ID, Date Added, Source, Type, Priority, Status, Resolution Target, Estimated Effort, Follow-up Story
- AC4: Existing 5 debt items migrated to new format
- AC5: technical-debt-analyzer subagent updated to parse YAML frontmatter

#### FR-02: /dev Phase 06 Unconditional Update

**As a** developer,
**I want** ALL user-approved deferrals to auto-add to the register,
**So that** no debt is lost during development workflows.

**Acceptance Criteria:**
- AC1: When user selects "Keep deferred" in Phase 06 Step 6, debt item is added to register
- AC2: Debt item uses new YAML format from FR-01
- AC3: Source field is set to "dev_phase_06"
- AC4: Analytics counters in YAML frontmatter are updated
- AC5: No user prompt required (unconditional addition after approval)

#### FR-03: Post-QA Debt Detection Hook

**As a** developer,
**I want** QA-discovered AC gaps to auto-prompt for register addition,
**So that** spec deviations found during QA become tracked debt.

**Acceptance Criteria:**
- AC1: Hook triggers when AC verification shows PARTIAL or NOT_IMPLEMENTED status
- AC2: User prompted via AskUserQuestion: "Add this gap to technical debt register?"
- AC3: If user confirms, debt item added with source="qa_discovery"
- AC4: Hook integrates with /qa Phase 3 (report generation)
- AC5: Hook can be disabled via configuration (opt-out)

#### FR-04: Remediation Story Automation

**As a** developer,
**I want** to be prompted to create a remediation story when debt is added,
**So that** debt items get scheduled for resolution.

**Acceptance Criteria:**
- AC1: After ANY debt item is added, AskUserQuestion prompts: "Create remediation story for {DEBT-ID}?"
- AC2: If user confirms, /create-story is invoked with pre-filled data from debt item
- AC3: Created story is linked back to debt item (Follow-up Story field)
- AC4: Behavior is "always ask" (configurable to "auto-create" or "never" in future)

#### FR-05: Threshold-Based Alerts

**As a** developer,
**I want** warnings when debt count exceeds thresholds,
**So that** debt compounding is prevented.

**Acceptance Criteria:**
- AC1: Warning displayed when total_open >= thresholds.warning_count (default: 5)
- AC2: Critical warning displayed when total_open >= thresholds.critical_count (default: 10)
- AC3: Blocking enforcement when total_open >= thresholds.blocking_count (default: 15)
- AC4: Blocking prevents /dev from starting new feature work until debt reduced
- AC5: Thresholds are configurable in YAML frontmatter

#### FR-06: /review-qa-reports Extension (COULD HAVE)

**As a** developer,
**I want** --add-to-debt and --create-stories flags on /review-qa-reports,
**So that** I can batch-process QA findings into debt items and stories.

**Acceptance Criteria:**
- AC1: `--add-to-debt` flag adds all gaps to register (with confirmation)
- AC2: `--create-stories` flag creates remediation stories for selected gaps
- AC3: Both flags work together: add to debt then create stories

### 3.2 Features Breakdown

| Feature | Stories | Priority | Effort |
|---------|---------|----------|--------|
| F1: Register Format | FR-01 | MUST (Foundation) | 3 pts |
| F2: /dev Automation | FR-02 | MUST | 2 pts |
| F3: QA Hook | FR-03 | MUST | 2 pts |
| F4: Story Automation | FR-04 | MUST | 3 pts |
| F5: Threshold Alerts | FR-05 | SHOULD | 1 pt |
| F6: Command Extension | FR-06 | COULD | 1 pt |

---

## 4. Data Requirements

### 4.1 Data Model

#### Entity: Technical Debt Register (v2.0)

**File:** `devforgeai/technical-debt-register.md`

**YAML Frontmatter Schema:**

```yaml
---
id: "DEBT-REGISTER"
version: "2.0"
last_updated: "2026-01-20T14:30:00Z"
last_analyzed: "2026-01-20T14:30:00Z"

analytics:
  total_open: 5          # Count of open items
  total_in_progress: 0   # Count of in-progress items
  total_resolved: 0      # Count of resolved items
  average_age_days: 4    # Average age of open items
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
    dev_phase_06: 0      # From /dev deferrals
    qa_discovery: 5      # From /qa verification

thresholds:
  warning_count: 5       # Display warning
  critical_count: 10     # Display critical warning
  blocking_count: 15     # Block new feature work
  stale_days: 90         # Flag items older than this

related_epics: []
related_adrs: []
---
```

#### Entity: Debt Item (DEBT-XXX)

**Structured Table Format:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ID | string | Yes | Format: DEBT-NNN (e.g., DEBT-001) |
| Date Added | date | Yes | ISO 8601 date (YYYY-MM-DD) |
| Source | enum | Yes | dev_phase_06 \| qa_discovery |
| Type | enum | Yes | story_split \| scope_change \| external_blocker |
| Priority | enum | Yes | high \| medium \| low |
| Status | enum | Yes | open \| in_progress \| resolved |
| Resolution Target | string | No | Sprint or story reference |
| Estimated Effort | string | No | Story points or T-shirt size |
| Follow-up Story | string | No | STORY-XXX reference |
| Description | text | Yes | What was deferred/missed |
| Impact | text | No | Business/technical impact |

### 4.2 Data Constraints

| Constraint | Rule |
|------------|------|
| ID Uniqueness | DEBT-XXX must be unique across register |
| ID Sequence | Next ID = max(existing IDs) + 1 |
| Source Validation | Must be dev_phase_06 or qa_discovery |
| Priority Validation | Must be high, medium, or low |
| Status Validation | Must be open, in_progress, or resolved |
| Date Format | Must be YYYY-MM-DD |

### 4.3 Data Relationships

```
DEBT-XXX ──────────────> STORY-XXX (Follow-up Story)
    │
    └──────────────────> Source (dev_phase_06 | qa_discovery)

EPIC-XXX <────────────── DEBT-REGISTER (related_epics)

Analytics <────────────── DEBT-XXX[] (aggregation)
```

---

## 5. Integration Requirements

### 5.1 Internal Integrations

| Integration | Direction | Purpose |
|-------------|-----------|---------|
| /dev Phase 06 | Skill → Register | Add deferrals to register |
| /qa Phase 3 | Skill → Hook → Register | Add AC gaps to register |
| /create-story | Register → Command | Create remediation stories |
| technical-debt-analyzer | Subagent ← Register | Parse YAML, analyze trends |
| /review-qa-reports | Command → Register | Batch add gaps |

### 5.2 Hook Configuration

**New Hook: post-qa-debt-detection**

```yaml
# .claude/hooks.yaml (or inline in /qa skill)
hooks:
  post-qa-debt-detection:
    trigger: "qa-validation-complete"
    condition: "gaps_found > 0"
    action: "prompt-debt-addition"
    parameters:
      source: "qa_discovery"
      auto_create_story: "ask"  # ask | always | never
```

### 5.3 File Modification Points

| File | Modification | Story |
|------|--------------|-------|
| `devforgeai/technical-debt-register.md` | Convert to v2.0 format | FR-01 |
| `.claude/skills/devforgeai-development/references/phase-06-deferral-challenge.md` | Add unconditional update | FR-02 |
| `.claude/skills/devforgeai-qa/SKILL.md` | Add hook invocation at Phase 3 | FR-03 |
| `.claude/agents/technical-debt-analyzer.md` | Update to parse YAML | FR-01 |
| `.claude/commands/review-qa-reports.md` | Add flags | FR-06 |

---

## 6. Non-Functional Requirements

### 6.1 Performance

| Metric | Target | Rationale |
|--------|--------|-----------|
| Hook execution overhead | <500ms | Minimal impact on /qa workflow |
| Register parsing | <100ms for <100 items | Responsive debt queries |
| Analytics update | <200ms | Real-time counter updates |

### 6.2 Security

| Requirement | Implementation |
|-------------|----------------|
| No sensitive data | Debt register contains no secrets |
| User confirmation | All additions require explicit approval |
| Audit trail | Date Added and Source fields track origin |

### 6.3 Scalability

| Metric | Target |
|--------|--------|
| Max debt items | 100 items (performance tested) |
| Large register handling | Lazy loading via Grep for >50 items |

### 6.4 Availability

| Requirement | Implementation |
|-------------|----------------|
| Atomic updates | Write full file (no partial updates) |
| Backup on modify | Create .backup before write |
| Graceful degradation | Manual fallback if hook fails |

---

## 7. Complexity Assessment

### 7.1 Score Breakdown

| Dimension | Score | Max | Notes |
|-----------|-------|-----|-------|
| Functional | 12 | 20 | 2 roles, 3 entities, 3 integrations, branching workflow |
| Technical | 8 | 20 | Low data volume, single user, no real-time |
| Team/Org | 5 | 10 | Solo development, co-located |
| NFR | 3 | 10 | Moderate performance, no compliance |
| **Total** | **28** | **60** | |

### 7.2 Architecture Tier

**Tier 2: Moderate Application** (Score 16-30)

- **Pattern:** Hook-based event system
- **Layers:** Command → Skill → Hook → File
- **Database:** File-based (Markdown with YAML)
- **Deployment:** In-place file updates

### 7.3 Technology Recommendations

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Format | YAML + Markdown | Human-readable, machine-parseable |
| Parsing | Grep patterns | Native Claude Code tool |
| Updates | Read/Edit/Write tools | Constitutional compliance |
| Automation | Hook system | Existing framework pattern |

---

## 8. Feasibility Analysis

### 8.1 Technical Feasibility: ✅ FEASIBLE

| Factor | Assessment | Risk |
|--------|------------|------|
| Hook system exists | Uses existing pattern | Low |
| YAML parsing | Python/Claude can parse | Low |
| Workflow integration | /dev and /qa have defined locations | Low |
| File operations | Read/Write/Edit tools available | Low |

### 8.2 Business Feasibility: ✅ FEASIBLE

| Factor | Assessment |
|--------|------------|
| Budget | No external costs (framework internal) |
| Team | Solo development capacity sufficient |
| Timeline | 1 sprint achievable for 12 points |

### 8.3 Resource Feasibility: ✅ FEASIBLE

| Factor | Assessment |
|--------|------------|
| Skills | All patterns already in framework |
| Tools | Native Claude Code tools sufficient |
| Dependencies | No external dependencies |

### 8.4 Risk Register

| Risk | Prob | Impact | Severity | Mitigation |
|------|------|--------|----------|------------|
| Format migration breaks parsers | Med | Med | MEDIUM | Test with existing 5 items |
| Hook doesn't trigger | Low | High | MEDIUM | Fallback manual command |
| Blocking too aggressive | Med | Med | MEDIUM | Configurable thresholds |
| Auto-story overwhelms user | Low | Low | LOW | Always-ask behavior |

---

## 9. Constraints & Assumptions

### 9.1 Technical Constraints

| Constraint | Source | Impact |
|------------|--------|--------|
| Must use existing hook system | architecture-constraints.md | Design follows hook pattern |
| Must work in Claude Code terminal | tech-stack.md | No external services |
| Native tools only | tech-stack.md | Use Read/Write/Edit, not Bash |

### 9.2 Business Constraints

| Constraint | Impact |
|------------|--------|
| No budget for external tools | All implementation uses framework internals |
| Solo development | Sequential implementation, no parallelization |

### 9.3 Assumptions (Validated)

| Assumption | Validation | Status |
|------------|------------|--------|
| Register format can be changed | User approved v2.0 format | ✅ Validated |
| Blocking at 15 items is acceptable | User approved threshold | ✅ Validated |
| Always-ask for story creation | User approved behavior | ✅ Validated |
| Existing 5 items should migrate | User approved migration | ✅ Validated |

---

## 10. Epic Breakdown

### 10.1 Implementation Roadmap

```
Week 1-2 (Sprint 1):
════════════════════════════════════════════════════════════
Day 1-2:   STORY-A: Register Format (Foundation) - 3 pts
Day 3-4:   STORY-B: /dev Phase 06 Fix - 2 pts
           STORY-C: QA Hook (parallel) - 2 pts
Day 5-7:   STORY-D: Auto-Story Creation - 3 pts
Day 8:     STORY-E: Threshold Alerts - 1 pt
Day 9-10:  STORY-F: Command Extension - 1 pt (if time permits)
════════════════════════════════════════════════════════════
Total: 12 points in 1 sprint
```

### 10.2 Dependency Graph

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

### 10.3 Epic Summary

| Epic | Features | Points | Status |
|------|----------|--------|--------|
| EPIC-048 | 6 features | 12 pts | Planning |

---

## 11. Next Steps

1. **Story Creation:** `/create-story EPIC-048` - Decompose features into detailed stories
2. **Sprint Planning:** `/create-sprint` - Assign stories to Sprint N
3. **Development:** `/dev STORY-XXX` - Implement via TDD workflow
4. **QA Validation:** `/qa STORY-XXX` - Validate each story

---

## Appendices

### A. Glossary

| Term | Definition |
|------|------------|
| Debt Item | A tracked technical compromise requiring future resolution |
| Deferral | Decision to postpone full implementation (Phase 06) |
| AC Gap | Acceptance criteria not fully met (QA discovery) |
| Hook | Event-triggered automation point in workflow |

### B. References

- **BRAINSTORM-006:** Technical Debt Register Automation (source document)
- **EPIC-048:** Epic document
- **phase-06-deferral-challenge.md:** Current /dev Phase 06 implementation
- **devforgeai-qa/SKILL.md:** Current /qa implementation

### C. Open Questions

None - all questions resolved during ideation via AskUserQuestion.

---

**Requirements Specification Version:** 1.0
**Created:** 2026-01-20
**Last Updated:** 2026-01-20
