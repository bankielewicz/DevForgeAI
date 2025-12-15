---
id: EPIC-014
title: Version Management & Installation Lifecycle
business-value: Enable seamless upgrades and lifecycle management, reducing version-related issues by 80%+
status: Planning
priority: High
complexity-score: 28
architecture-tier: Tier 2 (Moderate Application)
created: 2025-11-25
estimated-points: 30-40
target-sprints: 3-5 sprints
dependencies: ["EPIC-012", "EPIC-013"]
---

# Version Management & Installation Lifecycle

## Business Goal

Provide complete installation lifecycle management (install → upgrade → fix → uninstall) with version-aware intelligence, reducing version-related issues from 30%+ to <5% and enabling confident upgrades.

**Success Metrics:**
- Upgrade success rate: >95% across version pairs
- Version detection accuracy: 100% (correctly identifies installed version)
- Rollback success rate: >99% (restore previous version on upgrade failure)
- Uninstall completeness: 100% (removes all DevForgeAI files, preserves user content)

## Problem Statement

Current DevForgeAI lacks version management:
1. **No version detection:** Can't identify installed version or detect upgrades
2. **No upgrade path:** Manual process to upgrade between versions
3. **No migration scripts:** Version-specific changes require manual intervention
4. **No rollback:** Failed upgrades leave broken installations
5. **No repair capability:** Can't fix corrupted installations
6. **No uninstall:** Manual removal of files, easy to miss files or delete user content

This leads to:
- Users stuck on old versions (fear of breaking changes)
- Failed upgrades breaking projects (30%+ upgrade failure rate)
- Support burden from version conflicts
- Orphaned files after manual removal attempts

## Features

### Feature 1: Version Detection & Compatibility Checking
**Description:** Detect installed version and validate upgrade path compatibility
**User Stories (high-level):**
1. As a user, I want installer to detect my current version, so I'm prompted to upgrade instead of fresh install
2. As a user, I want to see version comparison (current vs available), so I know what's changing
3. As a user, I want incompatible upgrades blocked, so I don't break my installation

**Estimated Effort:** Medium (8-12 story points)

