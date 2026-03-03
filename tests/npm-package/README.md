# STORY-066: NPM Package Creation & Structure - Test Suite

**Status:** RED PHASE (All tests should fail initially)
**Coverage Target:** 95%+ for `bin/devforgeai.js`
**Test Framework:** Jest 29+

---

## Overview

This test suite validates the NPM package structure for DevForgeAI global installation via `npm install -g devforgeai`. Tests are organized following Test-Driven Development (TDD) principles:

- **RED Phase (Current):** All tests fail - implementation does not exist
- **GREEN Phase:** Implement minimal code to pass tests
- **REFACTOR Phase:** Improve code while keeping tests green

---

## Test Structure

```
tests/npm-package/
├── package.json                     # Jest configuration
├── README.md                        # This file
│
├── unit/                            # Unit tests (95%+ coverage target)
│   ├── package-json-validation.test.js   # AC#1, AC#3
│   ├── cli-entry-point.test.js           # AC#2, SVC-001-006
│   └── package-structure.test.js         # AC#4, AC#5, AC#7
│
└── integration/                     # Integration tests (85% coverage target)
    ├── npm-pack.test.js                  # AC#7, tarball creation
    └── global-installation.test.js       # AC#2, AC#6, global install
```

---

## Test Coverage Mapping

### Acceptance Criteria

| AC # | Description | Test File | Test Count |
|------|-------------|-----------|------------|
| AC#1 | Valid package.json metadata | package-json-validation.test.js | 12 tests |
| AC#2 | Bin entry point for global CLI | cli-entry-point.test.js | 18 tests |
| AC#3 | Runtime dependencies declared | package-json-validation.test.js | 4 tests |
| AC#4 | Package structure best practices | package-structure.test.js | 15 tests |
| AC#5 | README with installation instructions | package-structure.test.js | 10 tests |
| AC#6 | Cross-platform compatibility | global-installation.test.js | 8 tests |
| AC#7 | Package size optimization | npm-pack.test.js | 18 tests |

**Total:** 85+ tests

### Technical Specification Components

| Component | Requirement IDs | Test File | Test Count |
|-----------|----------------|-----------|------------|
| Configuration | CONF-001 - CONF-006 | package-json-validation.test.js, npm-pack.test.js | 20 tests |
| Service | SVC-001 - SVC-006 | cli-entry-point.test.js | 15 tests |
| DataModel | DM-001 - DM-005 | package-structure.test.js | 15 tests |
| Business Rules | BR-001 - BR-005 | All test files | 10 tests |
| NFRs | NFR-001 - NFR-006 | All test files | 12 tests |

**Total:** 72+ technical spec tests

---

## Running Tests

### Install Dependencies

```bash
cd tests/npm-package
npm install
```

### Run All Tests (RED Phase Expected)

```bash
npm test
```

**Expected Result:** All tests fail with clear error messages.

### Run Unit Tests Only

```bash
npm run test:unit
```

### Run Integration Tests Only

```bash
npm run test:integration
```

### Watch Mode (During Development)

```bash
npm run test:watch
```

### Generate Coverage Report

```bash
npm test
# Coverage report generated in: tests/npm-package/coverage/
```

---

## Test Execution Order

Tests should be run in this order for TDD workflow:

1. **Unit Tests First:**
   - `package-json-validation.test.js` - Fastest, foundational
   - `package-structure.test.js` - File structure validation
   - `cli-entry-point.test.js` - CLI behavior validation

2. **Integration Tests Second:**
   - `npm-pack.test.js` - Tarball creation and content
   - `global-installation.test.js` - Full installation workflow

---

## Expected Test Results (RED Phase)

### Unit Tests

**File:** `unit/package-json-validation.test.js`

```
FAIL  tests/npm-package/unit/package-json-validation.test.js
  AC#1: Valid package.json with complete metadata
    CONF-001: Required NPM metadata fields
      ✕ package.json file exists (2 ms)
      ✕ package.json is valid JSON
      ✕ name field is "devforgeai"
      ... (12 failures)
```

**File:** `unit/cli-entry-point.test.js`

```
FAIL  tests/npm-package/unit/cli-entry-point.test.js
  AC#2: CLI Entry Point Functionality
    SVC-001: Node.js shebang line
      ✕ bin/devforgeai.js file exists (2 ms)
      ✕ first line is exactly "#!/usr/bin/env node"
      ... (18 failures)
```

**File:** `unit/package-structure.test.js`

```
FAIL  tests/npm-package/unit/package-structure.test.js
  AC#4: Package structure follows NPM best practices
    DM-001: bin/ directory with CLI entry point
      ✕ bin/ directory exists (2 ms)
      ✕ bin/devforgeai.js exists
      ... (15 failures)
```

### Integration Tests

**File:** `integration/npm-pack.test.js`

