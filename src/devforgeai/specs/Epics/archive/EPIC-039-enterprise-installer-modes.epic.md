---
id: EPIC-039
title: Enterprise Installer Modes
epic: EPIC-039
status: Planning
priority: Medium
complexity-score: 8
architecture-tier: Tier 3
start-date: 2025-02-17
target-date: 2025-03-03
estimated-points: 34
target-sprints: 3
created: 2025-01-05
updated: 2025-01-05
depends-on: EPIC-035, EPIC-037
---

# Epic: Enterprise Installer Modes

## Business Goal

Provide enterprise-grade installation experiences including CLI wizard, graphical UI, and silent/headless modes for CI/CD automation. Enable offline/air-gapped installation, upgrade/repair/uninstall operations, and configuration-driven deployments suitable for enterprise environments.

## Success Metrics

- **Installation Modes:** 4 modes working (CLI, Wizard, GUI, Silent)
- **Enterprise Features:** Upgrade, repair, uninstall operations functional
- **Offline Support:** 100% functionality without network access
- **CI/CD Integration:** Silent mode completes in <60 seconds
- **User Satisfaction:** 90%+ success rate across all modes

**Measurement Plan:**
- Track installation success rates per mode
- Monitor upgrade path completion rates
- Measure installation time per mode
- Collect user feedback on installation experience
- Review frequency: After each release

## Scope

### Overview

Implement multiple installation modes (CLI, Wizard, GUI, Silent) along with enterprise maintenance operations (upgrade, repair, uninstall) and offline installation support.

### Features

1. **Feature 1: CLI Wizard Installer** (8 SP)
   - Description: Step-by-step terminal interface with component selection
   - User Value: Guided installation for first-time users
   - Estimated Points: 8 story points

2. **Feature 2: GUI Installer Template** (8 SP)
   - Description: Electron-based cross-platform installer template
   - User Value: Native desktop installation experience
   - Estimated Points: 8 story points

3. **Feature 3: Silent/Headless Installer** (5 SP)
   - Description: Configuration-driven installation for CI/CD
   - User Value: Automated deployments without interaction
   - Estimated Points: 5 story points

4. **Feature 4: Offline Installation Mode** (5 SP)
   - Description: Bundle all dependencies for air-gapped networks
   - User Value: Installation without internet access
   - Estimated Points: 5 story points

5. **Feature 5: Maintenance Operations** (8 SP)
   - Description: Upgrade, repair, uninstall, and rollback
   - User Value: Complete lifecycle management
   - Estimated Points: 8 story points

### Out of Scope

- Actual Electron implementation (provides template)
- Windows MSI custom actions (use WiX defaults)
- Auto-update service (future epic)
- Remote deployment (use silent mode + scripts)
- License key validation (open source project)

## Target Sprints

**Estimated Duration:** 3 sprints / 2-3 weeks

**Sprint Breakdown:**
- **Sprint 1:** CLI & Silent Modes (13 SP)
  - F1: CLI Wizard (8 SP) - 4 stories
  - F3: Silent Installer (5 SP) - 3 stories
- **Sprint 2:** GUI & Offline Modes (13 SP)
  - F2: GUI Template (8 SP) - 4 stories
  - F4: Offline Mode (5 SP) - 3 stories
- **Sprint 3:** Maintenance Operations (8 SP)
  - F5: Upgrade/Repair/Uninstall (8 SP) - 4 stories

## Dependencies

### External Dependencies

- **Node.js/Electron (GUI only):** For GUI template
  - Owner: User
  - Impact if missing: Skip GUI mode
- **inquirer (optional):** For enhanced CLI wizard
  - Owner: Framework
  - Impact if missing: Use basic input()

### Internal Dependencies

- **EPIC-035:** Pre-flight validation (used by all modes)
  - Status: In Progress
  - Impact if missing: No validation before install
- **EPIC-037:** Package Phase (provides installable packages)
  - Status: Not Started
  - Impact if missing: No packages to install

### Blocking Issues

- None identified

## Stakeholders

- **Product Owner:** DevForgeAI Framework Team
- **Tech Lead:** Claude (AI orchestration)
- **Users:** Enterprise developers, DevOps engineers, first-time users

## Requirements

### Functional Requirements

#### User Stories

**User Story 1:**
```
As a first-time DevForgeAI user,
I want a guided wizard installation,
So that I can configure my project step-by-step without reading documentation.
```

