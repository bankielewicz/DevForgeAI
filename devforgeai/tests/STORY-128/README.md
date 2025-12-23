# STORY-128: Git Lock File Recovery - Test Suite

## Overview

This directory contains the TDD Red Phase test suite for STORY-128: Git Lock File Recovery. The story adds documentation for recovering from stale `.git/index.lock` files in WSL2 environments.

**Current Phase: RED** - All tests are failing (as expected) because the documentation doesn't exist yet.

## Test Files

### Test Structure

Each test file targets a specific Acceptance Criterion (AC) from the story:

| Test File | AC # | Target | Status |
|-----------|------|--------|--------|
| `test-ac1-section-exists.sh` | AC#1 | Lock File Recovery section exists | RED |
| `test-ac2-diagnosis-commands.sh` | AC#2 | Diagnosis commands documented | RED |
| `test-ac3-recovery-warning.sh` | AC#3 | Recovery with safety warning | RED |
| `test-ac4-wsl2-guidance.sh` | AC#4 | WSL2-specific guidance | RED |
| `test-ac5-prevention-tips.sh` | AC#5 | Prevention tips documented | RED |

### Running Tests

**Run all tests to verify RED phase:**
```bash
bash devforgeai/tests/STORY-128/verify-red-phase.sh
```

**Run individual test:**
```bash
bash devforgeai/tests/STORY-128/test-ac1-section-exists.sh
bash devforgeai/tests/STORY-128/test-ac2-diagnosis-commands.sh
bash devforgeai/tests/STORY-128/test-ac3-recovery-warning.sh
bash devforgeai/tests/STORY-128/test-ac4-wsl2-guidance.sh
bash devforgeai/tests/STORY-128/test-ac5-prevention-tips.sh
```

## Test Details

### AC#1: Lock File Recovery Section Exists

**What it tests:** The git-workflow-conventions.md file contains a "Lock File Recovery" section with proper subsections.

**Assertions:**
1. Section header `## Lock File Recovery` exists
2. Problem subsection exists
3. Diagnosis subsection exists
4. Recovery subsection exists
5. WSL2-Specific Notes subsection exists
6. Safety warning exists

