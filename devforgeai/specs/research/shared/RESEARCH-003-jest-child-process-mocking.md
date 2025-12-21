---
research_id: RESEARCH-003
epic_id: null
story_id: STORY-066
workflow_state: In Development
research_mode: discovery
timestamp: 2025-11-27T00:00:00Z
quality_gate_status: PASS
version: "2.0"
---

# Jest Code Coverage with Mocked Modules and Promise Handling

## 1. Executive Summary

Researched why Jest coverage doesn't register lines 30-31 in `bin/devforgeai.js` despite tests executing them. **Root cause:** Not a coverage bug - the code paths are genuinely not executed due to mock behavior. The mocked `cli.run()` returns a Promise that resolves immediately (already fulfilled), bypassing the Promise detection logic at lines 29-31. Solution requires either changing mock implementation or refactoring code structure.

## 2. Research Scope

**Questions:**
1. Why doesn't Jest coverage register lines 30-31 when tests appear to execute them?
2. How do mocked modules interact with coverage instrumentation?
3. Are there Jest configuration options to improve coverage with mocks?
4. Should alternative mocking strategies or coverage tools be used?

**Boundaries:**
- Focus on Jest coverage with `jest.mock()`
- Async/Promise handling with mocked dependencies
- Coverage providers (Babel/Istanbul vs V8)

**Assumptions:**
- Using Jest's default coverage provider (Babel/Istanbul)
- Tests are async and properly await promises
- Mock implementation is correct for test purposes

## 3. Methodology Used

**Research Mode:** Discovery
**Duration:** 1 hour
**Data Sources:**
- Official Jest documentation
- GitHub issues (jest/jest repository)
- Stack Overflow technical discussions
- Developer blog posts

**Methodology Steps:**
1. Web research on Jest coverage with mocked modules
2. Investigation of Promise handling in Jest tests
3. Comparison of coverage providers (V8 vs Babel/Istanbul)
4. Analysis of async/await coverage tracking
5. Alternative coverage tool evaluation

## 4. Findings

### 4.1 Core Issue: Code Not Executed vs Coverage Not Tracked

**Critical Discovery:** The problem is NOT coverage instrumentation failure. The code at lines 30-31 is genuinely NOT executed.

**Why:**
```javascript
// Test code
cli.run.mockReturnValue(Promise.resolve(0));
const exitCode = await binEntry.main(['install', '/tmp']);
```

When `Promise.resolve(0)` is returned by the mock:
1. The Promise is **already fulfilled** (not pending)
2. Line 29 check: `result && typeof result.then === 'function'` → TRUE (Promises have `.then`)
3. BUT: The Promise resolves **synchronously** in the microtask queue
4. By the time execution reaches line 30, the Promise is already resolved
5. **However:** The code path at lines 30-31 is for handling **thenable objects**, not direct Promise returns

**The Real Problem:**
The code assumes `cli.run()` might return a thenable (Promise-like object) that needs explicit awaiting. But `mockReturnValue(Promise.resolve(0))` returns an actual Promise, which JavaScript's `await` handles automatically **before** entering the `main()` function body.

```javascript
// What actually happens:
async function main(argv) {
  try {
    const result = await cli.run(argv);  // Promise already resolved here

    // result = 0 (the resolved value), NOT the Promise
    if (typeof result === 'number') {
      return result;  // ✅ This branch executes
    }

    // Lines 29-31: Dead code path for this test
    if (result && typeof result.then === 'function') {
      const exitCode = await result;  // Never reached
      return exitCode;
    }
  }
}
```

### 4.2 How Jest Coverage Works

**Babel/Istanbul (Default Provider):**
- Instruments code by inserting coverage tracking statements
- Operates on **original source code** before transpilation
- Tracks statement, branch, function, and line coverage
- More precise but slower (memory-intensive)

**V8 Coverage Provider:**
- Uses Node.js built-in V8 coverage engine
- Faster (no instrumentation overhead)
- Less precise (tracks blocks, not statements)
- Converts V8 output to Istanbul format via source maps

