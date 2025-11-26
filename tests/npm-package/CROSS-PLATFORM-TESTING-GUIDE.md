# Cross-Platform Testing Guide for STORY-066

## Prerequisites

**All Platforms:**
- Node.js ≥18.0.0
- npm ≥8.0.0
- Python 3.10+
- Git (for cloning repository)

## Quick Start (All Platforms)

### 1. Clone and Setup
```bash
# Clone repository
git clone https://github.com/bankielewicz/DevForgeAI.git
cd DevForgeAI

# Checkout story branch
git checkout story-066

# Install test dependencies
cd tests/npm-package
npm install
```

### 2. Run Tests
```bash
# From tests/npm-package/ directory
npm test

# Expected result: 185 tests passing, 6 skipped
# Test Suites: 9 passed, 9 total
# Tests: 6 skipped, 185 passed, 191 total
```

### 3. Test Global Installation
```bash
# From project root
cd /path/to/DevForgeAI

# Create package
npm pack

# Install globally
npm install -g devforgeai-1.0.0.tgz

# Test commands
devforgeai --version  # Should output: devforgeai v1.0.0
devforgeai --help     # Should show usage information

# Cleanup
npm uninstall -g devforgeai
```

---

## Platform-Specific Instructions

### Linux (Ubuntu/Debian)

**Environment Verified:** Ubuntu 20.04+, WSL2

**Run Tests:**
```bash
cd tests/npm-package
npm test
```

**Expected Output:**
```
Test Suites: 9 passed, 9 total
Tests:       6 skipped, 185 passed, 191 total
Snapshots:   0 total
Time:        ~50s
```

**Verify Global Install:**
```bash
npm pack
sudo npm install -g devforgeai-1.0.0.tgz
which devforgeai  # Should show: /usr/local/bin/devforgeai
devforgeai --version
sudo npm uninstall -g devforgeai
```

---

### macOS (Intel & Apple Silicon)

**Environment:** macOS 11+ (Big Sur or newer)

**Setup:**
```bash
# Ensure Homebrew installed
brew --version

# Install Node.js if needed
brew install node@18

# Install Python 3.10+ if needed
brew install python@3.10

# Verify versions
node --version  # Should be ≥18.0.0
npm --version   # Should be ≥8.0.0
python3 --version  # Should be ≥3.10.0
```

**Run Tests:**
```bash
cd tests/npm-package
npm install
npm test
```

**Expected Result:** Same as Linux (185 passing, 6 skipped)

**Verify Global Install:**
```bash
npm pack
npm install -g devforgeai-1.0.0.tgz
which devforgeai  # Should show path in npm global bin
devforgeai --version
npm uninstall -g devforgeai
```

**macOS-Specific Checks:**
- Verify shebang works: `head -1 bin/devforgeai.js` should show `#!/usr/bin/env node`
- Verify executable permissions: `ls -la bin/devforgeai.js` should show `-rwxr-xr-x`

---

### Windows (Native & WSL2)

#### Windows WSL2 (Tested ✅)

**Environment:** Windows 10/11 with WSL2 (Ubuntu)

**Setup:**
```bash
# Inside WSL2 terminal
node --version  # ≥18.0.0
npm --version   # ≥8.0.0
python3 --version  # ≥3.10.0
```

**Run Tests:**
```bash
cd tests/npm-package
npm test
```

**Expected Result:** 185 passing, 6 skipped (verified ✅)

---

#### Windows Native (Command Prompt / PowerShell)

**Environment:** Windows 10/11 native (no WSL)

**Setup:**
```powershell
# Install Node.js from https://nodejs.org (18.x LTS or newer)
node --version  # Should be v18.x.x+

# Install Python from https://www.python.org (3.10+)
python --version  # Should be 3.10.x+
# OR
python3 --version
```

**IMPORTANT - Python Command:**
Windows uses `python` or `python3` depending on installation:
```powershell
# Check which command is available
where python
where python3

# If only `python` exists, create python3 alias:
# Add to PATH or create python3.exe copy:
copy "C:\Python310\python.exe" "C:\Python310\python3.exe"
```

**Run Tests:**
```powershell
# From PowerShell or CMD
cd tests\npm-package
npm install
npm test
```

