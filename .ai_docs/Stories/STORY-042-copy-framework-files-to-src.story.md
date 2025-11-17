---
id: STORY-042
title: Copy Framework Files from Operational Folders to src/
epic: EPIC-009
sprint: Backlog
status: Backlog
points: 8
priority: High
assigned_to: TBD
created: 2025-11-16
format_version: "2.0"
---

# Story: Copy Framework Files from Operational Folders to src/

## Description

**As a** Framework Maintainer,
**I want** to copy all DevForgeAI framework files from operational directories (.claude/, .devforgeai/) to the new src/ structure while preserving originals intact,
**so that** I can establish a clean separation between operational framework (current development) and packaged source (for distribution) without disrupting ongoing work.

## Acceptance Criteria

### 1. [ ] Copy .claude/ Framework Files to src/claude/ Preserving Structure

**Given** the operational .claude/ directory contains ~370 framework files across 5 subdirectories (agents, commands, memory, scripts, skills)
**When** the migration script executes the copy operation
**Then** all files are copied to src/claude/ with identical directory structure
**And** file count matches exactly (~370 files, verified with `find src/claude -type f | wc -l`)
**And** original .claude/ directory remains completely unchanged (verified via checksum comparison before/after)
**And** directory structure depth preserved (e.g., .claude/skills/devforgeai-development/references/ → src/claude/skills/devforgeai-development/references/)

---

### 2. [ ] Copy .devforgeai/ Configuration and Documentation Only

**Given** the operational .devforgeai/ directory contains config, docs, protocols, specs, and tests subdirectories, plus generated content (qa/reports, RCA, adrs)
**When** the migration script executes the copy operation
**Then** only config/, docs/, protocols/, specs/, and tests/ subdirectories are copied to src/devforgeai/
**And** generated content directories (qa/reports/, RCA/, adrs/, feedback/imported/, logs/) are explicitly excluded
**And** file count is validated:
  - config: ~8 files
  - docs: ~17 files
  - protocols: ~10 files
  - specs: ~30 files (enhancements/, requirements/)
  - tests: ~15 files
  - Total: ~80 files in src/devforgeai/
**And** original .devforgeai/ remains unchanged (checksum verified)

---

### 3. [ ] Copy CLAUDE.md as Template with No Modifications

**Given** the root CLAUDE.md file (1,061 lines, ~37KB) serves as the project-wide framework guide
**When** the migration script copies CLAUDE.md to src/CLAUDE.md
**Then** the file is copied byte-for-byte (SHA256 checksum matches source)
**And** file size matches exactly (verified with `stat -c%s CLAUDE.md` = `stat -c%s src/CLAUDE.md`)
**And** the original CLAUDE.md remains in root directory unchanged
**And** src/CLAUDE.md is marked as template (add comment at top: `<!-- TEMPLATE: This is the source template. Installer merges this with user's CLAUDE.md -->`)

---

### 4. [ ] Validate File Integrity with Checksum Verification

**Given** ~450 total files will be copied (.claude/ ~370, .devforgeai/ ~80, CLAUDE.md 1)
**When** the migration completes
**Then** a validation report is generated showing:
- Total files copied: 450 ±10 (allowing for file count variance during development)
- Checksum verification: 100% match between source and destination (SHA256 for all files)
- File size verification: 100% match (0 size discrepancies)
- Directory structure verification: All subdirectories recreated (verify with `diff <(cd .claude && find . -type d) <(cd src/claude && find . -type d)`)
- Zero corruption detected (no partial writes, no permission errors, all files readable)
**And** checksums.txt manifest created with format: `<sha256> <file-path>` for all 450 files
**And** validation command `shasum -c checksums.txt` exits with code 0 (all checksums OK)

---

### 5. [ ] Exclude Backup Files and Build Artifacts

**Given** the source directories may contain .backup files, temporary files, and build artifacts
**When** the migration script executes
**Then** the following patterns are explicitly excluded from copying:
- `*.backup*` (all backup files, ~60 files excluded)
- `*.tmp`, `*.temp` (temporary files)
- `__pycache__/`, `*.pyc` (Python compiled bytecode)
- `*.egg-info/` (Python package metadata)
- `htmlcov/` (coverage HTML reports)
- `.coverage` (coverage data files)
- `node_modules/` (if present in any skill)
- `.git/` (version control, excluded by default)
**And** validation confirms zero excluded patterns present in src/ (grep search returns no matches)
**And** exclusion report shows count of files excluded per pattern (e.g., "Excluded 60 .backup files, 25 __pycache__ dirs")

