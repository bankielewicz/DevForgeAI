---
id: STORY-067
title: NPM Registry Publishing Workflow
epic: EPIC-012
sprint: Backlog
status: Backlog
points: 5
priority: Medium
assigned_to: TBD
created: 2025-11-25
format_version: "2.1"
---

# Story: NPM Registry Publishing Workflow

## Description

**As a** package maintainer,
**I want** an automated NPM publishing workflow that triggers on git tags and supports semantic versioning (including pre-release versions),
**so that** releases are consistent, reproducible, and users can access stable and pre-release versions from the NPM registry.

## Acceptance Criteria

### AC#1: NPM Registry Account Configuration

**Given** the DevForgeAI package needs to be published to NPM
**When** the NPM registry account is configured
**Then** the account includes:
- Organization scope `@devforgeai` registered on npmjs.com
- NPM_TOKEN generated with Automation access level (publish permissions)
- NPM_TOKEN stored as GitHub repository secret
- Package name reserved and available

---

### AC#2: GitHub Actions Workflow Triggers on Version Tags

**Given** a git tag matching semantic versioning pattern is pushed to the repository
**When** the tag follows format `v{major}.{minor}.{patch}` or `v{major}.{minor}.{patch}-{prerelease}`
**Then** GitHub Actions workflow automatically triggers:
- Detects stable versions (e.g., `v1.0.0`, `v2.1.3`)
- Detects pre-release versions (e.g., `v1.1.0-beta.1`, `v2.0.0-rc.2`)
- Workflow runs only on tags (not on branch pushes or PRs)

---

### AC#3: Package Build and Validation Before Publishing

**Given** the GitHub Actions workflow has been triggered by a version tag
**When** the workflow executes the build stage
**Then** the workflow performs:
- Dependency installation (`npm ci` for reproducible builds)
- Test execution (`npm test`) with 100% pass rate
- Package validation (checks `package.json` version matches tag version)
- Workflow fails and stops if any validation step fails

---

### AC#4: NPM Publish with Provenance and Tag Management

**Given** all build and validation steps have passed
**When** the workflow executes the publish stage
**Then** the package is published with:
- Provenance enabled (`npm publish --provenance` for supply chain transparency)
- Correct dist-tag assignment:
  - Stable versions (e.g., `v1.0.0`) → `latest` tag
  - Beta versions (e.g., `v1.1.0-beta.1`) → `beta` tag
  - RC versions (e.g., `v2.0.0-rc.1`) → `rc` tag
- Publish succeeds with HTTP 200/201 response
- Package version visible on npmjs.com within 5 minutes

---

### AC#5: Package Discoverability and Metadata

**Given** the package has been successfully published to NPM
**When** a user searches for the package using `npm search devforgeai`
**Then** the package listing displays:
- Package name
- Description from `package.json`
- Latest stable version number
- Repository URL (GitHub link)
- Keywords for discoverability

---

### AC#6: Version Tag Validation and Error Handling

**Given** a git tag is pushed that does NOT match semantic versioning pattern
**When** the GitHub Actions workflow evaluates the tag
**Then** the workflow:
- Detects invalid tag format
- Logs clear error message: "Invalid tag format. Must match vX.Y.Z or vX.Y.Z-prerelease"
- Exits with non-zero status code
- Does NOT attempt to publish to NPM

---

### AC#7: Idempotency and Duplicate Version Prevention