**Acceptance Criteria:**
- Read `.devforgeai/.version.json` to identify installed version
- Parse version strings (semver: major.minor.patch, e.g., 1.2.3)
- Validate upgrade path (e.g., can't downgrade major version without --force)
- Display version comparison: "Upgrading from v1.0.0 → v1.1.0"
- Detect breaking changes (major version bump) and warn user
- Block unsafe downgrades (major version decrease) unless --force
- Support pre-release versions (beta, RC): v1.1.0-beta.1

### Feature 2: Upgrade Mode with Migration Scripts
**Description:** Execute version-aware upgrades with automatic migrations
**User Stories (high-level):**
1. As a user, I want to upgrade to latest version, so I get new features and bug fixes
2. As a user, I want migration scripts to run automatically, so I don't have to manually update files
3. As a user, I want backup before upgrade, so I can rollback if something breaks

**Estimated Effort:** Large (15-20 story points)

**Acceptance Criteria:**
- Detect upgrade scenario (existing version < source version)
- Create backup before upgrade (includes old version for rollback)
- Run version-specific migration scripts (e.g., `migrations/v1.0-to-v1.1.py`)
- Migration types: file moves, config updates, schema changes, deprecation handling
- Validate migration success (check expected files exist, schemas valid)
- Update `.version.json` with new version and upgrade timestamp
- Rollback automatically if migration fails
- Display upgrade summary: files added/updated/removed, migrations executed

### Feature 3: Fix/Repair Installation Mode
**Description:** Detect and repair corrupted or incomplete installations
**User Stories (high-level):**
1. As a user, I want to run `devforgeai fix`, so I can repair corrupted installation
2. As a user, I want fix mode to detect missing files, so I know what's wrong
3. As a user, I want fix mode to restore missing files, so installation works again

**Estimated Effort:** Medium (10-15 story points)

**Acceptance Criteria:**
- Validate installation integrity: check manifest vs actual files
- Detect issues: missing files, corrupted files (checksum mismatch), wrong versions
- Repair strategies: restore missing files, fix checksums, update broken links
- Non-destructive: don't overwrite user-modified files (prompt for confirmation)
- Display repair report: issues found, actions taken, remaining issues (if any)
- Update installation manifest after repair
- Exit code 0 if fully repaired, 1 if partially repaired (manual intervention needed)

### Feature 4: Rollback to Previous Version
**Description:** Restore previous version if upgrade fails or user wants to revert
**User Stories (high-level):**
1. As a user, I want automatic rollback on upgrade failure, so I'm not left with broken installation
2. As a user, I want to manually rollback, so I can revert bad upgrade
3. As a user, I want to see rollback options, so I know which backup to restore

**Estimated Effort:** Medium-Large (12-18 story points)

**Acceptance Criteria:**
- Automatic rollback: triggered when upgrade fails (validation error, migration error)
- Manual rollback: `devforgeai rollback` command restores previous version
- List available backups: show version, backup date, backup size
- Restore from backup: copy files back, revert `.version.json`, validate restoration
- Preserve user content: don't overwrite user-created stories, epics, context files
- Rollback validation: verify restored version works (run smoke tests)
- Display rollback summary: version restored, files restored, validation status

### Feature 5: Uninstall with User Content Preservation
**Description:** Clean removal of DevForgeAI with option to preserve user-created content
**User Stories (high-level):**
1. As a user, I want to uninstall DevForgeAI cleanly, so no orphaned files remain
2. As a user, I want to preserve my stories/epics/context files, so I don't lose my work
3. As a user, I want dry-run mode, so I can see what would be removed before confirming

**Estimated Effort:** Medium (10-15 story points)

**Acceptance Criteria:**
- Detect all installed files via manifest (`.devforgeai/.install-manifest.json`)
- Uninstall modes:
  - **Complete removal:** Remove all DevForgeAI files (.claude/, .devforgeai/, CLI, CLAUDE.md)
  - **Preserve user content:** Keep user-created stories, epics, custom context files, ADRs
- Dry-run mode: `devforgeai uninstall --dry-run` shows what would be removed
- Confirmation prompt: list files to remove, ask for confirmation (unless --yes flag)
- Backup before uninstall: create backup in case user wants to re-install
- Display uninstall summary: files removed, files preserved, backup location
- Cleanup: remove empty directories, clean up PATH/bin entries

### Feature 6: Version-Aware Configuration Management
**Description:** Persist user preferences and configuration across upgrades
**User Stories (high-level):**
1. As a user, I want my install preferences remembered, so I don't re-enter them on upgrade
2. As a user, I want configuration migrated automatically, so upgrades don't break my settings
3. As a user, I want to export/import configuration, so I can replicate setup across projects

**Estimated Effort:** Small-Medium (5-8 story points)

**Acceptance Criteria:**
- Store user preferences: target path, merge strategy, optional features enabled
- Configuration file: `.devforgeai/.install-config.json` (user preferences)
- Migrate configuration on upgrade: convert old format to new format if schema changes
- Export configuration: `devforgeai config export > config.json`
- Import configuration: `devforgeai config import config.json`
- Configuration validation: reject invalid configs with clear error messages

## Requirements Summary

### Functional Requirements
1. **Version Detection:** Read .version.json, parse semver, validate upgrade paths
2. **Upgrade Mode:** Backup, run migrations, update version, rollback on failure
3. **Fix Mode:** Validate integrity, detect issues, repair automatically
4. **Rollback:** Automatic (on failure) + manual, restore from backup, validate restoration
5. **Uninstall:** Complete removal or preserve user content, dry-run mode, backup
6. **Configuration:** Persist preferences, migrate on upgrade, export/import

### Data Model
**Entities:**
- **Version Metadata (.version.json):** version, installed_at, mode, schema_version
- **Installation Manifest (.install-manifest.json):** files (path, checksum, size), directories, version
- **Backup Metadata (.backup-manifest.json):** backup_path, from_version, to_version, timestamp, reason
- **User Configuration (.install-config.json):** target_path, merge_strategy, options, preferences

**Relationships:**
- Installation → Version Metadata (one-to-one, current version)
- Installation → Manifests (one-to-many, one per version)
- Installation → Backups (one-to-many, one per upgrade/uninstall)
- Installation → Configuration (one-to-one, user preferences)

### Integration Points
1. **Backup system:** Create/restore backups via installer/backup.py
2. **Rollback system:** Revert changes via installer/rollback.py
3. **Migration system:** Execute version-specific scripts in migrations/ directory
4. **Git:** Check repository status, create commits for version milestones

### Non-Functional Requirements

**Performance:**
- Version detection: <1 second
- Upgrade (without migrations): <2 minutes
- Upgrade (with migrations): <5 minutes (depends on migration complexity)
- Rollback: <1 minute
- Uninstall: <30 seconds

**Reliability:**
- **Rollback success rate: >99%** (must reliably restore previous version)
- **Upgrade success rate: >95%** (most upgrades complete without issues)
- **Fix mode success rate: >90%** (can repair most common issues)
- **Uninstall completeness: 100%** (removes all files, no orphans)

**Backward Compatibility:**
- Support upgrades from v1.0.0 to current version (no skipping required)
- Maintain .version.json schema compatibility (version schema_version field if format changes)
- Detect old installations without .version.json (pre-v1.0.0), prompt for version

## Architecture Considerations

**Complexity Tier:** 2 (Moderate Application)

**Recommended Architecture:**
- Pattern: State Machine (Installation States: Fresh → Upgrade → Fix → Uninstall)
- Layers: CLI layer (commands), State Management (track installation state), Migration Engine (run version scripts), Backup/Rollback (restore state)
- Migration System: Convention-based (migrations/v1.0-to-v1.1.py), executed in order

**Technology Recommendations (Tier 2):**
- **Version Parsing:** Semver.js (semantic versioning)
- **State Management:** FSM (finite state machine) pattern for installation states
- **Migration Engine:** Python scripts in migrations/ directory, invoked by installer
- **Backup System:** Existing installer/backup.py (create/restore backups)
- **Rollback System:** Existing installer/rollback.py (revert changes)

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Version migration complexity** | HIGH | Create migration testing framework, test all version pairs, provide migration validator |
| **Rollback fails leaving broken state** | CRITICAL | Test rollback extensively, create backup before every operation, validate rollback success |
| **User content accidentally deleted during uninstall** | CRITICAL | Implement content-type detection (framework vs user), dry-run mode mandatory, confirmation prompts |
| **Migration script errors** | HIGH | Wrap migrations in try/catch, rollback on error, log detailed migration errors, provide manual migration guide |
| **Incompatible version downgrades** | MEDIUM | Block dangerous downgrades, require --force for downgrades, warn about breaking changes |

## Dependencies

**Prerequisites:**
- EPIC-012: NPM Package Distribution (provides version metadata in package)
- EPIC-013: Interactive Installer & Validation (provides wizard UI for upgrade prompts)
- Existing installer code (`installer/backup.py`, `installer/rollback.py`, `installer/version.py`)

**Dependents:**
- None (this is the final epic in installer enhancement initiative)

## Success Criteria

### Definition of Done (Epic-Level)
- [ ] Version detection works for all installations (including pre-v1.0.0)
- [ ] Upgrade mode functional with migration script support
- [ ] Fix mode can repair >90% of common issues
- [ ] Rollback works automatically on upgrade failure and manually on demand
- [ ] Uninstall removes all files with option to preserve user content
- [ ] Configuration persisted and migrated across upgrades
- [ ] Upgrade success rate >95%, rollback success rate >99%
- [ ] Documentation complete (upgrade guide, migration guide, troubleshooting)

### User Acceptance
- [ ] Users can upgrade confidently (>90% report "easy" upgrade experience)
- [ ] Rollback provides safety net (users trust they can revert if needed)
- [ ] Uninstall clean and predictable (no surprise deletions)
- [ ] Version-related support tickets reduced by 80%

## Stories

**6 stories created (2025-11-25):**

| Story ID | Title | Points | Status |
|----------|-------|--------|--------|
| [STORY-077](../Stories/STORY-077-version-detection-compatibility.story.md) | Version Detection & Compatibility Checking | 10 | Backlog |
| [STORY-078](../Stories/STORY-078-upgrade-mode-migration-scripts.story.md) | Upgrade Mode with Migration Scripts | 13 | Backlog |
| [STORY-079](../Stories/STORY-079-fix-repair-installation-mode.story.md) | Fix/Repair Installation Mode | 10 | Backlog |
| [STORY-080](../Stories/STORY-080-rollback-previous-version.story.md) | Rollback to Previous Version | 12 | Backlog |
| [STORY-081](../Stories/STORY-081-uninstall-user-content-preservation.story.md) | Uninstall with User Content Preservation | 10 | Backlog |
| [STORY-082](../Stories/STORY-082-version-aware-config-management.story.md) | Version-Aware Configuration Management | 8 | Backlog |

**Total Story Points:** 63 points

**Recommended Implementation Order:**
1. STORY-077 (Version Detection) - Foundation for all other features
2. STORY-078 (Upgrade Mode) - Core upgrade capability + backup infrastructure
3. STORY-082 (Config Management) - Configuration persistence for upgrades
4. STORY-080 (Rollback) - Safety net using backup infrastructure
5. STORY-079 (Fix/Repair) - Uses manifest infrastructure from upgrade
6. STORY-081 (Uninstall) - Final cleanup capability

## Next Steps

1. ~~**Story Creation:** Break down 6 features into 15-20 implementable stories~~ ✅ COMPLETE
   - 6 stories created covering all features
2. **Architecture Phase:** Design migration system, state machine, rollback validation
   - Update `devforgeai/context/architecture-constraints.md` with state management patterns
3. **Sprint Planning:** Assign stories to Sprint 3-5 (after EPIC-012 and EPIC-013)
   - Run `/create-sprint 3` and select EPIC-014 stories
4. **Implementation:** TDD workflow for each story
   - Run `/dev STORY-XXX` for each story

## Notes

- Reuse existing backup/rollback code (`installer/backup.py`, `installer/rollback.py`)
- Migration scripts convention: `migrations/vX.Y-to-vA.B.py` (e.g., `v1.0-to-v1.1.py`)
- Version metadata format already defined (`.version.json`) - extend if needed
- Consider migration testing framework: apply migration, rollback, re-apply (idempotency test)
- Uninstall must preserve: `devforgeai/specs/Stories/`, `devforgeai/specs/Epics/`, `devforgeai/specs/Sprints/`, user ADRs, custom context files
- Uninstall should remove: `.claude/`, `.devforgeai/` (framework files), `CLAUDE.md` (if DevForgeAI-managed), CLI binaries
