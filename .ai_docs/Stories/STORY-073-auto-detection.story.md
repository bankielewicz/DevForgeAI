---
id: STORY-073
title: Auto-Detection (Project Type & Existing Installs)
epic: EPIC-013
sprint: Sprint-4
status: Backlog
points: 10
priority: Medium
assigned_to: TBD
created: 2025-11-25
format_version: "2.1"
---

# Story: Auto-Detection (Project Type & Existing Installs)

## Description

**As a** DevForgeAI installer user,
**I want** the installer to automatically detect my project's context (existing installations, project type, potential conflicts),
**so that** I can make informed decisions without manually inspecting files, reduce configuration errors, and safely upgrade/downgrade installations.

## Acceptance Criteria

### AC#1: Existing installation version detection

**Given** a project directory with `.devforgeai/.version.json` file
**When** the installer runs auto-detection
**Then** the installer reads the version.json file, extracts installed_version, installed_at timestamp, and installation_source fields, and displays "Found existing DevForgeAI installation: v{version} installed on {timestamp} from {source}"

---

### AC#2: Version comparison with recommendations

**Given** an existing installation is detected with version X and the installer source has version Y
**When** version comparison executes
**Then** the installer compares semantic versions (major.minor.patch), and displays recommendations:
- If Y > X: "Upgrade available: v{X} → v{Y} (recommended)"
- If Y < X: "Downgrade detected: v{X} → v{Y} (warning: may lose features)"
- If Y == X: "Same version detected: v{X} (reinstall available if needed)"
- If version malformed or missing: "Unable to compare versions (manual review required)"

---

### AC#3: CLAUDE.md detection and backup offer

**Given** a project directory with existing `CLAUDE.md` file
**When** the installer detects CLAUDE.md
**Then** the installer warns "Existing CLAUDE.md detected ({size} bytes, modified {date}). Installation will merge with template." and offers backup option "Create backup as CLAUDE.md.backup-{timestamp}? [Y/n]" with default Yes

---

### AC#4: Git repository root detection

**Given** the installer is invoked from any subdirectory within a git repository
**When** git repository root detection runs
**Then** the installer executes `git rev-parse --show-toplevel` to find repository root, displays "Git repository detected: {root_path}" as default target directory, and falls back to current working directory if not a git repository (with message "No git repository detected, using current directory: {cwd}")

---

### AC#5: File conflict detection

