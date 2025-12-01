# Release Script Test Suite (STORY-070)

Comprehensive Jest test suite for `scripts/release.sh` automation workflow.

## Test Structure

```
tests/release/
├── unit/
│   ├── release-script.test.js          # Phase 0-2 tests
│   └── release-script-phases.test.js   # Phase 3-7 tests
├── integration/
│   └── release-workflow.integration.test.js  # End-to-end workflow tests
├── fixtures/
│   ├── version.json                     # Test version metadata
│   ├── checksums.txt                    # Test checksum file
│   └── release-config.sh                # Test configuration
├── helpers/
│   └── mock-helpers.js                  # Reusable mock functions
└── README.md                            # This file
```

## Test Coverage

### Unit Tests (tests/release/unit/)

**release-script.test.js** - Phases 0-2:
- ✅ SCR-002: Git working tree validation
- ✅ Test suite execution
- ✅ External tools validation (gh CLI, npm)
- ✅ SCR-001: Interactive version selection
- ✅ Version bump calculation (patch/minor/major/custom)
- ✅ BR-001: Version uniqueness validation
- ✅ SCR-003: Claude directory sync with exclusions
- ✅ SCR-004: DevForgeAI directory sync with exclusions
- ✅ MAN-001: Sync manifest generation

**release-script-phases.test.js** - Phases 3-7:
- ✅ DAT-001: version.json update with semver format
- ✅ CHANGELOG.md generation with commit grouping
- ✅ Git tag creation
- ✅ Release commit
- ✅ SCR-005: SHA-256 checksum generation
- ✅ CHK-001: Checksum file format validation
- ✅ CHK-002: Alphabetical sorting
- ✅ CHK-003: Minimum entry count (50+)
- ✅ SCR-006: GitHub release creation via gh CLI
- ✅ BR-002: Pre-release detection (beta versions)
- ✅ SCR-007: NPM publish execution
- ✅ BR-005: STORY-067 integration (src/package.json)
- ✅ SCR-008: Rollback on failure
- ✅ BR-003: Atomic phases
- ✅ SCR-009: --dry-run flag
- ✅ SCR-010: --yes flag for CI

### Integration Tests (tests/release/integration/)

**release-workflow.integration.test.js**:
- ✅ BR-004: Phase execution order validation
- ✅ Full workflow success scenario
- ✅ Failure scenarios and rollback for each phase
- ✅ NFR-003: Total execution time (<5 minutes)
- ✅ NFR-011: Cross-platform compatibility
- ✅ LOG-001: Phase timing capture
- ✅ LOG-002: Command output logging
- ✅ LOG-003: Error detail logging
- ✅ NFR-005: No credentials in logs
- ✅ NFR-006: Sensitive file exclusion

## Running Tests

### All Tests
```bash
npm test tests/release/
```

### Unit Tests Only
```bash
npm test tests/release/unit/
```

### Integration Tests Only
```bash
npm test tests/release/integration/
```

### Specific Test File
```bash
npm test tests/release/unit/release-script.test.js
```

### Watch Mode (TDD)
```bash
npm test tests/release/ -- --watch
```

### Coverage Report
```bash
npm test tests/release/ -- --coverage
```

## Test Approach

### Mock-Based Subprocess Testing

Since Bats/shellspec would require external dependencies (violating dependencies.md), we use **Jest with child_process mocks**:

1. **Mock child_process.execSync** - All bash commands are intercepted
2. **Test script logic** - Validate phase execution, error handling, rollback
3. **Verify command patterns** - Ensure correct git/npm/gh CLI usage
4. **Simulate failures** - Test rollback at each phase

### Example Mock Pattern

```javascript
// Mock successful git status check
execSync.mockImplementation((cmd) => {
  if (cmd.includes('git status --porcelain')) {
    return ''; // Clean tree
  }
  return '';
});
```

### AAA Pattern (Arrange, Act, Assert)

