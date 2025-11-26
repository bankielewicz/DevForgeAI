---
id: STORY-070
title: Framework Release Automation
epic: EPIC-012
sprint: Backlog
status: Backlog
points: 12
priority: High
assigned_to: Unassigned
created: 2025-11-25
format_version: "2.1"
depends_on:
  - STORY-067
---

# Story: Framework Release Automation

## Description

**As a** DevForgeAI framework maintainer,
**I want** to run a single `scripts/release.sh` command that orchestrates the complete release workflow (sync operational files to src/, update version.json, generate checksums, create GitHub release, and publish to npm),
**so that** framework releases are consistent, auditable, and error-free without manual intervention across multiple complex steps.

## Acceptance Criteria

### AC#1: Interactive Version Selection and Pre-Flight Validation

**Given** I am in the DevForgeAI repository root with a clean git working tree (no uncommitted changes)
**When** I execute `bash scripts/release.sh`
**Then** the script:
- Prompts me to select version bump type: major, minor, patch, or custom (e.g., 1.2.3)
- Validates git status shows no uncommitted changes (blocks release if dirty tree detected)
- Runs test suite (`npm test` or equivalent) and blocks release if any tests fail
- Displays current version (from src/version.json) and calculated next version before proceeding
- Requires explicit confirmation (Y/N) before starting release process

---

### AC#2: Operational Files Sync to Distribution Source

**Given** the version bump is confirmed
**When** the sync phase executes
**Then** the script:
- Syncs `.claude/` → `src/claude/` recursively, excluding `*.backup*`, `__pycache__/`, `*.pyc`, `.DS_Store`
- Syncs `.devforgeai/` → `src/devforgeai/` recursively, excluding `backups/`, `qa/reports/`, `feedback/sessions/`, `*.log`
- Validates sync completeness by comparing file counts and directory structure (source vs destination)
- Reports any missing files or sync failures with specific file paths
- Creates `src/.sync-manifest.json` containing: sync timestamp, file count, excluded patterns, source hash

---

### AC#3: Version Metadata and Changelog Update

**Given** the operational files are synced successfully
**When** the versioning phase executes
**Then** the script:
- Updates `src/version.json` with: new version number (semver format), release date (ISO 8601 format), release notes path (`CHANGELOG.md#v{version}`)
- Generates or updates `CHANGELOG.md` with auto-generated release notes from git commits since last tag (format: `## [v{version}] - {date}`, grouped by type: feat, fix, chore, docs)
- Creates git tag `v{version}` with message "Release v{version}" and includes changelog excerpt
- Commits changes with message: "chore(release): bump version to {version}"

---

### AC#4: Integrity Verification with Checksum Generation

**Given** version metadata is updated
**When** the checksum generation phase executes
**Then** the script:
- Generates `src/checksums.txt` containing SHA-256 hashes for all files in `src/` directory (recursive, one file per line: `{hash}  {relative-path}`)
- Excludes from checksums: `checksums.txt` itself, `node_modules/`, `.git/`, temporary files
- Sorts checksums.txt alphabetically by file path for deterministic output
- Validates checksums file is >0 bytes and contains at least 50 entries (framework has 100+ files)
- Appends checksum file hash to version.json (`checksum_file_sha256` field)

---

### AC#5: GitHub Release Creation with Automated Changelog

**Given** checksums are generated and git tag is created
**When** the GitHub release phase executes
**Then** the script:
- Verifies `gh` CLI is installed and authenticated (`gh auth status`)
- Creates GitHub release using `gh release create v{version}` with:
  - Release title: "DevForgeAI v{version}"
  - Release notes: Auto-generated changelog from git commits (same content as CHANGELOG.md section)
  - Attachments: `src/checksums.txt` file
- Marks release as "latest" (not pre-release, unless version contains hyphen)
- Pushes git tag and release commit to origin/main
- Outputs release URL for verification

---

### AC#6: NPM Package Publication Integration

