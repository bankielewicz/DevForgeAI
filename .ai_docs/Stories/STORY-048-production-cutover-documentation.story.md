---
id: STORY-048
title: Production Cutover, Documentation, and Distribution Package
epic: EPIC-009
sprint: Backlog
status: Backlog
points: 8
priority: High
assigned_to: TBD
created: 2025-11-16
format_version: "2.0"
depends_on: STORY-047
---

# Story: Production Cutover, Documentation, and Distribution Package

## Description

**As a** DevForgeAI framework maintainer completing the src/ migration,
**I want** to finalize documentation, create distribution packages, deprecate the old .claude/ manual copy approach, and enable the team to use the new installer-based workflow,
**so that** DevForgeAI can be distributed to external users reliably and the development team adopts the proper SDLC (source → installer → deploy → test).

## Acceptance Criteria

### 1. [ ] README.md Updated with Installer-Based Installation Instructions

**Given** README.md currently describes manual .claude/ folder copying
**When** I update the Installation section
**Then** new instructions use installer:
```markdown
## Installation

### For New Projects

```bash
# 1. Clone DevForgeAI repository
git clone https://github.com/user/DevForgeAI2.git

# 2. Navigate to your project
cd /path/to/your/project

# 3. Run installer
python /path/to/DevForgeAI2/installer/install.py --target=.
```

### For Existing DevForgeAI Projects

```bash
# Upgrade to latest version
python /path/to/DevForgeAI2/installer/install.py --target=. --mode=upgrade
```
```
**And** old manual copy instructions removed or moved to "Legacy Installation (Deprecated)" section
**And** Prerequisites section lists: Python 3.8+, Git, Claude Code Terminal 0.8.0+
**And** Installation section tested by new user (follows steps, successfully installs)

---

### 2. [ ] INSTALL.md Created with Comprehensive Installation Guide

**Given** users need detailed installation documentation
**When** I create installer/INSTALL.md
**Then** the guide covers all installation scenarios:

**Sections included:**
1. **Prerequisites** - System requirements, tool versions
2. **Installation Modes** - Descriptions of 5 modes (fresh, upgrade, rollback, validate, uninstall)
3. **Fresh Installation** - Step-by-step for new projects (with screenshots/examples)
4. **Upgrading** - How to upgrade existing installation (patch, minor, major)
5. **Rollback** - How to revert to previous version (list backups, select, restore)
6. **Validation** - How to check installation integrity
7. **Uninstallation** - How to cleanly remove DevForgeAI
8. **Troubleshooting** - Common issues and solutions (15+ scenarios)
9. **FAQ** - Frequently asked questions (10+ Q&A)
10. **Support** - Where to get help (GitHub issues, docs)

**And** guide tested with 2 new users (both successfully install following guide)
**And** all command examples copy-pasteable (tested for accuracy)
**And** troubleshooting scenarios cover issues found in STORY-047 testing

---

### 3. [ ] MIGRATION-GUIDE.md Created for Existing DevForgeAI Users

**Given** existing users have DevForgeAI manually copied to .claude/
**When** I create MIGRATION-GUIDE.md for migration to installer-based approach
**Then** the guide provides step-by-step migration:

**Migration workflow:**
1. **Backup current installation** - `cp -r .claude .claude.pre-migration-backup`
2. **Pull latest DevForgeAI** - `git pull` in DevForgeAI2 repo
3. **Run installer** - `python installer/install.py --target=. --mode=upgrade`
4. **Verify installation** - `python installer/install.py --target=. --mode=validate`
5. **Update workflow** - Edit files in DevForgeAI2/src/, run installer to deploy
6. **Test changes** - Create test story, run /dev, verify works
7. **Cleanup old backups** - Remove .claude.pre-migration-backup after validation

**And** migration guide includes:
  - Safety checklist (backup verification, rollback plan)
  - Workflow changes (before: edit .claude/, after: edit src/ + installer)
  - Troubleshooting migration issues
  - Rollback procedure if migration fails

**And** guide tested with simulated migration (manual .claude/ → installer-based)

---

### 4. [ ] Distribution Package Created and Tested

**Given** DevForgeAI ready for distribution to external users
**When** I create distribution package
**Then** package bundles all necessary files:

**Package contents:**
- src/ directory (all 450 framework source files)
- installer/ directory (install.py, rollback.py, validate.py, config.yaml)
- INSTALL.md (installation guide)
- MIGRATION-GUIDE.md (migration guide for existing users)
- LICENSE (MIT license)
- version.json (framework version metadata)

**Package formats:**
- devforgeai-1.0.1.tar.gz (Linux/macOS)
- devforgeai-1.0.1.zip (Windows)

**And** package tested on 3 external projects:
  - Extract package: `tar -xzf devforgeai-1.0.1.tar.gz`
  - Run installer: `python devforgeai-1.0.1/installer/install.py --target=.`
  - Verify installation: All 3 projects install successfully (100% success rate)
**And** package size: ~25 MB compressed, ~40 MB extracted

---

### 5. [ ] Old .claude/ Manual Copy Approach Deprecated

**Given** the installer is production-ready
**When** I deprecate the manual copy approach
**Then** deprecation notices added:

**In README.md:**
```markdown
## ⚠️ DEPRECATED: Manual .claude/ Copy

**Old approach (DEPRECATED):** Manually copying .claude/ folder

**New approach:** Use installer

[Link to Installation section]
```

**In .claude/README.md (NEW):**
```markdown
# ⚠️ DEPRECATED: Direct .claude/ Folder Usage

This folder structure is for deployed framework only.

**For framework development:**
Edit files in `src/claude/` and run installer to deploy.

**For new installations:**
Use `installer/install.py` instead of copying this folder.

[See INSTALL.md]
```

**And** deprecation date: 2025-11-17 (documented in ROADMAP.md)
**And** support timeline: Manual approach supported until v2.0.0 (gives users 6-12 months to migrate)

---

### 6. [ ] ROADMAP.md Updated with Migration Completion

**Given** src/ migration is complete
**When** I update ROADMAP.md
**Then** Phase 4 marked complete:
```markdown
## Phase 4: src/ Migration and Installer ✅ COMPLETE (2025-11-17)

- ✅ STORY-041: Infrastructure setup
- ✅ STORY-042: File migration
- ✅ STORY-043: Path reference updates
- ✅ STORY-044: Internal testing
- ✅ STORY-045: Installer core algorithm
- ✅ STORY-046: CLAUDE.md merge logic
- ✅ STORY-047: External integration testing
- ✅ STORY-048: Production cutover

**Deliverables:**
- Version-aware installer with 5 modes
- src/ source tree (450 files)
- Distribution packages (tar.gz, zip)
- Complete documentation (INSTALL.md, MIGRATION-GUIDE.md)

**Next Phase:** Phase 5: Public Release and Community Onboarding
```
**And** version number updated to 1.0.1 (if not already)
**And** release notes added with breaking changes (if any)

---

### 7. [ ] Team Onboarding Complete (New Workflow Adopted)

**Given** the development team needs to adopt the new src/ workflow
**When** I conduct team onboarding
**Then** all team members trained on new process:

**Onboarding checklist per developer:**
- [ ] Understand src/ structure (source) vs .claude/ (deployed)
- [ ] Know how to edit files (edit src/, run installer)
- [ ] Tested installer (install on personal test project)
- [ ] Read INSTALL.md and MIGRATION-GUIDE.md
- [ ] Can create stories using /create-story
- [ ] Can develop stories using /dev
- [ ] Understand rollback procedure (if deployment breaks something)

