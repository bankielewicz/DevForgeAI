---
id: STORY-077
title: Version Detection & Compatibility Checking
epic: EPIC-014
sprint: Backlog
status: Backlog
points: 10
priority: Medium
assigned_to: Unassigned
created: 2025-11-25
format_version: "2.1"
---

# Story: Version Detection & Compatibility Checking

## Description

**As a** DevForgeAI user,
**I want** the installer to detect my current installed version and validate upgrade path compatibility,
**So that** I can confidently upgrade to newer versions knowing whether the upgrade is safe or requires caution.

**Business Context:**
This feature addresses the version management gap in DevForgeAI where users cannot identify their installed version or determine if an upgrade is safe. By implementing version detection and compatibility checking, users will see clear version comparisons (current vs available), receive warnings about breaking changes, and be protected from unsafe downgrades.

## Acceptance Criteria

### AC#1: Version File Detection

**Given** DevForgeAI is installed with `.devforgeai/.version.json` present,
**When** the installer or version command runs,
**Then** the current version is read from the file,
**And** version information is displayed to the user (e.g., "Current version: v1.2.3"),
**And** operation completes within 1 second.

---

### AC#2: Semver Parsing

**Given** a version string in any valid semver format,
**When** the version parser processes the string,
**Then** major, minor, and patch components are correctly extracted,
**And** pre-release identifiers are correctly parsed (e.g., "1.2.3-beta.1" → pre-release: "beta.1"),
**And** build metadata is handled if present (e.g., "1.2.3+build.456"),
**And** invalid version strings return a clear error message.

**Examples:**
- "1.0.0" → { major: 1, minor: 0, patch: 0, prerelease: null }
- "2.1.3-alpha.2" → { major: 2, minor: 1, patch: 3, prerelease: "alpha.2" }
- "1.0.0-rc.1+20231105" → { major: 1, minor: 0, patch: 0, prerelease: "rc.1", build: "20231105" }

---

### AC#3: Upgrade Path Validation

**Given** a current installed version and a target version,
**When** the compatibility checker compares versions,
**Then** the relationship is correctly identified as one of:
- **Upgrade:** target > current (e.g., 1.0.0 → 1.1.0)
- **Downgrade:** target < current (e.g., 2.0.0 → 1.9.0)
- **Same version:** target == current
- **Major upgrade:** target.major > current.major (breaking changes possible)
- **Minor upgrade:** only target.minor > current.minor (backward compatible)
- **Patch upgrade:** only target.patch > current.patch (bug fixes only)

---

### AC#4: Breaking Change Warning

**Given** the target version has a different major version than current,
**When** the user initiates an upgrade,
**Then** a clear warning is displayed explaining potential breaking changes,
**And** the warning lists known breaking changes (if available from changelog),
**And** the user is prompted to confirm continuation,
**And** the warning uses visual emphasis (⚠️ icon, color if supported).

**Warning Format:**
```
⚠️  MAJOR VERSION UPGRADE DETECTED

Upgrading from v1.x.x → v2.x.x may include breaking changes.

Known breaking changes in v2.0.0:
- Context file format changed (migration required)
- Deprecated commands removed: /old-command
- Configuration schema updated

Do you want to continue? [y/N]
```

---

### AC#5: Downgrade Blocking

**Given** the target version's major is less than current version's major,
**When** the user attempts to downgrade without --force flag,
**Then** the operation is blocked with a clear error message,
**And** the error explains why downgrades are dangerous,
**And** the error suggests using --force flag to override,
**And** exit code is non-zero (1 = blocked operation).

**Error Format:**
```
❌ DOWNGRADE BLOCKED

Cannot downgrade from v2.0.0 to v1.5.0 (major version decrease).

Major version downgrades may cause:
- Data loss or corruption
- Incompatible configuration files
- Missing required features

If you understand the risks, use: devforgeai upgrade --force
```

---

### AC#6: Missing Version File Handling

**Given** `.devforgeai/.version.json` does not exist,
**When** the installer or version command runs,
**Then** the user is notified that no version file was found,
**And** the user is prompted to either:
  - Specify the installed version manually
  - Treat as fresh installation (version 0.0.0)
  - Abort the operation
**And** if version is specified, it is validated as valid semver.

---

### AC#7: Pre-release Version Handling

**Given** current or target version includes pre-release identifier,
**When** version comparison is performed,
**Then** pre-release versions are correctly ordered:
  - 1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0-rc.1 < 1.0.0
