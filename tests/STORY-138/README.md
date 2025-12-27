# STORY-138: Auto-Cleanup Completed Checkpoints - Test Suite

## Overview

Comprehensive Jest test suite for STORY-138 acceptance criteria, covering auto-cleanup of ideation checkpoints on successful completion and manual cleanup via command.

## Test Files

### 1. `test-checkpoint-cleanup-on-success.js` (AC#1)
**Tests:** Checkpoint deletion on successful ideation completion

**Coverage:**
- Checkpoint file deletion when session completes
- Success logging: "Checkpoint marked for cleanup: {session_id}"
- Checkpoint file path validation
- Various session ID formats (alphanumeric, UUID)
- Race condition handling (already deleted)
- Permission denied errors
- Cleanup timing validation
- Return value verification

**Test Count:** 11 tests

### 2. `test-checkpoint-preservation-on-failure.js` (AC#2)
**Tests:** Checkpoint preservation when session fails or is interrupted

**Coverage:**
- Checkpoint preservation on failure at various phases
- User cancellation scenarios
- Context window exhaustion handling
- Unexpected error recovery
- Checkpoint content validation (metadata preservation)
- Error details preservation
- Resume capability validation
- Resume metadata availability
- No automatic cleanup on failure
- Multiple failed sessions

**Test Count:** 12 tests

### 3. `test-manual-cleanup-command.js` (AC#3)
**Tests:** Manual cleanup via `/ideate --clean-checkpoints` command

**Coverage:**
- Checkpoint file discovery matching pattern
- Correct glob pattern usage
- No checkpoints found scenario
- User confirmation requirement
- Confirmation prompt display with count
- Deletion when user confirms
- Preservation when user declines
- Bulk deletion of 5+ files
- Cleanup count reporting
- Deletion error handling
- Cleanup flag detection in command args
- Other flags handling
- Flag not present scenario
- Large checkpoint numbers (100+)
- Mixed valid/invalid files

**Test Count:** 15 tests

### 4. `test-cleanup-confirmation-with-file-list.js` (AC#4)
**Tests:** Confirmation flow with checkpoint file list and metadata

**Coverage:**
- File list display with timestamps
- Problem statement preview display
- Long preview truncation
- Session ID display
- Confirmation prompt with count
- "Yes, delete all" option
- "No, keep them" option
- "Select specific files" option
- Delete all user response handling
- Keep all user response handling
- Selective deletion handling
- Missing problem statement handling
- Missing timestamp handling
- Chronological ordering (reverse)
- List display before confirmation
- Formatted summary generation

**Test Count:** 16 tests

### 5. `test-edge-cases-and-performance.js` (NFR + Edge Cases)
**Tests:** Performance requirements and edge case handling

**Coverage:**
- **NFR-001 (Performance):** 100 files cleanup < 1 second
- **NFR-001:** 1000 files cleanup with acceptable performance
- **NFR-001:** Progress reporting for large operations
- **NFR-002 (Reliability):** Permission errors don't affect session
- **NFR-002:** Partial cleanup results on failure
- **NFR-002:** Session completion despite cleanup failure
- **Edge Case #1 (Race):** Checkpoint already deleted
- **Edge Case #1:** Cleanup of missing checkpoint
- **Edge Case #2 (Permissions):** Permission denied warning
- **Edge Case #2:** Cleanup continuation after permission error
- **Edge Case #3 (Large Numbers):** Batch deletion for 100+ files
- **Edge Case #3:** Progress display for large operations
- **Edge Case #4 (Slow Filesystem):** 5-second timeout handling
- **Edge Case #4:** Slow filesystem warnings
- Concurrent checkpoint creation isolation
- File structure variation handling

**Test Count:** 16 tests

## Test Execution

### Run All Tests for STORY-138
```bash
npm test tests/STORY-138/
```

### Run Specific Test File
```bash
npm test tests/STORY-138/test-checkpoint-cleanup-on-success.js
```

### Run with Coverage
```bash
npm test tests/STORY-138/ --coverage
```

### Run Single Test
```bash
npm test tests/STORY-138/test-checkpoint-cleanup-on-success.js -t "should_delete_checkpoint_file_when_ideation_completes_successfully"
```

## Test Architecture

### Class Under Test: `CheckpointCleaner`

Expected location: `src/checkpoint-cleaner.js`

