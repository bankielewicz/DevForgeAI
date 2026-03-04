# RCA-017: test-automator Source Tree Constraint Violation

**Date:** 2025-12-05
**Severity:** HIGH
**Component:** test-automator subagent
**Status:** IN_PROGRESS

---

## Issue Description

**What Happened:**
- test-automator subagent generated test files in `tests/installer/` directory
- source-tree.md constraint specifies correct location as `installer/tests/`
- Violation caused test directory fragmentation, leading to QA coverage analysis failures

**When Happened:**
- STORY-077 created test files in wrong directory (commit 96a0556, Dec 5, 2025)
- Issue discovered during STORY-078 QA validation (Dec 5, 2025)

**Where Happened:**
- `tests/installer/` directory created instead of using `installer/tests/`
- Multiple test files: test_version_*.py, test_compatibility_checker.py, test_integration_*.py

**Expected vs Actual:**
- **Expected:** All installer tests in `installer/tests/` per source-tree.md line 378
- **Actual:** Tests in `tests/installer/` directory
- **Impact:** QA coverage tool ran only one test directory, reported 0% coverage for version modules despite tests existing in different directory

---

## 5 Whys Analysis

### Why #1: Why did test-automator generate tests in tests/installer/?
**Answer:** test-automator subagent does not read source-tree.md before generating test files. It has no logic to validate test file locations against framework constraints.

**Evidence:**
`.claude/agents/test-automator.md:346-407` - Phase 2 workflow shows Step 4 reads tech-stack.md for framework choice, but NO Step reading source-tree.md for file location validation.

---

### Why #2: Why doesn't test-automator read source-tree.md?
**Answer:** The subagent specification was written without including source-tree.md validation in the workflow. Developer focused on test generation logic (AAA pattern, assertions) but didn't address WHERE tests should be placed relative to framework constraints.

**Evidence:**
`.claude/agents/test-automator.md:851-856` - References section lists tech-stack.md, story files, coverage reports but NOT source-tree.md.

---

### Why #3: Why was source-tree.md validation omitted from test-automator design?
**Answer:** test-automator was created before context-file validation pattern was systematically enforced across all subagents. The pattern exists in devforgeai-development skill (Phase 0) but wasn't applied to subagents invoked by development.

**Evidence:**
Commit history shows test-automator predates systematic context validation in subagents. Later subagents like deferral-validator explicitly read context files, but test-automator has no such validation.

---

### Why #4: Why didn't devforgeai-development skill enforce context file reading before invoking test-automator?
**Answer:** The development skill invokes test-automator during Phase 1 (Red - Test First) but doesn't explicitly provide or validate context about test file locations. Skill assumes test-automator "just knows" where tests should go.

**Evidence:**
devforgeai-development skill Phase 1 invokes test-automator without setting explicit context markers indicating test directory location requirements from source-tree.md.

---

### **Why #5 (ROOT CAUSE): Why wasn't source-tree.md validation established as a mandatory precondition for ALL file-generation subagents?**

**Answer:** The framework's context file constraint system (source-tree.md, dependencies.md, coding-standards.md, etc.) is treated as immutable architectural boundaries, but enforcement happens REACTIVELY via QA validation (after files created) rather than PROACTIVELY (before file creation). There is no automated guard in subagent design requiring reading source-tree.md BEFORE calling Write().

**Evidence:**

1. **source-tree.md CLEARLY DEFINES CONSTRAINT** (lines 378-380):
   ```
   installer/
     ├── tests/                  # Installer test suite
     │   ├── test_offline_installer.py
     │   └── test_*.py
   ```

2. **Multiple subagents CALL Write()** but none validate output paths:
   - test-automator (generates tests)
   - story-requirements-analyst (generates story sections)
   - api-designer (generates API specs)
   - documentation-writer (generates docs)

3. **Pattern ALREADY EXISTS in devforgeai-development**:
   - Phase 0 validates context files
   - But this pattern NOT APPLIED to subagents that invoke file operations

