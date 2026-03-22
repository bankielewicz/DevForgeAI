---
id: STORY-313
title: Consolidate Triple Mirror Pattern to Single Source of Truth
type: refactor
epic: EPIC-050
sprint: Backlog
status: QA Approved
points: 5
depends_on: []
priority: Medium
created: 2026-01-25
updated: 2026-01-25
format_version: "2.7"
---

# STORY-313: Consolidate Triple Mirror Pattern to Single Source of Truth

## Description

**As a** DevForgeAI maintainer,
**I want** a single source of truth for framework code,
**so that** changes don't need to be made in 3 places (/src/, /.claude/, /bundled/).

**ADR Required:** Yes - ADR-XXX: Triple Mirror Consolidation Strategy

**Approach:** Build-time copy (recommended over symlinks for Windows compatibility)

---

## Provenance

```xml
<provenance>
  <origin document="EPIC-050" section="Friction Points">
    <quote>"FP-4: Triple mirror pattern (src/, .claude/, bundled/) - MEDIUM priority, 5 points"</quote>
    <line_reference>EPIC-050-installation-process-improvements.epic.md</line_reference>
    <quantified_impact>Every framework change requires 3x the effort to maintain consistency</quantified_impact>
  </origin>
  <decision rationale="Windows compatibility over elegance">
    <selected>Build-time copy script (cross-platform)</selected>
    <rejected alternative="symlinks">Windows compatibility issues with git and symlinks</rejected>
    <rejected alternative="git submodules">Complexity overhead for internal repository</rejected>
    <trade_off>Script maintenance required, but works on all platforms</trade_off>
  </decision>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Build-time sync copies files automatically

```xml
<acceptance_criteria id="AC1">
  <given>/src/claude/ directory as source of truth</given>
  <when>Build/release process runs</when>
  <then>Files are copied to /.claude/ and /bundled/ automatically</then>
  <verification>
    <source_files>
      <file hint="Sync script">scripts/sync-mirrors.sh</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#2: CI verifies mirror sync

```xml
<acceptance_criteria id="AC2">
  <given>The sync script</given>
  <when>CI pipeline runs</when>
  <then>Verification confirms all three locations are in sync</then>
  <verification>
    <source_files>
      <file hint="CI workflow">.github/workflows/sync-verification.yml</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#3: ADR documents decision

```xml
<acceptance_criteria id="AC3">
  <given>ADR for triple mirror consolidation</given>
  <when>Architecture decision is documented</when>
  <then>ADR explains rationale, options considered, and chosen approach</then>
  <verification>
    <source_files>
      <file hint="Architecture decision">devforgeai/specs/adrs/ADR-XXX-triple-mirror-consolidation.md</file>
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
    - type: "Script"
      name: "Mirror Sync Script"
      file_path: "scripts/sync-mirrors.sh"
      requirements:
        - id: "SCR-001"
          description: "Copy all files from src/claude/ to .claude/"
          testable: true
          test_requirement: "Test: diff -r src/claude .claude shows no differences after sync"
          priority: "Critical"
        - id: "SCR-002"
          description: "Copy all files from src/devforgeai/ to devforgeai/"
          testable: true
          test_requirement: "Test: diff -r src/devforgeai devforgeai shows no differences after sync"
          priority: "Critical"
        - id: "SCR-003"
          description: "Preserve file permissions and timestamps"
          testable: true
          test_requirement: "Test: rsync -a or cp -p used for copying"
          priority: "Medium"
        - id: "SCR-004"
          description: "Report sync status (files copied, skipped, errors)"
          testable: true
          test_requirement: "Test: Script outputs sync summary"
          priority: "Medium"

    - type: "CI"
      name: "Sync Verification Workflow"
      file_path: ".github/workflows/sync-verification.yml"
      requirements:
        - id: "CI-001"
          description: "Run diff check on every PR"
          testable: true
          test_requirement: "Test: Workflow runs on pull_request trigger"
          priority: "High"
        - id: "CI-002"
          description: "Fail PR if mirrors are out of sync"
          testable: true
          test_requirement: "Test: Non-zero exit code on diff failure"
          priority: "Critical"

    - type: "Documentation"
      name: "ADR"
      file_path: "devforgeai/specs/adrs/ADR-XXX-triple-mirror-consolidation.md"
      requirements:
        - id: "ADR-001"
          description: "Document context, decision, and consequences"
          testable: true
          test_requirement: "Test: ADR contains all required sections"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "src/ is the single source of truth for framework files"
      test_requirement: "Test: All edits happen in src/, mirrors are generated"
    - id: "BR-002"
      rule: "Mirrors must be identical to source after sync"
      test_requirement: "Test: diff -r shows no differences"
    - id: "BR-003"
      rule: "Sync must work on Windows, macOS, and Linux"
      test_requirement: "Test: CI runs on all three platforms"
