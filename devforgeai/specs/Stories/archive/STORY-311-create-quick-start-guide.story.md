---
id: STORY-311
title: Create TARGET-PROJECT-QUICK-START.md Guide
type: documentation
epic: EPIC-050
sprint: Backlog
status: QA Approved
points: 3
depends_on: ["STORY-308", "STORY-309"]
priority: High
created: 2026-01-25
updated: 2026-01-25
format_version: "2.7"
---

# STORY-311: Create TARGET-PROJECT-QUICK-START.md Guide

## Description

**As a** new DevForgeAI user,
**I want** a 5-minute quick-start guide,
**so that** I can set up DevForgeAI without reading the 700+ line INSTALL.md.

---

## Provenance

```xml
<provenance>
  <origin document="EPIC-050" section="Friction Points">
    <quote>"FP-7: No quick-start guide for target projects - HIGH priority, 3 points"</quote>
    <line_reference>EPIC-050-installation-process-improvements.epic.md</line_reference>
    <quantified_impact>New users face 700+ line INSTALL.md barrier to entry</quantified_impact>
  </origin>
  <decision rationale="Progressive disclosure pattern">
    <selected>Create separate quick-start guide with essential steps only</selected>
    <rejected>Simplify INSTALL.md (would lose important details for advanced users)</rejected>
    <trade_off>Two documents to maintain, but optimized for different user needs</trade_off>
  </decision>
</provenance>
```

---

## Acceptance Criteria

### AC#1: 5-minute setup achievable

```xml
<acceptance_criteria id="AC1">
  <given>A new user with Python 3.8+ and Git installed</given>
  <when>They follow TARGET-PROJECT-QUICK-START.md</when>
  <then>They have a working DevForgeAI installation in under 5 minutes</then>
  <verification>
    <source_files>
      <file hint="Quick start guide">docs/installer/TARGET-PROJECT-QUICK-START.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Single verification command

```xml
<acceptance_criteria id="AC2">
  <given>The quick-start guide</given>
  <when>User reaches the verification step</when>
  <then>They can confirm installation with a single command</then>
  <verification>
    <source_files>
      <file hint="Quick start guide">docs/installer/TARGET-PROJECT-QUICK-START.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Documentation"
      name: "Quick Start Guide"
      file_path: "docs/installer/TARGET-PROJECT-QUICK-START.md"
      requirements:
        - id: "DOC-001"
          description: "Create 4-step quick-start guide for external projects"
          testable: true
          test_requirement: "Test: New user completes setup in under 5 minutes"
          priority: "Critical"
        - id: "DOC-002"
          description: "Include prerequisites, setup, verification, and next steps"
          testable: true
          test_requirement: "Test: All 4 sections present in document"
          priority: "High"
        - id: "DOC-003"
          description: "Include troubleshooting section for common issues"
          testable: true
          test_requirement: "Test: Troubleshooting section exists"
          priority: "Medium"

    - type: "Documentation"
      name: "INSTALL.md Cross-Reference"
      file_path: "installer/INSTALL.md"
      requirements:
        - id: "DOC-004"
          description: "Add link to quick-start guide at top of INSTALL.md"
          testable: true
          test_requirement: "Test: INSTALL.md links to quick-start guide"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Quick-start must be completable in under 5 minutes"
      test_requirement: "Test: Time new user completing guide"
    - id: "BR-002"
      rule: "Quick-start must not require reading any other documentation"
      test_requirement: "Test: All required commands included inline"
```

---

## Content Structure

```markdown
# DevForgeAI Quick Start for External Projects

## Prerequisites
- Python 3.8+
- Git initialized repository
- Claude Code Terminal

## 5-Minute Setup

### Step 1: Get DevForgeAI
[Clone or npm install instructions]

### Step 2: Run Installer
```bash
python3 -m installer install /path/to/your-project
```

### Step 3: Install CLI
```bash
cd /path/to/your-project
pip install -e .claude/scripts/
```

### Step 4: Verify
```bash
devforgeai-validate validate-context
```

## What's Next?
- `/create-context` - Set up your project constraints
- `/ideate` - Transform business idea into requirements
- `/create-story` - Create your first user story

## Troubleshooting
[Common issues and solutions]
```

---

## Definition of Done

### Implementation
- [x] Quick-start guide created at docs/installer/TARGET-PROJECT-QUICK-START.md
- [x] All 4 steps documented with copy-paste commands
- [x] Troubleshooting section with common issues
- [x] What's Next section with 3 recommended commands

### Testing
- [ ] Tested with fresh project (no prior DevForgeAI) **DEFERRED: DEBT-002** - Requires manual testing
- [ ] Completion time under 5 minutes verified **DEFERRED: DEBT-002** - Requires manual testing

### Documentation
- [x] Linked from main INSTALL.md
- [x] Linked from README.md

---

## AC Verification Checklist

### AC#1: 5-minute setup achievable
- [x] Guide created - **Phase:** 3 - **Evidence:** TARGET-PROJECT-QUICK-START.md
- [x] 4 steps documented - **Phase:** 3 - **Evidence:** section count
- [ ] Time verified - **Phase:** 4 - **Evidence:** DEFERRED to DEBT-002 (manual test)

### AC#2: Single verification command
- [x] Verify step present - **Phase:** 3 - **Evidence:** Step 4 section
- [x] Command is single-line - **Phase:** 3 - **Evidence:** verify command

---

## Implementation Notes

- [x] Quick-start guide created at docs/installer/TARGET-PROJECT-QUICK-START.md - Completed: File created with 151 lines
- [x] All 4 steps documented with copy-paste commands - Completed: Steps 1-4 with bash code blocks
- [x] Troubleshooting section with common issues - Completed: 6 common issues documented
- [x] What's Next section with 3 recommended commands - Completed: /create-context, /ideate, /create-story
- [x] Linked from main INSTALL.md - Completed: Link added at line 3
- [x] Linked from README.md - Completed: Link added in Installation section
- [ ] Tested with fresh project (no prior DevForgeAI) - DEFERRED: DEBT-002 - User approved: 2026-01-26 - Manual testing requires actual user testing
- [ ] Completion time under 5 minutes verified - DEFERRED: DEBT-002 - User approved: 2026-01-26 - Manual timing test cannot be automated

**Summary:**
- All 13 structural tests pass (8+3+2)
- Documentation follows DevForgeAI markdown standards

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-25 | claude/opus | Created | Story created from EPIC-050 plan | STORY-311-create-quick-start-guide.story.md |
| 2026-01-26 | claude/dev | Dev Complete | TDD implementation complete. Quick-start guide created. Manual testing deferred (DEBT-002). | docs/installer/TARGET-PROJECT-QUICK-START.md, installer/INSTALL.md, README.md |
| 2026-01-26 | claude/qa | QA Deep | PASSED: 100% traceability, 1/1 validators, deferrals valid (DEBT-002) | devforgeai/qa/reports/STORY-311-qa-report.md |

---

## Notes

**Dependencies:** STORY-308 and STORY-309 must be completed first so the documented command names are correct.

**References:**
- installer/INSTALL.md
- docs/installer/ directory
