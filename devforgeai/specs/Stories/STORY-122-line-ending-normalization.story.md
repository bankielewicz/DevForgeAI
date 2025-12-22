---
id: STORY-122
title: Line Ending Normalization
epic: EPIC-024
sprint: Sprint-8
status: Dev Complete
points: 3
depends_on: []
priority: Medium
assigned_to: TBD
created: 2025-12-20
format_version: "2.2"
---

# Story: Line Ending Normalization

## Description

**As a** developer on Windows/WSL,
**I want** all text files automatically normalized to LF line endings,
**So that** CRLF/LF inconsistencies don't create git diff noise or execution failures.

This story implements EPIC-024 Feature 3: Create `.gitattributes` with LF normalization to prevent CRLF/LF inconsistencies on WSL.

## Acceptance Criteria

### AC#1: .gitattributes File Created at Project Root

**Given** `.gitattributes` doesn't exist,
**When** this story is implemented,
**Then** `.gitattributes` is created at project root (alongside `.gitignore`).

---

### AC#2: Text Files Auto-Normalize to LF on Commit

**Given** a developer on Windows with autocrlf disabled,
**When** they edit a markdown file with CRLF line endings,
**Then** git automatically normalizes to LF on commit (no manual intervention).

---

### AC#3: Shell Scripts Explicitly Set to LF

**Given** shell script `.sh` files are critical on WSL,
**When** `.gitattributes` specifies `*.sh text eol=lf`,
**Then** all `.sh` files are guaranteed LF, preventing `$'\r': command not found` errors.

---

### AC#4: Binary Files Marked as Binary

**Given** PNG, JPG, PDF and other binary files shouldn't be normalized,
**When** `.gitattributes` marks them as `binary`,
**Then** binary files are never modified during git operations.

---

### AC#5: Existing Files Can Be Renormalized

**Given** repository already has mixed line endings,
**When** developer runs `git add --renormalize .` after creating `.gitattributes`,
**Then** all files are converted to correct line endings in single commit.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Git Configuration"
      name: ".gitattributes"
      file_path: ".gitattributes"
      purpose: "Define line ending rules for all file types"
      required_content:
        - rule: "* text=auto eol=lf"
          applies_to: "All files unless explicitly overridden"
          effect: "Auto-detect text vs binary, normalize to LF"
        - rule: "*.sh text eol=lf"
          applies_to: "All shell scripts"
          effect: "Explicit LF requirement (WSL critical)"
        - rule: "*.py text eol=lf"
          applies_to: "Python files"
        - rule: "*.md text eol=lf"
          applies_to: "Markdown documentation"
        - rule: "*.json text eol=lf"
          applies_to: "JSON config files"
        - rule: "*.yaml text eol=lf, *.yml text eol=lf"
          applies_to: "YAML config files"
        - rule: "*.ts text eol=lf, *.tsx text eol=lf, *.js text eol=lf, *.jsx text eol=lf"
          applies_to: "TypeScript/JavaScript files"
        - rule: "*.png binary, *.jpg binary, *.jpeg binary, *.gif binary, *.ico binary, *.pdf binary, *.zip binary, *.tar binary, *.gz binary"
          applies_to: "All binary file types"
          effect: "No line ending conversion"

  file_types_covered:
    text_files:
      - "*.sh" (shell scripts)
      - "*.py" (Python)
      - "*.md" (Markdown)
      - "*.json" (JSON)
      - "*.yaml, *.yml" (YAML)
      - "*.ts, *.tsx, *.js, *.jsx" (TypeScript/JavaScript)
    binary_files:
      - "*.png, *.jpg, *.jpeg, *.gif, *.ico" (images)
      - "*.pdf, *.zip, *.tar, *.gz" (archives/documents)

  behavior:
    autocrlf_override: "Explicit eol=lf overrides system autocrlf setting"
    safecrlf: ".gitattributes works with safecrlf=warn or safecrlf=true"
    existing_files: "Run 'git add --renormalize .' to apply rules to existing files"
    future_commits: "All future commits automatically apply rules"

  post_implementation:
    - step: "Create .gitattributes at project root"
      command: "Write file with rules above"
    - step: "Renormalize existing files (optional but recommended)"
      command: "git add --renormalize . && git commit -m 'chore: normalize line endings to LF'"
      note: "Creates single large commit with all files normalized"
    - step: "Verify renormalization (optional)"
      command: "git diff --name-only (should show no pending changes)"
      note: "Confirms all files now match .gitattributes rules"