**And** stable releases are considered higher than pre-releases of same version,
**And** upgrading from pre-release to stable is treated as normal upgrade.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "VersionDetector"
      file_path: "installer/version_detector.py"
      interface: "IVersionDetector"
      lifecycle: "Singleton"
      dependencies:
        - "IFileSystem"
        - "IVersionParser"
      requirements:
        - id: "SVC-001"
          description: "Read version from .devforgeai/.version.json"
          testable: true
          test_requirement: "Test: Given .version.json exists with valid JSON, When read_version() called, Then returns Version object with correct fields"
          priority: "Critical"
        - id: "SVC-002"
          description: "Handle missing version file gracefully"
          testable: true
          test_requirement: "Test: Given .version.json does not exist, When read_version() called, Then returns None (not exception)"
          priority: "Critical"
        - id: "SVC-003"
          description: "Handle corrupted version file"
          testable: true
          test_requirement: "Test: Given .version.json contains invalid JSON, When read_version() called, Then returns error result with clear message"
          priority: "High"

    - type: "Service"
      name: "VersionParser"
      file_path: "installer/version_parser.py"
      interface: "IVersionParser"
      lifecycle: "Singleton"
      dependencies: []
      requirements:
        - id: "SVC-004"
          description: "Parse standard semver strings (X.Y.Z)"
          testable: true
          test_requirement: "Test: Given '1.2.3', When parse() called, Then returns Version(major=1, minor=2, patch=3)"
          priority: "Critical"
        - id: "SVC-005"
          description: "Parse pre-release versions (X.Y.Z-prerelease)"
          testable: true
          test_requirement: "Test: Given '1.0.0-beta.1', When parse() called, Then returns Version with prerelease='beta.1'"
          priority: "High"
        - id: "SVC-006"
          description: "Parse build metadata (X.Y.Z+build)"
          testable: true
          test_requirement: "Test: Given '1.0.0+build.123', When parse() called, Then returns Version with build='build.123'"
          priority: "Medium"
        - id: "SVC-007"
          description: "Reject invalid version strings"
          testable: true
          test_requirement: "Test: Given 'invalid', When parse() called, Then returns error with message 'Invalid semver format'"
          priority: "High"

    - type: "Service"
      name: "VersionComparator"
      file_path: "installer/version_comparator.py"
      interface: "IVersionComparator"
      lifecycle: "Singleton"
      dependencies:
        - "IVersionParser"
      requirements:
        - id: "SVC-008"
          description: "Compare two versions and return relationship"
          testable: true
          test_requirement: "Test: Given v1.0.0 and v2.0.0, When compare() called, Then returns CompareResult.UPGRADE with is_major=True"
          priority: "Critical"
        - id: "SVC-009"
          description: "Detect downgrade scenarios"
          testable: true
          test_requirement: "Test: Given v2.0.0 (current) and v1.5.0 (target), When compare() called, Then returns CompareResult.DOWNGRADE"
          priority: "Critical"
        - id: "SVC-010"
          description: "Handle pre-release version ordering"
          testable: true
          test_requirement: "Test: Given v1.0.0-alpha and v1.0.0-beta, When compare() called, Then returns UPGRADE (beta > alpha)"
          priority: "High"
        - id: "SVC-011"
          description: "Identify upgrade type (major/minor/patch)"
          testable: true
          test_requirement: "Test: Given v1.0.0 and v1.1.0, When compare() called, Then returns UPGRADE with upgrade_type='minor'"
          priority: "High"

    - type: "Service"
      name: "CompatibilityChecker"
      file_path: "installer/compatibility_checker.py"
      interface: "ICompatibilityChecker"
      lifecycle: "Singleton"
      dependencies:
        - "IVersionComparator"
        - "IChangelogReader"
      requirements:
        - id: "SVC-012"
          description: "Check if upgrade path is safe"
          testable: true
          test_requirement: "Test: Given minor version upgrade, When check_compatibility() called, Then returns safe=True, warnings=[]"
          priority: "Critical"
        - id: "SVC-013"
          description: "Return breaking changes for major upgrades"
          testable: true
          test_requirement: "Test: Given major upgrade with changelog, When check_compatibility() called, Then returns breaking_changes list"
          priority: "High"
        - id: "SVC-014"
          description: "Block unsafe downgrades without force flag"
          testable: true
          test_requirement: "Test: Given major downgrade without force, When check_compatibility() called, Then returns blocked=True"
          priority: "Critical"

    - type: "DataModel"
      name: "Version"
      table: "N/A (In-memory)"
      purpose: "Represents a parsed semantic version"
      fields:
        - name: "major"
          type: "Int"
          constraints: "Required, >= 0"
          description: "Major version number"
          test_requirement: "Test: Version with negative major raises ValueError"
        - name: "minor"
          type: "Int"
          constraints: "Required, >= 0"
          description: "Minor version number"
          test_requirement: "Test: Version with negative minor raises ValueError"
        - name: "patch"
          type: "Int"
          constraints: "Required, >= 0"
          description: "Patch version number"
          test_requirement: "Test: Version with negative patch raises ValueError"
        - name: "prerelease"
          type: "String"
          constraints: "Optional"
          description: "Pre-release identifier (e.g., 'alpha.1', 'beta', 'rc.1')"
          test_requirement: "Test: Version.prerelease correctly stores and retrieves value"
        - name: "build"
          type: "String"
          constraints: "Optional"
          description: "Build metadata (e.g., 'build.123', '20231105')"
          test_requirement: "Test: Build metadata does not affect version comparison"
      indexes: []
      relationships: []

    - type: "DataModel"
      name: "VersionMetadata"
      table: ".devforgeai/.version.json"
      purpose: "Persisted version information for installed DevForgeAI"
      fields:
        - name: "version"
          type: "String"
          constraints: "Required, valid semver"
          description: "Currently installed version"
          test_requirement: "Test: JSON with missing 'version' field fails validation"
        - name: "installed_at"
          type: "DateTime (ISO8601)"
          constraints: "Required"
          description: "When this version was installed"
          test_requirement: "Test: installed_at is updated on fresh install and upgrade"
        - name: "upgraded_from"
          type: "String"
          constraints: "Optional"
          description: "Previous version (if upgraded)"
          test_requirement: "Test: upgraded_from is set after upgrade, null on fresh install"
        - name: "schema_version"
          type: "Int"
          constraints: "Required, default 1"
          description: "Schema version for future format changes"
          test_requirement: "Test: schema_version defaults to 1 if not present"
      indexes: []
      relationships: []

    - type: "DataModel"
      name: "CompareResult"
      table: "N/A (In-memory)"
      purpose: "Result of version comparison"
      fields:
        - name: "relationship"
          type: "Enum"
          constraints: "Required"
          description: "UPGRADE, DOWNGRADE, SAME"
          test_requirement: "Test: All three relationship types are correctly returned"
        - name: "upgrade_type"
          type: "Enum"
          constraints: "Optional (only for UPGRADE)"
          description: "MAJOR, MINOR, PATCH"
          test_requirement: "Test: upgrade_type is MAJOR when only major differs"
        - name: "is_breaking"
          type: "Boolean"
          constraints: "Required"
          description: "True if major version change"
          test_requirement: "Test: is_breaking=True for major changes, False otherwise"
        - name: "warnings"
          type: "List[String]"
          constraints: "Optional"
          description: "List of warnings for user"
          test_requirement: "Test: Warnings populated from changelog for breaking changes"
      indexes: []
      relationships: []

    - type: "Configuration"
      name: ".version.json"
      file_path: ".devforgeai/.version.json"
      required_keys:
        - key: "version"
          type: "string"
          example: "1.2.3"
          required: true
          default: null
          validation: "Must match semver regex"
          test_requirement: "Test: VersionDetector reads 'version' field correctly"
        - key: "installed_at"
          type: "string"
          example: "2025-11-25T10:30:00Z"
          required: true
          default: "Current timestamp"
          validation: "Must be valid ISO8601"
          test_requirement: "Test: installed_at is parseable as datetime"
        - key: "upgraded_from"
          type: "string"
          example: "1.1.0"
          required: false
          default: null
          validation: "Must match semver regex if present"
          test_requirement: "Test: upgraded_from is optional, null on fresh install"
        - key: "schema_version"
          type: "int"
          example: "1"
          required: false
          default: "1"
          validation: "Must be positive integer"
          test_requirement: "Test: Missing schema_version defaults to 1"

  business_rules:
    - id: "BR-001"
      rule: "Major version downgrades are blocked by default"
      trigger: "When target major < current major"
      validation: "Compare major version numbers"
      error_handling: "Display blocking message with --force suggestion"
      test_requirement: "Test: Downgrade from 2.0.0 to 1.x.x blocked without --force"
      priority: "Critical"

    - id: "BR-002"
      rule: "Pre-release versions follow semver precedence"
      trigger: "When comparing versions with pre-release identifiers"
      validation: "alpha < beta < rc < release"
      error_handling: "N/A (informational)"
      test_requirement: "Test: 1.0.0-alpha < 1.0.0-beta < 1.0.0"
      priority: "High"

    - id: "BR-003"
      rule: "Build metadata is ignored in comparisons"
      trigger: "When comparing versions with build metadata"
      validation: "Strip build metadata before comparison"
      error_handling: "N/A"
      test_requirement: "Test: 1.0.0+build.1 == 1.0.0+build.2"
      priority: "Medium"

    - id: "BR-004"
      rule: "Missing version file allows fresh install path"
      trigger: "When .version.json does not exist"
      validation: "File existence check"
      error_handling: "Prompt user for version or treat as fresh install"
      test_requirement: "Test: Missing .version.json does not block installation"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Version detection completes within 1 second"
      metric: "< 1000ms for read_version() call"
      test_requirement: "Test: read_version() completes in < 1000ms with file I/O"
      priority: "High"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Version parsing is near-instantaneous"
      metric: "< 10ms for parse() call"
      test_requirement: "Test: parse() completes in < 10ms for valid input"
      priority: "Medium"

    - id: "NFR-003"
      category: "Reliability"
      requirement: "Version detection does not crash on corrupted files"
      metric: "100% graceful error handling for malformed JSON"
      test_requirement: "Test: Corrupted .version.json returns error result, not exception"
      priority: "Critical"

    - id: "NFR-004"
      category: "Security"
      requirement: "Version file is read-only during detection"
      metric: "No writes to .version.json during read operations"
      test_requirement: "Test: read_version() does not modify file timestamp"
      priority: "High"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Version detection: < 1 second (including file I/O)
