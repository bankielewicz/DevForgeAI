---
id: EPIC-036
title: Release Skill Build Phase Enhancement
epic: EPIC-036
status: Planning
priority: High
complexity-score: 6
architecture-tier: Tier 2
start-date: 2025-01-13
target-date: 2025-01-27
estimated-points: 21
target-sprints: 2
created: 2025-01-05
updated: 2025-01-05
depends-on: EPIC-035
---

# Epic: Release Skill Build Phase Enhancement

## Business Goal

Enable the devforgeai-release skill to automatically detect project technology stacks and execute the correct build commands before deployment. This transforms the release skill from "deployment only" to a complete "build → deploy" workflow that works with ANY language ecosystem (Node.js, Python, C#/.NET, Java, Go, Rust, etc.).

## Success Metrics

- **Stack Detection:** 95%+ accuracy detecting Node.js, Python, C#/.NET, Java, Go, Rust projects
- **Build Success:** 90%+ of detected stacks build successfully on first attempt
- **Cross-Platform:** Build for win-x64, linux-x64, osx-x64 targets where applicable
- **Zero Config:** Works without user configuration for standard project layouts

**Measurement Plan:**
- Track detection accuracy via test suite across sample projects
- Monitor build command success/failure rates
- Collect metrics on cross-compilation usage
- Review frequency: End of each sprint

## Scope

### Overview

Add Phase 0.1 (Tech Stack Detection) and Phase 0.2 (Build/Compile) to the devforgeai-release skill, enabling language-agnostic builds before deployment.

### Features

1. **Feature 1: Tech Stack Detection (Phase 0.1)** (8 SP)
   - Description: Detect project type from indicator files
   - User Value: Automatic build configuration without manual setup
   - Estimated Points: 8 story points

2. **Feature 2: Build Command Execution (Phase 0.2)** (8 SP)
   - Description: Execute detected build commands for each tech stack
   - User Value: Standardized build process across all languages
   - Estimated Points: 8 story points

3. **Feature 3: Release Skill Integration** (5 SP)
   - Description: Update SKILL.md with Phase 0.1-0.2 and references
   - User Value: Seamless integration into release workflow
   - Estimated Points: 5 story points

### Out of Scope

- Package creation (see EPIC-037)
- Installer generation (see EPIC-037)
- Registry publishing (see EPIC-038)
- Custom build scripts (standard conventions only)
- Build optimization/caching strategies

## Target Sprints

**Estimated Duration:** 2 sprints / 2 weeks

**Sprint Breakdown:**
- **Sprint 1:** Tech Stack Detection (8 SP) - 3 stories
- **Sprint 2:** Build Execution + Integration (13 SP) - 7 stories

## Dependencies

### External Dependencies

- **Build tools installed:** npm, python, dotnet, mvn, gradle, go, cargo
  - Owner: User's development environment
  - Impact if missing: Skip unsupported stacks with warning

### Internal Dependencies

- **EPIC-035:** Platform detection complete (for cross-platform builds)
  - Status: In Progress
  - Impact if missing: Cannot determine target platforms

### Blocking Issues

- None identified

## Stakeholders

- **Product Owner:** DevForgeAI Framework Team
- **Tech Lead:** Claude (AI orchestration)
- **Users:** Developers using Node.js, Python, .NET, Java, Go, Rust

## Requirements

### Functional Requirements

#### User Stories

**User Story 1:**
```
As a developer with a Node.js project,
I want the release skill to auto-detect my tech stack,
So that I don't need to manually configure build commands.
```

**Acceptance Criteria:**
- [ ] package.json detected as Node.js project
- [ ] `npm run build` executed automatically
- [ ] Build output directory (dist/) identified

**User Story 2:**
```
As a developer with a .NET project,
I want cross-platform builds generated automatically,
So that I can distribute to Windows, Linux, and macOS users.
```

**Acceptance Criteria:**
- [ ] *.csproj detected as .NET project
- [ ] `dotnet publish -c Release` executed for each target
- [ ] win-x64, linux-x64, osx-x64 builds available

**User Story 3:**
```
As a developer with a monorepo,
I want each workspace detected and built,
So that all packages are ready for release.
```

**Acceptance Criteria:**
- [ ] Lerna/Nx/Turborepo workspaces detected
- [ ] Build command executed for each workspace
- [ ] Build order respects dependencies

### Non-Functional Requirements (NFRs)

#### Performance
- **Stack detection:** < 5 seconds for any project
- **Build command lookup:** < 100ms
- **Build execution:** Varies by project (no timeout enforced)

#### Compatibility
- **Node.js:** 18+ supported
- **Python:** 3.9+ supported
- **.NET:** 6.0+ supported
- **Java:** 11+ supported
- **Go:** 1.20+ supported
- **Rust:** 1.70+ supported

## Architecture Considerations

### Complexity Tier
**Tier 2: Moderate Enhancement**
- **Score:** 6/60 points
- **Rationale:** Adds new phases to release skill with cross-language support

### Detection Matrix

| Indicator File | Tech Stack | Build Command | Output Dir |
|----------------|------------|---------------|------------|
| `package.json` | Node.js | `npm run build` | `dist/` |
| `pyproject.toml` | Python | `python -m build` | `dist/` |
| `requirements.txt` | Python | `pip install -r` | N/A |
| `*.csproj` | .NET | `dotnet publish -c Release` | `publish/` |
| `*.sln` | .NET | `dotnet build -c Release` | `bin/Release/` |
| `pom.xml` | Java/Maven | `mvn clean package` | `target/` |
| `build.gradle` | Java/Gradle | `gradle build` | `build/libs/` |
| `go.mod` | Go | `go build -o ./bin/` | `bin/` |
| `Cargo.toml` | Rust | `cargo build --release` | `target/release/` |

### Recommended Technology Stack

**Detection:**
- **Tools:** Glob + Read (native Claude Code tools)
- **Pattern:** Indicator file scanning

**Build Execution:**
- **Tools:** Bash (whitelisted for builds in tech-stack.md)
- **Pattern:** Platform-aware command execution

### Technology Constraints

- **Constraint 1:** Use existing tech-stack-detector subagent as foundation
- **Constraint 2:** No external dependencies for detection logic

## Risks & Constraints

### Technical Risks

**Risk 1: Non-Standard Project Layouts**
- **Description:** Projects may not follow standard conventions
- **Probability:** High
- **Impact:** Medium
- **Mitigation:** Support override via devforgeai.yaml config file

**Risk 2: Build Tool Version Incompatibility**
- **Description:** User's build tools may be incompatible versions
- **Probability:** Medium
- **Impact:** High
- **Mitigation:** Detect tool versions before build, warn on mismatches

**Risk 3: Monorepo Detection Complexity**
- **Description:** Monorepos have varied configurations
- **Probability:** High
- **Impact:** Medium
- **Mitigation:** Support common patterns (Lerna, Nx, Turborepo, workspace)

### Constraints

**Constraint 1: Bash for Builds Only**
- **Description:** Native tools for detection, Bash only for build execution
- **Impact:** Consistent with tech-stack.md constraints
- **Mitigation:** Already aligned with framework rules

## Assumptions

1. Standard project layouts follow language conventions
2. Build tools are installed and on PATH
3. Projects have standard build scripts (npm run build, etc.)

## Next Steps

### Immediate Actions
1. **Create references/tech-stack-detection.md:** Detection matrix and logic
2. **Create references/build-commands.md:** Build command templates
3. **Update SKILL.md:** Add Phase 0.1-0.2 workflow

### Pre-Development Checklist
- [x] Architecture context files validated
- [ ] EPIC-035 dependencies met
- [x] Stories created in devforgeai/specs/Stories/
- [ ] Test projects prepared for each tech stack

## Stories

| Story ID | Title | Points | Status | Depends On |
|----------|-------|--------|--------|------------|
| STORY-238 | Tech Stack Detection Module | 8 | Backlog | - |
| STORY-239 | Build Command Execution Module | 8 | Backlog | STORY-238 |
| STORY-240 | Release Skill Build Phase Integration | 5 | Backlog | STORY-238, STORY-239 |
| **Total** | | **21** | | |

### Development Workflow
Stories will progress through:
1. **Ready for Dev** → devforgeai-development (TDD implementation)
2. **Dev Complete** → devforgeai-qa (quality validation)
3. **QA Approved** → devforgeai-release (deployment)

## Files to Create/Modify

| Component | Path | Action | Size Target |
|-----------|------|--------|-------------|
| Release Skill | `.claude/skills/devforgeai-release/SKILL.md` | MODIFY | +100 lines |
| Detection Ref | `.claude/skills/devforgeai-release/references/tech-stack-detection.md` | CREATE | ~400 lines |
| Build Ref | `.claude/skills/devforgeai-release/references/build-commands.md` | CREATE | ~500 lines |
| Config Schema | `devforgeai/deployment/build-config.yaml` | CREATE | ~100 lines |

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 21 | 3 | 0 | 0 | 0 |
| **Total** | **0%** | **21** | **3** | **0** | **0** | **0** |

### Burndown
- **Total Points:** 21
- **Completed:** 0
- **Remaining:** 21
- **Velocity:** TBD

## Notes

- Leverages existing tech-stack-detector subagent
- Cross-compilation support varies by language
- Consider caching detection results for repeated builds

---

**Epic Status:**
- ⚪ **Planning** - Requirements being defined

**Last Updated:** 2025-01-05 by Claude
**Plan Reference:** /home/bryan/.claude/plans/dazzling-juggling-ritchie.md