**Given** GitHub release is created successfully
**When** the npm publish phase executes
**Then** the script:
- Changes directory to `src/` (where package.json exists per STORY-067)
- Updates `src/package.json` version field to match `src/version.json` version
- Executes `npm publish` (or `npm publish --dry-run` if `--dry-run` flag passed to release.sh)
- Validates npm publish succeeded by checking exit code and npm registry response
- Tags npm package with `latest` dist-tag (or `beta` if pre-release version)
- Outputs npm package URL: `https://www.npmjs.com/package/@devforgeai/framework/v/{version}`

---

### AC#7: Rollback and Error Recovery

**Given** any phase fails during release execution
**When** an error is detected (non-zero exit code, validation failure, user cancellation)
**Then** the script:
- Immediately halts execution (does not proceed to next phase)
- Displays clear error message with failed phase name and specific error details
- Reverts uncommitted changes using `git reset --hard HEAD` (only if changes were made by script in current session)
- Deletes created git tag if it exists but GitHub release was not created: `git tag -d v{version}`
- Does NOT push to GitHub or npm if any local validation fails
- Outputs rollback summary: what was reverted, what remains
- Exits with code 1 (failure)

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Script"
      name: "release.sh"
      file_path: "scripts/release.sh"
      description: "Main release automation orchestrator script"
      interpreter: "bash"
      platform: "cross-platform (Linux, macOS, Windows via Git Bash/WSL)"
      requirements:
        - id: "SCR-001"
          description: "Must provide interactive version bump selection (major/minor/patch/custom)"
          testable: true
          test_requirement: "Test: Mock stdin input, verify version calculation"
          priority: "Critical"
        - id: "SCR-002"
          description: "Must validate clean git working tree before proceeding"
          testable: true
          test_requirement: "Test: Create dirty tree, verify script exits with error"
          priority: "Critical"
        - id: "SCR-003"
          description: "Must sync .claude/ to src/claude/ with exclusion patterns"
          testable: true
          test_requirement: "Test: Verify excluded files (*.backup*, __pycache__) not copied"
          priority: "High"
        - id: "SCR-004"
          description: "Must sync .devforgeai/ to src/devforgeai/ with exclusion patterns"
          testable: true
          test_requirement: "Test: Verify excluded dirs (backups/, qa/reports/) not copied"
          priority: "High"
        - id: "SCR-005"
          description: "Must generate SHA-256 checksums for all src/ files"
          testable: true
          test_requirement: "Test: Verify checksum file format and hash correctness"
          priority: "High"
        - id: "SCR-006"
          description: "Must create GitHub release via gh CLI"
          testable: true
          test_requirement: "Test: Mock gh CLI, verify release creation command"
          priority: "High"
        - id: "SCR-007"
          description: "Must execute npm publish for package distribution"
          testable: true
          test_requirement: "Test: Mock npm CLI, verify publish command with correct options"
          priority: "High"
        - id: "SCR-008"
          description: "Must rollback on any phase failure"
          testable: true
          test_requirement: "Test: Induce failure at each phase, verify rollback actions"
          priority: "Critical"
        - id: "SCR-009"
          description: "Must support --dry-run flag for simulation mode"
          testable: true
          test_requirement: "Test: Run with --dry-run, verify no external changes made"
          priority: "Medium"
        - id: "SCR-010"
          description: "Must support --yes flag for CI automation (skip confirmations)"
          testable: true
          test_requirement: "Test: Run with --yes, verify no interactive prompts"
          priority: "Medium"
      dependencies_external:
        - "git >= 2.25"
        - "gh >= 2.0 (GitHub CLI)"
        - "npm >= 8.0"
        - "bash >= 4.0"
        - "sha256sum OR shasum (platform-dependent)"
        - "rsync (optional, Linux/macOS)"

    - type: "Configuration"
      name: "release-config.sh"
      file_path: ".devforgeai/config/release-config.sh"
      description: "Release script configuration with customizable settings"
      requirements:
        - id: "CFG-001"
          description: "Must define EXCLUDE_PATTERNS array for sync operations"
          testable: true
          test_requirement: "Test: Verify patterns array is valid bash array syntax"
          priority: "High"
        - id: "CFG-002"
          description: "Must define NPM_REGISTRY URL (default: registry.npmjs.org)"
          testable: true
          test_requirement: "Test: Verify URL format and reachability check"
          priority: "Medium"
        - id: "CFG-003"
          description: "Must define CHECKSUM_ALGORITHM (default: sha256)"
          testable: true
          test_requirement: "Test: Verify only allowed algorithms (sha256, sha512)"
          priority: "Medium"

    - type: "DataModel"
      name: "version.json"
      file_path: "src/version.json"
      description: "Version metadata tracking file"
      schema:
        version: "string (semver format)"
        release_date: "string (ISO 8601)"
        release_notes_path: "string (path to changelog section)"
        checksum_file_sha256: "string (64-char hex hash)"
      requirements:
        - id: "DAT-001"
          description: "version field must match semver regex"
          testable: true
          test_requirement: "Test: Validate regex ^\\d+\\.\\d+\\.\\d+(-[a-zA-Z0-9]+)?"
          priority: "Critical"
        - id: "DAT-002"
          description: "release_date must be ISO 8601 format"
          testable: true
          test_requirement: "Test: Parse date with date -d, verify no error"
          priority: "High"

    - type: "DataModel"
      name: "checksums.txt"
      file_path: "src/checksums.txt"
      description: "SHA-256 integrity verification file for all distribution files"
      format: "BSD-style checksum format ({hash}  {filepath})"
      requirements:
        - id: "CHK-001"
          description: "Each line must match format: ^[a-f0-9]{64}  .+$"
          testable: true
          test_requirement: "Test: Regex validation on every line"
          priority: "High"
        - id: "CHK-002"
          description: "File must be sorted alphabetically by filepath"
          testable: true
          test_requirement: "Test: Compare checksums.txt with sorted version"
          priority: "Medium"
        - id: "CHK-003"
          description: "Must contain at least 50 entries (framework minimum)"
          testable: true
          test_requirement: "Test: wc -l checksums.txt >= 50"
          priority: "Medium"

    - type: "DataModel"
      name: "sync-manifest.json"
      file_path: "src/.sync-manifest.json"
      description: "Sync operation metadata for validation and auditing"
      schema:
        sync_timestamp: "string (ISO 8601)"
        file_count: "integer"
        excluded_patterns: "string[] (patterns applied)"
        source_hash: "string (hash of source directories)"
      requirements:
        - id: "MAN-001"
          description: "file_count must match actual synced file count"
          testable: true
          test_requirement: "Test: Compare manifest count with find src/ | wc -l"
          priority: "High"

    - type: "Logging"
      name: "release-log"
      file_path: ".devforgeai/releases/release-{version}-{timestamp}.log"
      description: "Audit trail log for release operations"
      log_level: "INFO"
      format: "[{timestamp}] [{phase}] {message}"
      retention: "Permanent (audit requirement)"
      requirements:
        - id: "LOG-001"
          description: "Must capture start/end timestamp of each phase"
          testable: true
          test_requirement: "Test: Parse log, verify phase timing entries exist"
          priority: "Medium"
        - id: "LOG-002"
          description: "Must capture all command outputs (git, npm, gh)"
          testable: true
          test_requirement: "Test: Run release, verify external commands logged"
          priority: "Medium"
        - id: "LOG-003"
          description: "Must capture error details on failure"
          testable: true
          test_requirement: "Test: Induce failure, verify error logged with stack"
          priority: "High"

  business_rules:
    - id: "BR-001"
      name: "Version Uniqueness"
      description: "Version number must not already exist in npm registry or git tags"
      validation: "Check npm view versions AND git tag -l before proceeding"
      test_requirement: "Test: Mock existing version, verify script blocks with error"

    - id: "BR-002"
      name: "Pre-Release Detection"
      description: "Versions with hyphen (e.g., -beta.1) are marked as pre-release"
      validation: "If version contains '-', set github prerelease=true and npm tag=beta"
      test_requirement: "Test: Create beta release, verify prerelease flags set"

    - id: "BR-003"
      name: "Atomic Phases"
      description: "Each phase must fully complete or fully revert - no partial states"
      validation: "Wrap each phase in transaction-like error handling"
      test_requirement: "Test: Interrupt mid-phase, verify clean state after rollback"

    - id: "BR-004"
      name: "Dependency Order"
      description: "Phases must execute in order: preflight → sync → version → checksum → github → npm"
      validation: "Sequential function calls with validation checkpoints"
      test_requirement: "Test: Add phase logging, verify execution order"

    - id: "BR-005"
      name: "STORY-067 Integration"
      description: "NPM publish workflow must use STORY-067 infrastructure (src/package.json)"
      validation: "Verify src/package.json exists and is valid before npm phase"
      test_requirement: "Test: Remove src/package.json, verify script fails with helpful error"

  non_functional_requirements:
    - category: "Performance"
      requirements:
        - id: "NFR-001"
          description: "Sync phase < 60 seconds for 1,000 files"
          metric: "Duration measured via time command"
          threshold: "60s"
          test_requirement: "Test: Create 1,000 test files, measure sync duration"
        - id: "NFR-002"
          description: "Checksum generation < 30 seconds for 1,000 files"
          metric: "Duration measured via time command"
          threshold: "30s"
          test_requirement: "Test: Generate checksums for 1,000 files, measure duration"
        - id: "NFR-003"
          description: "Total execution < 5 minutes (excluding network I/O)"
          metric: "End-to-end duration (dry-run mode)"
          threshold: "300s"
          test_requirement: "Test: Full dry-run, measure total duration"

    - category: "Security"
      requirements:
        - id: "NFR-004"
          description: "Use SHA-256 for all checksums (not MD5/SHA-1)"
          metric: "Algorithm validation in code review"
          threshold: "SHA-256 only"
          test_requirement: "Test: Verify sha256sum used, not md5sum/sha1sum"
        - id: "NFR-005"
          description: "No credentials in logs or output"
          metric: "Grep logs for token patterns"
          threshold: "Zero matches"
          test_requirement: "Test: Run release, grep for npm_token/ghp_/github_token in logs"
        - id: "NFR-006"
          description: "Exclude sensitive files from sync (*.env, *.key, secrets/)"
          metric: "Verify exclusion patterns in config"
          threshold: "All patterns present"
          test_requirement: "Test: Create .env file in source, verify not synced"

    - category: "Reliability"
      requirements:
        - id: "NFR-007"
          description: "Rollback on any non-zero exit code from external commands"
          metric: "Error handling code coverage"
          threshold: "100% of external calls wrapped"
          test_requirement: "Test: Mock failing git/npm/gh, verify rollback triggered"
        - id: "NFR-008"
          description: "Dry-run mode makes zero external changes"
          metric: "File system and network diff before/after"
          threshold: "Zero changes"
          test_requirement: "Test: Snapshot before dry-run, compare after"
        - id: "NFR-009"
          description: "Idempotent checksums (same input = same output)"
          metric: "Run checksum twice, compare files"
          threshold: "Identical files"
          test_requirement: "Test: Generate checksums twice, diff should be empty"

    - category: "Maintainability"
      requirements:
        - id: "NFR-010"
          description: "Script organized into modular functions"
          metric: "Function count and average function length"
          threshold: "≥10 functions, ≤50 lines each"
          test_requirement: "Test: Static analysis with shellcheck, count functions"
        - id: "NFR-011"
          description: "Cross-platform compatibility (Linux, macOS, Git Bash)"
          metric: "Test on all platforms"
          threshold: "100% tests pass on all 3"
          test_requirement: "Test: CI matrix with Ubuntu, macOS, Windows (Git Bash)"
