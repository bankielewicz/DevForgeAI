---
brainstorm_id: BRAINSTORM-008
title: QA Warning Follow-up Functionality
status: Complete
confidence: HIGH
created: 2026-01-30
topic: "Should DevForgeAI provide functionality to review QA reports for follow-up on warnings?"
discovery_trigger: "8 Treelint QA reports revealed PASS WITH WARNINGS results with God Module violations and security hardening recommendations that had no follow-up mechanism"
---

## Key Files for Context

| File | Purpose |
|------|---------|
| `.claude/skills/devforgeai-qa/SKILL.md` | QA validation workflow that generates reports |
| `.claude/skills/devforgeai-qa-remediation/SKILL.md` | Gap processing and story creation skill |
| `.claude/commands/review-qa-reports.md` | Command that invokes qa-remediation skill |
| `devforgeai/qa/reports/*-gaps.json` | Structured gap files (currently FAILED only) |
| `devforgeai/specs/context/anti-patterns.md` | Defines God Module threshold (500 lines) |

## Glossary

- **Phase**: A numbered step (01-10) in the DevForgeAI development workflow
- **gaps.json**: Structured JSON file containing QA violations for remediation tracking
- **blocking**: A violation that prevents QA approval (CRITICAL/HIGH severity)
- **advisory**: A non-blocking warning that should be addressed in follow-up work
- **DoD**: Definition of Done - completion criteria for a story
- **God Module**: Anti-pattern where a single file exceeds 500 lines (per anti-patterns.md)
- **PASS WITH WARNINGS**: QA result where story is approved but has HIGH severity non-blocking issues

---

## Executive Summary

DevForgeAI's QA workflow generates comprehensive reports with warnings for issues like God Modules (>500 lines), security hardening recommendations, and code quality concerns. However, **PASS WITH WARNINGS results don't generate gaps.json files**, so the existing `/review-qa-reports` command cannot process them for follow-up. This causes warnings to be lost after story approval, accumulating as silent technical debt.

**Recommendation:** Extend the gaps.json schema to include non-blocking warnings with a `blocking: boolean` field, enabling unified tracking and automated follow-up story creation.

---

## 1. Stakeholder Analysis

### Primary Stakeholders

| Stakeholder | Role | Goals | Concerns |
|-------------|------|-------|----------|
| Solo Developer | Framework user | Track all QA findings | Manual overhead |
| Framework Maintainers | DevForgeAI development | Framework completeness | Backward compatibility |

### Secondary Stakeholders

| Stakeholder | Role | Goals | Concerns |
|-------------|------|-------|----------|
| External Project Users | Teams adopting DevForgeAI | Import reports from their projects | Integration complexity |
| Future Team Members | Potential adopters | Clear follow-up workflow | Learning curve |

### Stakeholder Consensus
- **Agreement:** All stakeholders benefit from automated warning tracking
- **Concern:** Must maintain backward compatibility with existing workflows

---

## 2. Problem Analysis

### Problem Statement

> DevForgeAI users experience **lost QA warnings** because **gaps.json only captures blocking failures**, resulting in **untracked technical debt** that accumulates silently until discovered in post-hoc report reviews.

### 5 Whys Root Cause Analysis

| Level | Question | Answer |
|-------|----------|--------|
| Why 1 | Why do QA warnings get lost? | No persistence mechanism; gaps.json only for failures; no workflow trigger |
| Why 2 | Why doesn't QA generate gaps.json for PASS WITH WARNINGS? | Original design choice - gaps.json designed for remediation of blockers |
| Why 3 | Why was gaps.json limited to blocking issues? | Remediation focus - /dev --fix needs to know exactly what blocks the story |
| Why 4 | Why isn't there a separate mechanism for warnings? | Feature not prioritized during initial framework development |
| Why 5 | Why wasn't it prioritized until now? | Discovery barrier - didn't realize warnings were accumulating without follow-up |

### Current State

```
QA Workflow (Current):
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ QA Validation│────▶│ QA Report   │────▶│ Story Status│
│   (Deep)    │     │   (.md)     │     │   Update    │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ IF FAILED:  │
                    │ gaps.json   │◀── Only blocking issues captured
                    └─────────────┘
                           │
                    ┌──────┴──────┐
                    ▼             ▼
              ┌─────────┐   ┌─────────┐
              │PASS WITH│   │ FAILED  │
              │WARNINGS │   │         │
              └─────────┘   └─────────┘
                    │             │
                    ▼             ▼
              ❌ No gaps.json  ✅ gaps.json
                 (LOST!)        (tracked)
```

### Pain Points

1. **God Module warnings lost** - STORY-008 had 1098-line watcher.rs, no follow-up created
2. **Security recommendations forgotten** - STORY-007 had DoS prevention recommendations, not tracked
3. **Manual story creation required** - User must read reports and manually create follow-up stories
4. **No aggregation** - Can't see all warnings across multiple stories in one view

### Failed Solutions History
- N/A - First attempt to address this gap

---

## 3. Opportunity Analysis

### Ideal State

