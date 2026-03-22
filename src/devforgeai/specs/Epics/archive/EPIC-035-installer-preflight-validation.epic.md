---
id: EPIC-035
title: Installer Pre-Flight Validation & Platform Detection
epic: EPIC-035
status: Planning
priority: Critical
complexity-score: 4
architecture-tier: Tier 1
start-date: 2025-01-05
target-date: 2025-01-12
estimated-points: 13
target-sprints: 1
created: 2025-01-05
updated: 2025-01-05
---

# Epic: Installer Pre-Flight Validation & Platform Detection

## Business Goal

Prevent installation failures caused by permission errors, insufficient disk space, and cross-filesystem issues (WSL accessing NTFS) by implementing pre-flight validation that catches problems BEFORE deployment begins. Enable graceful degradation and platform-aware error messages.

## Success Metrics

- **Error Prevention:** 100% of permission errors detected before deployment starts
- **Platform Detection:** Correct identification of Windows, macOS, Linux, and WSL environments
- **User Experience:** Platform-specific resolution steps provided for all error scenarios
- **Installation Success:** Reduce failed installations by 90%

**Measurement Plan:**
- Track installation success/failure rates
- Monitor pre-flight check pass/fail counts
- Collect error codes from exit_codes.py usage
- Review frequency: After each release

## Scope

### Overview

Implement comprehensive pre-flight validation for the DevForgeAI installer to detect platform-specific issues before deployment begins, preventing failed installations and providing actionable guidance.

### Features

1. **Feature 1: Security Exclusion Patterns** (3 SP) ✅ COMPLETE
   - Description: Add security-critical files to exclusion patterns
   - User Value: Prevents deployment of files with hardcoded secrets
   - Estimated Points: 3 story points

2. **Feature 2: Platform Detection Module** (3 SP)
   - Description: Detect OS, WSL version, and filesystem type
   - User Value: Enables platform-specific handling and error messages
   - Estimated Points: 3 story points

3. **Feature 3: Pre-Flight Validator** (5 SP)
   - Description: Orchestrate disk space, permission, and compatibility checks
   - User Value: Catches errors before deployment starts
   - Estimated Points: 5 story points

4. **Feature 4: Enhanced Exit Codes** (2 SP)
   - Description: Add exit codes for disk, NTFS, and file lock errors
   - User Value: Enables CI/CD integration and automation
   - Estimated Points: 2 story points

### Out of Scope

- GUI installer (see EPIC-039)
- Build/package phases (see EPIC-036, EPIC-037)
- Registry publishing (see EPIC-038)
- Full installer wizard (see EPIC-039)

## Target Sprints

**Estimated Duration:** 1 sprint / 1 week

**Sprint Breakdown:**
- **Sprint 1:** All Features - 13 story points
  - F1: Security Exclusions (3 SP) - ✅ COMPLETE
  - F2: Platform Detection (3 SP)
  - F3: Pre-Flight Validator (5 SP)
  - F4: Exit Codes (2 SP)

## Dependencies

### External Dependencies

- **Python 3.10+:** Required for installer execution
  - Impact if missing: Installer cannot run

### Internal Dependencies

- **installer/deploy.py:** Security exclusions applied ✅
  - Status: Complete
  - Impact if missing: Security files deployed

### Blocking Issues

- None identified

## Stakeholders

- **Product Owner:** DevForgeAI Framework Team
- **Tech Lead:** Claude (AI orchestration)
- **Users:** DevForgeAI installers (Windows, macOS, Linux, WSL)

## Requirements

### Functional Requirements

#### User Stories

**User Story 1:**
```
As a developer installing DevForgeAI on WSL,
I want the installer to detect cross-filesystem issues,
So that I receive actionable guidance instead of cryptic permission errors.
```

**Acceptance Criteria:**
- [ ] Installer detects when target is on /mnt/c (NTFS via WSL)
- [ ] Warning displayed with resolution steps
- [ ] chmod operations skipped with explanation

**User Story 2:**
```
As a CI/CD pipeline operator,
I want specific exit codes for different failure types,
So that I can implement appropriate retry or fallback logic.
```

**Acceptance Criteria:**
- [ ] Exit code 5 for disk space errors
- [ ] Exit code 6 for NTFS permission errors
- [ ] Exit code 7 for file lock errors

**User Story 3:**
```
As a DevForgeAI user,
I want pre-flight validation before installation begins,
So that I don't waste time on installations that will fail.
```