**Given** the installer is about to copy files to target directory
**When** file conflict detection scans target
**Then** the installer identifies all existing files that would be overwritten, categorizes conflicts by type (framework files: .claude/*, .devforgeai/*; user files: CLAUDE.md, .gitignore), and displays "File conflicts detected: {count} framework files, {count} user files"

---

### AC#6: Auto-detection summary display

**Given** all auto-detection checks complete
**When** summary generation executes before user prompts
**Then** the installer displays formatted summary with:
- Installation Status section (existing version or "Clean install")
- Project Context section (git root path)
- Conflicts section (file count by category, first 5 conflicts)
- Recommendations section (upgrade/downgrade/reinstall/clean install action)

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    # Auto-Detection Orchestrator
    - type: "Service"
      name: "AutoDetectionService"
      file_path: "src/installer/services/auto_detection_service.py"
      interface: "IAutoDetectionService"
      lifecycle: "Singleton"
      dependencies:
        - "IVersionDetectionService"
        - "IClaudeMdDetectionService"
        - "IGitDetectionService"
        - "IFileConflictDetectionService"
        - "ISummaryFormatterService"
      requirements:
        - id: "SVC-001"
          description: "Orchestrate all auto-detection checks and return DetectionResult"
          testable: true
          test_requirement: "Test: detect_all() returns DetectionResult with all fields populated"
          priority: "Critical"
        - id: "SVC-002"
          description: "Execute checks concurrently where possible"
          testable: true
          test_requirement: "Test: detect_all() completes faster than sequential execution"
          priority: "High"
        - id: "SVC-003"
          description: "Handle partial failures gracefully"
          testable: true
          test_requirement: "Test: One check fails, others still complete and return results"
          priority: "High"

    # Version Detection Service
    - type: "Service"
      name: "VersionDetectionService"
      file_path: "src/installer/services/version_detection_service.py"
      interface: "IVersionDetectionService"
      lifecycle: "Singleton"
      dependencies:
        - "json"
        - "pathlib"
        - "semver"
      requirements:
        - id: "SVC-004"
          description: "Read .devforgeai/.version.json and parse installed version"
          testable: true
          test_requirement: "Test: read_version() returns VersionInfo with all fields"
          priority: "Critical"
        - id: "SVC-005"
          description: "Compare installed vs source version using semantic versioning"
          testable: true
          test_requirement: "Test: compare_versions('1.0.0', '1.1.0') returns action='upgrade'"
          priority: "Critical"
        - id: "SVC-006"
          description: "Handle corrupted version.json gracefully"
          testable: true
          test_requirement: "Test: Invalid JSON returns None and logs error"
          priority: "High"
        - id: "SVC-007"
          description: "Handle non-standard versions (null, 'latest', 'dev')"
          testable: true
          test_requirement: "Test: Non-parseable version returns action='unknown'"
          priority: "Medium"

    # CLAUDE.md Detection Service
    - type: "Service"
      name: "ClaudeMdDetectionService"
      file_path: "src/installer/services/claudemd_detection_service.py"
      interface: "IClaudeMdDetectionService"
      lifecycle: "Singleton"
      dependencies:
        - "os"
        - "pathlib"
        - "datetime"
      requirements:
        - id: "SVC-008"
          description: "Detect existing CLAUDE.md and extract metadata (size, modified date)"
          testable: true
          test_requirement: "Test: detect() returns ClaudeMdInfo with exists=True, size, modified"
          priority: "Critical"
        - id: "SVC-009"
          description: "Determine if backup is needed (skip for 0-byte files)"
          testable: true
          test_requirement: "Test: Empty file returns needs_backup=False"
          priority: "High"
        - id: "SVC-010"
          description: "Generate backup filename with timestamp"
          testable: true
          test_requirement: "Test: generate_backup_name() returns 'CLAUDE.md.backup-YYYYMMDD-HHMMSS'"
          priority: "Medium"

    # Git Detection Service
    - type: "Service"
      name: "GitDetectionService"
      file_path: "src/installer/services/git_detection_service.py"
      interface: "IGitDetectionService"
      lifecycle: "Singleton"
      dependencies:
        - "subprocess"
        - "pathlib"
        - "shutil"
      requirements:
        - id: "SVC-011"
          description: "Execute git rev-parse --show-toplevel to find repository root"
          testable: true
          test_requirement: "Test: detect_git_root() returns Path to repository root"
          priority: "Critical"
        - id: "SVC-012"
          description: "Handle non-git directories gracefully"
          testable: true
          test_requirement: "Test: Non-git directory returns None"
          priority: "High"
        - id: "SVC-013"
          description: "Validate git command availability"
          testable: true
          test_requirement: "Test: Missing git returns None with log message"
          priority: "High"
        - id: "SVC-014"
          description: "Detect and warn about unusual repository roots (/)"
          testable: true
          test_requirement: "Test: Root path '/' returns None with warning"
          priority: "Medium"

    # File Conflict Detection Service
    - type: "Service"
      name: "FileConflictDetectionService"
      file_path: "src/installer/services/file_conflict_detection_service.py"
      interface: "IFileConflictDetectionService"
      lifecycle: "Singleton"
      dependencies:
        - "os"
        - "pathlib"
      requirements:
        - id: "SVC-015"
          description: "Scan target directory for files that would be overwritten"
          testable: true
          test_requirement: "Test: detect_conflicts() returns list of conflicting file paths"
          priority: "Critical"
        - id: "SVC-016"
          description: "Categorize conflicts by type (framework vs user files)"
          testable: true
          test_requirement: "Test: Categorization returns framework_count and user_count"
          priority: "High"
        - id: "SVC-017"
          description: "Use generators for large directory scans"
          testable: true
          test_requirement: "Test: Memory usage <50MB for 100k files"
          priority: "High"
        - id: "SVC-018"
          description: "Validate file paths are within target directory"
          testable: true
          test_requirement: "Test: Path with '..' is rejected"
          priority: "Critical"
        - id: "SVC-019"
          description: "Resolve symlinks before conflict detection"
          testable: true
          test_requirement: "Test: Symlinked directory uses resolved path"
          priority: "Medium"

    # Summary Formatter Service
    - type: "Service"
      name: "SummaryFormatterService"
      file_path: "src/installer/services/summary_formatter_service.py"
      interface: "ISummaryFormatterService"
      lifecycle: "Singleton"
      dependencies:
        - "typing"
        - "datetime"
      requirements:
        - id: "SVC-020"
          description: "Format DetectionResult into human-readable summary"
          testable: true
          test_requirement: "Test: format_summary() returns multi-line string with 4 sections"
          priority: "Critical"
        - id: "SVC-021"
          description: "Apply color coding for terminal output"
          testable: true
          test_requirement: "Test: Output includes ANSI escape codes when supported"
          priority: "Medium"
        - id: "SVC-022"
          description: "Paginate conflict lists (show first 10)"
          testable: true
          test_requirement: "Test: 50 conflicts shows first 10 with '...and 40 more'"
          priority: "Medium"

    # Detection Result Data Model
    - type: "DataModel"
      name: "DetectionResult"
      table: "N/A (in-memory)"
      purpose: "Stores all auto-detection results"
      fields:
        - name: "version_info"
          type: "VersionInfo | None"
          constraints: "Optional"
          description: "Detected version information"
          test_requirement: "Test: None if version detection fails"
        - name: "claudemd_info"
          type: "ClaudeMdInfo | None"
          constraints: "Optional"
          description: "CLAUDE.md detection results"
          test_requirement: "Test: None if CLAUDE.md not found"
        - name: "git_info"
          type: "GitInfo | None"
          constraints: "Optional"
          description: "Git repository detection results"
          test_requirement: "Test: None if not in git repo"
        - name: "conflicts"
          type: "ConflictInfo"
          constraints: "Required"
          description: "File conflict detection results"
          test_requirement: "Test: Empty list if no conflicts"

    # Version Info Data Model
    - type: "DataModel"
      name: "VersionInfo"
      table: "N/A (in-memory)"
      purpose: "Stores installed version metadata"
      fields:
        - name: "installed_version"
          type: "String"
          constraints: "Required, semver format"
          description: "Installed version string"
          test_requirement: "Test: Format X.Y.Z"
        - name: "installed_at"
          type: "DateTime"
          constraints: "Required, ISO 8601"
          description: "Installation timestamp"
          test_requirement: "Test: Parses ISO 8601"
        - name: "installation_source"
          type: "String"
          constraints: "Required"
          description: "Installation method (installer, manual, ci)"
          test_requirement: "Test: One of allowed values"

    # CLAUDE.md Info Data Model
    - type: "DataModel"
      name: "ClaudeMdInfo"
      table: "N/A (in-memory)"
      purpose: "Stores CLAUDE.md detection results"
      fields:
        - name: "exists"
          type: "Boolean"
          constraints: "Required"
          description: "Whether CLAUDE.md exists"
          test_requirement: "Test: True if file exists"
        - name: "size"
          type: "Integer"
          constraints: "Required if exists"
          description: "File size in bytes"
          test_requirement: "Test: Accurate byte count"
        - name: "modified"
          type: "DateTime"
          constraints: "Required if exists"
          description: "Last modified timestamp"
          test_requirement: "Test: Accurate mtime"
        - name: "needs_backup"
          type: "Boolean"
          constraints: "Computed"
          description: "Whether backup is recommended"
          test_requirement: "Test: False for 0-byte files"

    # Git Info Data Model
    - type: "DataModel"
      name: "GitInfo"
      table: "N/A (in-memory)"
      purpose: "Stores git repository detection results"
      fields:
        - name: "repository_root"
          type: "Path | None"
          constraints: "Optional"
          description: "Git repository root path"
          test_requirement: "Test: None if not in git repo"
        - name: "is_submodule"
          type: "Boolean"
          constraints: "Required"
          description: "Whether repository is a submodule"
          test_requirement: "Test: Detect submodule correctly"

    # Conflict Info Data Model
    - type: "DataModel"
      name: "ConflictInfo"
      table: "N/A (in-memory)"
      purpose: "Stores file conflict detection results"
      fields:
        - name: "conflicts"
          type: "List[Path]"
          constraints: "Required"
          description: "List of conflicting file paths"
          test_requirement: "Test: Empty list if no conflicts"
        - name: "framework_count"
          type: "Integer"
          constraints: "Computed"
          description: "Count of framework file conflicts"
          test_requirement: "Test: Accurate count"
        - name: "user_count"
          type: "Integer"
          constraints: "Computed"
          description: "Count of user file conflicts"
          test_requirement: "Test: Accurate count"

  business_rules:
    - id: "BR-001"
      rule: "Auto-detection failures are non-fatal"
      trigger: "Any detection check raises exception"
      validation: "Catch exceptions, log warning, continue with other checks"
      error_handling: "Return partial DetectionResult with None for failed checks"
      test_requirement: "Test: Version check fails, git check still runs"
      priority: "Critical"

    - id: "BR-002"
      rule: "Summary displays before any user prompts"
      trigger: "All detection checks complete"
      validation: "Display summary, then prompt for action"
      error_handling: "If summary generation fails, display raw detection results"
      test_requirement: "Test: Summary appears before first interactive prompt"
      priority: "High"

    - id: "BR-003"
      rule: "CLAUDE.md backup skipped for empty files"
      trigger: "CLAUDE.md exists with size=0"
      validation: "Check file size, skip backup offer if 0 bytes"
      error_handling: "N/A (silent skip)"
      test_requirement: "Test: 0-byte CLAUDE.md has needs_backup=False"
      priority: "Medium"

    - id: "BR-004"
      rule: "Git root validation rejects filesystem root"
      trigger: "git rev-parse returns '/' or 'C:\\'"
      validation: "Compare root path against filesystem root"
      error_handling: "Log warning, use current directory instead"
      test_requirement: "Test: Root path '/' returns None with warning"
      priority: "High"

    - id: "BR-005"
      rule: "File paths must be within target directory"
      trigger: "Conflict detection scans files"
      validation: "Validate path doesn't escape target via .."
      error_handling: "Skip invalid paths, log security warning"
      test_requirement: "Test: Path '../etc/passwd' is rejected"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Auto-detection completes in <500ms for typical projects"
      metric: "< 500ms for <10,000 files"
      test_requirement: "Test: Measure detection time with mock filesystem"
      priority: "High"

    - id: "NFR-002"
      category: "Performance"
      requirement: "File conflict detection scans at ≥1000 files/second"
      metric: "≥ 1000 files/second on HDD"
      test_requirement: "Test: Benchmark conflict scan with 10k files"
      priority: "High"

    - id: "NFR-003"
      category: "Performance"
      requirement: "Git detection completes in <100ms"
      metric: "< 100ms for git rev-parse"
      test_requirement: "Test: Measure git command execution time"
      priority: "Medium"

    - id: "NFR-004"
      category: "Security"
      requirement: "Path validation prevents directory traversal"
      metric: "Zero traversal vulnerabilities"
      test_requirement: "Test: Malicious paths rejected"
      priority: "Critical"

    - id: "NFR-005"
      category: "Security"
      requirement: "Git command uses shell=False"
      metric: "No shell injection possible"
      test_requirement: "Test: subprocess.run called with shell=False"
      priority: "Critical"

    - id: "NFR-006"
      category: "Reliability"
      requirement: "Graceful fallback when git not available"
      metric: "No crash when git missing"
      test_requirement: "Test: Missing git returns None without error"
      priority: "High"

    - id: "NFR-007"
      category: "Scalability"
      requirement: "Memory usage <50MB during conflict scan"
      metric: "< 50MB heap for 100k files"
      test_requirement: "Test: Monitor memory during large scan"
      priority: "High"

    - id: "NFR-008"
      category: "Usability"
      requirement: "Summary uses color coding when supported"
      metric: "ANSI colors applied on capable terminals"
      test_requirement: "Test: Verify ANSI codes in color-capable terminal"
      priority: "Medium"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Overall:**
- Auto-detection completes in < 500ms for projects with <10,000 files
- Conflict detection scans at ≥ 1000 files/second

**Individual Components:**
- Version.json parsing: < 10ms
- Git detection: < 100ms
- Summary generation: < 50ms

---

### Security

**Path Validation:**
- Prevent directory traversal (reject `..` paths)
- Validate paths within target directory

**Subprocess Safety:**
- Git command uses `shell=False`
- No command injection via user input

---

### Reliability

**Graceful Degradation:**
- Missing git → Use current directory
- Corrupted version.json → Treat as unknown version
- Permission denied → Mark check as UNKNOWN

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-072:** Pre-Flight Validation Checks
  - **Why:** Shares OutputFormatter for colored messages
  - **Status:** Backlog

### Technology Dependencies

- [ ] **semver:** Semantic version parsing library
  - **Purpose:** Parse and compare version strings
  - **Approved:** Pending
  - **Added to dependencies.md:** Pending

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Version Detection:** Valid JSON, corrupted JSON, missing file, null version
2. **CLAUDE.md Detection:** Exists, doesn't exist, empty file, large file
3. **Git Detection:** Valid repo, not a repo, git not installed, root path
4. **Conflict Detection:** No conflicts, framework conflicts, user conflicts, traversal attempt

---

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **Full Detection Flow:** All checks complete successfully
2. **Partial Failures:** Version fails, others succeed
3. **Summary Generation:** All data types formatted correctly

---

## Edge Cases

1. **Corrupted .version.json:** Invalid JSON treated as unknown version with warning
2. **Multiple git repositories (nested):** Use innermost repository root
3. **Symlinked directories:** Resolve symlinks before conflict detection
4. **Permission-denied during detection:** Mark affected checks as UNKNOWN
5. **Version.json with null version:** Treat as corrupted, recommend clean install
6. **0-byte CLAUDE.md:** Skip backup offer
7. **Git root is filesystem root:** Use current directory instead
8. **Pre-release versions:** Parse with semver, warn about stability

---

## Data Validation Rules

1. **.version.json schema:** Required fields: installed_version, installed_at, installation_source
2. **Semantic version format:** Regex `^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$`
3. **Git path validation:** Must be absolute path and existing directory
4. **File path validation:** Must be within target directory
5. **Timestamp validation:** ISO 8601 format

---

## Acceptance Criteria Verification Checklist

### AC#1: Version detection

- [ ] Read .version.json - **Phase:** 2 - **Evidence:** version_detection_service.test.py
- [ ] Parse installed_version - **Phase:** 2 - **Evidence:** version_detection_service.test.py
- [ ] Display version message - **Phase:** 2 - **Evidence:** summary_formatter_service.test.py

### AC#2: Version comparison

- [ ] Compare semantic versions - **Phase:** 2 - **Evidence:** version_detection_service.test.py
- [ ] Display upgrade recommendation - **Phase:** 2 - **Evidence:** summary_formatter_service.test.py
- [ ] Handle malformed versions - **Phase:** 2 - **Evidence:** version_detection_service.test.py

### AC#3: CLAUDE.md detection

- [ ] Detect existing file - **Phase:** 2 - **Evidence:** claudemd_detection_service.test.py
- [ ] Extract size and date - **Phase:** 2 - **Evidence:** claudemd_detection_service.test.py
- [ ] Offer backup - **Phase:** 2 - **Evidence:** integration test

### AC#4: Git root detection

- [ ] Execute git rev-parse - **Phase:** 2 - **Evidence:** git_detection_service.test.py
- [ ] Handle non-git directories - **Phase:** 2 - **Evidence:** git_detection_service.test.py
- [ ] Fallback to cwd - **Phase:** 2 - **Evidence:** git_detection_service.test.py

### AC#5: File conflict detection

- [ ] Identify conflicting files - **Phase:** 2 - **Evidence:** file_conflict_detection_service.test.py
- [ ] Categorize by type - **Phase:** 2 - **Evidence:** file_conflict_detection_service.test.py

### AC#6: Summary display

- [ ] Display all sections - **Phase:** 2 - **Evidence:** summary_formatter_service.test.py
- [ ] Color coding applied - **Phase:** 4 - **Evidence:** E2E test

---

**Checklist Progress:** 0/17 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] AutoDetectionService orchestrates all checks
- [ ] VersionDetectionService reads and compares versions
- [ ] ClaudeMdDetectionService detects CLAUDE.md
- [ ] GitDetectionService finds repository root
- [ ] FileConflictDetectionService identifies conflicts
- [ ] SummaryFormatterService formats output
- [ ] All data models defined

### Quality
- [ ] All 6 acceptance criteria have passing tests
- [ ] Edge cases covered (8 documented)
- [ ] Path validation prevents traversal
- [ ] NFRs met (<500ms detection, <50MB memory)
- [ ] Code coverage >95%

### Testing
- [ ] Unit tests for VersionDetectionService
- [ ] Unit tests for ClaudeMdDetectionService
- [ ] Unit tests for GitDetectionService
- [ ] Unit tests for FileConflictDetectionService
- [ ] Unit tests for SummaryFormatterService
- [ ] Integration tests for full detection flow
- [ ] E2E test with real git repo

### Documentation
- [ ] Docstrings for all public methods
- [ ] Summary output format documented

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Concurrent execution for independent checks (performance)
- Partial failures don't block other checks (reliability)
- 10-conflict limit in summary (usability)

**Related ADRs:**
- ADR-004: NPM Package Distribution

**References:**
- EPIC-013: Interactive Installer & Validation

---

**Story Template Version:** 2.1
**Last Updated:** 2025-11-25