All tests follow TDD best practices:

```javascript
test('should reject dirty git working tree', () => {
  // Arrange - Mock dirty tree
  execSync.mockImplementation((cmd) => {
    if (cmd.includes('git status --porcelain')) {
      return 'M  file1.txt\n?? file2.txt\n';
    }
    return '';
  });

  // Act & Assert
  expect(() => {
    execSync('bash scripts/release.sh');
  }).toThrow(/Uncommitted changes detected/);
});
```

## Coverage Target

- **Target**: ≥ 80% for script logic
- **Current**: 0% (TDD Red phase - tests fail until script implemented)

## Fixtures

### version.json
Test fixture for version metadata validation.

### checksums.txt
Test fixture for checksum format validation (5 sample entries).

### release-config.sh
Test configuration with exclusion patterns, registry URLs, and settings.

## Mock Helpers

Reusable mock functions in `helpers/mock-helpers.js`:

- `mockGitCleanTree()` - Clean working tree
- `mockGitDirtyTree()` - Uncommitted changes
- `mockTestsPassing()` - Successful test suite
- `mockTestsFailing()` - Failed tests
- `mockGhAuthenticated()` - gh CLI authenticated
- `mockNpmAuthenticated()` - npm authenticated
- `mockSyncSuccess()` - Successful file sync
- `mockChecksumGeneration()` - SHA-256 checksums
- `mockGithubReleaseSuccess()` - GitHub release created
- `mockNpmPublishSuccess()` - NPM publish successful
- `mockGitTagSuccess()` - Git tag created
- `mockGitTagExists()` - Tag already exists
- `mockRollbackCommands()` - Rollback operations
- `mockFullReleaseSuccess()` - Complete successful release

## TDD Workflow

### Red Phase (Current)
```bash
npm test tests/release/
# All tests FAIL (expected - script not implemented yet)
```

### Green Phase (Next)
1. Implement `scripts/release.sh`
2. Implement `scripts/release-functions.sh` (helper functions)
3. Run tests until all pass

### Refactor Phase (Final)
1. Improve script organization
2. Extract reusable functions
3. Add error handling
4. Optimize performance
5. Keep tests passing

## Test Requirements Traceability

| Test File | AC Coverage | Technical Spec Coverage |
|-----------|-------------|-------------------------|
| `release-script.test.js` | AC#1, AC#2 | SCR-001, SCR-002, SCR-003, SCR-004, MAN-001, BR-001 |
| `release-script-phases.test.js` | AC#3, AC#4, AC#6, AC#7 | SCR-005, SCR-006, SCR-007, SCR-008, SCR-009, SCR-010, DAT-001, CHK-001/002/003, BR-002, BR-003, BR-005, NFR-004, NFR-009 |
| `release-workflow.integration.test.js` | All ACs | BR-004, NFR-003, NFR-005, NFR-006, NFR-011, LOG-001/002/003 |

## Known Limitations

1. **No actual file system operations** - Tests mock `execSync`, don't create real files
2. **No real network I/O** - GitHub/NPM operations are mocked
3. **Platform-specific commands** - Tests assume Linux/macOS (sha256sum vs shasum)
4. **Interactive prompts** - User input not tested (requires mock-stdin or similar)

## Future Enhancements

1. Add E2E tests with real file system in temp directory
2. Test interactive prompts with mock-stdin
3. Add performance benchmarks (NFR-001, NFR-002)
4. Test on Windows/macOS/Linux via CI matrix
5. Add visual regression tests for terminal output formatting

## References

- **Story**: `.ai_docs/Stories/STORY-070-framework-release-automation.story.md`
- **Script** (to be created): `scripts/release.sh`
- **Config** (to be created): `.devforgeai/config/release-config.sh`
- **Jest Docs**: https://jestjs.io/docs/getting-started
- **Subprocess Mocking**: https://jestjs.io/docs/mock-functions