```

## UI Specification

### Interface Type: Terminal CLI

**Command Syntax:**
```bash
bash scripts/release.sh [OPTIONS]
```

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `--dry-run` | Simulate release without pushing to GitHub/npm | false |
| `--yes`, `-y` | Skip interactive confirmations (CI mode) | false |
| `--help`, `-h` | Show usage information and exit | - |
| `--version`, `-v` | Show script version and exit | - |

---

### Interactive Prompts

**Prompt 1: Version Selection**
```
=== DevForgeAI Release Workflow ===
Current version: 1.2.3

Select version bump type:
  1) patch  (1.2.3 → 1.2.4)
  2) minor  (1.2.3 → 1.3.0)
  3) major  (1.2.3 → 2.0.0)
  4) custom (enter specific version)

Enter selection [1-4]:
```

**Prompt 2: Confirmation (before destructive operations)**
```
⚠️  Release v1.2.4 will:
  - Create git tag v1.2.4
  - Push to origin/main
  - Create GitHub release
  - Publish to npm registry

Proceed? [y/N]:
```

---

### Progress Indicators

**Phase Progress Display:**
```
[1/7] Pre-flight validation...
      ✓ Git working tree clean
      ✓ Tests passing (156 tests)
      ✓ gh CLI authenticated
      ✓ npm authenticated