**Ignore Syntax:**
- Babel/Istanbul: `/* istanbul ignore next */`
- V8: `/* c8 ignore next */`

### 4.3 Common Mocking Pitfalls

**1. Mocking the File Under Test**
```javascript
// ❌ WRONG - This makes actual implementation show 0% coverage
jest.mock('../lib/my-module');

// ✅ CORRECT - Only mock dependencies, not the module you're testing
jest.mock('../lib/dependency');
```

**2. Not Awaiting Async Operations**
```javascript
// ❌ WRONG - Test completes before code runs
test('async test', () => {
  someAsyncFunction();  // Not awaited
});

// ✅ CORRECT - Wait for async code to complete
test('async test', async () => {
  await someAsyncFunction();
});
```

**3. Promise Timing Issues**
```javascript
// Mock returns already-resolved Promise
cli.run.mockReturnValue(Promise.resolve(0));

// Better: Mock returns pending Promise for async path testing
cli.run.mockImplementation(() => {
  return new Promise((resolve) => {
    setTimeout(() => resolve(0), 0);
  });
});
```

### 4.4 Coverage Provider Comparison

| Feature | Babel/Istanbul | V8 |
|---------|----------------|-----|
| **Speed** | Slower (instrumentation overhead) | Faster (native V8) |
| **Precision** | Statement-level tracking | Block-level tracking |
| **Branch Coverage** | Tracks implicit else branches | Only explicit branches |
| **Source Maps** | Direct source code | Via v8-to-istanbul conversion |
| **Ignore Comments** | `/* istanbul ignore next */` | `/* c8 ignore next */` |
| **Memory Usage** | Higher (instrumented code) | Lower (native) |
| **Accuracy** | More precise | Less precise (inherent conversion issues) |

**Recommendation:** Stick with Babel/Istanbul for precision unless performance is critical.

### 4.5 Alternative Coverage Tools

**nyc (Istanbul CLI):**
- Jest uses nyc under the hood
- No benefit to using separately with Jest

**c8 (V8 Coverage CLI):**
- Standalone V8 coverage tool
- Used by Vitest (not Jest)
- Faster but less precise than Istanbul

**Conclusion:** Jest's built-in coverage is sufficient. Switching tools won't solve the fundamental issue (code not executing).

## 5. Framework Compliance Check

**Validation Date:** 2025-11-27T00:00:00Z
**Context Files Checked:** N/A (research for npm package, not framework project)

| Context File | Status | Violations | Details |
|--------------|--------|------------|---------|
| tech-stack.md | N/A | 0 | Research topic (no tech changes) |
| source-tree.md | N/A | 0 | Research topic |
| dependencies.md | N/A | 0 | Research topic |
| coding-standards.md | N/A | 0 | Research topic |
| architecture-constraints.md | N/A | 0 | Research topic |
| anti-patterns.md | N/A | 0 | Research topic |

**Quality Gate Status:** PASS
**Recommendation:** No framework violations. Research findings apply to test implementation strategy.

## 6. Workflow State

**Current State:** In Development
**Research Focus:** Debugging patterns and test coverage optimization
**Staleness Check:** CURRENT (research conducted 2025-11-27 for active story STORY-066)

## 7. Recommendations

### Recommendation #1: Refactor Code to Remove Dead Path (HIGHEST PRIORITY)

**Score:** 95/100
**Benefits:**
- Eliminates dead code (lines 29-31 are unreachable with current architecture)
- Achieves 100% coverage naturally
- Simplifies code logic
- Reflects actual `cli.run()` contract (always returns Promise)

**Drawbacks:**
- Requires code change
- Slightly less defensive (removes thenable check)

**Implementation:**
```javascript
// Current code (lines 23-34)
async function main(argv) {
  try {
    const result = await cli.run(argv);

    if (typeof result === 'number') {
      return result;
    }

    // Lines 29-31: Dead code - cli.run() always returns Promise
    if (result && typeof result.then === 'function') {
      const exitCode = await result;
      return exitCode;
    }

    return 0;
  } catch (error) {
    return error.exitCode || 1;
  }
}

// Refactored code (remove lines 29-31)
async function main(argv) {
  try {
    const result = await cli.run(argv);

    // cli.run() contract: returns Promise<number> or number
    if (typeof result === 'number') {
      return result;
    }

    // If not a number, assume success
    return 0;
  } catch (error) {
    return error.exitCode || 1;
  }
}
```