4. **Problem ONLY CAUGHT by QA** (reactive):
   - Tests created in wrong location
   - QA tool runs one directory, reports 0% coverage
   - Human discovers constraint violation AFTER files written

**This is a framework-level ARCHITECTURAL GAP**: File-generation subagents should validate output paths against source-tree.md BEFORE writing, not after QA discovers violation.

---

## Files Examined

### test-automator.md (CRITICAL)
**Lines:** 346-407
**Finding:** Phase 2 workflow lacks source-tree.md validation step
**Excerpt:**
```markdown
4. **Read Tech Stack for Framework**
   Read(file_path="devforgeai/context/tech-stack.md")
   - Identify test framework (pytest, Jest, xUnit, JUnit, etc.)

5. **Generate Unit Tests**
   - Follow AAA pattern (Arrange, Act, Assert)
```
**Significance:** Explicitly reads one context file (tech-stack) but omits another (source-tree). This selective pattern shows the subagent was not designed with comprehensive context file validation.

---

### source-tree.md (CRITICAL)
**Lines:** 378-380
**Finding:** Clearly defines correct test location
**Excerpt:**
```
├── installer/
│   ├── tests/                  # Installer test suite
│   │   ├── test_offline_installer.py  # Offline mode tests
│   │   └── test_*.py
```
**Significance:** Immutable architectural constraint that test-automator violates. The constraint exists and is explicit; subagent simply doesn't validate against it.

---

