# ADR-006: Interactive CLI Library ESM/CommonJS Compatibility

**Status:** Accepted
**Date:** 2025-12-01 (Updated: 2025-12-01 Session 3)
**Deciders:** User (via AskUserQuestion)
**Story:** STORY-071 (Wizard-Driven Interactive UI)

## Context

During STORY-071 implementation (Sessions 1-3), module format conflicts were discovered across multiple interactive CLI libraries:

**Session 1 (inquirer):**
1. **dependencies.md** specified `inquirer@^9.0.0` (locked dependency)
2. **inquirer@9.x** is ESM-only (uses `import` syntax)
3. **Project uses CommonJS** (no `"type": "module"` in package.json)
4. **Jest tests fail** with `SyntaxError: Cannot use import statement outside a module`

**Session 3 (ora and chalk):**
5. **dependencies.md** specified `ora@^7.0.0` and `chalk@^5.0.0`
6. **ora@6.x+** and **chalk@5.x+** are ESM-only
7. **Same Jest test failures** when tests load these modules via `require()`

### Root Cause Analysis

- **Commit 5c5aa87** (Nov 25, 2025) updated dependencies.md with `inquirer@^9.0.0`
- This was a batch commit adding EPIC-012 through EPIC-015
- The dependency was specified without considering module format compatibility
- No story was associated with this context file change (framework violation)
- STORY-066 mentioned "STORY-071 will add Inquirer.js" but didn't implement it

### Impact

- 5 test suites failing (prompt-service, install-wizard, output-formatter, progress-service, signal-handler)
- Runtime would work with dynamic imports, but Jest/CommonJS testing infrastructure breaks
- Blocks STORY-071 completion

## Decision

**Use last CommonJS-compatible versions for all interactive CLI libraries:**
- `inquirer`: 8.2.6 (9.x is ESM-only)
- `ora`: 5.4.1 (6.x+ is ESM-only)
- `chalk`: 4.1.2 (5.x+ is ESM-only)
- `cli-progress`: 3.12.0 (CommonJS compatible)

### Rationale

1. **Minimal disruption** - Only changes dependency version, not project architecture
2. **Maintains test infrastructure** - Jest and CommonJS continue working
3. **No functionality loss** - inquirer@8.2.6 has all features needed for STORY-071
4. **Future-proof path** - Can upgrade to ESM in future dedicated story if needed

### Alternatives Considered

1. **Convert project to ESM** - Too disruptive, affects all files, requires major refactoring
2. **Use dynamic imports** - Workaround that complicates code, doesn't fix test infrastructure
3. **Mock inquirer in tests** - Hides the problem, tests don't exercise real library

## Consequences

### Positive

- Tests pass immediately
- No architectural changes required
- Clear audit trail of the fix

### Negative

- Using older versions:
  - inquirer: 8.2.6 (vs 9.x latest)
  - ora: 5.4.1 (vs 8.x latest)
  - chalk: 4.1.2 (vs 5.x latest)
- May need future upgrade when project migrates to ESM

### Neutral

- These older versions have all features needed for STORY-071
- No functionality differences for interactive CLI use cases
- CommonJS/ESM transition is an industry-wide migration pattern

## Implementation

**Session 1 (inquirer):**
1. Update `devforgeai/context/dependencies.md`:
   - Change `"inquirer": "^9.0.0"` to `"inquirer": "^8.2.6"`
2. Update `package.json` to match
3. Run `npm install`

**Session 3 (ora and chalk):**
4. Update `devforgeai/context/dependencies.md`:
   - Change `"ora": "^7.0.0"` to `"ora": "^5.4.1"`
   - Change `"chalk": "^5.0.0"` to `"chalk": "^4.1.2"`
   - Add `"cli-progress": "^3.12.0"` (was missing from initial spec)
5. Update `package.json` to match
6. Run `npm install`
7. Verify all tests pass

## References

- Commit 5c5aa87: Batch commit that introduced the conflict
- STORY-066: Referenced STORY-071 would add Inquirer.js
- inquirer changelog: v9.0.0 dropped CommonJS support
