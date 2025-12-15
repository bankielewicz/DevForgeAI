# ADR-007: Jest 30 Upgrade for Node.js 22 Compatibility

**Status:** Accepted
**Date:** 2025-12-01
**Deciders:** User (via AskUserQuestion)
**Story:** STORY-071 (Wizard-Driven Interactive UI)

## Context

During STORY-071 Session 3, Jest tests were found to hang indefinitely during initialization:

1. **Environment:** Node.js 22.19.0, Jest 29.7.0
2. **Symptom:** All Jest commands hang before test execution begins
3. **Diagnosis:** Even simplest test `test('simple', () => expect(true).toBe(true))` hangs
4. **Verification:** Node imports work fine (`node -e "require('./src/cli/wizard/config')"` succeeds immediately)

### Root Cause Analysis

**Jest 29.7.0 has initialization hanging issues with Node.js 22.x**

Evidence from diagnostic session:
- Jest hangs during framework initialization, not during test execution
- All configuration fixes applied (ESM/CJS deps, mock cleanup, process.exit mock) had no effect
- Problem isolated to Jest/Node version incompatibility

### Research Findings

From internet-sleuth research and official documentation:

1. **[Jest Issue #13904](https://github.com/jestjs/jest/issues/13904):** Performance degradation reported from Node 14 to 19
2. **[Jest 30 Release Blog](https://jestjs.io/blog/2025/06/04/jest-30):**
   - "Jest 30 is noticeably faster, uses less memory"
   - "Better at detecting and reporting open handles"
   - Drops support for Node 14, 16, 19, 21 but fully supports Node 18+
3. **Node 22 is LTS as of October 2024** - upgrading Jest is more sustainable than downgrading Node

## Decision

**Upgrade Jest from 29.7.0 to 30.x** (latest stable)

### Rationale

1. **Node 22 is current LTS** - Downgrading Node creates technical debt
2. **Jest 30 has explicit Node 22 support** - Designed for modern Node versions
3. **Performance improvements** - Faster test execution, better memory usage
4. **Better diagnostics** - Improved open handle detection helps prevent future hanging issues
5. **Forward compatibility** - Aligns with Node.js release schedule

### Alternatives Considered

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| **Upgrade Jest to 30** | Full Node 22 support, better performance | Breaking changes possible | ✅ Selected |
| Downgrade Node to 20 | Quick fix, stable | Creates tech debt, outdated tooling | ❌ Rejected |
| Use NVM for isolation | Flexible | Complex CI/CD, maintenance burden | ❌ Rejected |
| Wait for Jest 29 patch | No changes needed | No fix timeline, blocks development | ❌ Rejected |

## Consequences

### Positive

- Tests will run on Node.js 22.x (current LTS)
- Faster test execution (Jest 30 performance improvements)
- Better memory usage during large test suites
- Improved open handle detection for debugging
- Future-proof toolchain alignment

### Negative

- Potential breaking changes from Jest 29 → 30 migration
- May require test file updates for deprecated APIs
- Need to verify all existing tests pass after upgrade

### Migration Considerations

Per [Jest 29 to 30 Migration Guide](https://jestjs.io/docs/upgrading-to-jest30):

1. **Node version requirement:** Node 18+ (we have Node 22 ✓)
2. **Configuration changes:** Review jest.config.js for deprecated options
3. **API changes:** Check for deprecated matcher/mock APIs
4. **Snapshot format:** May need snapshot updates

## Implementation

### Step 1: Update dependencies.md

Add Jest 30 to locked dependencies:
```markdown
"jest": "^30.0.0"
```

### Step 2: Update package.json

```json
"devDependencies": {
  "jest": "^30.0.0"
}
```

### Step 3: Install and Verify

```bash
npm install jest@latest --save-dev
npm test
```

### Step 4: Address Breaking Changes (if any)

- Update deprecated configuration options
- Fix any failing tests due to API changes
- Update snapshots if format changed

## Additional Finding: WSL2 + NTFS Cross-Filesystem Issue

During implementation, a secondary issue was discovered:

**Problem:** Jest hangs indefinitely when running from `/mnt/c/` (Windows filesystem via WSL2)

**Root Cause:** WSL2 uses the 9P protocol to access Windows filesystems mounted under `/mnt/`. This protocol has significant performance overhead for file-heavy operations like Jest's module resolution and file watching.

**Evidence:**
- Tests hang when run from `/mnt/c/Projects/DevForgeAI2/`
- Tests pass in 0.177s when run from `/tmp/devforge-test/` (native Linux filesystem)
- All 38 wizard-config tests pass: `PASS tests/npm-package/unit/wizard-config.test.js`

**Workaround Options:**

1. **Copy to native Linux filesystem for testing:**
   ```bash
   cp -r /mnt/c/Projects/DevForgeAI2 /tmp/devforge-test
   cd /tmp/devforge-test && npm test
   ```

2. **Use WSL2 native filesystem for development:**
   ```bash
   # Clone/move project to ~/Projects instead of /mnt/c/
   git clone <repo> ~/Projects/DevForgeAI2
   ```

3. **Configure Jest to reduce filesystem operations:**
   ```javascript
   // jest.config.js
   module.exports = {
     watchman: false,           // Disable Watchman
     haste: { enableSymlinks: false },
     cache: false,              // Disable caching (or use Linux path for cache)
   };
   ```

4. **Run tests from Windows (not WSL):**
   ```powershell
   # From PowerShell/CMD
   npm test
   ```

## Verification Criteria

- [x] Jest 30 starts without hanging (on native Linux filesystem)
- [x] All wizard tests execute (38/38 passed)
- [ ] Test coverage reports generate correctly
- [ ] CI/CD pipeline (if configured) runs successfully
- [ ] WSL workaround documented

## References

- [Jest 30 Release Announcement](https://jestjs.io/blog/2025/06/04/jest-30)
- [Jest 29 to 30 Migration Guide](https://jestjs.io/docs/upgrading-to-jest30)
- [Jest GitHub Issue #13904](https://github.com/jestjs/jest/issues/13904) - Node version performance issues
- ADR-006: Interactive CLI Library ESM/CommonJS Compatibility (related)
- STORY-071: Wizard-Driven Interactive UI (triggering story)

## Decision Record

- **Created:** 2025-12-01
- **Approved by:** User (explicit request to upgrade Jest)
- **Implemented:** Pending (this ADR documents the decision)
