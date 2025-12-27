# STORY-138 Tests - Quick Start Guide

## Verify Tests Are Ready

```bash
# Check test files exist
ls tests/STORY-138/test-*.js

# Count test cases
grep -c "test('should_" tests/STORY-138/test-*.js | awk -F: '{sum+=$2} END {print "Total:", sum}'
```

**Expected:** 5 test files, 69 test cases

## Run Tests (Will All Fail - Expected)

### Option 1: Run All STORY-138 Tests
```bash
npm test tests/STORY-138/
```

**Expected Result:**
```
FAIL tests/STORY-138/test-checkpoint-cleanup-on-success.js
  AC#1: Checkpoint Deletion on Successful Completion
    ✕ should_delete_checkpoint_file_when_ideation_completes_successfully
    ✕ should_log_success_message_when_checkpoint_deleted
    [... more failures ...]

Test Suites: 5 failed
Tests: 69 failed, 69 total
Duration: 0.5s
```

### Option 2: Run Individual Test File
```bash
# AC#1 tests only
npm test tests/STORY-138/test-checkpoint-cleanup-on-success.js

# AC#2 tests only
npm test tests/STORY-138/test-checkpoint-preservation-on-failure.js

# AC#3 tests only
npm test tests/STORY-138/test-manual-cleanup-command.js

# AC#4 tests only
npm test tests/STORY-138/test-cleanup-confirmation-with-file-list.js

# Edge cases and performance tests
npm test tests/STORY-138/test-edge-cases-and-performance.js
```

### Option 3: Run Single Test
```bash
npm test tests/STORY-138/test-checkpoint-cleanup-on-success.js \
  -t "should_delete_checkpoint_file_when_ideation_completes_successfully"
```

## Understanding the Failures

All tests will fail with messages like:
```
● AC#1: Checkpoint Deletion on Successful Completion › should_delete_checkpoint_file_when_ideation_completes_successfully

  Cannot find module '../../src/checkpoint-cleaner'

  Require stack:
    tests/STORY-138/test-checkpoint-cleanup-on-success.js:8
```

This is **correct and expected**. The tests are testing business logic that hasn't been implemented yet.

## What These Test Failures Mean

The tests are failing because:

1. **Module doesn't exist** - `src/checkpoint-cleaner.js` needs to be created
2. **Class not implemented** - `CheckpointCleaner` class needs to be written
3. **Methods don't exist** - Required methods need to be implemented

This follows **Test-Driven Development (TDD)** principles:
- ✅ Red Phase: Tests fail (CURRENT STATE)
- ⏳ Green Phase: Implement code to pass tests
- ⏳ Refactor Phase: Improve code quality

## Next: Implementation (Phase 3)

Once you're ready to implement, create:

```javascript
// src/checkpoint-cleaner.js

class CheckpointCleaner {
  constructor(logger) {
    this.logger = logger;
  }

  cleanupOnCompletion(sessionId) {
    // Implementation for AC#1
  }

  discoverCheckpointFiles() {
    // Implementation for AC#3
  }

  cleanupAllCheckpointsWithConfirmation(confirmed) {
    // Implementation for AC#3
  }

  displayCheckpointList() {
    // Implementation for AC#4
  }

  displayConfirmationQuestion(askUserQuestion) {
    // Implementation for AC#4
  }

  handleUserResponse(response, selectedFiles) {
    // Implementation for AC#4
  }

  parseCleanupFlag(args) {
    // Implementation for AC#3
  }
}

module.exports = CheckpointCleaner;
```

Then run tests again - they should start passing as you implement each method.

## Test Files Overview

| File | AC | Tests | Focus |
|------|-----|-------|-------|
| test-checkpoint-cleanup-on-success.js | #1 | 11 | Auto-cleanup on completion |
| test-checkpoint-preservation-on-failure.js | #2 | 12 | Preserve on failure |
| test-manual-cleanup-command.js | #3 | 15 | Manual cleanup command |
| test-cleanup-confirmation-with-file-list.js | #4 | 16 | Confirmation + file list |
| test-edge-cases-and-performance.js | NFR | 16 | Performance & edge cases |

## Key Test Patterns Used

### 1. File System Testing
```javascript
beforeEach(() => {
  if (!fs.existsSync(tempDir)) {
    fs.mkdirSync(tempDir, { recursive: true });
  }
});

afterEach(() => {
  // Cleanup test files
  if (fs.existsSync(filePath)) {
    fs.unlinkSync(filePath);
  }
});
```

### 2. Logger Mocking
```javascript
const mockLogger = {
  info: (msg) => logOutput.push(msg),
  error: (msg) => logOutput.push({ error: msg }),
  warn: (msg) => logOutput.push({ warn: msg })
};
```

### 3. Assertion Patterns
```javascript
// Verify file deleted
expect(fs.existsSync(filePath)).toBe(false);

// Verify log message
expect(logOutput).toContain(`Checkpoint marked for cleanup: ${sessionId}`);

// Verify error handling
expect(() => { cleaner.cleanup(); }).not.toThrow();
```

## Test Statistics

- **Total Test Cases:** 69
- **Total Lines of Test Code:** 1,836
- **Acceptance Criteria Covered:** 4/4 (100%)
- **Edge Cases Covered:** 4 major scenarios
- **Performance Tests:** 3 (< 1 second for 100+ files)

## Troubleshooting

### "Cannot find module" Error
**Cause:** `src/checkpoint-cleaner.js` doesn't exist
**Fix:** Create the file and implement the `CheckpointCleaner` class

### "Expected false to be true" Error
**Cause:** Checkpoint file wasn't deleted when expected
**Fix:** Implement file deletion logic in `cleanupOnCompletion()`

### Timeout Error
**Cause:** Performance test failing (cleanup takes too long)
**Fix:** Optimize file deletion, use batch operations

## Files Reference

| File | Purpose |
|------|---------|
| `tests/STORY-138/README.md` | Detailed test documentation |
| `tests/STORY-138/test-*.js` | Test suites (5 files) |
| `.claude/plans/STORY-138-test-generation-summary.md` | Implementation guidance |

---

**Status:** TDD Red Phase - All tests failing (as expected)
**Next:** Implement `src/checkpoint-cleaner.js` in Phase 3
