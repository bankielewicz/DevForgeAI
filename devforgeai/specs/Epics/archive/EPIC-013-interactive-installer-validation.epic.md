---
id: EPIC-013
title: Interactive Installer & Validation
business-value: Reduce installation failures from 20%+ to <5% through wizard-driven UX and comprehensive validation
status: Planning
priority: High
complexity-score: 28
architecture-tier: Tier 2 (Moderate Application)
created: 2025-11-25
estimated-points: 25-35
target-sprints: 3-4 sprints
dependencies: ["EPIC-012"]
---

# Interactive Installer & Validation

## Business Goal

Transform installation from error-prone manual process to guided wizard experience with proactive validation, reducing installation failures from 20%+ to <5% and support burden by 60%+.

**Success Metrics:**
- Installation failure rate: <5% (down from ~20%)
- Average installation time: <5 minutes (including prompts)
- User satisfaction: >90% report "easy" or "very easy" installation
- Support tickets: 60% reduction in installation-related issues

## Problem Statement

Current installer lacks:
1. **Guided UX:** Users don't know what to configure or where to install
2. **Pre-flight validation:** Errors discovered mid-installation, leaving broken state
3. **Clear error messages:** Cryptic failures without resolution guidance
4. **Auto-detection:** Manual input for paths, versions, existing installations
5. **Progress feedback:** No visibility into long-running operations

This leads to:
- High failure rates (20%+ of installations fail)
- User frustration and abandoned installations
- High support burden (troubleshooting installation issues)
- Poor first impression of DevForgeAI framework

## Features

### Feature 1: Wizard-Driven Interactive UI
**Description:** Step-by-step wizard guiding user through installation configuration
**User Stories (high-level):**
1. As a user, I want a wizard that asks clear questions, so I know what to configure
2. As a user, I want to see installation progress, so I know it's working
3. As a user, I want confirmation prompts for destructive actions, so I don't accidentally overwrite files
4. As a CI/CD pipeline, I want to skip wizard via --yes flag, so I can automate installation

**Estimated Effort:** Medium (8-12 story points)

**Acceptance Criteria:**
- Interactive prompts for: target directory, installation mode, CLAUDE.md merge strategy
- Progress indicators (spinners, progress bars) for long operations
- Color-coded output (green=success, yellow=warning, red=error)
- Confirmation prompts for overwrite/uninstall/destructive actions
- --yes flag skips all prompts (uses defaults or CLI args)
- --quiet flag suppresses non-error output

### Feature 2: Pre-Flight Validation Checks
**Description:** Validate environment before installation to catch issues early
**User Stories (high-level):**
1. As a user, I want validation errors before installation starts, so I can fix issues proactively
2. As a user, I want clear error messages with resolution steps, so I know what to fix
3. As a user, I want warnings (non-blocking) vs errors (blocking), so I can decide whether to proceed

**Estimated Effort:** Medium (8-12 story points)

**Acceptance Criteria:**
- **Python version check:** Verify Python 3.10+ available (WARN if missing - CLI optional)
- **Disk space check:** Verify >100MB available (ERROR if insufficient)
- **Existing installation check:** Detect previous DevForgeAI install, prompt for upgrade vs fresh
- **Permission check:** Verify write permissions on target directory (ERROR if denied)
- **Validation summary:** Display all checks (✓ PASS, ⚠ WARN, ✗ FAIL) before proceeding
- **Blocking errors:** Installation halts if critical checks fail
- **Override flag:** --force flag bypasses non-critical warnings

### Feature 3: Auto-Detection (Project Type & Existing Installs)
**Description:** Automatically detect project context to reduce manual configuration
**User Stories (high-level):**
1. As a user, I want installer to detect existing DevForgeAI, so I'm prompted to upgrade instead of overwriting
2. As a user, I want installer to suggest target directory, so I don't have to guess correct path
3. As a user, I want installer to detect existing CLAUDE.md, so I know merge is needed

**Estimated Effort:** Medium (8-12 story points)

**Acceptance Criteria:**
- **Existing install detection:** Read `devforgeai/.version.json` to identify version
- **Version comparison:** Compare installed vs source version, recommend upgrade/downgrade/reinstall
- **CLAUDE.md detection:** Detect existing CLAUDE.md, warn about merge, offer backup
- **Project root detection:** Find git repository root as default target directory
- **File conflict detection:** Identify existing files that would be overwritten
- **Auto-detection summary:** Display findings before prompting user