**And** onboarding session conducted (1 hour presentation + 1 hour hands-on)
**And** all developers complete training checklist (100% completion)
**And** no blockers reported (developers comfortable with new workflow)

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Worker"
      name: "DistributionPackager"
      file_path: "scripts/create-distribution.sh"
      requirements:
        - id: "WKR-001"
          description: "Bundle src/, installer/, docs into tar.gz archive"
          testable: true
          test_requirement: "Test: tar -tzf devforgeai-1.0.1.tar.gz lists all required files"
          priority: "High"

        - id: "WKR-002"
          description: "Create ZIP archive for Windows users"
          testable: true
          test_requirement: "Test: unzip -l devforgeai-1.0.1.zip lists same files as tar.gz"
          priority: "Medium"

        - id: "WKR-003"
          description: "Include LICENSE, INSTALL.md, MIGRATION-GUIDE.md in package"
          testable: true
          test_requirement: "Test: Extract package, verify all 3 docs present in root"
          priority: "High"

        - id: "WKR-004"
          description: "Test package extraction and installation on 3 projects"
          testable: true
          test_requirement: "Test: Extract, run installer, verify 3/3 successes"
          priority: "Critical"

    - type: "Configuration"
      name: "DocumentationUpdates"
      file_path: "docs/"
      requirements:
        - id: "CONF-001"
          description: "Update README.md installation section with installer commands"
          testable: true
          test_requirement: "Test: README.md contains 'python installer/install.py' not 'copy .claude/'"
          priority: "Critical"

        - id: "CONF-002"
          description: "Create INSTALL.md with 10 sections covering all scenarios"
          testable: true
          test_requirement: "Test: INSTALL.md has sections for fresh, upgrade, rollback, validate, uninstall"
          priority: "Critical"

        - id: "CONF-003"
          description: "Create MIGRATION-GUIDE.md for existing user migration"
          testable: true
          test_requirement: "Test: Guide has 7-step migration workflow with safety checklist"
          priority: "High"

        - id: "CONF-004"
          description: "Update ROADMAP.md marking migration complete"
          testable: true
          test_requirement: "Test: ROADMAP.md shows Phase 4 complete, version 1.0.1"
          priority: "Medium"

        - id: "CONF-005"
          description: "Add deprecation notice to .claude/README.md"
          testable: true
          test_requirement: "Test: .claude/README.md contains DEPRECATED warning"
          priority: "High"

    - type: "Logging"
      name: "OnboardingTracker"
      file_path: ".devforgeai/onboarding/team-training-log.md"
      requirements:
        - id: "LOG-001"
          description: "Track team member onboarding completion"
          testable: true
          test_requirement: "Test: Log shows each developer with checklist completion status"
          priority: "Medium"

        - id: "LOG-002"
          description: "Document onboarding session (date, attendees, topics covered)"
          testable: true
          test_requirement: "Test: Log contains session metadata and 7 onboarding checklist items"
          priority: "Low"

  business_rules:
    - id: "BR-001"
      rule: "Documentation must be accurate (all installation commands must work as documented)"
      test_requirement: "Test: Follow README.md steps, verify installation succeeds"

    - id: "BR-002"
      rule: "Distribution package must contain all files needed for installation"
      test_requirement: "Test: Extract package to empty dir, install, verify no missing files"

    - id: "BR-003"
      rule: "Deprecation notice required before removing old approach (6-month warning period)"
      test_requirement: "Test: .claude/README.md has deprecation date, support until date"

    - id: "BR-004"
      rule: "Team onboarding 100% completion required before production cutover"
      test_requirement: "Test: All developers complete training checklist (count=team_size)"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Usability"
      requirement: "Documentation clear for new users"
      metric: "New user can install following docs with 0 support requests"
      test_requirement: "Test: 2 new users install independently, both succeed without help"

    - id: "NFR-002"
      category: "Usability"
      requirement: "Distribution package easy to extract and use"
      metric: "2-step process: Extract + run installer (no complex setup)"
      test_requirement: "Test: tar -xzf + python install.py, verify works"

    - id: "NFR-003"
      category: "Reliability"
      requirement: "Package integrity verifiable"
      metric: "SHA256 checksum provided for package verification"
      test_requirement: "Test: Provide devforgeai-1.0.1.tar.gz.sha256, users can verify with shasum"