**Applicability:** Immediate. Aligns with actual `cli.run()` implementation which always returns a Promise.

### Recommendation #2: Use Coverage Ignore Comments (TEMPORARY WORKAROUND)

**Score:** 60/100
**Benefits:**
- No code changes required
- Quick fix for coverage threshold
- Documents intentional coverage gap

**Drawbacks:**
- Hides potential dead code
- Reduces overall coverage metrics
- Doesn't solve root issue

**Implementation:**
```javascript
// Lines 29-31 with ignore comment
/* istanbul ignore next */
if (result && typeof result.then === 'function') {
  const exitCode = await result;
  return exitCode;
}
```

**Applicability:** Use only if lines 29-31 are genuinely needed for edge cases. Otherwise, prefer Recommendation #1.

### Recommendation #3: Mock Implementation Testing (ADVANCED)

**Score:** 75/100
**Benefits:**
- Tests the Promise-handling code path
- Achieves 100% coverage
- Validates defensive coding

**Drawbacks:**
- Requires understanding Promise internals
- Adds test complexity
- Tests implementation detail, not behavior

**Implementation:**
```javascript
// Create custom thenable (not Promise)
test('handles thenable object', async () => {
  const thenable = {
    then: (resolve) => {
      setTimeout(() => resolve(0), 0);
      return thenable;  // For chaining
    }
  };

  cli.run.mockReturnValue(thenable);
  const exitCode = await binEntry.main(['install', '/tmp']);
  expect(exitCode).toBe(0);
});
```

**Applicability:** Use if `cli.run()` contract explicitly allows non-Promise thenables. Otherwise, over-engineering.

## 8. Risk Assessment

