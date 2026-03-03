---
id: EPIC-037
title: Release Skill Package & Installer Generation
epic: EPIC-037
status: Planning
priority: High
complexity-score: 7
architecture-tier: Tier 2
start-date: 2025-01-27
target-date: 2025-02-10
estimated-points: 26
target-sprints: 2
created: 2025-01-05
updated: 2025-01-05
depends-on: EPIC-036
---

# Epic: Release Skill Package & Installer Generation

## Business Goal

Enable the devforgeai-release skill to create distributable packages in multiple formats (npm, pip, NuGet, Docker, MSI, deb, rpm) and generate installer configurations. This transforms built artifacts into deployable packages for various distribution channels and enterprise installation scenarios.

## Success Metrics

- **Package Formats:** Support 8+ package formats (npm, pip, NuGet, jar, deb, rpm, Docker, zip)
- **Platform Coverage:** Generate packages for Windows, Linux, macOS
- **Installer Modes:** Support CLI, Wizard, GUI, and Silent installation modes
- **Zero External Tools:** Use only native system package tools (npm, pip, docker, etc.)

**Measurement Plan:**
- Track successful package creation per format
- Monitor cross-platform package generation
- Measure installer configuration completeness
- Review frequency: End of each sprint

## Scope

### Overview

Add Phase 0.3 (Package Creation) and Phase 0.4 (Installer Generation) to the devforgeai-release skill, enabling multi-format packaging and installer mode configuration.

### Features

1. **Feature 1: Language-Specific Package Creation (Phase 0.3)** (10 SP)
   - Description: Create packages for npm, pip, NuGet, Docker, etc.
   - User Value: Distribution-ready packages for all channels
   - Estimated Points: 10 story points

2. **Feature 2: OS-Specific Installer Generation (Phase 0.4a)** (8 SP)
   - Description: Generate installer configs for Windows, Linux, macOS
   - User Value: Native installation experience per platform
   - Estimated Points: 8 story points

3. **Feature 3: Installer Mode Configuration (Phase 0.4b)** (8 SP)
   - Description: Support CLI, Wizard, GUI, Silent installation modes
   - User Value: Flexible installation for different user types
   - Estimated Points: 8 story points

### Out of Scope

- Registry publishing (see EPIC-038)
- Actual GUI implementation (provides templates only)
- Code signing (enterprise feature, future epic)
- Auto-update mechanisms (future epic)

## Target Sprints

**Estimated Duration:** 2 sprints / 2 weeks

**Sprint Breakdown:**
- **Sprint 1:** Package Creation (10 SP) - 5 stories
- **Sprint 2:** Installer Generation (16 SP) - 8 stories

## Dependencies

### External Dependencies

- **Package tools installed:** npm, pip, dotnet, mvn, docker
  - Owner: User's development environment
  - Impact if missing: Skip unsupported formats with warning
- **Installer tools (optional):** WiX, NSIS, dpkg-deb, rpmbuild
  - Owner: User's build environment
  - Impact if missing: Generate config only, skip build

### Internal Dependencies

- **EPIC-036:** Build Phase complete (provides build artifacts)
  - Status: Not Started
  - Impact if missing: No artifacts to package

### Blocking Issues

- None identified

## Stakeholders

- **Product Owner:** DevForgeAI Framework Team
- **Tech Lead:** Claude (AI orchestration)
- **Users:** Developers packaging for distribution

## Requirements

### Functional Requirements

#### User Stories

**User Story 1:**
```
As a developer with a Node.js library,
I want to create an npm package automatically,
So that I can publish to npm registry.
```

**Acceptance Criteria:**
- [ ] npm pack executed for Node.js projects
- [ ] .tgz file generated with correct name/version
- [ ] package.json validated before packing

**User Story 2:**
```
As a developer distributing to enterprises,
I want multiple installer formats generated,
So that users on different platforms have native installers.
```

**Acceptance Criteria:**
- [ ] Windows: MSI and/or EXE installer configs generated
- [ ] Linux: deb and rpm package configs generated
- [ ] macOS: pkg and/or dmg configs generated

**User Story 3:**
```
As a DevOps engineer,
I want a silent installer mode,
So that I can automate installations in CI/CD pipelines.
```

**Acceptance Criteria:**
- [ ] Silent mode accepts config file
- [ ] No interactive prompts in silent mode
- [ ] Exit code indicates success/failure

### Non-Functional Requirements (NFRs)

#### Performance
- **Package creation:** < 60 seconds per format
- **Installer config generation:** < 10 seconds
- **Docker image build:** Varies (no timeout)

#### Compatibility
- **Windows:** MSI (WiX), EXE (NSIS/Inno Setup)
- **Linux:** deb (dpkg-deb), rpm (rpmbuild)
- **macOS:** pkg (pkgbuild), dmg (hdiutil)
- **Cross-platform:** Docker images

## Architecture Considerations

### Complexity Tier
**Tier 2: Moderate Enhancement**
- **Score:** 7/60 points
- **Rationale:** Adds packaging and installer modes with cross-platform support

### Package Format Matrix