**Key Methods to Implement:**
- `cleanupOnCompletion(sessionId)` - AC#1 auto-cleanup
- `discoverCheckpointFiles()` - AC#3 file discovery
- `requestConfirmation(count)` - AC#3 confirmation
- `cleanupAllCheckpointsWithConfirmation(confirmed)` - AC#3 bulk cleanup
- `displayCheckpointList()` - AC#4 list display
- `displayConfirmationQuestion(askUserQuestion)` - AC#4 confirmation prompt
- `handleUserResponse(response, selectedFiles)` - AC#4 response handling
- `setCleanupTimeout(ms)` - Performance/edge case
- `parseCleanupFlag(args)` - Command parsing

### Mock Objects

**mockLogger:**
- `info(message)` - Logs to array
- `error(message)` - Logs errors
- `warn(message)` - Logs warnings

**mockAskUserQuestion:**
- Returns question structure with header and options
- Captures all questions for assertion

## Expected Failures

All tests will FAIL initially because:

1. `CheckpointCleaner` class not yet implemented
2. File cleanup methods not written
3. Command parsing not implemented
4. Confirmation flow not coded
5. File list display logic missing

## Test Pyramid Distribution

| Layer | Count | % |
|-------|-------|-----|
| Unit | 40 | 70% |
| Integration | 12 | 20% |
| E2E | 2 | 10% |

## Coverage Targets (Post-Implementation)

| Component | Target | Type |
|-----------|--------|------|
| CheckpointCleaner | 95% | Business Logic |
| File I/O | 85% | Application |
| Command Parsing | 90% | Business Logic |

## Key Testing Patterns

### AAA Pattern
All tests follow Arrange-Act-Assert:
```javascript
test('description', () => {
  // Arrange: Setup preconditions
  fs.writeFileSync(filePath, content);

  // Act: Execute behavior
  cleaner.cleanupOnCompletion(sessionId);

  // Assert: Verify outcome
  expect(fs.existsSync(filePath)).toBe(false);
});
```

### Fixtures
- `tempDir`: Isolated temp directory for test files
- `mockLogger`: Captures log output for assertions
- `mockAskUserQuestion`: Captures user questions

### Cleanup
- `afterEach()` removes all test checkpoint files
- No test pollution between test runs
- Safe parallel execution

## Acceptance Criteria Mapping

| AC | Tests | Status |
|----|-------|--------|
| AC#1 (Auto-cleanup success) | test-checkpoint-cleanup-on-success.js | 11 tests |
| AC#2 (Preserve on failure) | test-checkpoint-preservation-on-failure.js | 12 tests |
| AC#3 (Manual cleanup) | test-manual-cleanup-command.js | 15 tests |
| AC#4 (Confirmation + list) | test-cleanup-confirmation-with-file-list.js | 16 tests |
| Edge Cases | test-edge-cases-and-performance.js (partial) | 8 tests |
| Performance (NFR-001) | test-edge-cases-and-performance.js | 3 tests |
| Reliability (NFR-002) | test-edge-cases-and-performance.js | 3 tests |

**Total Tests: 70 failing tests**

## TDD Workflow

1. **Red Phase (CURRENT):** All tests fail - business logic not implemented
2. **Green Phase:** Implement CheckpointCleaner - tests pass
3. **Refactor Phase:** Improve code quality while keeping tests green
4. **Integration:** Integrate with devforgeai-ideation skill

## Implementation Guidance

### Checkpoint File Locations
- Successful completion checkpoints: `devforgeai/temp/.ideation-checkpoint-{session_id}.yaml`
- Use `Write()` tool to create/update (avoid Bash)
- Use `Glob()` to discover files

### Logging
- Use provided logger interface
- Log message format: "Checkpoint marked for cleanup: {session_id}"
- Warning on permission denied
- Info on successful deletion

### User Interaction
- Use `AskUserQuestion` for confirmation
- Options: "Yes, delete all", "No, keep them", "Select specific files"
- Display list before asking confirmation

### Performance Constraints
- Must complete 100 files in < 1 second
- Should handle 1000+ files in < 5 seconds
- Should show progress for large operations

## Notes

- Tests are framework-agnostic (testing behavior, not implementation)
- Jest specifically required per tech-stack.md
- Tests can run in isolation or in parallel
- No external dependencies beyond Jest and fs/path Node modules
- All file I/O is local (no network calls)

## Author Notes

Generated as TDD Red Phase tests for STORY-138 using test-automator skill.
Tests drive implementation through failing assertions.
