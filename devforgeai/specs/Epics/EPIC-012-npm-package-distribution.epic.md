---
id: EPIC-012
title: NPM Package Distribution for DevForgeAI Installer
business-value: Enable frictionless installation via `npm install -g devforgeai` reducing adoption barriers by 70%+
status: Planning
priority: High
complexity-score: 28
architecture-tier: Tier 2 (Moderate Application)
created: 2025-11-25
estimated-points: 15-20
target-sprints: 2-3 sprints
---

# NPM Package Distribution for DevForgeAI Installer

## Business Goal

Transform DevForgeAI installation from manual process to one-command NPM installation, reducing installation time from 15+ minutes to <5 minutes and increasing adoption by 50%+ among Node.js developers.

**Success Metrics:**
- Installation time: <5 minutes from `npm install` to working framework
- Installation success rate: >95% across Windows/Mac/Linux
- NPM package downloads: 100+ in first month
- Installation errors: <5% failure rate

## Problem Statement

Current DevForgeAI installation requires:
1. Manual cloning of repository or downloading source
2. Understanding file structure to copy files correctly
3. Running multiple setup scripts
4. Troubleshooting path/permission issues
5. No version management (upgrades require manual process)

This complexity prevents many developers from trying DevForgeAI, limiting adoption and community growth.

## Features

### Feature 1: NPM Package Creation & Structure
**Description:** Create installable NPM package with proper structure, dependencies, and manifest
**User Stories (high-level):**
1. As a developer, I want to install DevForgeAI via `npm install -g devforgeai`, so I can start using it immediately
2. As a maintainer, I want package.json with correct dependencies, so users get all required tools
3. As a CI/CD pipeline, I want to install DevForgeAI programmatically, so I can automate project setup

**Estimated Effort:** Small-Medium (5-8 story points)

**Acceptance Criteria:**
- package.json includes all dependencies (Python CLI, node scripts, etc.)
- Package structure follows NPM best practices
- Bin entry point (`devforgeai`) registered globally
- README with installation instructions
- LICENSE and metadata complete

### Feature 2: NPM Registry Publishing Workflow
**Description:** Establish process to publish package to NPM registry with versioning
**User Stories (high-level):**
1. As a maintainer, I want automated NPM publishing via GitHub Actions, so releases are consistent
2. As a user, I want to see package versions on NPM, so I can choose which version to install
3. As a maintainer, I want to publish beta/RC versions, so we can test before stable release

**Estimated Effort:** Small (3-5 story points)

**Acceptance Criteria:**
- NPM account created for @devforgeai scope
- GitHub Actions workflow publishes on git tag
- Supports version tags (v1.0.0, v1.1.0-beta.1, etc.)
- npm publish succeeds with provenance
- Package discoverable via `npm search devforgeai`

### Feature 3: Global CLI Entry Point
**Description:** Provide `devforgeai` command available globally after npm install
**User Stories (high-level):**
1. As a user, I want to run `devforgeai install /path/to/project`, so I can install framework
2. As a user, I want to run `devforgeai --help`, so I can see available commands
3. As a user, I want to run `devforgeai --version`, so I can verify installed version

**Estimated Effort:** Small (3-5 story points)

**Acceptance Criteria:**
- `devforgeai` command available in PATH after npm install -g
- Command routes to installer entry point (install.py or wrapper script)
- --help flag shows usage and options
- --version flag shows current version
- Works on Windows (PowerShell/CMD), Mac (Bash/Zsh), Linux (Bash)

### Feature 4: Offline Installation Support
**Description:** Enable installer to work without internet access (air-gapped environments)
**User Stories (high-level):**
1. As a security-conscious org, I want to install DevForgeAI without internet, so it passes security review
2. As a user, I want installer to bundle all files, so no external downloads required
3. As a user, I want clear error if network needed, so I know what's missing

**Estimated Effort:** Small-Medium (5-8 story points)

**Acceptance Criteria:**
- All framework files bundled in NPM package (~50MB)
- No external downloads during installation (except npm install itself)
- Python CLI bundled or installed via pip (optional dependency)
- Fallback mode if optional dependencies unavailable
- Clear error messages if internet required for optional features