### Feature 4: Comprehensive Error Handling
**Description:** Catch errors gracefully with clear messages and resolution guidance
**User Stories (high-level):**
1. As a user, I want helpful error messages, so I know what went wrong and how to fix it
2. As a user, I want installation to rollback on failure, so I'm not left with broken state
3. As a user, I want error log written to file, so I can share with support if needed

**Estimated Effort:** Medium-Large (10-15 story points)

**Acceptance Criteria:**
- **Error taxonomy:** Categorize errors (missing source, permission denied, git dirty, file conflicts)
- **User-friendly messages:** No stack traces in console (technical details in log file)
- **Resolution guidance:** Each error includes 1-3 steps to resolve
- **Automatic rollback:** On failure, restore backup and clean up partial installation
- **Error logging:** Write detailed log to `devforgeai/install.log` with timestamps
- **Exit codes:** 0=success, 1=source missing, 2=permission denied, 3=rollback occurred, 4=validation failed

### Feature 5: Installation Reporting & Logging
**Description:** Provide detailed reports and logs for troubleshooting and auditing
**User Stories (high-level):**
1. As a user, I want installation summary at end, so I know what was installed
2. As a user, I want detailed log file, so I can troubleshoot issues or share with support
3. As a maintainer, I want JSON output mode, so I can parse results in CI/CD

**Estimated Effort:** Small-Medium (5-8 story points)

**Acceptance Criteria:**
- **Installation summary report:** Success/failure, version installed, files count, errors encountered
- **Detailed log file:** `devforgeai/install.log` with all actions, timestamps, file operations
- **JSON output mode:** --json flag outputs structured JSON for parsing
- **Manifest file:** `devforgeai/.install-manifest.json` lists all installed files
- **Report display:** Console summary (interactive), log file (always), JSON (if --json)

### Feature 6: CLAUDE.md Smart Merge
**Description:** Intelligently merge DevForgeAI CLAUDE.md with user's existing content
**User Stories (high-level):**
1. As a user, I want installer to preserve my CLAUDE.md customizations, so I don't lose my instructions
2. As a user, I want clear merge conflict resolution, so I can choose what to keep
3. As a user, I want backup before merge, so I can restore if something goes wrong

**Estimated Effort:** Medium-Large (10-15 story points)