**Acceptance Criteria:**
- [ ] Disk space checked (minimum 25MB)
- [ ] Write permission probed via temp file
- [ ] Platform compatibility validated

### Non-Functional Requirements (NFRs)

#### Performance
- **Pre-flight validation:** < 2 seconds total
- **Platform detection:** < 100ms
- **Disk space check:** < 500ms

#### Compatibility
- **Windows 10+:** Full support
- **macOS 11+:** Full support
- **Linux:** Ubuntu, Debian, RHEL, Arch supported
- **WSL 1/2:** Full support with NTFS handling

## Architecture Considerations

### Complexity Tier
**Tier 1: Simple Enhancement**
- **Score:** 4/60 points
- **Rationale:** Adds validation layer to existing installer without architectural changes

### Recommended Technology Stack

**Backend:**
- **Language:** Python 3.10+ (stdlib only)
- **Detection:** Platform-specific APIs (platform, os modules)
- **Validation:** File I/O operations for probing

### Technology Constraints

- **Constraint 1:** Zero external Python dependencies (per dependencies.md)
- **Constraint 2:** Must work on all supported platforms

## Risks & Constraints

### Technical Risks

**Risk 1: WSL Detection Unreliable**
- **Description:** /proc/version parsing may fail on some configurations
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:** Multiple detection methods (env vars, filesystem checks)

**Risk 2: Permission Probe Creates Orphan Files**
- **Description:** Test file creation may leave artifacts
- **Probability:** Low
- **Impact:** Low
- **Mitigation:** Always clean up in finally block, use unique filenames

### Constraints

**Constraint 1: No External Dependencies**
- **Description:** Cannot add pip packages to installer
- **Impact:** Limited to Python stdlib functionality
- **Mitigation:** Use platform, os, pathlib modules

## Assumptions

1. Python 3.10+ is available on target systems
2. User has at least read access to target directory
3. WSL users accessing /mnt/c expect some limitations

## Next Steps

### Immediate Actions
1. **Create platform_detector.py:** Implement OS/WSL/filesystem detection
2. **Create preflight.py:** Implement validation orchestrator
3. **Update exit_codes.py:** Add codes 5-7

### Pre-Development Checklist
- [x] Architecture context files validated
- [ ] Stories created in devforgeai/specs/Stories/
- [ ] Unit tests planned for detection logic
- [ ] Integration tests planned for WSL scenarios

### Development Workflow
Stories will progress through:
1. **Ready for Dev** → devforgeai-development (TDD implementation)
2. **Dev Complete** → devforgeai-qa (quality validation)
3. **QA Approved** → devforgeai-release (deployment)

## Files to Create/Modify

| Component | Path | Action | Size Target |
|-----------|------|--------|-------------|
| Platform Detector | `installer/platform_detector.py` | CREATE | ~150 lines |
| Pre-Flight Validator | `installer/preflight.py` | CREATE | ~200 lines |
| Exit Codes | `installer/exit_codes.py` | MODIFY | +15 lines |
| Deploy Module | `installer/deploy.py` | MODIFIED | ✅ Complete |

## Stories

| Story ID | Title | Points | Feature | Status |
|----------|-------|--------|---------|--------|
| STORY-235 | Platform Detection Module | 3 | F2 | Backlog |
| STORY-236 | Pre-Flight Validator | 5 | F3 | Backlog |
| STORY-237 | Enhanced Exit Codes | 2 | F4 | Backlog |

**Note:** Feature 1 (Security Exclusion Patterns) was completed as a Quick Win without a formal story.

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | In Progress | 13 | 4 | 1 | 0 | 0 |
| **Total** | **23%** | **13** | **4** | **1** | **0** | **0** |

### Burndown
- **Total Points:** 13
- **Completed:** 3 (Feature 1 - Quick Win)
- **Remaining:** 10 (STORY-235: 3, STORY-236: 5, STORY-237: 2)
- **Velocity:** TBD

## Notes

- Quick Win (security exclusions) already applied to deploy.py
- Platform detector should handle edge cases like Docker-in-WSL
- Consider caching platform detection results for performance

---

**Epic Status:**
- 🔵 **Planning** - Requirements being defined

**Last Updated:** 2025-01-05 by Claude
**Plan Reference:** /home/bryan/.claude/plans/dazzling-juggling-ritchie.md
