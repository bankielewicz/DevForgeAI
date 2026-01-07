---
id: EPIC-038
title: Release Skill Registry Publishing
epic: EPIC-038
status: Planning
priority: Medium
complexity-score: 5
architecture-tier: Tier 2
start-date: 2025-02-10
target-date: 2025-02-17
estimated-points: 13
target-sprints: 1
created: 2025-01-05
updated: 2025-01-05
depends-on: EPIC-037
---

# Epic: Release Skill Registry Publishing

## Business Goal

Enable the devforgeai-release skill to publish packages to appropriate registries (npm, PyPI, NuGet, Docker Hub, GitHub Packages, crates.io) as part of the release workflow. This completes the "Build → Package → Publish → Deploy" lifecycle by automating distribution to public and private registries.

## Success Metrics

- **Registry Support:** Publish to 6+ registries (npm, PyPI, NuGet, Docker Hub, GitHub, crates.io)
- **Authentication:** Secure credential handling via environment variables
- **Publish Success:** 95%+ successful publications for properly configured projects
- **Idempotency:** Re-publish attempts detect existing versions and skip gracefully

**Measurement Plan:**
- Track successful publish operations per registry
- Monitor authentication failure rates
- Measure time from package creation to registry availability
- Review frequency: End of each sprint

## Scope

### Overview

Add Phase 0.5 (Registry Publishing) to the devforgeai-release skill, enabling automated publication to package registries with secure credential handling.

### Features

1. **Feature 1: Registry Publishing Commands (Phase 0.5)** (8 SP)
   - Description: Publish to npm, PyPI, NuGet, Docker Hub, GitHub, crates.io
   - User Value: Automated distribution to all package registries
   - Estimated Points: 8 story points

2. **Feature 2: Registry Configuration** (3 SP)
   - Description: Registry endpoints, credentials, version conflict detection
   - User Value: Secure, configurable registry publishing
   - Estimated Points: 3 story points

3. **Feature 3: Release Skill Integration** (2 SP)
   - Description: Add Phase 0.5 to SKILL.md with reference documentation
   - User Value: Seamless integration into release workflow
   - Estimated Points: 2 story points

### Out of Scope

- Credential storage/vaulting (use environment variables)
- Private registry setup (user responsibility)
- Package signing (future epic)
- Version bump automation (use existing version.py)

## Target Sprints

**Estimated Duration:** 1 sprint / 1 week

**Sprint Breakdown:**
- **Sprint 1:** All Features (13 SP)
  - F1: Registry Publishing (8 SP) - 4 stories
  - F2: Registry Configuration (3 SP) - 2 stories
  - F3: Skill Integration (2 SP) - 1 story

## Dependencies

### External Dependencies

- **Registry accounts:** npm, PyPI, NuGet, Docker Hub, GitHub
  - Owner: User
  - Impact if missing: Skip publishing with warning
- **Environment credentials:** Token/API keys configured
  - Owner: User
  - Impact if missing: Authentication failure

### Internal Dependencies

- **EPIC-037:** Package Phase complete (provides packages to publish)
  - Status: Not Started
  - Impact if missing: No packages to publish

### Blocking Issues

- None identified

## Stakeholders

- **Product Owner:** DevForgeAI Framework Team
- **Tech Lead:** Claude (AI orchestration)
- **Users:** Developers publishing to package registries

## Requirements

### Functional Requirements

#### User Stories

**User Story 1:**
```
As a developer with an npm package,
I want automatic publishing to npm registry,
So that users can install my package with npm install.
```

**Acceptance Criteria:**
- [ ] npm publish executed with correct registry
- [ ] NPM_TOKEN environment variable used for auth
- [ ] Version conflict detected and skipped gracefully

**User Story 2:**
```
As a developer with a Docker image,
I want automatic publishing to Docker Hub,
So that users can pull my image with docker pull.
```

**Acceptance Criteria:**
- [ ] docker push executed with correct tags
- [ ] DOCKER_USERNAME/DOCKER_PASSWORD used for auth
- [ ] Multi-architecture images supported

**User Story 3:**
```
As a security-conscious developer,
I want credentials masked in all log output,
So that my API tokens are never exposed.
```

**Acceptance Criteria:**
- [ ] Credentials masked with *** in logs
- [ ] Build fails if credential detected in output
- [ ] Dry-run mode available for testing

### Non-Functional Requirements (NFRs)

#### Performance
- **Credential validation:** < 2 seconds
- **npm publish:** < 60 seconds (network-dependent)
- **Docker push:** Varies (image size dependent)
- **Dry-run validation:** < 5 seconds

#### Security
- **No hardcoded credentials:** Environment variables only
- **Credential masking:** All log output sanitized
- **Secure transport:** HTTPS/TLS for all registry communication

## Architecture Considerations

### Complexity Tier
**Tier 2: Moderate Enhancement**
- **Score:** 5/60 points
- **Rationale:** Adds registry publishing with security requirements

### Registry Matrix