---

### 6. [ ] Git Track All Copied Files for Version Control

**Given** all files have been successfully copied and validated in src/
**When** the migration script completes
**Then** all ~450 copied files are added to Git staging area (`git add src/ CLAUDE.md`)
**And** Git status shows 450 new files ready to commit (verified with `git status --porcelain | grep "^A" | wc -l`)
**And** a pre-commit validation confirms:
  - No binary files >1MB staged (framework is text-based)
  - No secrets detected (grep for API_KEY, PASSWORD, SECRET patterns returns no matches)
  - All files have proper line endings (LF on Linux, CRLF on Windows if needed)
**And** Git diff --cached shows only additions (no deletions or modifications to existing files)

---

### 7. [ ] Preserve Original Operational Directories for Parallel Development

**Given** the .claude/ and .devforgeai/ directories are actively used for ongoing development
**When** the migration completes
**Then** both original directories remain:
- Byte-for-byte identical to pre-migration state (verified via `sha256sum -c checksums-before.txt`)
- Fully functional (Claude Code Terminal continues to load skills/commands from .claude/)
- No symbolic links or references created (true file copies, not links - verified with `find src/ -type l | wc -l` returns 0)
- File count unchanged (before: N files, after: N files in operational folders)
**And** validation script confirms zero modifications to operational directories
**And** commands continue to work (`/dev --help`, `/qa --help` both exit 0)

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Worker"
      name: "MigrationScript"
      file_path: "src/scripts/migrate-framework-files.sh"
      requirements:
        - id: "WKR-001"
          description: "Copy all .claude/ files to src/claude/ preserving directory structure"
          testable: true
          test_requirement: "Test: diff -r .claude/ src/claude/ excluding excluded patterns returns no differences"
          priority: "Critical"

        - id: "WKR-002"
          description: "Copy config/docs/protocols/specs/tests from .devforgeai/ to src/devforgeai/"
          testable: true
          test_requirement: "Test: File count in src/devforgeai/ matches expected ~80 files"
          priority: "Critical"

        - id: "WKR-003"
          description: "Exclude backup files, generated content, and build artifacts"
          testable: true
          test_requirement: "Test: find src/ -name '*.backup*' returns 0 results"
          priority: "High"

        - id: "WKR-004"
          description: "Generate SHA256 checksums for all copied files"
          testable: true
          test_requirement: "Test: shasum -c checksums.txt exits 0, all checksums verified"
          priority: "Critical"

        - id: "WKR-005"
          description: "Preserve original operational folders unchanged"
          testable: true
          test_requirement: "Test: Checksum .claude/ before/after, verify identical"
          priority: "Critical"

        - id: "WKR-006"
          description: "Stage all copied files in Git for version control"
          testable: true
          test_requirement: "Test: git status --porcelain | grep '^A' | wc -l returns ~450"
          priority: "High"

        - id: "WKR-007"
          description: "Copy CLAUDE.md to src/CLAUDE.md as template"
          testable: true
          test_requirement: "Test: sha256sum CLAUDE.md and sha256sum src/CLAUDE.md match"
          priority: "High"

    - type: "Configuration"
      name: "MigrationConfig"
      file_path: "src/scripts/migration-config.json"
      requirements:
        - id: "CONF-001"
          description: "Define source directories to copy (.claude/, .devforgeai/, CLAUDE.md)"
          testable: true
          test_requirement: "Test: jq -r '.sources[]' migration-config.json returns 3 paths"
          priority: "High"

        - id: "CONF-002"
          description: "Define exclusion patterns for backup/generated files"
          testable: true
          test_requirement: "Test: jq -r '.exclude_patterns[]' migration-config.json | wc -l >= 8"
          priority: "High"

        - id: "CONF-003"
          description: "Define validation thresholds (100% checksum match, ±10 file variance)"
          testable: true
          test_requirement: "Test: jq -r '.validation.checksum_match_percentage' returns 100"
          priority: "Medium"

    - type: "DataModel"
      name: "ChecksumManifest"
      file_path: "checksums.txt"
      requirements:
        - id: "DATA-001"
          description: "Generate SHA256 checksum manifest for all copied files"
          testable: true
          test_requirement: "Test: wc -l checksums.txt returns ~450 lines"
          priority: "Critical"

        - id: "DATA-002"
          description: "Manifest format: <sha256> <filepath> (standard shasum format)"
          testable: true
          test_requirement: "Test: head -1 checksums.txt matches regex '^[a-f0-9]{64}\\s+.+$'"
          priority: "High"

        - id: "DATA-003"
          description: "Manifest verifiable with standard shasum tool"
          testable: true
          test_requirement: "Test: shasum -c checksums.txt exits 0"
          priority: "Critical"

    - type: "Logging"
      name: "MigrationLogger"
      file_path: "src/scripts/migration.log"
      requirements:
        - id: "LOG-001"
          description: "Log all file copy operations with timestamps"
          testable: true
          test_requirement: "Test: grep 'COPY:' migration.log | wc -l returns ~450"
          priority: "Medium"

        - id: "LOG-002"
          description: "Log all validation checks (checksum, file size, structure)"
          testable: true
          test_requirement: "Test: grep 'VALIDATE:' migration.log | wc -l returns ~450"
          priority: "High"

        - id: "LOG-003"
          description: "Log all exclusions with pattern matched"
          testable: true
          test_requirement: "Test: grep 'EXCLUDE:' migration.log shows excluded files with matching pattern"
          priority: "Medium"

        - id: "LOG-004"
          description: "Log summary statistics at completion"
          testable: true
          test_requirement: "Test: tail -10 migration.log contains 'Files copied:', 'Checksums verified:', 'Exclusions:'"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Original operational folders (.claude/, .devforgeai/) must remain completely unchanged"
      test_requirement: "Test: Generate checksums before migration, verify identical after migration"

    - id: "BR-002"
      rule: "Only framework source files copied (no generated content like qa/reports, RCA, adrs)"
      test_requirement: "Test: ls src/devforgeai/ excludes qa/reports/, RCA/, adrs/, feedback/imported/, logs/"

    - id: "BR-003"
      rule: "File integrity must be 100% (no corruption tolerated)"
      test_requirement: "Test: All checksums match, zero file size discrepancies"

    - id: "BR-004"
      rule: "Exclusion patterns must prevent backup/artifact pollution in src/"
      test_requirement: "Test: find src/ -name '*.backup*' -o -name '*.pyc' -o -name '__pycache__' returns 0 results"

    - id: "BR-005"
      rule: "Migration must be idempotent (safe to run multiple times)"
      test_requirement: "Test: Run script twice, second run skips files with matching checksums, no duplicate copies"

    - id: "BR-006"
      rule: "Script must fail fast on first corruption/error (atomic per directory)"
      test_requirement: "Test: Simulate corruption, verify script halts and reports error before continuing"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Copy operation completes quickly for ~450 files"
      metric: "< 2 minutes for ~450 files (~15 MB total) on SSD"
      test_requirement: "Test: time bash migrate-framework-files.sh, assert elapsed < 120s"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Checksum validation efficient for all files"
      metric: "< 1 minute for ~450 checksums with parallel processing"
      test_requirement: "Test: time shasum -c checksums.txt, assert elapsed < 60s"

    - id: "NFR-003"
      category: "Performance"
      requirement: "Memory footprint minimal during large file operations"
      metric: "< 50 MB memory usage (streaming copy, not loading files into memory)"
      test_requirement: "Test: Monitor memory during execution, assert peak < 50 MB"

    - id: "NFR-004"
      category: "Reliability"
      requirement: "Atomic operation per directory (all files or none)"
      metric: "0 partial directory states (if directory fails, no files left behind)"
      test_requirement: "Test: Simulate failure during skills/ copy, verify no partial skills/ in src/"

    - id: "NFR-005"
      category: "Reliability"
      requirement: "Rollback capability on failure"
      metric: "100% cleanup on error (all copied files removed, src/ returned to Phase 1 state)"
      test_requirement: "Test: Trigger error mid-migration, verify rollback removes all files, src/ structure remains with only .gitkeep files"

    - id: "NFR-006"
      category: "Reliability"
      requirement: "Idempotent execution (safe to run multiple times)"
      metric: "0 errors on second execution (skips files with matching checksums)"
      test_requirement: "Test: Run script twice, second run reports 'X files already copied (checksums match), 0 files copied'"

    - id: "NFR-007"
      category: "Security"
      requirement: "File permissions preserved during copy"
      metric: "100% permission match (chmod values identical source vs destination)"
      test_requirement: "Test: stat -c %a .claude/scripts/install_hooks.sh = stat -c %a src/claude/scripts/install_hooks.sh (both 755)"

    - id: "NFR-008"
      category: "Security"
      requirement: "Exclusion patterns prevent copying sensitive files"
      metric: "0 .env, secrets.json, *.key files in src/"
      test_requirement: "Test: grep -r 'API_KEY\\|PASSWORD\\|SECRET' src/ returns no matches (or only in documentation/examples)"