- Version parsing: < 10ms per parse operation
- Version comparison: < 5ms per comparison

**Throughput:**
- N/A (user-initiated operations, not high-volume)

---

### Security

**Authentication:**
- None required (local file operations)

**Authorization:**
- File system read permissions for .devforgeai/ directory

**Data Protection:**
- Version metadata is not sensitive
- No encryption required

---

### Reliability

**Error Handling:**
- Follow Result Pattern (per coding-standards.md)
- Return clear error messages for all failure cases
- Never crash on malformed input

**Retry Logic:**
- Not applicable (file operations are synchronous)

---

### Observability

**Logging:**
- Log level: INFO for version detection success
- Log level: WARN for missing or corrupted version file
- Log level: ERROR for unexpected failures
- Include version numbers in log messages for debugging

---

## Dependencies

### Prerequisite Stories

- [ ] **EPIC-012 stories:** NPM Package Distribution (provides version in package.json)
  - **Why:** Package version must be available for comparison
  - **Status:** In Progress

### External Dependencies

None - all file operations are local.

### Technology Dependencies

- [ ] **semver** (Python package) or equivalent
  - **Purpose:** Standard semver parsing and comparison
  - **Approved:** Pending (needs to be added to dependencies.md)
  - **Added to dependencies.md:** No

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**