```

### Dependencies

**Prerequisite Stories:**
- ALL previous stories (STORY-041 through STORY-047)

**Blocked Stories:**
- None (final story in epic)

---

## Edge Cases

### 1. Documentation Out of Sync with Installer
**Scenario:** INSTALL.md describes --mode=update but installer uses --mode=upgrade
**Expected:** Documentation review catches discrepancy, docs updated to match installer
**Handling:** Cross-reference all command examples in docs with actual installer arguments

### 2. Distribution Package Corrupted During Download
**Scenario:** User downloads tar.gz, file corrupted (incomplete download)
**Expected:** SHA256 checksum verification detects corruption, user re-downloads
**Handling:** Provide .sha256 file, instruct users to verify: `shasum -c devforgeai-1.0.1.tar.gz.sha256`

### 3. Team Member Skips Onboarding (Uses Old Workflow)
**Scenario:** Developer edits .claude/ directly instead of src/ + installer
**Expected:** Git pre-commit hook detects .claude/ modifications, warns: "Edit src/ instead, run installer to deploy"
**Handling:** Add pre-commit hook checking for .claude/ changes, remind developer of new workflow

### 4. Old .claude/ Manual Copy Still Referenced in Docs
**Scenario:** Some documentation still says "copy .claude/ folder"
**Expected:** Documentation audit finds all old references, updates to installer approach
**Handling:** grep -r "copy .claude" docs/, update all matches

### 5. Version Number Inconsistency
**Scenario:** version.json says 1.0.1 but ROADMAP.md says 1.0.0
**Expected:** Version audit detects mismatch, all version references updated to 1.0.1
**Handling:** grep for version numbers across all docs, ensure consistency

### 6. Package Too Large for Email/Slack
**Scenario:** 25 MB compressed package exceeds email attachment limits
**Expected:** Provide alternative distribution (GitHub release, download link, npm package)
**Handling:** Document multiple distribution channels in INSTALL.md

### 7. Team Training During Active Development
**Scenario:** Onboarding scheduled during sprint when developers are busy
**Expected:** Record training session, provide async training materials, schedule makeup sessions
**Handling:** Create training video, written guide, allow async completion of checklist

---

## Data Validation Rules

1. **Documentation accuracy:** All commands in docs must match installer actual arguments

2. **Package completeness:** Extract and count files, must equal src/ file count (450)

3. **Checksum verification:** SHA256 of package must match published checksum

4. **Version consistency:** All version references across docs must match (1.0.1)

5. **Onboarding completion:** All team members must complete 7-item checklist (100%)

6. **Deprecation timeline:** Old approach support end date must be ≥6 months from deprecation

---

## Implementation Notes

Status: Backlog - Pending implementation. This story is in the planning phase and has not yet been developed.

All Definition of Done items are currently unchecked [ ] and will be completed during the TDD development cycle.

---

## Non-Functional Requirements

### Usability
- Documentation clarity: New user success without support
- Package extraction: 2-step process (extract + run)
- Onboarding: 2-hour session (1h presentation + 1h hands-on)

### Reliability
- Package integrity: SHA256 verification available
- Documentation accuracy: 100% command correctness
- Distribution: Multiple channels (GitHub, direct download)

---

## Definition of Done

### Implementation
- [ ] README.md installation section updated
- [ ] INSTALL.md created (10 sections, 15+ troubleshooting scenarios, 10+ FAQ)
- [ ] MIGRATION-GUIDE.md created (7-step workflow with safety checklist)
- [ ] ROADMAP.md updated (Phase 4 complete, version 1.0.1)
- [ ] .claude/README.md created with deprecation notice
- [ ] Distribution package created (tar.gz and zip)
- [ ] SHA256 checksums generated for packages
- [ ] Package tested on 3 diverse projects (100% install success)

### Quality
- [ ] All 7 acceptance criteria validated
- [ ] All 4 business rules enforced
- [ ] All 3 NFRs met
- [ ] All 7 edge cases handled
- [ ] Documentation tested by 2 new users
- [ ] Package integrity verified (checksum matches)

### Testing
- [ ] Documentation walkthrough (2 new users)
- [ ] Package extraction test (3 projects)
- [ ] Installation from package (3/3 success)
- [ ] Migration simulation (manual → installer)
- [ ] Team onboarding (all developers)
- [ ] Cross-reference validation (docs vs installer)

### Documentation
- [ ] All 5 documentation files created
- [ ] Old references updated (no "copy .claude")
- [ ] Version numbers consistent (all say 1.0.1)
- [ ] Deprecation timeline documented
- [ ] EPIC-009 marked complete

### Release Readiness
- [ ] Git commit final documentation
- [ ] Distribution package published (GitHub release)
- [ ] Team onboarded (100% completion)
- [ ] Old workflow deprecated (notices added)
- [ ] Production cutover complete (src/ is source of truth)
- [ ] Ready for external user distribution

---

## Workflow History

- **2025-11-16:** Story created for EPIC-009 Phase 8 (production cutover)
- **2025-11-16:** Priority: High, Points: 8 (documentation and packaging)
- **2025-11-16:** Depends on ALL previous stories (STORY-041 through STORY-047)
- **2025-11-16:** Final story in EPIC-009 (completes 8-phase migration)
- **2025-11-16:** Low risk (documentation only, no code changes)
- **2025-11-16:** Status: Backlog (awaiting STORY-047 validation)