**Current Status:** RED (Section doesn't exist yet)

---

### AC#2: Diagnosis Commands Documented

**What it tests:** The diagnosis section includes proper commands for checking lock file status and running git processes.

**Assertions:**
1. Command `ls -la .git/index.lock` documented
2. Command `ps aux | grep git` documented
3. Both commands in bash code block
4. Comment explaining ls command intent ("Check if lock")
5. Comment explaining ps command intent ("Check for running git")

**Current Status:** RED (Commands not documented yet)

---

### AC#3: Recovery Commands with Safety Warning

**What it tests:** The recovery section includes the rm command with prominent safety warnings.

**Assertions:**
1. Recovery section exists
2. Command `rm -f .git/index.lock` documented
3. Safety warning "no git processes are running" present
4. WARNING marker bold and prominent (`**WARNING:**`)
5. Recovery command in bash code block
6. Comment explaining recovery intent ("Remove stale lock")

**Current Status:** RED (Recovery section not documented yet)

---

### AC#4: WSL2-Specific Guidance

**What it tests:** The section documents WSL2-specific causes and prevention for lock files.

**Assertions:**
1. WSL2-Specific Notes section exists
2. Common Causes subsection exists
3. VS Code with Git extension mentioned as cause
4. Cross-filesystem cause mentioned
5. Git crash without cleanup mentioned
6. Prevention section exists
7. Close VS Code Git panels prevention tip documented
8. Native WSL paths (/mnt/c/) mentioned
9. Windows paths (C:\) shown as anti-pattern

**Current Status:** RED (WSL2 guidance not documented yet)

---

### AC#5: Prevention Tips Documented

**What it tests:** Prevention section includes all three prevention tips in numbered list format.

**Assertions:**
1. Prevention section exists
2. Prevention tips in numbered list format (1., 2., 3.)
3. Tip 1: Close VS Code Git panels before terminal git operations
4. Tip 2: Use native WSL paths (/mnt/c/) not Windows paths
5. Tip 3: Avoid running git from both Windows and WSL simultaneously
6. Example path /mnt/c/ shown for native paths
7. Windows path anti-pattern (C:\) shown
8. "same repo" mentioned in Windows/WSL tip

**Current Status:** RED (Prevention tips not documented yet)

---

## Test Execution Flow

### Phase: RED (Current)
- All tests FAIL (documentation doesn't exist)
- Tests verify expected structure and content requirements
- No implementation exists yet

### Phase: GREEN (Next)
Add "Lock File Recovery" section to `.claude/skills/devforgeai-development/references/git-workflow-conventions.md`

Required content from STORY-128 Technical Specification:
```markdown
## Lock File Recovery

### Problem
Git fails with error: "fatal: Unable to create '.git/index.lock': File exists"

### Diagnosis
```bash
# Check if lock file exists
ls -la .git/index.lock

# Check for running git processes
ps aux | grep git

# On Windows (if using PowerShell)
tasklist | findstr git
```

### Recovery
**WARNING:** Only proceed if no git processes are running.

```bash
# Remove stale lock file
rm -f .git/index.lock
```

### WSL2-Specific Notes

**Common Causes:**
- VS Code with Git extension is open and polling for changes
- Cross-filesystem access between Windows (C:\) and WSL (/mnt/c/)
- Previous git command crashed without cleanup
- File system sync issues between Windows and WSL

**Prevention:**
1. Close VS Code Git panels before running git in terminal
2. Use native WSL paths (/mnt/c/Projects/) not Windows paths (C:\Projects\)
3. Avoid running git from both Windows CMD and WSL on same repo
4. If using VS Code, disable "Git: Autofetch" setting temporarily

**Alternative Recovery (if rm fails):**
```bash
# Force remove on Windows filesystem
rm -rf .git/index.lock 2>/dev/null || cmd.exe /c "del /f /q .git\\index.lock"
```
```

### Phase: REFACTOR (After)
- All tests PASS (documentation complete)
- Review content quality and formatting
- Ensure examples are copy-paste ready
- Update related documentation as needed

## TDD Workflow

This test suite follows Test-Driven Development (TDD) principles:

### Red Phase (Current)
- Write tests BEFORE implementation
- Tests fail because code doesn't exist
- Tests define acceptance criteria
- Provides specification for implementation

### Green Phase (Next)
- Implement minimal code to make tests pass
- Add documentation content from spec
- Run tests to verify all pass
- Don't optimize or add extras yet

### Refactor Phase (After)
- Improve documentation quality
- Fix formatting and clarity
- Remove duplication
- Add examples and cross-references

## Test Assertions

All tests use **grep pattern matching** for content verification:

```bash
# Check if text exists in file
grep -q "pattern" file.md

# Check if line starts with pattern
grep -q "^## Lock File Recovery" file.md

# Check if pattern exists in context (multiple lines)
grep -A5 "^### Diagnosis" file.md | grep -q "ls -la"
```

**Why grep?**
- Simple and reliable
- Works with documentation files
- Easy to understand and maintain
- Verifies exact content presence
- Tests from external perspective (integration test style)

## Coverage

This test suite covers:
- **Section structure** (headers, subsections)
- **Content presence** (required text, commands)
- **Formatting** (code blocks, bold emphasis)
- **Completeness** (all ACs addressed)

This test suite does NOT cover:
- Exact wording or phrasing
- Markdown syntax validation (use linter for that)
- Style or formatting preferences
- Command functionality (use integration tests for that)

## File Structure

```
devforgeai/tests/STORY-128/
├── README.md                              # This file
├── verify-red-phase.sh                    # Run all tests and report status
├── test-ac1-section-exists.sh             # AC#1: Section structure
├── test-ac2-diagnosis-commands.sh         # AC#2: Diagnosis commands
├── test-ac3-recovery-warning.sh           # AC#3: Recovery safety
├── test-ac4-wsl2-guidance.sh              # AC#4: WSL2 notes
└── test-ac5-prevention-tips.sh            # AC#5: Prevention tips
```

## Dependencies

- Bash 4.0+
- grep
- Standard Unix utilities (cut, wc, head, tail)

**No external dependencies** - Uses only standard Unix tools.

## Making Tests Pass (Green Phase)

To transition from RED to GREEN phase:

1. **Add "Lock File Recovery" section** to:
   ```
   .claude/skills/devforgeai-development/references/git-workflow-conventions.md
   ```

2. **Include all required subsections:**
   - Problem
   - Diagnosis
   - Recovery
   - WSL2-Specific Notes

3. **Add all required content:**
   - Diagnosis commands (ls, ps aux)
   - Recovery command (rm -f)
   - Safety warning (bold, prominent)
   - WSL2 causes (VS Code, cross-filesystem, crashes)
   - Prevention tips (numbered list, 3+ items)

4. **Run tests to verify:**
   ```bash
   bash devforgeai/tests/STORY-128/verify-red-phase.sh
   ```

   Expected output when GREEN:
   ```
   Status: GREEN PHASE CONFIRMED - All 5 tests passing
   Next: Refactor and QA validation
   ```

## Notes

- Tests are **intentionally strict** to ensure complete implementation
- All patterns are **case-sensitive** (match exactly)
- Code blocks MUST be marked with ` ```bash ` fence
- WSL path patterns use literal slashes (/mnt/c/)
- Windows path patterns use escaped backslashes (C:\\)

## References

- Story File: `devforgeai/specs/Stories/STORY-128-git-lock-recovery.story.md`
- Target File: `.claude/skills/devforgeai-development/references/git-workflow-conventions.md`
- TDD Workflow: `.claude/skills/devforgeai-development/references/tdd-red-phase.md`
