# EPIC-040: QA Runtime Validation Enhancements

---
id: EPIC-040
title: QA Runtime Validation Enhancements
status: Active
created: 2026-01-15
source_rca: RCA-002
complexity: Medium
priority: Critical
---

## Overview

This epic addresses critical gaps in QA validation workflow discovered through RCA-002 (QA CLI Execution and Gaps File Validation Missing). The primary issues are:

1. **CLI Execution Not Tested:** QA validation passed stories without verifying actual runtime execution (tests using CliRunner bypass entry points)
2. **gaps.json Not Created:** Mandatory gaps.json file not automatically created when QA fails outside normal workflow

## Business Value

- **Prevent False Positives:** Stories marked "QA Approved" will only pass when deliverable actually executes
- **Enable Remediation:** gaps.json automatically created enables `/dev` remediation workflow
- **Quality Assurance:** Runtime smoke tests catch entry point issues before release

## Features

### F1: Runtime Smoke Test Integration (REC-1) - CRITICAL
Add Step 1.3 Language-Agnostic Runtime Smoke Test to QA Phase 1 validation to verify deliverables can actually execute (supports Python, Node.js, .NET, Go, Java, Rust).

**Story:** STORY-266 (replaces archived STORY-257 - framework-agnostic design)

### F2: gaps.json Status Transition Link (REC-2) - HIGH
Link gaps.json creation to QA Failed status transition in atomic status update protocol.

**Story:** STORY-258

### F3: gaps.json Phase 4 Verification (REC-3) - HIGH
Add gaps.json existence verification checkpoint to Phase 4 execution summary.

**Story:** STORY-259

### F4: Deep Validation Workflow Documentation (REC-4) - MEDIUM
Document language-agnostic runtime smoke test commands for all 6 supported languages and project type detection in reference files.

**Story:** STORY-267 (replaces archived STORY-260 - covers all 6 languages: Python, Node.js, .NET, Go, Java, Rust)

### F5: Quality Gate 3 Update (REC-5) - MEDIUM
Update quality-gates.md to include runtime smoke test as Gate 3 criteria.

**Story:** STORY-261

### F6: AC Verification Checklist Real-Time Updates - HIGH
Integrate the existing ac-checklist-update-workflow.md into TDD phase reference files so AC items are automatically checked off as each phase completes.

**Story:** STORY-268

## Dependencies

- None (standalone enhancement epic)

## Success Criteria

- [ ] All 6 stories implemented and QA approved
- [ ] Runtime smoke test catches missing `__main__.py` in CLI projects
- [ ] gaps.json automatically created when QA status changes to Failed
- [ ] Documentation updated with smoke test procedures
- [ ] Quality Gate 3 includes runtime verification requirement

## Related Documents

- **Source RCA:** `devforgeai/RCA/RCA-002-qa-cli-execution-gaps-validation.md`
- **QA Skill:** `.claude/skills/devforgeai-qa/SKILL.md`
- **Quality Gates:** `.claude/rules/core/quality-gates.md`

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | Epic created from RCA-002 recommendations | /create-stories-from-rca |
| 2026-01-16 | Added F6: AC Verification Checklist Real-Time Updates (STORY-268) | /create-story |