```
QA Workflow (Proposed):
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ QA Validation│────▶│ QA Report   │────▶│ Story Status│
│   (Deep)    │     │   (.md)     │     │   Update    │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────────────────────┐
                    │ ALWAYS: gaps.json           │
                    │ - blocking: true (failures) │
                    │ - blocking: false (warnings)│
                    └─────────────────────────────┘
                           │
                    ┌──────┴──────┐
                    ▼             ▼
              ┌─────────┐   ┌─────────┐
              │PASS WITH│   │ FAILED  │
              │WARNINGS │   │         │
              └─────────┘   └─────────┘
                    │             │
                    ▼             ▼
              ✅ gaps.json   ✅ gaps.json
              (advisory)    (blocking)
                    │             │
                    └──────┬──────┘
                           ▼
                    ┌─────────────────┐
                    │/review-qa-reports│
                    │ --blocking-only │◀── New filter option
                    │ --include-warnings│
                    └─────────────────┘
```

### Solution Approach

**Unified gaps.json with blocking field:**
- Single file format, one source of truth
- Backward compatible - existing gaps.json files work unchanged
- New `blocking: boolean` field distinguishes severity
- `/review-qa-reports` gets new filter flags

### Technology Fit
- No new dependencies required
- Uses existing framework patterns
- Extends existing JSON schema

---

## 4. Constraints

| Constraint Type | Description | Impact |
|-----------------|-------------|--------|
| **Backward Compatible** | Existing gaps.json files must continue to work | gaps.json files without `blocking` field default to `blocking: true` |
| **No New Dependencies** | Use existing framework patterns and tools | No external packages needed |
| **Schema Evolution** | gaps.json schema must be additive | New fields optional, old files remain valid |

---

## 5. Hypotheses

| ID | Hypothesis | Validation Approach | Risk if Wrong |
|----|------------|---------------------|---------------|
| **H1** | Adding `blocking: false` gaps won't break `/review-qa-reports` | Run with mixed gaps.json, verify filtering | Remediation workflow breaks |
| **H2** | Users will create follow-up stories from warnings | Track story creation rate post-release | Feature unused |
| **H3** | Unified file easier to maintain than separate files | Compare implementation complexity | Technical debt |

**Critical Hypothesis:** H1 (Backward Compatibility) - Must validate during architecture phase

---

## 6. Prioritized Capabilities

### MoSCoW Classification

| Priority | Capability | Effort | Value |
|----------|------------|--------|-------|
| **Must Have** | Generate gaps.json for PASS WITH WARNINGS | Medium | High |
| **Must Have** | Add `blocking: boolean` field to gap schema | Low | High |
| **Must Have** | Update `/review-qa-reports` to filter by blocking | Medium | High |
| **Should Have** | Auto-create follow-up stories from warnings | Medium | Medium |
| **Could Have** | Parse existing markdown reports into gaps.json | High | Medium |
| **Won't Have** | Dashboard aggregation across stories | High | Low |

### Impact-Effort Matrix

```
HIGH IMPACT
    │
    │  [Must: Schema Change]     [Must: Generate gaps.json]
    │  Low Effort ────────────── Medium Effort
    │
    │  [Should: Auto-stories]    [Could: Parse MD]
    │  Medium Effort ─────────── High Effort
    │
LOW IMPACT
    │
    │                            [Won't: Dashboard]
    │                            High Effort
    └───────────────────────────────────────────────
                              EFFORT →
```

### Recommended Sequence

1. **Quick Win:** Add `blocking` field to gaps.json schema
2. **Core Fix:** Modify QA skill to generate gaps.json for PASS WITH WARNINGS
3. **Integration:** Update `/review-qa-reports` with `--include-warnings` flag
4. **Automation:** Add option to auto-create advisory stories

---

## 7. Evidence from Discovery

### QA Reports Analyzed

| Report | Result | Warnings | Follow-up Mechanism |
|--------|--------|----------|---------------------|
| STORY-008 | PASS WITH WARNINGS | God Module (1098 lines) | ❌ None |
| STORY-007 | PASS WITH WARNINGS | DoS prevention, security | ❌ None |
| STORY-003 | PASS WITH WARNINGS | PRAGMA validation, God Object risk | ❌ None |
| STORY-005 | PASSED | None | N/A |
| STORY-001 | PASSED | None | N/A |

### Pattern Observed
- 3 of 5 analyzed reports had PASS WITH WARNINGS
- All warnings required manual review to discover
- No structured data for remediation workflow

---

## 8. Recommended Next Steps

1. **Run `/ideate`** to transform this brainstorm into formal requirements
2. **Architecture Phase:** Design gaps.json schema extension with ADR
3. **Story Creation:** Create stories for Must Have capabilities
4. **Validation:** Test backward compatibility with existing gaps.json files

### Suggested Epic Structure

```
EPIC: QA Warning Follow-up System
├── STORY: Extend gaps.json schema with blocking field
├── STORY: Generate gaps.json for PASS WITH WARNINGS
├── STORY: Update /review-qa-reports with warning filters
└── STORY: Add auto-create option for advisory stories
```

---

## 9. Session Metadata

| Metric | Value |
|--------|-------|
| Session Duration | ~15 minutes |
| Questions Asked | 12 |
| Stakeholders Identified | 4 |
| Pain Points | 4 |
| Capabilities Prioritized | 6 |
| Confidence Level | HIGH |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-30 | Initial brainstorm session | Claude (devforgeai-brainstorming) |