**Acceptance Criteria:**
- [ ] Wizard displays welcome screen
- [ ] Component selection with checkboxes
- [ ] Progress bar during installation
- [ ] Success/failure summary at end

**User Story 2:**
```
As a DevOps engineer,
I want a silent installation mode,
So that I can automate DevForgeAI deployments in CI/CD pipelines.
```

**Acceptance Criteria:**
- [ ] Silent mode accepts YAML config file
- [ ] No interactive prompts
- [ ] Exit codes match exit_codes.py
- [ ] Log file generated

**User Story 3:**
```
As an enterprise administrator,
I want offline installation support,
So that I can deploy to air-gapped networks without internet access.
```

**Acceptance Criteria:**
- [ ] Offline bundle includes all files
- [ ] Checksum validation from bundle
- [ ] No network calls during installation
- [ ] Same features as online mode

**User Story 4:**
```
As a DevForgeAI user with a corrupted installation,
I want a repair operation,
So that I can fix my installation without losing configuration.
```

**Acceptance Criteria:**
- [ ] Repair detects missing/corrupted files
- [ ] Repair preserves user configurations
- [ ] Repair restores files from bundle
- [ ] Report of repaired files generated

### Non-Functional Requirements (NFRs)

#### Performance
- **CLI wizard:** < 30 seconds (excluding downloads)
- **Silent mode:** < 60 seconds
- **GUI launch:** < 5 seconds
- **Offline validation:** < 10 seconds
- **Upgrade:** < 2 minutes

#### Compatibility
- **CLI:** All platforms with Python 3.10+
- **GUI:** Windows 10+, macOS 11+, Ubuntu 20.04+
- **Silent:** All platforms with bash/PowerShell

## Architecture Considerations

### Complexity Tier
**Tier 3: Significant Enhancement**
- **Score:** 8/60 points
- **Rationale:** Multiple installation modes with enterprise features

### Installation Mode Matrix

| Mode | Interface | Interaction | Use Case |
|------|-----------|-------------|----------|
| CLI | Terminal | Interactive | Developer setup |
| Wizard | Terminal | Step-by-step | First-time users |
| GUI | Desktop window | Point-and-click | Non-technical users |
| Silent | None | Config file | CI/CD automation |

### Wizard Step Flow

```
Step 1: Welcome
  ↓
Step 2: License Agreement
  ↓
Step 3: Installation Path
  ↓
Step 4: Component Selection
  □ Core Framework (.claude/, devforgeai/)
  □ CLI Tools (devforgeai command)
  □ Templates (project templates)
  □ Examples (example projects)
  ↓
Step 5: Configuration Options
  □ Initialize Git repository
  □ Create initial commit
  □ Run validation after install
  ↓
Step 6: Installation Progress
  [████████████████████] 100%
  ↓
Step 7: Completion
  ✓ Installation successful!
```

### Recommended Technology Stack

**CLI Wizard:**
- **Language:** Python 3.10+ (stdlib)
- **UI:** inquirer or native input()

**GUI Template:**
- **Framework:** Electron
- **Packaging:** electron-builder

**Silent Mode:**
- **Config:** YAML/JSON
- **Logging:** Python logging module

### Technology Constraints

- **Constraint 1:** Python stdlib for core installer
- **Constraint 2:** Electron for GUI only (template)
- **Constraint 3:** No new Python dependencies

## Risks & Constraints

### Technical Risks

**Risk 1: Electron Bundle Size Too Large**
- **Description:** Electron adds 150MB+ to installer
- **Probability:** High
- **Impact:** Medium
- **Mitigation:** Use electron-builder, exclude dev dependencies

**Risk 2: Silent Mode Config Validation Failures**
- **Description:** Invalid config silently fails
- **Probability:** Medium
- **Impact:** High
- **Mitigation:** JSON Schema validation, dry-run mode

**Risk 3: Offline Bundle Integrity Issues**
- **Description:** Corrupted bundles cause failures
- **Probability:** Low
- **Impact:** High
- **Mitigation:** SHA256 checksums for all files

**Risk 4: Upgrade Path Breaking Changes**
- **Description:** Old version incompatible with new
- **Probability:** Medium
- **Impact:** High
- **Mitigation:** Version compatibility matrix, migration scripts

### Constraints

**Constraint 1: No New Python Dependencies**
- **Description:** Core installer must be stdlib only
- **Impact:** Limited TUI capabilities
- **Mitigation:** Use inquirer optionally, fall back to input()

## Assumptions

1. Python 3.10+ available on target systems
2. Users have write access to installation directory
3. Electron available for GUI mode (optional)