| Tech Stack | Registry | Publish Command | Auth Env Var |
|------------|----------|-----------------|--------------|
| Node.js | npm | `npm publish` | `NPM_TOKEN` |
| Node.js | GitHub | `npm publish --registry` | `GITHUB_TOKEN` |
| Python | PyPI | `twine upload` | `TWINE_USERNAME`, `TWINE_PASSWORD` |
| Python | Test PyPI | `twine upload --repository testpypi` | Same |
| .NET | NuGet.org | `dotnet nuget push` | `NUGET_API_KEY` |
| .NET | GitHub | `dotnet nuget push` | `GITHUB_TOKEN` |
| Java | Maven Central | `mvn deploy` | `MAVEN_USERNAME`, `MAVEN_PASSWORD` |
| Rust | crates.io | `cargo publish` | `CARGO_REGISTRY_TOKEN` |
| Docker | Docker Hub | `docker push` | `DOCKER_USERNAME`, `DOCKER_PASSWORD` |
| Docker | GitHub Container | `docker push ghcr.io/` | `GITHUB_TOKEN` |

### Recommended Technology Stack

**Publishing:**
- **Tools:** Bash for publish commands
- **Auth:** Environment variable injection

**Configuration:**
- **Format:** YAML for registry settings
- **Validation:** JSON Schema for config

### Technology Constraints

- **Constraint 1:** No hardcoded credentials (per no-hardcoded-secrets.md)
- **Constraint 2:** Bash for publish commands only
- **Constraint 3:** Environment variables for all auth

## Risks & Constraints

### Technical Risks

**Risk 1: Credential Exposure in Logs**
- **Description:** API tokens may appear in command output
- **Probability:** Medium
- **Impact:** Critical
- **Mitigation:** Mask credentials in all log output, use --quiet flags

**Risk 2: Registry Rate Limiting**
- **Description:** Too many publishes may trigger rate limits
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:** Implement exponential backoff, respect retry-after headers

**Risk 3: Version Already Exists**
- **Description:** Publishing existing version fails
- **Probability:** High
- **Impact:** Low
- **Mitigation:** Check version before publish, skip with info message

### Constraints

**Constraint 1: Environment-Only Credentials**
- **Description:** No credential files, only environment variables
- **Impact:** Users must set env vars before running
- **Mitigation:** Clear documentation of required variables

## Assumptions

1. Registry accounts exist and are configured
2. Environment variables are set correctly
3. Packages created in Phase 0.3 are valid

## Security Considerations

### Credential Handling
1. **NEVER** hardcode credentials in config files
2. **ALWAYS** use environment variables
3. **MASK** credentials in all log output
4. **VALIDATE** credentials before publish attempt
5. **FAIL** immediately if credentials appear in output

### Required Environment Variables
```bash
# npm
export NPM_TOKEN="npm_xxxx"

# PyPI (or use keyring)
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD="pypi-xxxx"

# NuGet
export NUGET_API_KEY="xxxx"

# Docker Hub
export DOCKER_USERNAME="user"
export DOCKER_PASSWORD="xxxx"

# GitHub (works for multiple registries)
export GITHUB_TOKEN="ghp_xxxx"

# crates.io
export CARGO_REGISTRY_TOKEN="xxxx"
```

## Next Steps

### Immediate Actions
1. **Create references/registry-publishing.md:** Publish commands per registry
2. **Create devforgeai/deployment/registry-config.yaml:** Config schema
3. **Update SKILL.md:** Add Phase 0.5 workflow

### Pre-Development Checklist
- [x] Architecture context files validated
- [ ] EPIC-037 dependencies met
- [ ] Stories created in devforgeai/specs/Stories/
- [ ] Security review completed

### Development Workflow
Stories will progress through:
1. **Ready for Dev** → devforgeai-development (TDD implementation)
2. **Dev Complete** → devforgeai-qa (quality validation)
3. **QA Approved** → devforgeai-release (deployment)

## Configuration Schema

### registry-config.yaml
```yaml
registries:
  npm:
    enabled: true
    registry: https://registry.npmjs.org
    access: public  # public | restricted
    dry-run: false

  pypi:
    enabled: true
    repository: pypi  # pypi | testpypi | custom
    skip-existing: true

  nuget:
    enabled: false
    source: https://api.nuget.org/v3/index.json

  docker:
    enabled: true
    registry: docker.io
    repository: devforgeai/framework
    tags:
      - latest
      - "{{version}}"

  github:
    enabled: true
    packages: true
    container-registry: true
```

## Files to Create/Modify

| Component | Path | Action | Size Target |
|-----------|------|--------|-------------|
| Release Skill | `.claude/skills/devforgeai-release/SKILL.md` | MODIFY | +80 lines |
| Registry Ref | `.claude/skills/devforgeai-release/references/registry-publishing.md` | CREATE | ~400 lines |
| Registry Config | `devforgeai/deployment/registry-config.yaml` | CREATE | ~100 lines |

## Stories

| Story ID | Title | Points | Status | Depends On |
|----------|-------|--------|--------|------------|
| STORY-244 | Registry Publishing Commands | 8 | Backlog | STORY-241 |
| STORY-245 | Registry Configuration | 3 | Backlog | - |
| STORY-246 | Release Skill Registry Integration | 2 | Backlog | STORY-244, STORY-245 |
| **Total** | | **13** | | |

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 13 | 3 | 0 | 0 | 0 |
| **Total** | **0%** | **13** | **3** | **0** | **0** | **0** |

### Burndown
- **Total Points:** 13
- **Completed:** 0
- **Remaining:** 13
- **Velocity:** TBD

## Notes

- Security is paramount - credential exposure is a critical risk
- Dry-run mode should be default for first-time setup
- Consider adding publish verification step (check registry after publish)

---

**Epic Status:**
- ⚪ **Planning** - Requirements being defined

**Last Updated:** 2025-01-06 by Claude
**Plan Reference:** /home/bryan/.claude/plans/dazzling-juggling-ritchie.md