1. **Happy Path:**
   - Parse valid semver string (standard, pre-release, build metadata)
   - Read version from valid .version.json
   - Compare versions and identify upgrade type

2. **Edge Cases:**
   - Version "0.0.0" (initial development)
   - Pre-release ordering (alpha vs beta vs rc)
   - Build metadata ignored in comparison
   - Version with all components (1.2.3-alpha.1+build.456)

3. **Error Cases:**
   - Invalid semver string ("not.a.version", "1.2", "v1.2.3")
   - Missing .version.json file
   - Corrupted JSON in .version.json
   - Empty .version.json file
   - Permission denied reading file

---

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**

1. **End-to-End Version Detection:**
   - Create .version.json → Read → Parse → Display

2. **Upgrade Path Validation:**
   - Current v1.0.0 + Target v1.1.0 → Minor upgrade (safe)
   - Current v1.0.0 + Target v2.0.0 → Major upgrade (warning)
   - Current v2.0.0 + Target v1.5.0 → Downgrade (blocked)

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

### AC#1: Version File Detection

- [ ] .version.json read successfully - **Phase:** 2 - **Evidence:** version_detector_test.py
- [ ] Version displayed to user - **Phase:** 2 - **Evidence:** CLI output test
- [ ] Operation completes < 1 second - **Phase:** 4 - **Evidence:** performance test