## CLI Examples

### Wizard Mode (Interactive)
```bash
python -m installer wizard /path/to/project
# Launches step-by-step wizard
```

### Silent Mode (CI/CD)
```bash
python -m installer install /path/to/project \
  --silent \
  --config install-config.yaml \
  --log install.log

# Or with environment variables
DEVFORGEAI_TARGET=/path/to/project \
DEVFORGEAI_COMPONENTS=core,cli \
python -m installer install --silent
```

### Silent Config File
```yaml
# install-config.yaml
target: /path/to/project
components:
  - core
  - cli
options:
  initialize-git: true
  create-backup: true
  run-validation: true
```

### Maintenance Operations
```bash
# Upgrade to latest version
python -m installer upgrade /path/to/project

# Repair corrupted installation
python -m installer repair /path/to/project

# Uninstall completely
python -m installer uninstall /path/to/project

# Rollback to previous version
python -m installer rollback /path/to/project --version 1.2.3
```

## GitHub Actions Integration

### Example Workflow
```yaml
name: DevForgeAI Installation
on: [push]

jobs:
  install:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install DevForgeAI
        run: |
          pip install devforgeai-installer
          devforgeai install . \
            --silent \
            --components core,cli \
            --log install.log

      - name: Validate Installation
        run: devforgeai validate .

      - name: Upload Install Log
        uses: actions/upload-artifact@v4
        with:
          name: install-log
          path: install.log
```

## Next Steps

### Immediate Actions
1. **Create installer/wizard.py:** CLI wizard implementation
2. **Create installer/silent.py:** Silent mode implementation
3. **Create installer-gui/:** Electron template

### Pre-Development Checklist
- [x] Architecture context files validated
- [ ] EPIC-035 dependencies met
- [ ] EPIC-037 dependencies met
- [x] Stories created in devforgeai/specs/Stories/

## Stories

| Story ID | Title | Points | Status | Depends On |
|----------|-------|--------|--------|------------|
| STORY-247 | CLI Wizard Installer | 8 | Backlog | STORY-235, STORY-236, STORY-237 |
| STORY-248 | GUI Installer Template | 8 | Backlog | STORY-247 |
| STORY-249 | Silent/Headless Installer | 5 | Backlog | STORY-235, STORY-236 |
| STORY-250 | Offline Installation Mode | 5 | Backlog | STORY-249 |
| STORY-251 | Maintenance Operations | 8 | Backlog | STORY-247, STORY-249, STORY-250 |
| **Total** | | **34** | | |

### Development Workflow
Stories will progress through:
1. **Ready for Dev** → devforgeai-development (TDD implementation)
2. **Dev Complete** → devforgeai-qa (quality validation)
3. **QA Approved** → devforgeai-release (deployment)

## Files to Create

| Component | Path | Action | Size Target |
|-----------|------|--------|-------------|
| CLI Wizard | `installer/wizard.py` | CREATE | ~300 lines |
| Silent Mode | `installer/silent.py` | CREATE | ~200 lines |
| Offline Mode | `installer/offline.py` | CREATE | ~150 lines |
| Upgrade | `installer/upgrade.py` | CREATE | ~200 lines |
| Repair | `installer/repair.py` | CREATE | ~150 lines |
| Uninstall | `installer/uninstall.py` | CREATE | ~150 lines |
| Main Entry | `installer/__main__.py` | MODIFY | +100 lines |
| GUI App | `installer-gui/main.js` | CREATE | ~200 lines |
| GUI Package | `installer-gui/package.json` | CREATE | ~50 lines |
| GUI HTML | `installer-gui/index.html` | CREATE | ~300 lines |

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 13 | 7 | 0 | 0 | 0 |
| Sprint 2 | Not Started | 13 | 7 | 0 | 0 | 0 |
| Sprint 3 | Not Started | 8 | 4 | 0 | 0 | 0 |
| **Total** | **0%** | **34** | **18** | **0** | **0** | **0** |

### Burndown
- **Total Points:** 34
- **Completed:** 0
- **Remaining:** 34
- **Velocity:** TBD

## Notes

- GUI template is optional - most users will use CLI or Silent
- Offline mode is critical for enterprise air-gapped environments
- Consider creating video tutorials for wizard mode

---

**Epic Status:**
- ⚪ **Planning** - Requirements being defined

**Last Updated:** 2025-01-05 by Claude
**Plan Reference:** /home/bryan/.claude/plans/dazzling-juggling-ritchie.md