### test-automator.md References (HIGH)
**Lines:** 851-856
**Finding:** Missing source-tree.md from list of references
**Excerpt:**
```markdown
## References

- **Story Files**: `devforgeai/specs/Stories/*.story.md`
- **Tech Stack**: `devforgeai/context/tech-stack.md`
- **Coverage Reports**: `devforgeai/qa/coverage/coverage-report.json`
```
**Significance:** source-tree.md not listed as dependency shows constraint not considered during design.

---

### devforgeai-development skill (HIGH)
**Section:** Phase 1 (Red - Test First)
**Finding:** Invokes test-automator without explicit source-tree.md context
**Significance:** Calling skill also doesn't enforce source-tree.md validation before invoking subagent.

---

### lean-orchestration-pattern.md (MEDIUM)
**Lines:** 32-42
**Finding:** Pattern defines skill/subagent responsibilities but doesn't mandate ALL context file validation
**Significance:** Framework architecture pattern exists but enforcement is inconsistent across components.

---

## Context File Compliance

| File | Status | Finding |
|------|--------|---------|
| tech-stack.md | OK | Not required to mention test locations (framework-agnostic) |
| **source-tree.md** | **VIOLATED** | Clearly defines installer/tests/ but test-automator uses tests/installer/ |
| dependencies.md | OK | Not relevant to test file locations |
| coding-standards.md | OK | Not relevant to test file locations |
| architecture-constraints.md | OK | Not relevant to test file locations |
| anti-patterns.md | OK | Not relevant to test file locations |

---

## Recommendations

### REC-1: CRITICAL - Add source-tree.md validation to test-automator Phase 2
**Implemented in:** STORY-203

**Priority:** CRITICAL - Prevents immediate constraint violations
**Problem Addressed:** test-automator generates tests without validating correct directory location

**Proposed Solution:**
Add mandatory Step 4.5 to test-automator.md Phase 2 workflow that reads source-tree.md and validates test file locations BEFORE generating tests.

**Implementation:**

**File:** `.claude/agents/test-automator.md`
**Section:** Phase 2: Generate Failing Tests
**Insertion Point:** After line 377 (after Step 4: "Read Tech Stack"), before line 379 (Step 5: "Generate Unit Tests")
**Action:** INSERT the following text:

```markdown
4.5. **Read Source Tree for Test File Locations (MANDATORY)**

   ```
   Read(file_path="devforgeai/context/source-tree.md")
   ```

   **Step A: Determine Test Directory from Source Tree**

   Extract test directory pattern for the module being tested:

   ```
   IF module in "installer/":
       test_directory = "installer/tests/"  # Per source-tree.md line 378
   ELSE IF module in ".claude/":
       test_directory = determine from source-tree.md (if defined)
   ELSE:
       test_directory = determine from source-tree.md pattern
   ```

   **Step B: Validate All Test Output Paths**

   BEFORE generating ANY tests, validate that test file locations match:

   ```
   FOR each test_file_path in planned_test_outputs:
       IF NOT test_file_path.startswith(test_directory):
           HALT test generation
           Return error message:
           """
           ❌ TEST LOCATION VIOLATION

           Test file location violates source-tree.md constraint:

           Expected directory: {test_directory}
           Attempted location: {test_file_path}

           Fix:
           1. Update planned test paths to start with: {test_directory}
           2. OR update source-tree.md with new pattern
           3. Retry test generation

           source-tree.md constraint (line 378):
           {excerpt from source-tree.md showing correct location}
           """
   ```

   **Why This Step:** source-tree.md is an immutable architectural constraint.
   All file-generation operations must validate against it BEFORE writing files.
   This proactive validation prevents constraint violations from occurring,
   rather than having them discovered later by QA tools.
```

**Rationale:**

source-tree.md is an immutable architectural constraint that defines where all framework files should be located. test-automator is a file-generation component that MUST validate output paths BEFORE calling Write().

This proactive validation pattern:
1. Prevents constraint violations at source (when test-automator runs)
2. Provides immediate feedback to developers
3. Makes source-tree.md an enforced constraint, not a suggestion
4. Prevents QA from discovering violations after files already created

This pattern already exists in devforgeai-development skill (Phase 0 reads and validates context files), but test-automator was created without it. Adding this step makes test-automator consistent with framework architecture principles.

**Evidence References:**
- source-tree.md:378-380 defines installer/tests/ location
- test-automator.md:346-407 shows no source-tree.md validation
- test-automator.md:851-856 missing source-tree.md reference
- Commit 96a0556 created tests in tests/installer/ (wrong location)

**Testing Procedure:**

1. **Setup:**
   - Create test story for installer module (e.g., STORY-X: Test new backup service)
   - Story includes acceptance criteria requiring unit tests

2. **Execute:**
   - Run: `/dev STORY-X`
   - Proceed through Phase 0 and Phase 1 (Red phase)
   - Observe test-automator invocation

3. **Verify Expected Behavior:**
   - ✅ Tests generated in `installer/tests/` directory (correct)
   - ✅ No tests in `tests/installer/` directory
   - ✅ Error thrown if attempting to place tests outside `installer/tests/`

4. **Verify Edge Case:**
   - Create module in location NOT defined in source-tree.md
   - Verify error message provides clear guidance: "Update source-tree.md or choose existing location"

**Effort Estimate:** 30 minutes
- Implementation: 15 min (add Step 4.5 with validation logic)
- Testing: 10 min (verify correct directory via test story)
- Documentation: 5 min (update this section)

**Impact:**
- **Benefit:** Prevents future source-tree.md violations by test-automator
- **Risk:** Low (adds validation guard, doesn't change existing test generation logic)
- **Scope:** Only test-automator affected; improves all future tests generated by it

---

### REC-2: HIGH - Update ALL file-generation subagents with source-tree.md validation
**Implemented in:** STORY-204

**Priority:** HIGH - Prevents pattern from recurring in other file-generation subagents
**Problem Addressed:** This issue could occur with any subagent that writes files

**Proposed Solution:**
Apply source-tree.md validation pattern to ALL subagents that have Write/Edit tools.

**Affected Subagents:**
1. test-automator (addressed by REC-1)
2. story-requirements-analyst (generates requirements section)
3. api-designer (generates API specifications)
4. documentation-writer (generates documentation files)
5. refactoring-specialist (uses Edit tool)

**Implementation Pattern** (apply to each subagent):

**For each subagent in `.claude/agents/`:

A. Add to References section:
```markdown
- **Source Tree:** `devforgeai/context/source-tree.md` (file location constraints)
```

B. Add Pre-Generation Validation section BEFORE first Write() call:
```markdown
**Pre-Generation Validation:**

Read(file_path="devforgeai/context/source-tree.md")
Determine correct directory for output files
Validate all file_path parameters match source-tree.md constraints
```

**Testing Procedure:**

1. For each updated subagent:
   - Run existing test suite (if any)
   - Verify all tests pass
   - Confirm output files in correct locations per source-tree.md

**Effort Estimate:** 2-3 hours
- 20 minutes per subagent × 5 subagents = ~100 minutes
- Testing: 30 minutes
- Documentation: 30 minutes
- Total: 160 minutes (2.5 hours)

---

### REC-3: MEDIUM - Create subagent design guidance document
**Implemented in:** STORY-205

**Priority:** MEDIUM - Prevents future designers from making same mistake
**Problem Addressed:** Future subagent designers need clear guidance on which context files to validate

**Proposed Solution:**
Create architectural guidance document specifying which context files each subagent type should read before file operations.

**Implementation:**

**Option A: Create new file**
- File: `.claude/SUBAGENT-DESIGN-GUIDE.md`
- Include checklist of context files for each subagent type

**Option B: Add to existing README**
- File: `.claude/agents/README.md` (if exists)
- Add "Context File Validation" section

**Content to Create:**
```markdown
## Subagent Context File Validation Checklist

### For ALL subagents:
- Understand which context files are required
- Read them BEFORE any file/code generation operations

### For File-Generation Subagents (using Write/Edit tools):
- [ ] Read source-tree.md - Validate output file paths
- [ ] Read dependencies.md - Verify no forbidden dependencies
- [ ] Read tech-stack.md - Validate technology choices

### For Code-Generation Subagents:
- [ ] Read coding-standards.md - Follow code patterns
- [ ] Read architecture-constraints.md - Respect layer boundaries
- [ ] Read anti-patterns.md - Avoid forbidden patterns

### For Specification/Documentation Subagents:
- [ ] Read tech-stack.md - Aligned with locked technologies
- [ ] Read dependencies.md - No external packages (if framework component)
- [ ] Read source-tree.md - Correct file locations

### CRITICAL RULE: Before ANY Write() call:
ALWAYS read source-tree.md and validate:
- ✅ File path is in correct directory per source-tree.md
- ✅ Directory structure matches defined patterns
- ✅ No conflicting file locations

### Example:
```markdown
**Wrong (violates source-tree.md):**
```python
Write(file_path="tests/installer/test_version.py")
```

**Correct (respects source-tree.md):**
```python
# First, read source-tree.md
Read(file_path="devforgeai/context/source-tree.md")
# Then validate: installer modules go in installer/tests/
Write(file_path="installer/tests/test_version.py")
```
```

**Rationale:** Prevents future subagent designers from repeating this pattern. Creates single source of truth for context file requirements.

**Testing:** N/A (guidance document only, no code change)

**Effort Estimate:** 1-2 hours (documentation only)

---

### REC-4: MEDIUM - Update devforgeai-development skill to explicitly pass source-tree context
**Implemented in:** STORY-206

**Priority:** MEDIUM - Provides redundant validation (defense in depth)
**Problem Addressed:** The skill invoking test-automator doesn't provide explicit context about expected test location

**Proposed Solution:**
Add context marker in devforgeai-development skill Phase 1 that explicitly tells test-automator where tests should go (even though REC-1 requires test-automator to read it).

**Implementation:**

**File:** `.claude/skills/devforgeai-development/SKILL.md`
**Section:** Phase 1 (Red - Test First)
**Insertion Point:** Before invoking test-automator subagent
**Action:** Add explicit context marker

```markdown
### Step 1.X: Set Test Directory Context (Before test-automator invocation)

Read source-tree.md to determine expected test directory for the module:

```
Read(file_path="devforgeai/context/source-tree.md")

# Extract test directory for current module
IF module_path.startswith("installer/"):
    test_dir = "installer/tests/"
ELSE:
    test_dir = determine from source-tree.md
```

Set explicit context in conversation:

```
**Module Under Test:** {module_name}
**Expected Test Directory:** {test_dir} (per source-tree.md)
**Constraint:** All generated tests must be in {test_dir}
```

This context is now available to test-automator subagent.
```

**Rationale:** While REC-1 requires test-automator to validate independently, having the CALLING skill also read and provide context creates redundant validation (defense in depth). Two validation points are better than one.

**Testing:** Verify context markers appear in /dev command output

**Effort Estimate:** 20 minutes

---

## Prevention Strategy

### Short-Term (Immediate - Weeks 1-2)

1. **Implement REC-1** (CRITICAL)
   - Add source-tree.md validation to test-automator Phase 2
   - Test with STORY-077 retrofit (generate tests in correct location)
   - Verify STORY-078 QA validation passes

2. **Update test-automator references**
   - Add source-tree.md to References section
   - Create unit test validating test directory enforcement

### Long-Term (Weeks 3-4)

3. **Implement REC-2** (HIGH)
   - Audit all subagents with Write/Edit tools
   - Apply same validation pattern to each
   - Systematic fix prevents recurrence in other components

4. **Implement REC-3 & REC-4** (MEDIUM)
   - Create subagent design guidance
   - Update development skill context passing
   - Ensures future developers understand pattern

### Monitoring & Validation

**Watch For:**
- Test files appearing in wrong directories during QA
- Coverage tools reporting 0% for existing test code
- QA violations of source-tree.md constraints

**When to Audit:**
- Every sprint (check for constraint violations in new work)
- Before major releases (validate all artifacts comply)

**Escalation Criteria:**
- 2+ source-tree.md violations in same sprint → Review all file-generation subagents
- Any violation in released code → Root cause analysis required

---

## Implementation Checklist

- [ ] **REC-1:** Add Step 4.5 to test-automator.md: See STORY-203
- [ ] Test REC-1 with new test story
- [ ] Verify tests generate in correct installer/tests/ directory
- [ ] Update test-automator References section with source-tree.md
- [ ] **REC-2:** Audit 5 file-generation subagents: See STORY-204
- [ ] Apply source-tree.md validation to each
- [ ] Run existing tests for each subagent
- [ ] **REC-3:** Create subagent design guidance document: See STORY-205
- [ ] **REC-4:** Add context markers to devforgeai-development Phase 1: See STORY-206
- [ ] Manual testing: /dev with new story verifies context markers appear
- [ ] Commit all changes with message referencing RCA-017

---

## Related RCAs

- **RCA-006:** Autonomous deferrals (similar pattern of reactive vs proactive validation)
- **RCA-007:** Multi-file story creation (subagent behavior control)
- **RCA-009:** Skill execution incomplete (similar pattern of validation gaps)
- **RCA-016:** QA skill phase skipping (validation enforcement patterns)

---

## Appendix: Impact Analysis

### Why STORY-077 Created Tests in Wrong Location

STORY-077 development invoked test-automator subagent without:
1. Reading source-tree.md before test generation
2. Explicit validation of test directory location
3. Error checking before Write() call

test-automator, following inherited pattern from earlier stories (which also had this issue), defaulted to `tests/{module}/` pattern, resulting in `tests/installer/` instead of `installer/tests/`.

### Why STORY-078 QA Detected This

QA skill's coverage analysis ran ONLY `pytest installer/tests/` command, which:
1. Found tests in `installer/tests/` directory
2. Did NOT find tests in `tests/installer/` directory (separate directory)
3. Reported 0% coverage for version modules
4. Human investigation revealed duplicate test directories

This highlights the reactive nature of current validation: constraints are only enforced AFTER files created, not before.

### Framework Evolution Needed

Current framework: **Reactive constraint validation** (QA discovers violations)
Needed: **Proactive constraint enforcement** (violations prevented at source)

This RCA addresses that gap by making file-generation subagents validate constraints before Write() calls.

---

**RCA-017 Complete**
**Generated:** 2025-12-05
**Status:** ANALYSIS AND RECOMMENDATIONS COMPLETE