### Risk #1: Dead Code Accumulation
- **Severity:** MEDIUM
- **Probability:** HIGH (lines 29-31 are unreachable with current `cli.run()` implementation)
- **Impact:** Code maintenance burden, confusing coverage gaps, potential bugs if assumptions change
- **Mitigation:** Remove dead code paths (Recommendation #1) or document as defensive coding

### Risk #2: Coverage False Sense of Security
- **Severity:** MEDIUM
- **Probability:** MEDIUM (coverage ≠ correctness)
- **Impact:** Tests might pass but miss edge cases
- **Mitigation:** Focus on behavior testing, not just coverage metrics. Add integration tests.

### Risk #3: Mocking Strategy Fragility
- **Severity:** LOW
- **Probability:** LOW
- **Impact:** Tests might not reflect real-world `cli.run()` behavior
- **Mitigation:** Add integration tests that don't mock `cli` module. Verify mock matches actual implementation.

### Risk #4: Coverage Provider Migration
- **Severity:** LOW
- **Probability:** LOW (switching to V8 provider)
- **Impact:** Coverage metrics might change, ignore comments break
- **Mitigation:** Stick with Babel/Istanbul unless performance critical. Document provider choice in jest.config.js.

### Risk #5: Async Timing Bugs
- **Severity:** HIGH
- **Probability:** LOW (proper await usage in tests)
- **Impact:** Flaky tests, unreliable coverage
- **Mitigation:** Always await async operations. Use `flush-promises` pattern if needed for nested async.

## 9. ADR Readiness

**ADR Required:** No

**Rationale:** This is a test implementation detail, not an architectural decision. The findings clarify Jest coverage behavior but don't introduce new technology or patterns requiring ADR documentation.

**If ADR Were Needed:**
- Title: "ADR-XXX: Jest Coverage Strategy for Mocked Modules"
- Evidence: Research shows Babel/Istanbul provides more precise coverage than V8
- Decision: Use default Babel/Istanbul provider, mock only dependencies (not files under test)

**Next Steps:**
1. Apply Recommendation #1: Remove dead code at lines 29-31
2. Update test to verify new code path coverage (should reach 100%)
3. Document `cli.run()` contract in JSDoc: "Returns Promise<number> or number"
4. No ADR required - implementation detail only

---

## Sources

### Jest Configuration and Coverage
- [Configuring Jest · Jest](https://jestjs.io/docs/configuration)
- [Jest CLI Options · Jest](https://mulder21c.github.io/jest/docs/en/cli)
- [Troubleshooting · Jest](https://jestjs.io/docs/troubleshooting)

### Coverage Issues with Mocked Modules
- [Jest not collecting coverage info on mocked functions · Issue #7953](https://github.com/jestjs/jest/issues/7953)
- [Jest - How to get coverage for mocked classes and implementations - Stack Overflow](https://stackoverflow.com/questions/50348317/jest-how-to-get-coverage-for-mocked-classes-and-implementations)
- [How to hit test coverage in jest mock test · Issue #8817](https://github.com/jestjs/jest/issues/8817)

### Async/Promise Coverage
- [Code coverage concern on promise/asynchronous unit testing using nockjs and jest - Stack Overflow](https://stackoverflow.com/questions/57656523/code-coverage-concern-on-promise-asynchronous-unit-testing-using-nockjs-and-jest)
- [An Async Example · Jest](https://jestjs.io/docs/tutorial-async)
- [Testing Asynchronous Code · Jest](https://jestjs.io/docs/asynchronous)
- [How to resolve Jest issues: tests passing, but code coverage fails! - DEV Community](https://dev.to/endymion1818/how-to-resolve-jest-issues-tests-passing-but-code-coverage-fails-41la)

### Coverage Providers (V8 vs Babel/Istanbul)
- [Document some of the tradeoffs of V8 coverage (vs Babel/Istanbul coverage) · Issue #11188](https://github.com/jestjs/jest/issues/11188)
- [Jest 25: 🚀 Laying foundations for the future · Jest](https://jestjs.io/blog/2020/01/21/jest-25)
- [JS code coverage tool in 2023 - Istanbul vs Jest vs JS Coverage vs CodeCov | Axolo Blog](https://axolo.co/blog/p/code-coverage-js-in-2023)

### Debugging Coverage
- [JestJS - show all uncovered lines in coverage report - Stack Overflow](https://stackoverflow.com/questions/48159875/jestjs-show-all-uncovered-lines-in-coverage-report)
- [Why is Jest not inferring tests coverage lines correctly? - Stack Overflow](https://stackoverflow.com/questions/68695560/why-is-jest-not-inferring-tests-coverage-lines-correctly)
- [Why is Jest reporting these lines in my async Node code as not covered by tests? - Stack Overflow](https://stackoverflow.com/questions/51526955/why-is-jest-reporting-these-lines-in-my-async-node-code-as-not-covered-by-tests)

### Mocking Best Practices
- [Mock Functions · Jest](https://jestjs.io/docs/mock-function-api)
- [Bypassing module mocks · Jest](https://jestjs.io/docs/bypassing-module-mocks)
- [Mocking asynchronous functions with Jest | Nishant Kaushish](https://www.nishant-kaushish.com/blog/0708187b-e8c3-5e09-bf32-abe18df77b26/)
- [How to Mock Asynchronous Methods with Jest | by Ben Morrison | Medium](https://medium.com/@benjimorr/how-to-mock-asynchronous-methods-with-jest-38408434a6f4)

### Coverage Tools Comparison
- [Coverage: give the choice between c8 and nyc · Issue #1252](https://github.com/vitest-dev/vitest/issues/1252)
- [Coverage | Guide | Vitest](https://vitest.dev/guide/coverage.html)
- [c8 - npm](https://www.npmjs.com/package/c8)

---

**Report Generated:** 2025-11-27
**Location:** /mnt/c/Projects/DevForgeAI2/devforgeai/research/shared/RESEARCH-003-jest-child-process-mocking.md
**Research ID:** RESEARCH-003
**Version:** 2.0