| Tech Stack | Primary Package | Secondary Package |
|------------|-----------------|-------------------|
| Node.js | `.tgz` (npm pack) | `.zip`, Docker |
| Python | `.whl`, `.tar.gz` | `.exe` (PyInstaller), Docker |
| .NET | `.nupkg` | `.exe`, `.msi`, Docker |
| Java | `.jar`, `.war` | `.zip`, Docker |
| Go | Binary | `.zip`, `.tar.gz`, Docker |
| Rust | Binary | `.zip`, `.tar.gz`, Docker |

### Installer Type Matrix

| Platform | Formats | Tools |
|----------|---------|-------|
| Windows | `.msi`, `.exe` | WiX Toolset, NSIS, Inno Setup |
| Linux (Debian) | `.deb` | dpkg-deb |
| Linux (RHEL) | `.rpm` | rpmbuild |
| macOS | `.dmg`, `.pkg` | hdiutil, pkgbuild |
| Cross-Platform | Docker | docker build |

### Recommended Technology Stack

**Package Creation:**
- **Tools:** Bash for package commands (npm, pip, dotnet, docker)
- **Config:** YAML for package settings

**Installer Generation:**
- **Templates:** Markdown/YAML configuration files
- **No code:** Configuration only, not implementation

### Technology Constraints

- **Constraint 1:** Skill < 1,000 lines (use references)
- **Constraint 2:** Templates are Markdown/YAML, not executable code
- **Constraint 3:** Bash for package commands only

## Risks & Constraints

### Technical Risks

**Risk 1: Platform-Specific Tool Availability**
- **Description:** Installer tools may not be installed
- **Probability:** High
- **Impact:** Medium
- **Mitigation:** Detect available tools, skip unavailable formats

**Risk 2: Docker Build Context Issues**
- **Description:** Large .dockerignore may be missing
- **Probability:** Medium
- **Impact:** High
- **Mitigation:** Generate optimized Dockerfile with .dockerignore

**Risk 3: Package Naming/Versioning Conflicts**
- **Description:** Version format varies by registry
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:** Standardize on semver, allow override

### Constraints

**Constraint 1: Config Only**
- **Description:** Generate configurations, not full implementations
- **Impact:** Users need installer tools installed
- **Mitigation:** Clear documentation of requirements

## Assumptions

1. Package tools (npm, pip, docker) are installed
2. Build artifacts exist from Phase 0.2
3. Standard package metadata formats are used

## Next Steps

### Immediate Actions
1. **Create references/package-formats.md:** Package creation for all formats
2. **Create references/installer-modes.md:** Installer mode documentation
3. **Update SKILL.md:** Add Phase 0.3-0.4 workflow

### Pre-Development Checklist
- [x] Architecture context files validated
- [ ] EPIC-036 dependencies met
- [x] Stories created in devforgeai/specs/Stories/
- [ ] Package tool availability documented

## Stories

| Story ID | Title | Points | Status | Depends On |
|----------|-------|--------|--------|------------|
| STORY-241 | Language-Specific Package Creation Module | 10 | Backlog | STORY-240 |
| STORY-242 | OS-Specific Installer Generation Module | 8 | Backlog | STORY-241 |
| STORY-243 | Installer Mode Configuration Module | 8 | Backlog | STORY-242 |
| **Total** | | **26** | | |

### Development Workflow
Stories will progress through:
1. **Ready for Dev** → devforgeai-development (TDD implementation)
2. **Dev Complete** → devforgeai-qa (quality validation)
3. **QA Approved** → devforgeai-release (deployment)

## Configuration Schemas

### package-config.yaml
```yaml
packaging:
  formats:
    - npm: { enabled: true, scope: "@devforgeai" }
    - pip: { enabled: true, name: "devforgeai" }
    - nuget: { enabled: false }
    - docker: { enabled: true, repository: "devforgeai/framework" }
  version-source: "package.json" | "pyproject.toml" | "version.json"
  include-docs: true
  include-examples: false
```

### installer-config.yaml
```yaml
installation:
  mode: wizard | cli | silent | gui
  target:
    path: /path/to/project
    create-if-missing: true
  components:
    - core
    - cli
    - templates
  post-install:
    - initialize-git: true
    - run-validation: true
```

## Files to Create/Modify

| Component | Path | Action | Size Target |
|-----------|------|--------|-------------|
| Release Skill | `.claude/skills/devforgeai-release/SKILL.md` | MODIFY | +150 lines |
| Package Ref | `.claude/skills/devforgeai-release/references/package-formats.md` | CREATE | ~600 lines |
| Installer Ref | `.claude/skills/devforgeai-release/references/installer-modes.md` | CREATE | ~500 lines |
| Package Config | `devforgeai/deployment/package-config.yaml` | CREATE | ~150 lines |
| Installer Config | `devforgeai/deployment/installer-config.yaml` | CREATE | ~200 lines |

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 26 | 3 | 0 | 0 | 0 |
| **Total** | **0%** | **26** | **3** | **0** | **0** | **0** |

### Burndown
- **Total Points:** 26
- **Completed:** 0
- **Remaining:** 26
- **Velocity:** TBD

## Notes

- Docker packaging works for all tech stacks
- Installer tools are optional (configs generated either way)
- Consider creating sample installer templates repository

---

**Epic Status:**
- ⚪ **Planning** - Requirements being defined

**Last Updated:** 2025-01-05 by Claude
**Plan Reference:** /home/bryan/.claude/plans/dazzling-juggling-ritchie.md