```
FAIL  tests/npm-package/integration/npm-pack.test.js
  Integration: npm pack tarball creation
    CONF-006: npm pack excludes development files
      ✕ npm pack --dry-run executes successfully (5 ms)
      ✕ tarball includes package.json
      ... (18 failures)
```

**File:** `integration/global-installation.test.js`

```
FAIL  tests/npm-package/integration/global-installation.test.js
  Integration: Global installation workflow
    Global installation from tarball
      ✕ npm install -g from tarball succeeds (10 ms)
      ✕ global installation creates bin symlink
      ... (8 failures)
```

---

## Test Implementation Details

### Unit Tests

**Coverage:** 95%+ for `bin/devforgeai.js`

**Focus Areas:**
1. **package.json Schema Validation:**
   - Semantic versioning format
   - Required metadata fields
   - Engines specifications
   - Zero runtime dependencies

2. **CLI Entry Point:**
   - Shebang line format
   - `--version` flag handling
   - `--help` flag output
   - Python subprocess invocation
   - Error handling (missing Python)
   - Argument passing

3. **File Structure:**
   - Directory existence (bin/, installer/, src/)
   - Required files (LICENSE, README.md, .npmignore)
   - Content validation (MIT license, installation instructions)

### Integration Tests

**Coverage:** 85%+

**Focus Areas:**
1. **NPM Pack:**
   - Tarball creation success
   - File inclusion/exclusion via .npmignore
   - Package size validation (≤2 MB unpacked)
   - Tarball extraction and integrity

2. **Global Installation:**
   - `npm install -g` workflow
   - Bin symlink creation
   - Command availability after install
   - Cross-platform path resolution
   - Installation performance (<30s)

---

## Edge Cases Covered

1. **Missing Python installation:** CLI detects and shows clear error
2. **Conflicting global installation:** Upgrade message shown
3. **Malformed package.json:** npm publish validation fails
4. **Broken bin symlink:** Post-install verification catches issue
5. **Network-restricted environments:** Offline installation works (zero npm dependencies)
6. **Node.js version mismatch:** Engines field blocks installation
7. **Spaces in paths:** Cross-platform path resolution handles correctly

---

## Success Criteria (GREEN Phase)

Tests will pass when:

- [ ] `package.json` created with all required fields
- [ ] `bin/devforgeai.js` created with shebang and CLI logic
- [ ] `.npmignore` configured to exclude dev files
- [ ] `LICENSE` file created with MIT license
- [ ] `README.md` created with ≥300 words and installation instructions
- [ ] `npm pack` creates valid tarball ≤2 MB unpacked
- [ ] `npm install -g` installs package globally
- [ ] `devforgeai --version` and `devforgeai --help` work
- [ ] CLI invokes Python installer subprocess
- [ ] All 85+ tests pass with 95%+ coverage

---

## Coverage Thresholds

**Configured in package.json:**

```json
"coverageThresholds": {
  "global": {
    "branches": 95,
    "functions": 95,
    "lines": 95,
    "statements": 95
  }
}
```

**Target Coverage:**
- `bin/devforgeai.js`: 95%+
- `package.json`: 100% (schema validation)
- `.npmignore`: 100% (pattern validation)

---

## Test Commands Summary

| Command | Purpose | Expected Result |
|---------|---------|-----------------|
| `npm test` | Run all tests with coverage | All fail (RED phase) |
| `npm run test:unit` | Run unit tests only | All fail (RED phase) |
| `npm run test:integration` | Run integration tests only | All fail (RED phase) |
| `npm run test:watch` | Run tests in watch mode | Continuous feedback |
| `npm run test:red` | Run without coverage | Faster execution |

---

## Next Steps (TDD GREEN Phase)

After confirming all tests fail:

1. **Create `package.json`** with required metadata (AC#1)
2. **Create `bin/devforgeai.js`** with shebang and CLI logic (AC#2)
3. **Create `.npmignore`** with exclusion patterns (AC#7)
4. **Create `LICENSE`** with MIT license (AC#4)
5. **Create `README.md`** with installation instructions (AC#5)
6. **Run tests iteratively** until all pass
7. **Verify coverage** meets 95%+ threshold
8. **Refactor** code while keeping tests green

---

## References

- **Story:** `devforgeai/specs/Stories/STORY-066-npm-package-creation-structure.story.md`
- **ADR:** `devforgeai/adrs/ADR-004-npm-package-distribution.md`
- **Epic:** `devforgeai/specs/Epics/EPIC-012-npm-package-distribution.epic.md`
- **Tech Stack:** `devforgeai/context/tech-stack.md` (NPM distribution section)

---

**Last Updated:** 2025-11-25
**Test Suite Version:** 1.0.0
**TDD Phase:** RED (All tests fail - implementation pending)