### Feature 5: Framework Release Automation
**Description:** Automate DevForgeAI framework release workflow with src/ sync, versioning, checksums, and GitHub releases
**User Stories (high-level):**
1. As a framework maintainer, I want to run `scripts/release.sh` to automate the entire release process
2. As a maintainer, I want operational files (.claude/, devforgeai/) automatically synced to src/, so distribution is always up-to-date
3. As a maintainer, I want version.json updated with semantic versioning, so releases are properly tracked
4. As a maintainer, I want checksums automatically generated, so users can verify package integrity
5. As a contributor, I want GitHub releases auto-created with changelogs, so release notes are transparent
6. As an end user, I want to see release history on GitHub, so I know what's changed between versions

**Estimated Effort:** Medium (10-12 story points)

**Acceptance Criteria:**
- `scripts/release.sh` script orchestrates full workflow
- Interactive prompt for version bump (major/minor/patch)
- Sync .claude/ → src/claude/ with exclusions (*.backup*, __pycache__)
- Sync devforgeai/ → src/devforgeai/ with exclusions (backups/, qa/reports/, feedback/sessions/)
- Update src/version.json with version, release date, release notes path
- Generate src/checksums.txt with SHA-256 hashes for all src/ files
- Create GitHub release via gh CLI with auto-generated changelog
- Validate sync completeness (no missing files)
- Cross-platform support (Windows/Mac/Linux via Bash or PowerShell equivalent)
- Pre-release validation: check for uncommitted changes, verify tests pass
- Rollback capability if any step fails
- Integration with NPM publish workflow (Feature 2)

## Requirements Summary

### Functional Requirements
1. **NPM Package Structure:** Proper package.json, bin entry, bundled files, dependencies
2. **Registry Publishing:** Automated workflow, versioning, scoped package (@devforgeai)
3. **Global CLI:** `devforgeai` command, --help/--version flags, cross-platform support
4. **Offline Support:** Bundled files, no external downloads, optional dependency handling

### Data Model
**Entities:**
- **Package Manifest (package.json):** Name, version, bin, dependencies, scripts, metadata
- **Version Metadata (.version.json):** Installed version, release date, installation mode
- **Bundle Manifest (files array):** List of all included files for verification

**Relationships:**
- NPM Package → Version Metadata (one-to-one, created during installation)
- NPM Package → Bundled Files (one-to-many, static list)

### Integration Points
1. **NPM Registry:** Publish packages via `npm publish` with provenance
2. **GitHub API:** Fetch release notes, check latest version (optional, online mode)
3. **Python PyPI:** Install devforgeai CLI via pip (optional dependency)

### Non-Functional Requirements

**Performance:**
- NPM install: <30 seconds on modern internet connection
- Package download size: <50MB compressed
- Global CLI invocation: <500ms to display help

**Security:**
- Package signature verification (npm provenance)
- Checksum validation for bundled files (SHA-256)
- No hardcoded secrets or credentials in package

**Scalability:**
- Support 1000+ concurrent npm installs (NPM registry handles scaling)
- Package size manageable for low-bandwidth users (<50MB)

**Availability:**
- NPM registry uptime (99.9%+ SLA from NPM)
- Offline mode as fallback if registry unavailable

## Architecture Considerations

**Complexity Tier:** 2 (Moderate Application)

**Recommended Architecture:**
- Pattern: Modular Monolith (NPM package with multiple entry points)
- Layers: CLI layer (entry point), Installer layer (install.py), Utilities (validation, backup)
- Package: Single NPM package with bundled Python CLI as dependency
- Deployment: NPM registry (public), GitHub releases (source)

**Technology Recommendations (Tier 2):**
- **Package Format:** NPM package (Node.js ecosystem standard)
- **CLI Framework:** Commander.js or Yargs (Node.js CLI wrapper)
- **Installer Core:** Existing Python installer (install.py) invoked by Node wrapper
- **Build Tool:** npm scripts, esbuild or webpack for bundling (if needed)
- **Publishing:** GitHub Actions workflow with `npm publish`