**Expected Challenges:**
- Line endings: Tests expect LF, Windows may have CRLF
  - **Fix:** Configure git: `git config core.autocrlf input`
- Path separators: Tests verify forward slashes (/) work
  - **Verification:** Tests should pass (Node.js handles this automatically)
- Python command: May be `python` not `python3`
  - **Fix:** See Python command section above

**Run Global Install Test:**
```powershell
# From project root
npm pack
npm install -g devforgeai-1.0.0.tgz

# Test (use PowerShell or CMD)
devforgeai --version
devforgeai --help

# Cleanup
npm uninstall -g devforgeai
```

---

## What to Test & Verify

### Critical Test Scenarios (All Platforms)

**1. Package Creation:**
```bash
npm pack
# Verify: devforgeai-1.0.0.tgz created (~2.9 MB)
# Verify: File count <1000 (run: tar -tzf devforgeai-1.0.0.tgz | wc -l)
```

**2. Global Installation:**
```bash
npm install -g devforgeai-1.0.0.tgz
which devforgeai  # (Unix) or where devforgeai (Windows)
# Verify: Command found in global bin
```

**3. CLI Commands:**
```bash
devforgeai --version
# Expected: devforgeai v1.0.0

devforgeai --help
# Expected: Usage information with commands

devforgeai
# Expected: Same as --help
```

**4. Python Detection:**
```bash
devforgeai install /tmp/test
# Expected: Python installer runs (or shows clear error if Python missing)
```

**5. Uninstallation:**
```bash
npm uninstall -g devforgeai
which devforgeai  # (Unix) or where devforgeai (Windows)
# Expected: Command not found
```

---

## Reporting Results

### Success Criteria (Per Platform)

For each platform (Linux, macOS, Windows native), verify:

- [ ] `npm test` shows 185+ tests passing
- [ ] `npm pack` creates tarball ~2.9 MB
- [ ] `npm install -g` succeeds without errors
- [ ] `devforgeai --version` outputs correct version
- [ ] `devforgeai --help` shows usage information
- [ ] `npm uninstall -g` removes command cleanly

### Report Template

```markdown
**Platform:** [Linux/macOS Intel/macOS ARM/Windows Native/WSL2]
**Node Version:** [output of `node --version`]
**npm Version:** [output of `npm --version`]
**Python Version:** [output of `python3 --version`]

**Test Results:**
- npm test: [PASS/FAIL] - [X passing, Y skipped, Z failed]
- npm pack: [PASS/FAIL] - Tarball size: [X MB]
- Global install: [PASS/FAIL]
- devforgeai --version: [PASS/FAIL] - Output: [actual output]
- devforgeai --help: [PASS/FAIL]
- Uninstall: [PASS/FAIL]

**Issues Found:** [None / List any failures or unexpected behavior]
```

---

## Troubleshooting

### Tests Fail with "python3: command not found"

**Cause:** Python 3.10+ not installed or not in PATH

**Fix (macOS):**
```bash
brew install python@3.10
```

**Fix (Windows):**
```powershell
# Download from https://www.python.org/downloads/
# During installation, check "Add Python to PATH"
# After install:
where python3
# If not found, create alias (see Python Command section above)
```

### Tests Fail with Line Ending Errors

**Cause:** Git configured with autocrlf=true (converts LF to CRLF on Windows)

**Fix:**
```bash
git config core.autocrlf input
git checkout story-066 --force  # Reapply with correct line endings
```

### Global Install Fails with Permission Error

**Cause:** npm global directory requires admin/sudo

**Fix (Linux/macOS):**
```bash
sudo npm install -g devforgeai-1.0.0.tgz
```

**Fix (Windows):**
```powershell
# Run PowerShell as Administrator
npm install -g devforgeai-1.0.0.tgz
```

### Coverage Thresholds Not Met in Local Run

**Expected:** Coverage collection works from project root

**Fix:**
```bash
# Run from PROJECT ROOT, not tests/npm-package/
cd /path/to/DevForgeAI
npx jest --coverage

# Should show:
# lib/cli.js: 95.16% statements, 100% lines, 100% functions
```

---

## Contact

**Questions?** Report results or issues to the STORY-066 implementation team.

**Success Criteria:** All 3 platforms (Linux, macOS, Windows native) should pass all critical test scenarios.