```

---

## Files to Create

1. `scripts/sync-mirrors.sh` - Sync script
2. `devforgeai/specs/adrs/ADR-XXX-triple-mirror-consolidation.md` - ADR
3. `.github/workflows/sync-verification.yml` - CI verification

## Files to Modify

1. `scripts/release.sh` - Add sync step before release
2. `CONTRIBUTING.md` - Document sync workflow for contributors

---

## Definition of Done

### Implementation
- [x] Sync script created and tested
- [x] Script handles src/claude/ → .claude/ copy
- [x] Script handles src/devforgeai/ → devforgeai/ copy (if applicable)
- [x] Script is cross-platform (bash for *nix, batch for Windows) [Note: Bash script works on Windows via Git Bash/WSL]

### Testing
- [x] Manual sync verification on local machine [Tests: 17/17 passed]
- [ ] CI workflow passes on all platforms [DEFERRED: Requires live GitHub Actions execution]
   User approved: 2026-01-27
- [ ] Diff check detects intentional out-of-sync state [DEFERRED: Requires live PR test]
   User approved: 2026-01-27

### Documentation
- [x] ADR created with full context and decision [ADR-011]
- [ ] CONTRIBUTING.md updated with sync instructions [DEFERRED: Follow-up documentation]
   User approved: 2026-01-27
- [ ] README mentions sync requirement [DEFERRED: Follow-up documentation]
   User approved: 2026-01-27

---

## AC Verification Checklist

### AC#1: Build-time sync works
- [x] Script created - **Phase:** 3 - **Evidence:** scripts/sync-mirrors.sh
- [x] Script copies files - **Phase:** 4 - **Evidence:** Test suite validates
- [x] Script reports status - **Phase:** 4 - **Evidence:** log_success function

### AC#2: CI verifies sync
- [x] Workflow created - **Phase:** 3 - **Evidence:** .github/workflows/sync-verification.yml
- [ ] Workflow runs on PR - **Phase:** 4 - **Evidence:** [DEFERRED: Requires live GitHub Actions] User approved: 2026-01-27
- [ ] Workflow fails on mismatch - **Phase:** 4 - **Evidence:** [DEFERRED: Requires live PR test] User approved: 2026-01-27

### AC#3: ADR documented
- [x] ADR created - **Phase:** 3 - **Evidence:** devforgeai/specs/adrs/ADR-011-triple-mirror-consolidation.md
- [x] Context section present - **Phase:** 3 - **Evidence:** Lines 8-23
- [x] Decision section present - **Phase:** 3 - **Evidence:** Lines 25-51

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-01-27
**Branch:** main

- [x] Sync script created and tested - Completed: scripts/sync-mirrors.sh (157 lines) with rsync-based sync
- [x] Script handles src/claude/ → .claude/ copy - Completed: sync_directory function lines 81-106
- [x] Script handles src/devforgeai/ → devforgeai/ copy - Completed: Lines 129-135
- [x] Script is cross-platform - Completed: Bash script works on Windows via Git Bash/WSL
- [x] Manual sync verification on local machine - Completed: 17/17 tests passed
- [x] ADR created with full context and decision - Completed: ADR-011-triple-mirror-consolidation.md

### Files Created
- `scripts/sync-mirrors.sh` - Mirror sync script (157 lines)
- `.github/workflows/sync-verification.yml` - CI verification workflow (86 lines)
- `devforgeai/specs/adrs/ADR-011-triple-mirror-consolidation.md` - ADR (86 lines)
- `tests/STORY-313/` - Test suite (4 files, 17 tests)

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-25 | claude/opus | Created | Story created from EPIC-050 plan | STORY-313-consolidate-triple-mirror.story.md |
| 2026-01-27 | claude/qa-result-interpreter | QA Deep | PASSED: 17/17 tests, 0 violations, 4 valid deferrals | - |

---

## Notes

**ADR Prerequisite:** This story requires an ADR to be created as part of the implementation. The ADR number will be assigned when the story is picked up.

**Independent Story:** This story has no dependencies and can be worked in Sprint 3.

**References:**
- source-tree.md (Dual-Location Architecture section)
- scripts/release.sh