**Acceptance Criteria:**
- **Merge detection:** Detect existing CLAUDE.md, prompt user for strategy (merge/replace/skip/manual)
- **Smart merge:** Parse user sections vs DevForgeAI sections, preserve user content, merge DevForgeAI updates
- **Conflict resolution:** If merge fails, prompt user for manual resolution or replace with backup
- **Backup creation:** Always backup existing CLAUDE.md before modification
- **Merge strategy options:** Auto-merge (default), replace (backup + overwrite), skip (don't touch), manual (user resolves)
- **Merge log:** Document merge decisions in install.log

## Requirements Summary

### Functional Requirements
1. **Wizard UI:** Interactive prompts, progress indicators, color-coded output, confirmation prompts
2. **Pre-Flight Validation:** Python check, disk space, permissions, existing install, git status
3. **Auto-Detection:** Version detection, CLAUDE.md detection, project root, file conflicts
4. **Error Handling:** Taxonomy, user-friendly messages, resolution guidance, automatic rollback
5. **Reporting:** Installation summary, detailed log, JSON output, manifest file
6. **CLAUDE.md Merge:** Detection, smart merge, conflict resolution, backup, strategy options

### Data Model
**Entities:**
- **Installation Config:** Target path, mode (fresh/upgrade/fix/uninstall), merge strategy, options
- **Validation Results:** Checks performed, status (PASS/WARN/FAIL), error messages, resolution steps
- **Installation Manifest:** Files installed, timestamps, checksums, version
- **Merge Result:** Strategy used, sections preserved, sections replaced, conflicts, backup path

**Relationships:**
- Installation Config → Validation Results (one-to-many)
- Installation Config → Installation Manifest (one-to-one, created on success)
- Installation Config → Merge Result (one-to-one, if CLAUDE.md exists)

### Integration Points
1. **Python subprocess:** Invoke existing installer/install.py from Node.js CLI wrapper
2. **Git commands:** Check repository status, detect uncommitted changes
3. **File system:** Read/write files, create backups, check permissions

### Non-Functional Requirements

**Performance:**
- Pre-flight validation: <5 seconds for all checks
- Installation (fresh): <2 minutes including prompts
- CLAUDE.md merge: <10 seconds for typical file (<20KB)
- Progress updates: Every 2-3 seconds for long operations

**Usability:**
- **Clear error messages:** <50 words, includes resolution steps
- **Confirmation prompts:** For all destructive actions (overwrite, uninstall, replace)
- **Color-coded output:** Green (success), yellow (warning), red (error), blue (info)
- **Progress indicators:** Spinners for indeterminate operations, progress bars for file operations

**Reliability:**
- **Atomic transactions:** All-or-nothing installation (no partial state)
- **Automatic rollback:** Restore backup if installation fails
- **Safe rollback:** Rollback tested and succeeds 99%+ of the time

## Architecture Considerations

**Complexity Tier:** 2 (Moderate Application)

**Recommended Architecture:**
- Pattern: Modular Monolith with Validation Pipeline
- Layers: CLI layer (prompts, output), Validation layer (pre-flight checks), Installer layer (install.py), Utilities (backup, rollback, merge)
- Validation Pipeline: Chain of responsibility pattern (check1 → check2 → check3 → install)
- State Management: Track installation state for rollback

**Technology Recommendations (Tier 2):**
- **CLI Framework:** Inquirer.js (interactive prompts), Commander.js (argument parsing)
- **Progress Indicators:** Ora (spinners), CLI-Progress (progress bars)
- **Output Formatting:** Chalk (colors), Boxen (bordered boxes), Table (tabular output)
- **Validation:** Existing Python validator scripts + Node.js wrappers
- **Merge Logic:** Existing installer/merge.py (CLAUDE.md parser)

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| **CLAUDE.md merge conflicts** | HIGH | Implement 4 merge strategies (auto/replace/skip/manual), always backup, provide merge log for audit |
| **Cross-platform bugs (Windows vs Linux)** | HIGH | Test on all 3 platforms in CI (GitHub Actions matrix), use cross-platform libraries (Node.js path module), handle permission differences |
| **Pre-flight checks too strict** | MEDIUM | Distinguish WARN vs ERROR, provide --force flag to override non-critical warnings, document check rationale |
| **Rollback fails leaving broken state** | CRITICAL | Test rollback extensively, use backup manifest to track all changes, implement "surgical rollback" (only undo what was done) |
| **User confusion with wizard prompts** | MEDIUM | User test prompts, provide --help for each prompt, use clear language (avoid jargon), show examples |

## Dependencies

**Prerequisites:**
- EPIC-012: NPM Package Distribution (provides `devforgeai` command as entry point)
- Existing installer code (`installer/install.py`, `installer/merge.py`, `installer/backup.py`, `installer/rollback.py`)

**Dependents:**
- EPIC-014: Version Management & Lifecycle (uses validation and wizard UI for upgrades)

## Success Criteria

### Definition of Done (Epic-Level)
- [ ] Wizard UI functional with prompts for all configuration options
- [ ] Pre-flight validation catches >90% of issues before installation
- [ ] Auto-detection works for existing installs, CLAUDE.md, project root
- [ ] Error messages user-friendly with resolution guidance
- [ ] Automatic rollback works on installation failure
- [ ] Installation success rate >95% across Windows/Mac/Linux
- [ ] CLAUDE.md merge preserves user content in >95% of cases
- [ ] Documentation complete (README, troubleshooting guide)

### User Acceptance
- [ ] Users report installation as "easy" or "very easy" (>90% satisfaction)
- [ ] Installation failures <5% (measured via telemetry or user reports)
- [ ] Support tickets reduced by 60% (fewer installation issues)
- [ ] Error messages clear and actionable (user feedback)

## Next Steps

1. **Story Creation:** Break down 6 features into 12-18 implementable stories
   - Run `/create-story [feature-description]` for each feature
2. **Architecture Phase:** Design validation pipeline, wizard flow, error taxonomy
   - Update `devforgeai/context/architecture-constraints.md` with validation patterns
3. **Sprint Planning:** Assign stories to Sprint 2-3 (after EPIC-012 completes)
   - Run `/create-sprint 2` and select EPIC-013 stories
4. **Implementation:** TDD workflow for each story
   - Run `/dev STORY-XXX` for each story

## Notes

- Reuse existing installer logic (`installer/install.py`) - this epic focuses on UX wrapper
- Existing merge logic (`installer/merge.py`) handles CLAUDE.md parsing - enhance error handling
- Pre-flight validation can reuse devforgeai CLI validators (`devforgeai check-git`, etc.)
- Consider spinner/progress bar libraries: Ora, CLI-Progress, Listr (task lists)
- Error taxonomy should match exit codes (align with existing installer conventions)