### AC#2: Semver Parsing

- [ ] Standard version parsed (X.Y.Z) - **Phase:** 2 - **Evidence:** version_parser_test.py
- [ ] Pre-release parsed correctly - **Phase:** 2 - **Evidence:** version_parser_test.py
- [ ] Build metadata handled - **Phase:** 2 - **Evidence:** version_parser_test.py
- [ ] Invalid strings return error - **Phase:** 2 - **Evidence:** version_parser_test.py

### AC#3: Upgrade Path Validation

- [ ] Upgrade correctly identified - **Phase:** 2 - **Evidence:** version_comparator_test.py
- [ ] Downgrade correctly identified - **Phase:** 2 - **Evidence:** version_comparator_test.py
- [ ] Same version identified - **Phase:** 2 - **Evidence:** version_comparator_test.py
- [ ] Upgrade type (major/minor/patch) correct - **Phase:** 2 - **Evidence:** version_comparator_test.py

### AC#4: Breaking Change Warning

- [ ] Warning displayed for major upgrade - **Phase:** 2 - **Evidence:** compatibility_checker_test.py
- [ ] Breaking changes listed from changelog - **Phase:** 2 - **Evidence:** compatibility_checker_test.py
- [ ] User confirmation prompted - **Phase:** 2 - **Evidence:** CLI integration test

### AC#5: Downgrade Blocking

- [ ] Major downgrade blocked - **Phase:** 2 - **Evidence:** compatibility_checker_test.py
- [ ] Error message displayed - **Phase:** 2 - **Evidence:** CLI output test
- [ ] --force flag overrides block - **Phase:** 2 - **Evidence:** CLI integration test
- [ ] Exit code is non-zero - **Phase:** 2 - **Evidence:** CLI integration test

### AC#6: Missing Version File Handling

- [ ] User notified of missing file - **Phase:** 2 - **Evidence:** version_detector_test.py
- [ ] User prompted for action - **Phase:** 2 - **Evidence:** CLI integration test
- [ ] Manual version validated as semver - **Phase:** 2 - **Evidence:** version_parser_test.py

### AC#7: Pre-release Version Handling

- [ ] Pre-release ordering correct - **Phase:** 2 - **Evidence:** version_comparator_test.py
- [ ] Stable > pre-release of same version - **Phase:** 2 - **Evidence:** version_comparator_test.py

---

**Checklist Progress:** 0/24 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] VersionDetector service implemented
- [ ] VersionParser service implemented
- [ ] VersionComparator service implemented
- [ ] CompatibilityChecker service implemented
- [ ] Version, VersionMetadata, CompareResult models implemented
- [ ] .version.json schema documented

### Quality
- [ ] All 7 acceptance criteria have passing tests
- [ ] Edge cases covered (pre-release, build metadata, missing file)
- [ ] Data validation enforced (semver format, JSON schema)
- [ ] NFRs met (< 1s detection, < 10ms parsing)
- [ ] Code coverage > 95% for business logic

### Testing
- [ ] Unit tests for VersionParser (parse valid/invalid)
- [ ] Unit tests for VersionComparator (all comparison scenarios)
- [ ] Unit tests for VersionDetector (file exists/missing/corrupted)
- [ ] Unit tests for CompatibilityChecker (safe/warning/blocked)
- [ ] Integration tests for end-to-end upgrade flow

### Documentation
- [ ] API documentation for version services
- [ ] .version.json schema documented in specs/
- [ ] Upgrade troubleshooting guide (for users)

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Using Python's built-in semver parsing or lightweight library (no heavy dependencies)
- Version file stored in .devforgeai/ to keep it with framework files
- Downgrade blocking is a safety feature (can be overridden with --force)
- Pre-release ordering follows semver specification exactly

**Open Questions:**
- [ ] Should we support non-semver versions for legacy compatibility? - **Owner:** TBD - **Due:** Before implementation

**Related ADRs:**
- None yet (may create ADR for version file format if changes needed)

**References:**
- [Semver Specification](https://semver.org/)
- EPIC-014: Version Management & Installation Lifecycle

---

**Story Template Version:** 2.1
**Last Updated:** 2025-11-25