**Given** a version has already been published to NPM
**When** the same version tag is pushed again
**Then** the workflow:
- Detects existing version on NPM registry
- Logs message: "Version already published. Skipping publish."
- Exits with success status (idempotent behavior)
- Does NOT fail the workflow

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "GitHubActionsWorkflow"
      file_path: ".github/workflows/npm-publish.yml"
      requirements:
        - id: "CONF-001"
          description: "Workflow triggers on version tags matching semver pattern"
          testable: true
          test_requirement: "Test: Push tag v1.0.0, verify workflow triggers"
          priority: "Critical"
        - id: "CONF-002"
          description: "Workflow runs npm ci, npm test before publish"
          testable: true
          test_requirement: "Test: Verify CI steps execute in order"
          priority: "Critical"
        - id: "CONF-003"
          description: "Workflow publishes with --provenance flag"
          testable: true
          test_requirement: "Test: npm publish command includes --provenance"
          priority: "High"
        - id: "CONF-004"
          description: "Workflow assigns correct dist-tag based on version"
          testable: true
          test_requirement: "Test: Beta version gets beta tag, stable gets latest"
          priority: "High"

    - type: "Configuration"
      name: "GitHubSecrets"
      file_path: "GitHub Repository Settings"
      requirements:
        - id: "CONF-005"
          description: "NPM_TOKEN secret configured in repository"
          testable: true
          test_requirement: "Test: Workflow can authenticate to NPM registry"
          priority: "Critical"

    - type: "Service"
      name: "VersionValidator"
      file_path: ".github/scripts/validate-version.js"
      requirements:
        - id: "SVC-001"
          description: "Script validates tag matches package.json version"
          testable: true
          test_requirement: "Test: Mismatch between tag v1.0.1 and package.json 1.0.0 fails"
          priority: "Critical"
        - id: "SVC-002"
          description: "Script detects invalid semver tags"
          testable: true
          test_requirement: "Test: Tag 'release-1.0' rejected as invalid"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Git tag must match semver with v prefix"
      test_requirement: "Test: Regex ^v\\d+\\.\\d+\\.\\d+(-[a-z0-9.]+)?$ validates tags"
    - id: "BR-002"
      rule: "Package.json version must match tag version (minus v prefix)"
      test_requirement: "Test: tag v1.0.0 requires package.json version 1.0.0"
    - id: "BR-003"
      rule: "Duplicate versions cannot be published (NPM enforces)"
      test_requirement: "Test: Second publish of same version skipped gracefully"
    - id: "BR-004"
      rule: "Pre-release versions use appropriate dist-tag"
      test_requirement: "Test: v1.0.0-beta.1 publishes to beta tag, not latest"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Workflow execution time"
      metric: "< 5 minutes from tag push to NPM availability"
      test_requirement: "Test: Time workflow execution end-to-end"
    - id: "NFR-002"
      category: "Security"
      requirement: "Token stored securely"
      metric: "NPM_TOKEN never exposed in logs"
      test_requirement: "Test: Grep workflow logs for NPM_TOKEN, expect 0 matches"
    - id: "NFR-003"
      category: "Security"
      requirement: "Provenance attestation"
      metric: "All packages have provenance metadata"
      test_requirement: "Test: npm view devforgeai shows attestations"
    - id: "NFR-004"
      category: "Reliability"
      requirement: "Retry on transient failures"
      metric: "3 retries with exponential backoff"
      test_requirement: "Test: Simulate 502 error, verify retry occurs"
```

---

## Non-Functional Requirements (NFRs)

### Performance
- Workflow execution time: < 5 minutes from tag push to NPM availability
- NPM registry propagation: Package searchable within 5 minutes of publish

### Security
- NPM_TOKEN stored as GitHub encrypted secret
- Provenance enabled for all packages (SLSA Level 2)
- Token never logged in workflow output (GitHub masks secrets)

### Reliability
- 3 retry attempts with exponential backoff (5s, 10s, 20s)
- Idempotent: Re-running workflow for existing version skips gracefully
- < 5% failure rate for valid tags

---

## Edge Cases

1. **NPM_TOKEN expires or is revoked:** Workflow detects HTTP 401/403, logs clear error with remediation steps
2. **Network failure during publish:** Retry up to 3 times, then fail with actionable error
3. **Package.json version mismatch:** Halt before publish, log version mismatch error
4. **Multiple tags pushed simultaneously:** Each workflow runs independently, idempotency prevents conflicts
5. **Pre-release after newer stable:** Warning logged but publish succeeds

---

## Definition of Done

### Implementation
- [ ] GitHub Actions workflow file created (.github/workflows/npm-publish.yml)
- [ ] Version validation script created
- [ ] NPM_TOKEN secret configured in repository
- [ ] Workflow triggers on v* tags only
- [ ] Provenance flag enabled in publish command
- [ ] Dist-tag logic implemented (latest/beta/rc)

### Quality
- [ ] All 7 acceptance criteria have passing tests
- [ ] Edge cases covered (5 documented scenarios)
- [ ] Workflow tested with test tag (e.g., v0.0.0-test.1)

### Testing
- [ ] Unit tests for version validation script
- [ ] Integration test: Tag → Workflow → NPM publish
- [ ] Idempotency test: Publish same version twice

### Documentation
- [ ] CONTRIBUTING.md: Release process documented
- [ ] README.md: Version management section added

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Use GitHub Actions (not CircleCI/Jenkins) for native GitHub integration
- Provenance enabled for supply chain transparency
- Scoped package (@devforgeai) for namespace ownership

**Related ADRs:**
- [ADR-004: NPM Package Distribution](../../../.devforgeai/adrs/ADR-004-npm-package-distribution.md)

**Dependencies:**
- STORY-066: NPM Package Creation & Structure (provides package.json)

---

**Story Template Version:** 2.1
**Last Updated:** 2025-11-25
