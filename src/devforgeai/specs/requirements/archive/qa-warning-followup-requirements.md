# QA Warning Follow-up System - Requirements Specification

**Version:** 1.0
**Date:** 2026-01-30
**Status:** Approved
**Author:** DevForgeAI Ideation
**Complexity Score:** 28/60 (Tier 2: Moderate)
**Epic Reference:** EPIC-054
**Brainstorm Reference:** BRAINSTORM-008

---

## 1. Project Overview

### 1.1 Project Context
**Type:** Brownfield (Framework Enhancement)
**Domain:** Developer Tooling / Quality Assurance
**Timeline:** 4 weeks (2 sprints)
**Team:** Solo developer (Framework maintainer)

### 1.2 Problem Statement

DevForgeAI users experience **lost QA warnings** because **gaps.json only captures blocking failures**, resulting in **untracked technical debt** that accumulates silently until discovered in post-hoc report reviews.

**Evidence from Discovery:**
- 3 of 5 analyzed QA reports had PASS WITH WARNINGS
- All warnings required manual review to discover
- No structured data exists for remediation workflow

**Specific Pain Points:**
1. God Module warnings lost (STORY-008 had 1098-line watcher.rs, no follow-up created)
2. Security recommendations forgotten (STORY-007 had DoS prevention recommendations, not tracked)
3. Manual story creation required (user must read reports and manually create follow-up stories)
4. No aggregation (can't see all warnings across multiple stories in one view)

### 1.3 Solution Overview

Extend the gaps.json schema to include non-blocking warnings with a `blocking: boolean` field, enabling unified tracking and automated follow-up story creation.

**Key Changes:**
1. gaps.json generated for ALL QA results (not just failures)
2. `blocking: boolean` field distinguishes severity
3. `/review-qa-reports` shows all gaps by default
4. Advisory stories clearly marked

### 1.4 Success Criteria

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| Warning capture rate | 0% | 100% | gaps.json generation for PASS WITH WARNINGS |
| Manual discovery effort | 100% | 0% | `/review-qa-reports` shows all automatically |
| Advisory story clarity | N/A | 100% | `[ADVISORY]` prefix + frontmatter flag |
| Backward compatibility | N/A | 100% | Existing gaps.json files work unchanged |

---

## 2. User Roles & Personas

### 2.1 Primary Users

| Role | Description | Count |
|------|-------------|-------|
| Framework Developer | Uses DevForgeAI to build software | Primary |
| Framework Maintainer | Develops DevForgeAI itself | Secondary |

### 2.2 User Personas

**Persona 1: Solo Developer (Bryan)**
- **Role:** Developer using DevForgeAI for project development
- **Goals:** Track all QA findings, minimize manual work
- **Needs:** Automated warning capture, clear follow-up workflow
- **Pain Points:** Warnings get lost, must manually review reports

**Persona 2: Framework Maintainer (DevForgeAI Team)**
- **Role:** Develops and maintains the DevForgeAI framework
- **Goals:** Framework completeness, user satisfaction
- **Needs:** Backward compatible changes, clean implementation
- **Pain Points:** User complaints about lost warnings

---

## 3. Functional Requirements

### 3.1 User Stories

| ID | User Story | Priority | Points |
|----|------------|----------|--------|
| FR-01 | As a developer, I want gaps.json generated for PASS WITH WARNINGS results, so that warnings are persisted for follow-up | Must Have | 5 |
| FR-02 | As a developer, I want a `blocking: boolean` field in gaps.json, so that I can distinguish failures from advisories | Must Have | 3 |
| FR-03 | As a developer, I want `/review-qa-reports` to show all gaps by default, so that I see the full picture | Must Have | 5 |
| FR-04 | As a developer, I want to filter gaps by `--blocking-only`, so that I can focus on blockers when needed | Must Have | 3 |
| FR-05 | As a developer, I want advisory stories marked with `[ADVISORY]` prefix and `advisory: true` frontmatter, so that they're clearly identified | Should Have | 5 |

### 3.2 Feature Requirements

#### Feature 1: Schema Extension

**FR-02: Extend gaps.json schema with `blocking` field**

**Current Schema:**
```json
{
  "story_id": "STORY-XXX",
  "gaps": [
    {
      "id": "GAP-001",
      "severity": "CRITICAL",
      "category": "coverage",
      "description": "Test coverage below threshold",
      "file": "src/module.py",
      "line": 42
    }
  ]
}
```

**Proposed Schema:**
```json
{
  "story_id": "STORY-XXX",
  "gaps": [
    {
      "id": "GAP-001",
      "severity": "HIGH",
      "category": "anti-pattern",
      "description": "God Module violation (1098 lines > 500 threshold)",
      "file": "src/watcher.rs",
      "line": 1,
      "blocking": false  // NEW FIELD
    }
  ]
}
```

**Validation Rules:**
- `blocking` field is optional (default: `true` if missing)
- `blocking: true` = CRITICAL/HIGH blocking violations
- `blocking: false` = Advisory warnings (HIGH/MEDIUM/LOW)

---

#### Feature 2: Gap Generation for Warnings

**FR-01: Generate gaps.json for PASS WITH WARNINGS**

**Trigger:** QA validation completes with PASS WITH WARNINGS result

**Behavior:**
```python
IF qa_result == "PASS WITH WARNINGS":
    gaps = extract_warnings(qa_report)
    FOR each warning in gaps:
        warning.blocking = False
    write_gaps_json(story_id, gaps)
```

**Severity Mapping:**
| QA Finding | Blocking? | Included? |
|------------|-----------|-----------|
| CRITICAL violation | Yes | Yes (always) |
| HIGH violation (blocking) | Yes | Yes (always) |
| HIGH warning (non-blocking) | No | Yes |
| MEDIUM warning | No | Yes |
| LOW warning | No | Yes |

---

#### Feature 3: Review Command Enhancement

**FR-03: Update `/review-qa-reports` default to show all**

**Current Behavior:**
- Shows only blocking gaps (gaps.json with implicit `blocking: true`)

**New Default Behavior:**
- Shows ALL gaps (blocking + warnings)
- Clear visual distinction between blocking and advisory

**Display Format:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  QA Report Review: 3 stories, 8 gaps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STORY-008: 3 gaps
  🔴 [BLOCKING] GAP-001: Test coverage below 95% threshold
  🟡 [ADVISORY] GAP-002: God Module (1098 lines > 500)
  🟡 [ADVISORY] GAP-003: Security hardening recommendation

STORY-007: 2 gaps
  🟡 [ADVISORY] GAP-004: DoS prevention recommendation
  🟡 [ADVISORY] GAP-005: Error handling improvement
```

**FR-04: Add `--blocking-only` filter flag**

**Usage:**
```bash
/review-qa-reports --blocking-only
```

**Behavior:**
- Filters to show only `blocking: true` gaps
- Matches legacy behavior for users who prefer focused view

---

#### Feature 4: Advisory Story Creation

**FR-05: Create advisory stories with `[ADVISORY]` prefix**

**Story Title Format:**
```
[ADVISORY] STORY-XXX-address-god-module-in-watcher-rs.story.md
```

**Story Frontmatter Addition:**
```yaml
---
id: STORY-XXX
title: "[ADVISORY] Address God Module in watcher.rs"
advisory: true  # NEW FIELD
source_gap: GAP-002
source_story: STORY-008
priority: low
---
```

**Auto-Creation Behavior:**
- Optional (user must enable with `--auto-create-advisory`)
- Groups related warnings into single story
- Links back to source story and gap

---

## 4. Data Requirements

### 4.1 Data Model

#### Entity: gaps.json

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| story_id | string | Yes | Source story ID |
| created | datetime | Yes | When gaps were detected |
| qa_result | string | Yes | FAILED, PASS WITH WARNINGS |
| gaps | array | Yes | List of gap objects |

#### Entity: Gap Object

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| id | string | Yes | - | Unique gap identifier |
| severity | enum | Yes | - | CRITICAL, HIGH, MEDIUM, LOW |
| category | string | Yes | - | coverage, anti-pattern, security, etc. |
| description | string | Yes | - | Human-readable description |
| file | string | No | - | Affected file path |
| line | integer | No | - | Affected line number |
| blocking | boolean | No | true | Whether gap blocks QA approval |

#### Entity: Story Frontmatter Extension

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| advisory | boolean | No | false | Story is advisory (non-blocking) |
| source_gap | string | No | - | Gap ID that created this story |
| source_story | string | No | - | Story where gap was found |

### 4.2 Data Constraints

- `blocking` field defaults to `true` for backward compatibility
- Existing gaps.json files without `blocking` field continue to work
- `advisory: true` stories should have lower default priority

---

## 5. Integration Requirements

### 5.1 Internal Components

| Component | Change Required | Impact |
|-----------|-----------------|--------|
| devforgeai-qa/SKILL.md | Generate gaps.json for PASS WITH WARNINGS | Medium |
| devforgeai-qa-remediation/SKILL.md | Handle `blocking: false` gaps | Low |
| /review-qa-reports command | New default, filter flag | Medium |
| Story template | Advisory frontmatter | Low |

### 5.2 File Locations

| Artifact | Path |
|----------|------|
| gaps.json files | `devforgeai/qa/reports/{STORY-ID}-gaps.json` |
| Story files | `devforgeai/specs/Stories/STORY-XXX-*.story.md` |
| QA skill | `.claude/skills/devforgeai-qa/SKILL.md` |
| Remediation skill | `.claude/skills/devforgeai-qa-remediation/SKILL.md` |
| Review command | `.claude/commands/review-qa-reports.md` |

---

## 6. Non-Functional Requirements

### 6.1 Performance
- Gap generation should add <1 second to QA workflow
- `/review-qa-reports` should complete in <5 seconds for 100 stories

### 6.2 Backward Compatibility
- **CRITICAL:** Existing gaps.json files must work unchanged
- Missing `blocking` field defaults to `true`
- Existing `/review-qa-reports` workflows continue to function

### 6.3 Usability
- Clear visual distinction between blocking and advisory gaps
- Consistent prefix `[ADVISORY]` for easy scanning
- Filter flags for focused workflows

---

## 7. Complexity Assessment

**Total Score:** 28/60
**Architecture Tier:** Tier 2: Moderate Application

### Score Breakdown

| Dimension | Score | Max | Assessment |
|-----------|-------|-----|------------|
| Functional | 12 | 20 | 1 role, 2 entities, 0 external integrations, linear workflow |
| Technical | 9 | 20 | Low data volume, single user, no real-time |
| Team/Org | 2 | 10 | Solo developer, no distribution |
| Non-Functional | 5 | 10 | No performance targets, backward compat required |

### Architecture Tier Recommendation

**Tier 2: Moderate Application**

Appropriate because:
- Multiple skill/command modifications required
- Schema evolution needs backward compatibility
- Testing across existing and new workflows
- Integration testing required

---

## 8. Feasibility Analysis

### 8.1 Technical Feasibility: ✅ FEASIBLE

| Factor | Assessment | Status |
|--------|------------|--------|
| Technology | Uses existing JSON schema patterns | ✅ |
| Complexity | Extends existing workflow, no new concepts | ✅ |
| Integration | Builds on existing QA and remediation skills | ✅ |
| Testing | Standard unit/integration tests applicable | ✅ |

### 8.2 Business Feasibility: ✅ FEASIBLE

| Factor | Assessment |
|--------|------------|
| Value | HIGH - Eliminates silent technical debt accumulation |
| Effort | 21 story points (~2 sprints) |
| ROI | High value / moderate effort = Good ROI |

### 8.3 Resource Feasibility: ✅ FEASIBLE

| Factor | Assessment |
|--------|------------|
| Developer capacity | Solo developer available |
| Skills required | Markdown, JSON schema, Claude Code skills |
| Learning curve | None - uses existing patterns |

### 8.4 Risk Register

| Risk | Category | Prob | Impact | Severity | Mitigation |
|------|----------|------|--------|----------|------------|
| R1: Backward compatibility break | Technical | Low | High | MEDIUM | Default `blocking: true` for missing field |
| R2: Default change confusion | Business | Medium | Low | LOW | Document clearly in changelog |
| R3: Advisory story noise | Business | Low | Medium | LOW | Optional auto-create flag |

---

## 9. Constraints & Assumptions

### 9.1 Technical Constraints

| Constraint | Source | Impact |
|------------|--------|--------|
| Backward Compatible | BRAINSTORM-008 | gaps.json without `blocking` field defaults to `true` |
| No New Dependencies | tech-stack.md | Use existing framework patterns |
| Schema Evolution | BRAINSTORM-008 | Additive changes only |

### 9.2 Business Constraints

| Constraint | Description |
|------------|-------------|
| Timeline | 4 weeks (2 sprints) |
| Scope | Must Have features only in MVP |

### 9.3 Assumptions (Require Validation)

| ID | Assumption | Validation Approach |
|----|------------|---------------------|
| A1 | Users will create follow-up stories from warnings | Track story creation rate post-release |
| A2 | Unified file easier to maintain than separate files | Compare implementation complexity |
| A3 | Show all by default improves discovery | User feedback after release |

---

## 10. Epic Breakdown

### Epic Roadmap

```
Sprint 1 (Week 1-2): Foundation & Core
├── STORY-A: Extend gaps.json schema (3 pts)
└── STORY-B: Generate gaps.json for warnings (5 pts)

Sprint 2 (Week 3-4): Integration & Automation
├── STORY-C: Update /review-qa-reports default (5 pts)
├── STORY-D: Add --blocking-only filter (3 pts)
└── STORY-E: Advisory story creation (5 pts)
```

### Epic Summary

**EPIC-xxx: QA Warning Follow-up System**
- **Business Goal:** Eliminate silent technical debt from lost QA warnings
- **Features:** 4 features, 5 stories
- **Points:** 21 total
- **Duration:** 4 weeks

### Story Dependencies

```
STORY-A (Schema Extension)
    │
    └──► STORY-B (Gap Generation)
             │
             └──► STORY-C (Default Show All)
                      │
                      ├──► STORY-D (Blocking Filter)
                      │
                      └──► STORY-E (Advisory Stories)
```

---

## 11. Next Steps

1. **Story Creation:** Run `/create-story` for each of the 5 stories
2. **Sprint Planning:** Run `/create-sprint` to assign stories to sprints
3. **Development:** Run `/dev STORY-A` to begin implementation

### Recommended Command Sequence

```bash
# 1. Create stories (in dependency order)
/create-story "Extend gaps.json schema with blocking field" --epic=EPIC-xxx
/create-story "Generate gaps.json for PASS WITH WARNINGS" --epic=EPIC-xxx
/create-story "Update /review-qa-reports default to show all" --epic=EPIC-xxx
/create-story "Add --blocking-only filter to /review-qa-reports" --epic=EPIC-xxx
/create-story "Create advisory stories with ADVISORY prefix" --epic=EPIC-xxx

# 2. Create sprint
/create-sprint 1 --epic=EPIC-xxx

# 3. Begin development
/dev STORY-XXX
```

---

## Appendices

### A. Glossary

| Term | Definition |
|------|------------|
| gaps.json | Structured JSON file containing QA violations for remediation tracking |
| blocking | A violation that prevents QA approval (CRITICAL/HIGH severity) |
| advisory | A non-blocking warning that should be addressed in follow-up work |
| God Module | Anti-pattern where a single file exceeds 500 lines |
| PASS WITH WARNINGS | QA result where story is approved but has non-blocking issues |

### B. References

- **BRAINSTORM-008:** `devforgeai/specs/brainstorms/BRAINSTORM-008-qa-warning-followup.brainstorm.md`
- **devforgeai-qa skill:** `.claude/skills/devforgeai-qa/SKILL.md`
- **devforgeai-qa-remediation skill:** `.claude/skills/devforgeai-qa-remediation/SKILL.md`
- **anti-patterns.md:** `devforgeai/specs/context/anti-patterns.md`

### C. Open Questions

| ID | Question | Status |
|----|----------|--------|
| Q1 | Should LOW severity warnings be included? | ✅ Resolved: Yes, include all |
| Q2 | What should be the default behavior? | ✅ Resolved: Show all by default |
| Q3 | How should advisory stories be marked? | ✅ Resolved: Prefix + frontmatter |

---

**Document Version:** 1.0
**Last Updated:** 2026-01-30
**Approved By:** User (via /ideate workflow)