[2/7] Syncing operational files...
      Copying .claude/ → src/claude/
      ├── skills/: 15 directories
      ├── commands/: 11 files
      ├── agents/: 20 files
      └── memory/: 8 files
      ✓ Synced 234 files (excluded 12)

[3/7] Updating version metadata...
      ✓ version.json updated to 1.2.4
      ✓ CHANGELOG.md updated
      ✓ Git tag v1.2.4 created

[4/7] Generating checksums...
      ████████████████████ 100%
      ✓ checksums.txt generated (230 files)

[5/7] Creating GitHub release...
      ✓ Release created: https://github.com/.../releases/tag/v1.2.4

[6/7] Publishing to npm...
      ✓ Published @devforgeai/framework@1.2.4

[7/7] Finalizing release...
      ✓ Pushed to origin/main
      ✓ Release log saved
```

---

### Output Formatting

**Success Summary:**
```
╔═══════════════════════════════════════════════════════════╗
║           ✅ Release v1.2.4 Complete                      ║
╠═══════════════════════════════════════════════════════════╣
║  Files synced:     234                                    ║
║  Checksum entries: 230                                    ║
║  Duration:         3m 45s                                 ║
╠───────────────────────────────────────────────────────────╣
║  GitHub release:                                          ║
║  https://github.com/user/repo/releases/tag/v1.2.4         ║
║                                                           ║
║  NPM package:                                             ║
║  https://www.npmjs.com/package/@devforgeai/framework      ║
╚═══════════════════════════════════════════════════════════╝
```

**Error Output:**
```
╔═══════════════════════════════════════════════════════════╗
║           ❌ Release Failed                               ║
╠═══════════════════════════════════════════════════════════╣
║  Phase:     [3/7] Updating version metadata               ║
║  Error:     Git tag v1.2.4 already exists                 ║
╠───────────────────────────────────────────────────────────╣
║  Rollback:  ✓ Reverted uncommitted changes                ║
║             ✓ Deleted local tag (if created)              ║
║             ✗ GitHub release: Not created                 ║
║             ✗ NPM publish: Not executed                   ║
╠───────────────────────────────────────────────────────────╣
║  To fix:    Delete existing tag:                          ║
║             git tag -d v1.2.4                             ║
║             git push origin --delete v1.2.4               ║
╚═══════════════════════════════════════════════════════════╝
```

---

### Color Coding (ANSI)

| Element | Color Code | Usage |
|---------|------------|-------|
| Success (`✓`) | Green (`\033[32m`) | Completed steps |
| Error (`❌`) | Red (`\033[31m`) | Failed operations |
| Warning (`⚠️`) | Yellow (`\033[33m`) | Confirmations, cautions |
| Info (`ℹ️`) | Blue (`\033[34m`) | Progress updates |
| Phase numbers | Cyan (`\033[36m`) | Phase headers |
| Reset | `\033[0m` | Return to default |

**Color Fallback:** Detect `NO_COLOR` environment variable or non-TTY output, disable colors.

---

### Accessibility

- **Non-visual indicators:** All status (success/failure) communicated via exit codes (0/1) for CI
- **Screen reader compatible:** Progress uses text descriptions, not just emojis
- **High contrast:** Uses standard ANSI colors, visible on both light/dark terminals
- **No flashing:** Progress bars use static updates (carriage return), no animation

## Edge Cases

1. **Dirty Git Working Tree:** User has uncommitted changes before running release script. Script detects dirty state in pre-flight validation (AC#1), displays file list, and blocks release with message: "Uncommitted changes detected. Commit or stash changes before releasing."

2. **Network Failures During GitHub/NPM Operations:** GitHub release or npm publish fails due to network timeout, authentication error, or API rate limit. Script catches error, displays specific failure reason (e.g., "gh CLI authentication expired - run `gh auth login`"), and does NOT proceed to subsequent phases.

3. **Checksum File Corruption or Missing Files:** After sync, some source files are missing. Sync validation (AC#2) detects mismatch between expected and actual file counts, halts with error: "Sync incomplete: expected 150 files, found 148. Missing: [list]."

4. **Duplicate Version Number:** User selects version bump that results in version number already published to npm or tagged in GitHub. Script checks `npm view versions` and `git tag -l` during pre-flight, detects duplicate, and blocks with error.

5. **Cross-Platform Path Separator Issues:** Script runs on Windows where path separators differ. Script normalizes all paths to forward slashes using bash parameter expansion or cross-platform path utilities.

6. **Large File Sync Performance:** Framework grows to 10,000+ files. Sync phase displays progress indicator using rsync --progress or equivalent.

7. **Pre-Release or Beta Versions:** User wants to publish pre-release version (e.g., v2.0.0-beta.1). Script supports custom version input and marks GitHub release as "pre-release" if version contains hyphen.

8. **Rollback After Partial GitHub Release:** GitHub release created successfully but npm publish fails. Script does NOT auto-delete GitHub release. Outputs manual recovery commands.

9. **Concurrent Releases from Different Branches:** Two maintainers attempt release simultaneously. Second detects version conflict during npm publish (409 Conflict).

10. **Changelog Generation from Merge Commits Only:** Repository uses squash-merge strategy. Script falls back to using GitHub pull request titles for changelog via `gh pr list`.

## Dependencies

**Depends on:**
- **STORY-067 (NPM Registry Publishing Workflow):**
  - Requires `src/package.json` to exist and be valid
  - Uses npm publish workflow defined in STORY-067
  - Integrates with npm version update mechanism (AC#6)

**External Dependencies:**
- **Git:** Version 2.25+ (for tag signing, submodule support if needed)
- **gh CLI:** Version 2.0+ (GitHub CLI for release creation, authenticated)
- **npm CLI:** Version 8.0+ (for package publishing, authenticated to registry)
- **Bash:** Version 4.0+ (POSIX-compliant shell, available on all platforms)
- **rsync:** (optional, for faster sync on Linux/macOS, falls back to cp -r on Windows)
- **sha256sum or shasum:** (for checksum generation, platform-dependent command)

## Definition of Done

### Implementation
- [ ] `scripts/release.sh` script created with all 7 phases
- [ ] `.devforgeai/config/release-config.sh` configuration file created
- [ ] Interactive version selection implemented
- [ ] Pre-flight validation (dirty tree, tests) implemented
- [ ] Operational files sync implemented with exclusion patterns
- [ ] Version.json update logic implemented
- [ ] CHANGELOG.md auto-generation implemented
- [ ] SHA-256 checksum generation implemented
- [ ] GitHub release creation via gh CLI implemented
- [ ] NPM publish integration with STORY-067 implemented
- [ ] Rollback on failure implemented for all phases
- [ ] --dry-run flag implemented
- [ ] --yes flag for CI automation implemented

### Quality
- [ ] All tests passing (unit + integration)
- [ ] Test coverage >= 80% for script logic (via bats or shellspec)
- [ ] Cyclomatic complexity within limits (per function < 10)
- [ ] No hardcoded secrets or credentials
- [ ] shellcheck linting passes with no errors

### Testing
- [ ] Unit tests for each script function
- [ ] Integration tests for full workflow (dry-run mode)
- [ ] Cross-platform tests (Linux, macOS, Windows Git Bash)
- [ ] Error scenario tests (network failure, auth failure, dirty tree)
- [ ] Rollback tests for each phase failure scenario
- [ ] Performance tests (sync 1,000 files < 60s)

### Documentation
- [ ] README section for release workflow added
- [ ] Inline script comments explaining each phase
- [ ] Error messages include resolution guidance
- [ ] Configuration options documented in release-config.sh

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Implementation Notes

_This section is populated during development._

### Files Created/Modified
- `scripts/release.sh` - Main release automation script
- `.devforgeai/config/release-config.sh` - Configuration file
- `src/version.json` - Version metadata (updated by script)
- `src/checksums.txt` - SHA-256 checksums (generated by script)
- `src/.sync-manifest.json` - Sync audit metadata
- `CHANGELOG.md` - Release notes (updated by script)

### Test Files
- `tests/release/test_release.bats` - Bats test suite
- `tests/release/fixtures/` - Test fixtures for mocking

### Approved Deferrals
_None at story creation time._

## Acceptance Criteria Verification Checklist

_Updated during TDD phases. Maps granular verification items to phases._

### AC#1: Interactive Version Selection and Pre-Flight Validation
- [ ] Version bump selection prompt displays - Phase: 2 - Evidence: Manual testing
- [ ] Git dirty tree detection blocks release - Phase: 1 - Evidence: Unit test
- [ ] Test suite execution and validation - Phase: 4 - Evidence: Integration test
- [ ] Version confirmation prompt displayed - Phase: 2 - Evidence: Manual testing

### AC#2: Operational Files Sync to Distribution Source
- [ ] .claude/ sync with exclusions - Phase: 2 - Evidence: Unit test
- [ ] .devforgeai/ sync with exclusions - Phase: 2 - Evidence: Unit test
- [ ] File count validation - Phase: 2 - Evidence: Unit test
- [ ] sync-manifest.json generation - Phase: 2 - Evidence: Unit test

### AC#3: Version Metadata and Changelog Update
- [ ] version.json update with semver - Phase: 2 - Evidence: Unit test
- [ ] CHANGELOG.md auto-generation - Phase: 2 - Evidence: Unit test
- [ ] Git tag creation - Phase: 2 - Evidence: Unit test
- [ ] Commit with release message - Phase: 2 - Evidence: Unit test

### AC#4: Integrity Verification with Checksum Generation
- [ ] SHA-256 checksums generated - Phase: 2 - Evidence: Unit test
- [ ] Checksums sorted alphabetically - Phase: 2 - Evidence: Unit test
- [ ] Minimum entry count validation - Phase: 2 - Evidence: Unit test
- [ ] checksum_file_sha256 added to version.json - Phase: 2 - Evidence: Unit test

### AC#5: GitHub Release Creation
- [ ] gh CLI authentication check - Phase: 2 - Evidence: Unit test
- [ ] GitHub release creation - Phase: 4 - Evidence: Integration test (mocked)
- [ ] Release notes attached - Phase: 4 - Evidence: Integration test
- [ ] Release URL output - Phase: 4 - Evidence: Integration test

### AC#6: NPM Package Publication Integration
- [ ] package.json version update - Phase: 2 - Evidence: Unit test
- [ ] npm publish execution - Phase: 4 - Evidence: Integration test (mocked)
- [ ] Dist-tag application (latest/beta) - Phase: 4 - Evidence: Integration test
- [ ] NPM URL output - Phase: 4 - Evidence: Integration test

### AC#7: Rollback and Error Recovery
- [ ] Phase failure detection - Phase: 2 - Evidence: Unit test
- [ ] Git reset on failure - Phase: 2 - Evidence: Unit test
- [ ] Tag deletion on partial failure - Phase: 2 - Evidence: Unit test
- [ ] Rollback summary output - Phase: 2 - Evidence: Unit test
- [ ] Exit code 1 on failure - Phase: 2 - Evidence: Unit test
