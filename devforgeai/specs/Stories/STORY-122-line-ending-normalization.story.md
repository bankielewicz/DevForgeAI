---
id: STORY-122
title: Line Ending Normalization
epic: EPIC-024
sprint: Sprint-8
status: Backlog
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
- [ ] `.gitattributes` created at project root with complete rules
- [ ] All required file type patterns included
- [ ] Shell scripts explicitly `*.sh text eol=lf`
- [ ] Binary file types marked as `binary`

### Quality
- [ ] All integration tests passing (8 tests)
- [ ] Edge cases handled (3 tests)
- [ ] No file corruption on binary files verified

### Testing
- [ ] Manual test: Edit .sh file with CRLF, commit, verify LF
- [ ] Manual test: WSL script execution succeeds (no `$'\r'` error)
- [ ] Manual test: PNG/JPG binary files unchanged
- [ ] Manual test: Renormalize existing files successfully

### Documentation
- [ ] .gitattributes has inline comments explaining rules
- [ ] STORY-SCOPED-COMMITS.md or main README mentions line ending normalization
- [ ] Renormalization procedure documented

### Release
- [ ] All tests passing
- [ ] Backward compatibility verified (unaffected on systems already using LF)
- [ ] Renormalization commit created separately
- [ ] Ready for QA validation