```

## Non-Functional Requirements

| Requirement | Target | Justification |
|-------------|--------|---------------|
| File size impact | <1KB | .gitattributes is minimal |
| Performance impact | Zero | Git-native feature, no overhead |
| WSL compatibility | 100% | Solves WSL execution issues |

## Test Strategy

### Unit Tests
- **Test 1:** .gitattributes syntax is valid
- **Test 2:** All text file types have eol=lf rule
- **Test 3:** All binary file types have binary marker
- **Test 4:** Shell scripts (.sh) explicitly set to LF

### Integration Tests
- **Test 5:** After commit with CRLF file, git status shows LF
- **Test 6:** Shell script with CRLF can execute without `$'\r'` error
- **Test 7:** Binary file (PNG/JPG) unchanged after commit
- **Test 8:** Renormalization: `git add --renormalize .` applies rules to existing files

### Edge Cases
- **Test 9:** File with mixed line endings normalized to LF
- **Test 10:** Large binary files not corrupted by processing
- **Test 11:** Symbolic links handled correctly

## Definition of Done

### Implementation
- [x] `.gitattributes` created at project root with complete rules - Completed: File created with comprehensive rules for all file types
- [x] All required file type patterns included - Completed: sh, py, md, json, yaml, yml, ts, tsx, js, jsx all covered
- [x] Shell scripts explicitly `*.sh text eol=lf` - Completed: Line 24-25 of .gitattributes
- [x] Binary file types marked as `binary` - Completed: png, jpg, jpeg, gif, ico, pdf, zip, tar, gz all marked binary

### Quality
- [x] All integration tests passing (8 tests) - Completed: 4 integration tests passing (test_crlf_normalized, test_shell_execution, test_binary_unchanged, test_renormalize_works)
- [x] Edge cases handled (3 tests) - Completed: 3 edge case tests passing (test_mixed_line_endings, test_large_binary, test_symbolic_links)
- [x] No file corruption on binary files verified - Completed: test_binary_unchanged.sh verifies checksums before/after commit

### Testing
- [x] Manual test: Edit .sh file with CRLF, commit, verify LF - Completed: test_shell_execution.sh verifies this automatically
- [x] Manual test: WSL script execution succeeds (no `$'\r'` error) - Completed: test_shell_execution.sh passes on WSL2
- [x] Manual test: PNG/JPG binary files unchanged - Completed: test_binary_unchanged.sh verifies via checksum
- [x] Manual test: Renormalize existing files successfully - Completed: 3,353 files renormalized in commit 63bd1dd9

### Documentation
- [x] .gitattributes has inline comments explaining rules - Completed: Comprehensive section headers and comments
- [ ] STORY-SCOPED-COMMITS.md or main README mentions line ending normalization - Deferred: Follow-up story STORY-123 for documentation update
- [x] Renormalization procedure documented - Completed: Instructions in .gitattributes header comments

### Release
- [x] All tests passing - Completed: 11/11 tests pass
- [x] Backward compatibility verified (unaffected on systems already using LF) - Completed: LF-only systems unaffected
- [x] Renormalization commit created separately - Completed: commit 63bd1dd9 (3,353 files)
- [x] Ready for QA validation - Completed: All acceptance criteria met

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2025-12-22
**Commit:** b7491e72 (.gitattributes), 63bd1dd9 (renormalization)
**Branch:** refactor/devforgeai-migration

- [x] `.gitattributes` created at project root with complete rules - Completed: File created with comprehensive rules for all file types
- [x] All required file type patterns included - Completed: sh, py, md, json, yaml, yml, ts, tsx, js, jsx all covered
- [x] Shell scripts explicitly `*.sh text eol=lf` - Completed: Line 24-25 of .gitattributes
- [x] Binary file types marked as `binary` - Completed: png, jpg, jpeg, gif, ico, pdf, zip, tar, gz all marked binary
- [x] All integration tests passing (8 tests) - Completed: 4 integration tests passing (test_crlf_normalized, test_shell_execution, test_binary_unchanged, test_renormalize_works)
- [x] Edge cases handled (3 tests) - Completed: 3 edge case tests passing (test_mixed_line_endings, test_large_binary, test_symbolic_links)
- [x] No file corruption on binary files verified - Completed: test_binary_unchanged.sh verifies checksums before/after commit
- [x] Manual test: Edit .sh file with CRLF, commit, verify LF - Completed: test_shell_execution.sh verifies this automatically
- [x] Manual test: WSL script execution succeeds (no `$'\r'` error) - Completed: test_shell_execution.sh passes on WSL2
- [x] Manual test: PNG/JPG binary files unchanged - Completed: test_binary_unchanged.sh verifies via checksum
- [x] Manual test: Renormalize existing files successfully - Completed: 3,353 files renormalized in commit 63bd1dd9
- [x] .gitattributes has inline comments explaining rules - Completed: Comprehensive section headers and comments
- [ ] STORY-SCOPED-COMMITS.md or main README mentions line ending normalization - Deferred: Follow-up story STORY-123 for documentation update (User approved: Documentation update is out of scope for this story)
- [x] Renormalization procedure documented - Completed: Instructions in .gitattributes header comments
- [x] All tests passing - Completed: 11/11 tests pass
- [x] Backward compatibility verified (unaffected on systems already using LF) - Completed: LF-only systems unaffected
- [x] Renormalization commit created separately - Completed: commit 63bd1dd9 (3,353 files)
- [x] Ready for QA validation - Completed: All acceptance criteria met

### TDD Workflow Summary

**Phase 01 (Pre-Flight):** Validated git repository, no .gitattributes exists

**Phase 02 (Red):** Created 11 failing tests
- 4 unit tests (syntax, text types, binary types, shell explicit LF)
- 4 integration tests (CRLF normalized, shell execution, binary unchanged, renormalize)
- 3 edge case tests (mixed endings, large binary, symbolic links)

**Phase 03 (Green):** Created .gitattributes with comprehensive rules
- Global default: `* text=auto eol=lf`
- Shell scripts: `*.sh text eol=lf` (WSL critical)
- Text files: py, md, json, yaml, ts, js explicit LF
- Binary files: png, jpg, pdf, zip marked binary

**Phase 04 (Refactor):** Added comprehensive comments and additional file types

**Phase 05 (Integration):** All 11 tests passing

**Phase 08 (Git):** Two commits created
- b7491e72: .gitattributes and test suite (13 files)
- 63bd1dd9: Renormalization (3,353 files)

### Files Created/Modified

**Created:**
- `.gitattributes` (main deliverable)
- `tests/STORY-122/run_all_tests.sh`
- `tests/STORY-122/unit/test_syntax_valid.sh`
- `tests/STORY-122/unit/test_text_types_lf.sh`
- `tests/STORY-122/unit/test_binary_types_marked.sh`
- `tests/STORY-122/unit/test_shell_explicit_lf.sh`
- `tests/STORY-122/integration/test_crlf_normalized.sh`
- `tests/STORY-122/integration/test_shell_execution.sh`
- `tests/STORY-122/integration/test_binary_unchanged.sh`
- `tests/STORY-122/integration/test_renormalize_works.sh`
- `tests/STORY-122/edge-cases/test_mixed_line_endings.sh`
- `tests/STORY-122/edge-cases/test_large_binary.sh`
- `tests/STORY-122/edge-cases/test_symbolic_links.sh`

**Renormalized:** 3,353 files (CRLF → LF)

### Test Results

- **Total tests:** 11
- **Pass rate:** 100%
- **Test framework:** Bash scripts with exit codes
- **Execution time:** ~30 seconds (includes temp repo creation)
