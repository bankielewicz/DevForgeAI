# Investigation Patterns

Reference file for the root-cause-diagnosis skill. Documents 6 failure categories with symptoms, investigation steps, and resolution patterns.

---

## Category 1: Spec Drift

**Description:** Implementation diverges from what constitutional context files specify. Code works but violates project constraints.

**Common Symptoms:**
- QA validation fails with "constraint violation" but tests pass
- Anti-pattern scanner flags code that appears correct
- File placed in wrong directory per source-tree.md
- Unapproved library imported
- Layer boundary crossed (Domain depends on Infrastructure)

**Investigation Steps:**
1. Read the failing validation output to identify which context file is violated
2. Read the specific context file cited:
   ```
   Read(file_path="devforgeai/specs/context/{violated_file}.md")
   ```
3. Read the implementation file flagged in the violation
4. Compare implementation against the specific constraint (line numbers from context file)
5. Identify the exact point of divergence

**Resolution Patterns:**
- **Wrong location:** Move file to correct path per source-tree.md
- **Unapproved library:** Replace with approved alternative from tech-stack.md or create ADR
- **Layer violation:** Introduce interface in Domain layer, implement in Infrastructure
- **Naming violation:** Rename to match coding-standards.md conventions

---

## Category 2: Test Assertion Failures

**Description:** Test expects specific output but implementation produces different (possibly correct) output. The bug may be in the test, the implementation, or both.

**Common Symptoms:**
- `AssertionError: expected X but got Y`
- `Expected output to contain "string"` failures
- Test passes in isolation but fails in suite (ordering dependency)
- Test fails intermittently (timing, state leakage)

**Investigation Steps:**
1. Read the failing test file completely:
   ```
   Read(file_path="{test_file}")
   ```
2. Identify the exact assertion that fails (line number from test output)
3. Read the acceptance criteria from the story file to determine expected behavior
4. Read the implementation under test
5. Determine which is wrong: the test expectation or the implementation output
6. Check for test isolation issues (shared state, missing setup/teardown)

**Resolution Patterns:**
- **Test expects wrong value:** Update test to match correct behavior per AC
- **Implementation produces wrong value:** Fix implementation logic
- **Ordering dependency:** Add proper setup/teardown, ensure test isolation
- **String format mismatch:** Align output format between test and implementation
- **Floating point comparison:** Use approximate comparison (pytest.approx, toBeCloseTo)

---

## Category 3: Import/Dependency Failures

**Description:** Missing modules, wrong versions, circular imports, or unresolvable dependencies prevent code from loading.

**Common Symptoms:**
- `ModuleNotFoundError: No module named 'X'`
- `ImportError: cannot import name 'Y' from 'Z'`
- `TypeError: X is not a function` (wrong version API)
- Circular import causing `AttributeError` or partial module
- `Package version X does not satisfy requirement Y`

**Investigation Steps:**
1. Read the full error traceback to identify the import chain
2. Check if the module exists in the project:
   ```
   Glob(pattern="**/{module_name}.*")
   Glob(pattern="**/{module_name}/**")
   ```
3. Check dependencies.md for approved version:
   ```
   Read(file_path="devforgeai/specs/context/dependencies.md")
   ```
4. For circular imports, trace the import chain:
   ```
   Grep(pattern="from.*import|import.*", path="{module_a}")
   Grep(pattern="from.*import|import.*", path="{module_b}")
   ```
5. Verify installed version matches dependencies.md specification

**Resolution Patterns:**
- **Missing module:** Install from dependencies.md or add to dependencies.md (requires ADR if new)
- **Wrong version:** Pin to version specified in dependencies.md
- **Circular import:** Extract shared types to a separate module, use late imports, or restructure
- **Wrong import path:** Fix import to match source-tree.md structure
- **Missing __init__.py:** Add package initializer file

---

## Category 4: Coverage Gaps

**Description:** Test coverage falls below required thresholds (95% business logic, 85% application, 80% infrastructure).

**Common Symptoms:**
- QA validation reports coverage below threshold
- `Coverage: 82% (required: 95%)` for business logic
- Untested branches identified in coverage report
- New code added without corresponding tests

**Investigation Steps:**
1. Run coverage report to identify uncovered lines:
   ```
   Bash(command="pytest --cov=src --cov-report=term-missing tests/")
   ```