```

### Dependencies

**External Tools:**
- bash 4.0+ (for migration script)
- rsync 3.0+ or cp command (for file copying)
- sha256sum (Linux) or shasum (macOS) for checksum generation
- git (for staging files)
- find, wc, grep (standard Unix utilities)

**Internal Dependencies:**
- STORY-041 complete (src/ directory structure exists)
- version.json present (for migration status tracking)

---

## Edge Cases

### 1. Existing Files in src/ Directories
**Scenario:** src/claude/ or src/devforgeai/ already contain files from Phase 1 or previous runs
**Expected:** Script detects existing files, compares checksums, skips files with matching checksums, overwrites files with different checksums (after user confirmation), logs all conflict resolutions
**Handling:** Generate checksums for existing files, compare with source, prompt for conflicts: "Overwrite (file changed)", "Skip (file identical)", "Abort (manual resolution needed)"

### 2. Permission Errors During Copy
**Scenario:** Source file is unreadable (permission 000) or destination is unwritable
**Expected:** Script logs specific file path and error, continues with remaining files (fault-tolerant), reports all failures in summary with actionable fix commands
**Handling:** Try-catch on each copy operation, accumulate errors, display: "Failed to copy {path}: Permission denied. Run: chmod +r {source}"

### 3. Partial Copy Due to Interruption
**Scenario:** Script interrupted mid-execution (Ctrl+C, system crash, terminal closed)
**Expected:** Validation detects incomplete file count (e.g., 200/450 files copied), reports exact missing files via diff, provides resume command to complete migration without re-copying successful files
**Handling:** Use checkpoint file (.migration-checkpoint.json) tracking last successful file, resume from checkpoint on re-run

### 4. File Corruption Detection
**Scenario:** Checksum verification fails for any file (bit flip, disk error, incomplete write)
**Expected:** Script immediately halts on first corruption, reports corrupted files with source/destination checksums, provides rollback command to remove all copied files and retry
**Handling:** After each file copy, compute checksum, compare with source, fail fast: "CORRUPTION: {file} - Source: {hash1}, Dest: {hash2}. Rollback required."

### 5. Symlink Handling
**Scenario:** Source directories contain symbolic links (e.g., .claude/skills/shared → ../common)
**Expected:** Script detects symlinks (find -type l), logs them separately with target paths, follows symlink to copy target file (default behavior) or preserves symlink structure (configurable via --preserve-links flag), ensures no broken links in src/
**Handling:** Count symlinks, follow by default, log: "SYMLINK: .claude/skills/shared → ../common (copying target file)"

### 6. Large File Handling
**Scenario:** Individual file exceeds 10 MB (unlikely but possible for test fixtures, large documentation)
**Expected:** Script uses chunked copy with progress reporting (copying {file} - 25% complete), validates checksum in chunks to prevent memory overflow, reports success with total size copied
**Handling:** Detect file size >10MB, use streaming copy, display progress every 25%

### 7. Case-Sensitive Filesystem Conflicts
**Scenario:** Migrating between case-insensitive (Windows/macOS) and case-sensitive (Linux) filesystems where File.md and file.md both exist
**Expected:** Script detects potential case conflicts (compare lowercase filenames for duplicates), warns user with conflicting filenames, suggests resolution (rename one file, merge content, skip), halts until resolved
**Handling:** Build lowercase filename map, detect duplicates, prompt: "Case conflict: File.md and file.md both exist. Rename or skip?"

---

## Data Validation Rules

1. **File count validation:** Exact count per directory with ±10 tolerance:
   - src/claude/agents: ~24 files
   - src/claude/commands: ~22 files
   - src/claude/memory: ~11 files
   - src/claude/scripts: ~149 files
   - src/claude/skills: ~164 files across 10 skills
   - src/devforgeai/config: ~8 files
   - src/devforgeai/docs: ~17 files
   - src/devforgeai/protocols: ~10 files
   - src/devforgeai/specs: ~30 files
   - src/devforgeai/tests: ~15 files
   - Total: ~450 files

2. **Checksum validation:** SHA256 algorithm, 64-character hex digest, 100% match rate required (zero tolerance for corruption)

3. **File size validation:** Source and destination byte counts must match exactly (stat -c%s comparison), zero tolerance for size discrepancies

4. **Directory structure validation:** Recursive diff of directory trees, zero missing directories, zero extra directories beyond source structure

5. **Exclusion pattern validation:** All patterns in migration-config.json must be applied, validation: `find src/ -name [pattern]` returns 0 results for each exclusion

6. **Git staging validation:** All copied files show as "A" (added) in git status --porcelain, zero files show as "M" (modified - would indicate overwrite of tracked files)

7. **Symlink validation:** If symlinks preserved, target must exist in src/, no broken links (verify with `find src/ -xtype l` returns 0 - no broken symlinks)

8. **Permission validation:** Execute bits preserved for .sh files (chmod 755), read-only for .md files (chmod 644), verify with stat -c%a

---

## Non-Functional Requirements

### Performance
- Copy operation: < 2 minutes for ~450 files (~15 MB total)
- Checksum validation: < 1 minute (parallel processing, 4 threads)
- Memory usage: < 50 MB (streaming, not buffering)
- No blocking: Concurrent reads, sequential writes

### Security
- File permissions preserved (755 for scripts, 644 for docs)
- No sudo required (user permissions sufficient)
- Secret exclusion: grep for API_KEY, PASSWORD, SECRET in src/
- Pre-commit validation: Block secrets from being staged

### Reliability
- Atomic per directory (all files in dir copied or none)
- Rollback on failure (remove all copied files)
- Idempotent (safe to run multiple times, skip unchanged files)
- Error recovery: Resume from checkpoint

### Scalability
- Supports 500+ files (if framework grows)
- Parallel copy capable (copy .claude/ and .devforgeai/ simultaneously)
- Progress reporting (file N of M, ETA)
- Configurable exclusions (JSON config, no hardcoded patterns)

---

## Definition of Done

### Implementation
- [ ] migrate-framework-files.sh script created and executable
- [ ] migration-config.json created with all required fields
- [ ] All ~450 files copied to src/ with structure preserved
- [ ] checksums.txt manifest generated with all file hashes
- [ ] migration-report.md generated with results
- [ ] migration.log created with detailed operation log
- [ ] Exclusion patterns applied (0 backup/artifact files in src/)
- [ ] Git staging complete (450 files added)

### Quality
- [ ] All 7 acceptance criteria have passing validation tests
- [ ] All 6 business rules enforced and tested
- [ ] All 8 NFRs met and measured
- [ ] All 7 edge cases handled with test coverage
- [ ] Checksum verification: 100% match rate
- [ ] Original folders unchanged: 100% identical checksums

### Testing
- [ ] Unit test: File copy operation (10 files, verify all copied)
- [ ] Unit test: Checksum generation (verify SHA256 correct)
- [ ] Unit test: Exclusion patterns (verify .backup files excluded)
- [ ] Integration test: Full migration workflow (copy → validate → git stage)
- [ ] Integration test: Idempotency (run twice, same result)
- [ ] Edge case test: Existing files (conflict resolution)
- [ ] Edge case test: Corruption detection (fail fast)
- [ ] Edge case test: Symlink handling (follow links)
- [ ] Regression test: Original folders unchanged

### Documentation
- [ ] Script has inline comments explaining each step
- [ ] migration-config.json has example values and comments
- [ ] README.md in src/scripts/ explains migration process
- [ ] EPIC-009 updated with Phase 2 completion
- [ ] STORY-043 references this story as prerequisite

### Release Readiness
- [ ] Git commit with clear message
- [ ] migration-report.md reviewed (no errors)
- [ ] Validation: /dev --help, /qa --help still work
- [ ] Phase 2 Go/No-Go: 100% file integrity verified

---

## Workflow History

- **2025-11-16:** Story created for EPIC-009 Phase 2 (file migration to src/)
- **2025-11-16:** Priority: High, Points: 8, Sprint: Backlog
- **2025-11-16:** Depends on STORY-041 (directory structure must exist first)
- **2025-11-16:** Requirements analyst generated 7 ACs with detailed validation
- **2025-11-16:** Technical spec: 4 components (Worker, Configuration, DataModel, Logging) with 19 requirements
- **2025-11-16:** Status: Backlog (awaiting STORY-041 completion)