**Alternative Considered:**
- Pure Python package via PyPI (rejected: targets Node.js developers primarily)
- Shell script installer (rejected: lacks version management, hard to distribute)

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| **NPM publishing process unfamiliar** | MEDIUM | Create test package first, publish to test registry, follow NPM docs for provenance |
| **Package size exceeds NPM limits** | LOW | NPM limit is 500MB, DevForgeAI ~50MB; monitor size, use .npmignore to exclude unnecessary files |
| **Cross-platform CLI entry point fails** | HIGH | Test on Windows/Mac/Linux in CI, use npm's bin field (handles platform differences), provide troubleshooting guide |
| **Python CLI dependency fails to install** | MEDIUM | Make Python CLI optional, provide manual pip install instructions, bundle pre-built binaries if possible |
| **Offline mode incomplete** | MEDIUM | Clearly document online-only features (GitHub API checks), provide 100% offline fallback, bundle all core files |

## Dependencies

**Prerequisites:**
- Existing installer code (`installer/install.py` and modules)
- Python CLI package (`.claude/scripts/devforgeai_cli/`)
- GitHub repository with releases

**Dependents:**
- EPIC-013: Interactive Installer & Validation (uses NPM package as distribution mechanism)
- EPIC-014: Version Management & Lifecycle (uses NPM versions for upgrades)

## Success Criteria

### Definition of Done (Epic-Level)
- [ ] NPM package published to registry
- [ ] `npm install -g devforgeai` works on Windows/Mac/Linux
- [ ] `devforgeai --help` and `devforgeai --version` work
- [ ] Package includes all framework files (validated via manifest)
- [ ] Offline installation mode functional
- [ ] Installation success rate >95% (measured via telemetry or user reports)
- [ ] Documentation complete (README, INSTALL.md, troubleshooting)

### User Acceptance
- [ ] Users can install DevForgeAI in <5 minutes
- [ ] Installation errors <5% across platforms
- [ ] Clear error messages for common failures
- [ ] Support for air-gapped environments (offline mode)

## Stories

| Story ID | Feature | Title | Points | Status |
|----------|---------|-------|--------|--------|
| STORY-066 | Feature 1 | NPM Package Creation & Structure | 8 | Backlog |
| STORY-067 | Feature 2 | NPM Registry Publishing Workflow | 5 | Backlog |
| STORY-068 | Feature 3 | Global CLI Entry Point | 5 | Backlog |
| STORY-069 | Feature 4 | Offline Installation Support | 8 | Backlog |
| STORY-070 | Feature 5 | Framework Release Automation | 12 | Backlog |

**Total Points:** 38 / 15-20 estimated (expanded scope significantly)

## Next Steps

1. **Sprint Planning:** Assign stories to sprints based on dependencies
   - Sprint 3: STORY-066 (8 pts) - Foundation (package structure)
   - Sprint 4: STORY-067 (5 pts), STORY-070 (12 pts) - Publishing & Release Automation
   - Sprint 5: STORY-068 (5 pts), STORY-069 (8 pts) - CLI & Offline support
2. **Architecture Phase:** Define NPM package structure ✅ COMPLETED (2025-11-25)
   - ✅ Updated `devforgeai/context/tech-stack.md` with NPM/Node.js tooling
   - ✅ Updated `devforgeai/context/dependencies.md` with installer dependencies
   - ✅ Updated `devforgeai/context/architecture-constraints.md` with installer patterns
   - ✅ Updated `devforgeai/context/source-tree.md` with installer directory structure
   - ✅ Created ADR-004: NPM Package Distribution
3. **Implementation:** TDD workflow for each story
   - Start with `/dev STORY-066` (foundation for all other stories)
   - **STORY-070 depends on STORY-067** (release automation needs npm publish workflow)

## Notes

- Installer code already exists (`installer/` directory) - this epic focuses on NPM distribution wrapper
- Python CLI already exists (`.claude/scripts/devforgeai_cli/`) - include as dependency
- Existing tests in `installer/tests/` should be reused for validation
- Consider scoped package (@devforgeai/installer) to avoid name conflicts