2. Identify which layer the uncovered code belongs to (Domain/Application/Infrastructure)
3. Read the uncovered source file and identify untested paths:
   ```
   Read(file_path="{uncovered_file}")
   ```
4. Categorize uncovered code:
   - Error handling branches
   - Edge case conditions
   - Default/fallback paths
   - Guard clauses

**Resolution Patterns:**
- **Missing error path tests:** Add tests for exception/error scenarios
- **Missing edge case tests:** Add boundary value tests
- **Missing branch coverage:** Add tests for each conditional branch
- **Dead code:** Remove unreachable code (reduces denominator)
- **Infrastructure code:** Ensure at minimum 80% coverage with integration tests

---

## Category 5: Anti-Pattern Violations

**Description:** Code matches forbidden patterns defined in anti-patterns.md. These are structural issues, not functional bugs.

**Common Symptoms:**
- Anti-pattern scanner flags violations
- God Object detected (class > 500 lines)
- Direct instantiation instead of dependency injection
- SQL string concatenation detected
- Hardcoded secrets found

**Investigation Steps:**
1. Read anti-patterns.md to understand the specific violation:
   ```
   Read(file_path="devforgeai/specs/context/anti-patterns.md")
   ```
2. Read the flagged file and locate the violation:
   ```
   Read(file_path="{flagged_file}")
   ```
3. Determine violation severity (Critical/High/Medium/Low)
4. Check if the pattern has an approved alternative in coding-standards.md:
   ```
   Read(file_path="devforgeai/specs/context/coding-standards.md")
   ```
5. Assess refactoring scope (single file vs. cross-cutting)

**Resolution Patterns:**
- **God Object:** Extract responsibilities into separate classes (Single Responsibility)
- **Direct instantiation:** Introduce constructor injection, register in DI container
- **SQL concatenation:** Replace with parameterized queries
- **Hardcoded secrets:** Move to environment variables, reference by name
- **Missing error handling:** Add try/catch with proper error propagation
- **Tight coupling:** Introduce interfaces at layer boundaries

---

## Category 6: DoD/Commit Validation Failures

**Description:** Pre-commit hook blocks commit due to Definition of Done format errors or autonomous deferral detection.

**Common Symptoms:**
- `VALIDATION FAILED` in commit output
- `DoD item marked [x] but missing from Implementation Notes`
- `COMMIT BLOCKED`
- `AUTONOMOUS DEFERRAL DETECTED`

**Investigation Steps:**
1. Read the commit failure recovery guide:
   ```
   Read(file_path=".claude/rules/workflow/commit-failure-recovery.md")
   ```
2. Read the failing story file identified in validator output:
   ```
   Read(file_path="{story_file}")
   ```
3. Check for common format issues:
   - DoD items under `###` subsection (parser stops at first `###`)
   - DoD items not added to Implementation Notes at all
   - Text mismatch between DoD section and Implementation Notes
   - Autonomous deferral (marked `[x]` without user approval)
4. Count DoD items marked `[x]` and compare to Implementation Notes entries

**Resolution Patterns:**
- **Items under subsection:** Move items to flat list directly under `## Implementation Notes`, before any `###` headers
- **Items not added:** Copy each `[x]` item from DoD, add `- Completed: {description}` suffix
- **Text mismatch:** Copy exact text from DoD section (character-for-character)
- **Autonomous deferral:** HALT and escalate to user for approval
- **Validate before retry:** Run `devforgeai-validate validate-dod {STORY_FILE}` before re-committing

---

## Cross-Category Investigation

When a failure does not clearly fit one category, investigate in this priority order:

1. **Import/Dependency** (Category 3) - Check first, fastest to diagnose
2. **Test Assertion** (Category 2) - Check second, most common during TDD
3. **Spec Drift** (Category 1) - Check third, common during QA
4. **Anti-Pattern** (Category 5) - Check fourth, structural issues
5. **Coverage** (Category 4) - Check fifth, usually clear from reports
6. **DoD/Commit** (Category 6) - Check last, specific to commit phase

If failure spans multiple categories, document all contributing factors and prescribe fixes in dependency order (fix imports before fixing assertions, fix assertions before fixing coverage).
