---
id: STORY-309
title: Document Python CLI Installation as Required Prerequisite
type: documentation
epic: EPIC-050
sprint: Backlog
status: QA Approved
points: 1
depends_on: ["STORY-308"]
priority: High
created: 2026-01-25
updated: 2026-01-25
format_version: "2.7"
---

# STORY-309: Document Python CLI Installation as Required Prerequisite

## Description

**As a** new DevForgeAI user,
**I want** clear documentation that the Python CLI must be installed,
**so that** I don't encounter silent failures during Phase 01 preflight.

---

## Provenance

```xml
<provenance>
  <origin document="EPIC-050" section="Friction Points">
    <quote>"FP-3: Python CLI install not documented - CRITICAL priority"</quote>
    <line_reference>EPIC-050-installation-process-improvements.epic.md</line_reference>
    <quantified_impact>100% of new users unaware of required CLI installation step</quantified_impact>
  </origin>
  <decision rationale="Documentation before code">
    <selected>Add explicit installation step to INSTALL.md</selected>
    <rejected>Automatic CLI installation during npm install (complexity, cross-platform issues)</rejected>
    <trade_off>Manual step required, but transparent and debuggable</trade_off>
  </decision>
</provenance>
```

---

## Acceptance Criteria

### AC#1: INSTALL.md includes Python CLI step

```xml
<acceptance_criteria id="AC1">
  <given>INSTALL.md prerequisites section</given>
  <when>A user reads the installation guide</when>
  <then>They see explicit step: pip install -e .claude/scripts/</then>
  <verification>
    <source_files>
      <file hint="Installation guide">installer/INSTALL.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Verification command documented

```xml
<acceptance_criteria id="AC2">
  <given>The Python CLI installation step</given>
  <when>User completes the step</when>
  <then>A verification command is provided: devforgeai-validate --version</then>
  <verification>
    <source_files>
      <file hint="Installation guide">installer/INSTALL.md</file>
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
      name: "INSTALL.md Update"
      file_path: "installer/INSTALL.md"
      requirements:
        - id: "DOC-001"
          description: "Add 'Step 5: Install Python Validation CLI' section after Node.js setup"
          testable: true
          test_requirement: "Test: Grep for 'pip install -e .claude/scripts' in INSTALL.md"
          priority: "Critical"
        - id: "DOC-002"
          description: "Include verification command with expected output"
          testable: true
          test_requirement: "Test: Grep for 'devforgeai-validate --version' in INSTALL.md"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Installation documentation must include all required prerequisites"
      test_requirement: "Test: New user can complete installation following only documented steps"
```

---

## Content to Add

```markdown
### Step 5: Install Python Validation CLI (Required)

The DevForgeAI workflow requires the Python CLI for phase enforcement:

```bash
pip install -e .claude/scripts/
```

Verify installation:
```bash
devforgeai-validate --version
# Expected output: devforgeai-validate 0.1.0
```

> **Note:** This step is required for `/dev` and `/qa` commands to work correctly.
```

---

## Definition of Done

### Implementation
- [x] INSTALL.md updated with explicit Python CLI step
- [x] Verification command documented
- [x] Step positioned correctly in installation sequence (after Node.js, before hooks)

### Documentation
- [x] Step number is correct in sequence
- [x] Expected output shown for verification
- [x] Note explains why step is required

---

## AC Verification Checklist

### AC#1: INSTALL.md includes Python CLI step
- [x] Step 5 section added - **Phase:** 3 - **Evidence:** INSTALL.md
- [x] pip install command present - **Phase:** 3 - **Evidence:** INSTALL.md

### AC#2: Verification command documented
- [x] --version command shown - **Phase:** 3 - **Evidence:** INSTALL.md
- [x] Expected output documented - **Phase:** 3 - **Evidence:** INSTALL.md

---

## Implementation Notes

- [x] INSTALL.md updated with explicit Python CLI step - Completed: Added Step 5 section with pip install command at line 114
- [x] Verification command documented - Completed: devforgeai-validate --version at line 119 with expected output
- [x] Step positioned correctly in installation sequence (after Node.js, before hooks) - Completed: Step 5 positioned after Step 4 (Restart Terminal), before Upgrading section
- [x] Step number is correct in sequence - Completed: Step 5 follows Steps 1-4 in Fresh Installation section
- [x] Expected output shown for verification - Completed: Shows "devforgeai-validate 0.1.0" at line 120
- [x] Note explains why step is required - Completed: Note at line 123 explains requirement for /dev and /qa commands

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-25 | claude/opus | Created | Story created from EPIC-050 plan | STORY-309-document-python-cli-installation.story.md |
| 2026-01-26 | claude/opus | Phase 03 | Added Step 5 to INSTALL.md with Python CLI installation instructions | installer/INSTALL.md |
| 2026-01-26 | claude/opus | Phase 07 | DoD items completed, status updated to Dev Complete | STORY-309-document-python-cli-installation.story.md |
| 2026-01-26 | claude/qa-result-interpreter | QA Deep | PASSED: 100% traceability, 1/1 validators passed, 0 violations | installer/INSTALL.md |

---

## Notes

**Dependencies:** STORY-308 must be completed first so the documented command name is correct.

**References:**
- installer/INSTALL.md
- STORY-308: Fix Binary Name Mismatch
