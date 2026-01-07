# STORY-231 Test Coverage Remediation Plan

**Date:** 2026-01-05
**Current Status:** In Development (should be downgraded from "Dev Complete")
**Test Pass Rate:** 24/42 (57%)
**Target:** 42/42 (100%)

---

## Executive Summary

STORY-231 has partial implementation with 2 of 3 acceptance criteria fully tested and working (AC#2, AC#3). However, AC#1 is only 59% complete, with critical anti-pattern categories untested. This document provides a prioritized plan to close the 18 failing tests and achieve full Dev Complete status.

**Estimated Effort:** 2-3 hours of focused development work

---

## Priority 1: Critical AC#1 Implementation (4-6 hours)

### Gap 1a: Assumption Detection (Category 3) - 4 Failing Tests

**What's Failing:**
- Test 1.1: Detect "Install Redis" without AskUserQuestion
- Test 1.2: NOT flag AskUserQuestion usage as violation
- Test 1.3: Detect "Use PostgreSQL" assumption
- Test 1.4: Detect "Using React" assumption

**Root Cause:** Assumption detection logic NOT implemented in session-miner.md

**Implementation Required:**

1. **Add assumption pattern matching to session-miner.md** (after line 1176)

```markdown
### Category 3 Pattern Matching Implementation

Add assumption detection patterns:

ASSUMPTION_PATTERNS = [
  # Technology installations without tech-stack.md consultation
  r"Install\s+(Redis|Memcached|Elasticsearch|MongoDB|PostgreSQL|MySQL|MariaDB|Oracle)",
  r"(Use|Using|Adopt|Implement)\s+(PostgreSQL|MySQL|MongoDB|Redis|React|Vue|Angular|Django|Flask|FastAPI)",

  # Framework choices without AskUserQuestion
  r"Build\s+with\s+(React|Vue|Angular|Next\.js|Svelte|Django|Flask|FastAPI|ASP\.NET|Spring)",
  r"Using\s+(EF Core|Sequelize|SQLAlchemy|TypeORM|Prisma|TypeScript)",

  # Architecture choices without consultation
  r"Implement\s+(microservices|monolith|serverless|event-driven|CQRS)",
  r"Use\s+(gRPC|GraphQL|REST|SOAP|WebSocket)",
]

FUNCTION detect_assumption(user_input, entry_context):
  # Check if AskUserQuestion was used
  IF "AskUserQuestion" in entry_context:
    RETURN false  # Not a violation if user was asked

  # Check for assumption patterns
  FOR pattern in ASSUMPTION_PATTERNS:
    IF pattern_matches(user_input, pattern):
      # Verify no explicit user decision documented
      IF NOT contains_user_decision_marker(user_input):
        RETURN true  # Violation detected

  RETURN false
```

2. **Add exception rule for AskUserQuestion usage:**

```markdown
### Exception Rule: Justified Technology Decisions

A technology choice is NOT an assumption if:
- User was consulted via AskUserQuestion
- Documentation shows explicit decision rationale
- Context contains approved decision markers
```

3. **Update category matching function to call assumption detector:**

Line 1115-1131 (match_anti_patterns function) needs:
```
IF category_id == 3:
  IF detect_assumption(user_input, context):
    violations.append(...)
```

4. **Testing validation:**

Run individual test:
```bash
bash tests/STORY-231/unit/test_antipattern_matching_assumptions.sh
# Expected: All 4 tests PASSING
```

---

### Gap 1b: Size Violation Detection (Category 4) - 4 Failing Tests

**What's Failing:**
- Test 1.1: Detect SKILL.md exceeding 1000 lines
- Test 1.2: Detect command file exceeding 500 lines
- Test 1.3: Detect monolithic skill (ideation+architecture+dev combined)
- Test 1.4: NOT flag valid size (600 lines) as violation

**Root Cause:** Size violation detection logic NOT implemented

**Implementation Required:**

1. **Add size violation detection to session-miner.md** (after assumption section)

```markdown
### Category 4: Size Violation Detection

SIZE_VIOLATION_PATTERNS = {
  # SKILL files should not exceed 1000 lines (Phase 1 recommendation)
  "skill_file": {
    "pattern": r"(SKILL\.md|\.md.*skill)",
    "max_lines": 1000,
    "severity": "high"
  },

  # Command files should not exceed 500 lines (RCA-007)
  "command_file": {
    "pattern": r"(commands|COMMAND).*\.md",
    "max_lines": 500,
    "severity": "high"
  },

  # Agent/Subagent definitions should not exceed 800 lines
  "agent_file": {
    "pattern": r"(agents?|subagents?)/.*\.md",
    "max_lines": 800,
    "severity": "high"
  },

  # Monolithic skills combining multiple phases
  "monolithic_skill": {
    "pattern": r"(ideation.*architecture|architecture.*development|dev.*qa|qa.*release)",
    "violation": "combining_phases",
    "severity": "high"
  }
}

FUNCTION detect_size_violation(user_input):
  # Extract file references
  files_mentioned = extract_file_references(user_input)

  FOR file_ref in files_mentioned:
    file_type = classify_file_type(file_ref)

    # Get line count from context
    line_count = get_line_count(file_ref)

    # Check against thresholds
    IF file_type in SIZE_VIOLATION_PATTERNS:
      threshold = SIZE_VIOLATION_PATTERNS[file_type].max_lines
      IF line_count > threshold:
        RETURN {
          "violation": true,
          "file": file_ref,
          "lines": line_count,
          "threshold": threshold,
          "severity": SIZE_VIOLATION_PATTERNS[file_type].severity
        }

  # Check for monolithic pattern (combining multiple phases)
  IF "ideation" in user_input AND "architecture" in user_input AND "development" in user_input:
    IF in_single_file(user_input):
      RETURN {
        "violation": true,
        "type": "monolithic",
        "severity": "high"
      }

  RETURN null
```

2. **Update category matching function:**

Line 1115-1131 (match_anti_patterns) needs:
```
IF category_id == 4:
  violation = detect_size_violation(user_input)
  IF violation:
    violations.append(...)
```

3. **Testing validation:**

Run individual test:
```bash
bash tests/STORY-231/unit/test_antipattern_matching_size_violations.sh
# Expected: All 4 tests PASSING
```

---

## Priority 2: Exception Handling Implementation (2-3 hours)

### Gap 2a: Legitimate Bash Exceptions (Edge Cases E.1-E.2) - 2 Failing Tests

**What's Failing:**
- Test E.1: npm test NOT flagged as violation
- Test E.2: git commit NOT flagged as violation

**Current Issue:** Exception rule exists (lines 1141-1176) but not enforced

**Implementation Required:**

1. **Verify exception rule is being called in pattern matching:**

Line 1123 in pattern_matches function should check:
```python
IF NOT is_legitimate_exception(user_input, category_id):
  violations.append(...)
```

2. **Enhance exception list** (lines 1141-1176):

Current rules are incomplete. Extend to include:
```markdown
| `Bash(command="npm test")` | Test execution | Contains `test` or `pytest` or `dotnet test` |
| `Bash(command="npm run")` | Build/scripts | Contains `build`, `compile`, `deploy`, `publish` |
| `Bash(command="pip install")` | Package mgmt | Starts with `pip`, `npm`, `yarn`, `pnpm` |
| `Bash(command="docker build")` | Container ops | Starts with `docker `, `kubectl ` |
| `Bash(command="git commit")` | Version control | Starts with `git `, `svn `, `hg ` |
```

3. **Testing validation:**

Run edge case tests:
```bash
bash tests/STORY-231/edge-cases/test_antipattern_edge_cases.sh
# Expected: Tests E.1, E.2 should PASS
```

---

### Gap 2b: Case-Insensitive Matching (Edge Case E.4) - 1 Failing Test

**What's Failing:**
- Test E.4: Pattern matching is case-insensitive

**Root Cause:** normalize_input function (lines 1133-1139) exists but may not be applied consistently

**Implementation Required:**

1. **Verify normalization is applied in all pattern matching:**

Every pattern match should use:
```python
input_normalized = normalize_input(user_input)  # Converts to lowercase
RETURN pattern_lower in input_normalized
```

2. **Test case validation:**

```bash
# Should ALL match and be flagged as violations:
Bash(command="CAT file")
Bash(command="cat file")
Bash(command="Cat file")
```

3. **Testing validation:**

```bash
bash tests/STORY-231/edge-cases/test_antipattern_edge_cases.sh
# Expected: Test E.4 should PASS
```

---

### Gap 2c: Long Input Truncation (Edge Case E.5) - 1 Failing Test

**What's Failing:**
- Test E.5: Inputs > 10000 chars truncated safely

**Root Cause:** Truncation logic exists (line 1136) but not tested

**Implementation Required:**

The normalize_input function already handles this:
```python
IF len(normalized) > 10000:
  normalized = normalized[:10000]
```

Just verify it's being called for all inputs:

1. **Test validation:**

```bash
# Should truncate safely without errors:
LONG_INPUT=$(python3 -c "print('x' * 15000)")
# Should truncate to 10000 chars and continue processing
```

2. **Testing validation:**

```bash
bash tests/STORY-231/edge-cases/test_antipattern_edge_cases.sh
# Expected: Test E.5 should PASS
```

---

## Priority 3: Advanced Edge Cases Implementation (1-2 hours)

### Gap 3a: Context-Aware Matching (Edge Case E.7) - 1 Failing Test

**What's Failing:**
- Test E.7: "Bash" inside quotes NOT flagged as violation

**Example:**
```
"The anti-patterns.md mentions Bash(command=...) as a violation"
```

Should NOT be flagged because "Bash" is in a documentation reference, not actual code.

**Implementation Required:**

1. **Enhance is_false_positive_context function** (lines 1199-1222):

```markdown
FUNCTION is_false_positive_context(user_input, matched_pattern):
  input_lower = user_input.lower()

  # Documentation references (NOT violations)
  documentation_markers = [
    "documentation says",
    "anti-patterns.md mentions",
    "example:",
    "like:",
    "shows:",
    "from the spec",
    "quoted",
    "contains:"
  ]

  FOR marker in documentation_markers:
    IF marker in input_lower:
      # Check if pattern is in quotes after marker
      IF pattern_in_quotes_after_marker(input_lower, matched_pattern, marker):
        RETURN true

  # Check if pattern is in triple-quoted code block
  IF in_code_block(user_input, matched_pattern):
    RETURN true

  RETURN false
```

2. **Testing validation:**

```bash
bash tests/STORY-231/edge-cases/test_antipattern_edge_cases.sh
# Expected: Test E.7 should PASS
```

---

### Gap 3b: Multiple Violations Detection (Edge Case E.3) - 1 Failing Test

**What's Failing:**
- Test E.3: Multiple violations in single entry counted separately

**Example:**
```
Bash(command="cat /home/user/file.md")
```

Should detect TWO violations:
1. Category 1: bash_for_file_ops (cat command)
2. Category 10: hardcoded_paths (/home/user/ path)

**Implementation Required:**

The loop already handles this (lines 1120-1131):
```python
FOR category_id in [1..10]:
  FOR pattern in PATTERNS[category_id]:
    IF pattern_matches(...):
      violations.append(...)  # Appends each violation
```

Just verify both violations are being appended:

1. **Test validation:**

The current implementation should handle this. If failing, check:
- Are all 10 category patterns being checked?
- Is each violation being appended to the array?

2. **Testing validation:**

```bash
bash tests/STORY-231/edge-cases/test_antipattern_edge_cases.sh
# Expected: Test E.3 should PASS
```

---

### Gap 3c: Unicode Handling (Edge Case E.6) - 1 Failing Test

**What's Failing:**
- Test E.6: Unicode content in user_input handled correctly

**Example:**
```
Bash(command="cat файл.txt")  # Russian word for "file"
```

Should still be detected as violation.

**Implementation Required:**

Python's built-in string operations handle Unicode by default. Verify:

1. **Pattern matching works with Unicode:**

```python
# This should work automatically in Python 3
pattern = "bash"
input_text = "Bash(command='cat файл.txt')"
match = pattern.lower() in input_text.lower()  # Should be True
```

2. **Test validation:**

If test still fails, ensure:
- No ASCII-only regex being used
- Unicode is preserved through normalize_input()
- No encoding/decoding issues

3. **Testing validation:**

```bash
bash tests/STORY-231/edge-cases/test_antipattern_edge_cases.sh
# Expected: Test E.6 should PASS
```

---

### Gap 3d: Advanced Pattern Detection (Edge Cases E.9-E.10) - 2 Failing Tests

**What's Failing:**
- Test E.9: Circular dependency pattern detected
- Test E.10: Missing frontmatter pattern detected

**Root Cause:** These are special patterns not in standard Category 1-4 logic

**Implementation Required:**

1. **Circular Dependency Detection (Category 7):**

```markdown
PATTERN_CIRCULAR = [
  r"A\s*→\s*B\s*→\s*A",
  r"calls\s+.*which calls.*which calls.*which calls",
  r"circular\s+(import|require|depend|reference)"
]

FUNCTION detect_circular_dependency(user_input):
  FOR pattern in PATTERN_CIRCULAR:
    IF pattern_matches(user_input, pattern):
      RETURN true
  RETURN false
```

2. **Missing Frontmatter Detection (Category 9):**

```markdown
PATTERN_MISSING_FRONTMATTER = [
  r"no\s+frontmatter",
  r"no\s+YAML",
  r"missing\s+---",
  r"without\s+frontmatter"
]

FUNCTION detect_missing_frontmatter(user_input):
  FOR pattern in PATTERN_MISSING_FRONTMATTER:
    IF pattern_matches(user_input, pattern):
      RETURN true
  RETURN false
```

3. **Update category matching to include these:**

Lines 1120-1131 should check all 10 categories.

---

## Implementation Checklist

### Phase 1: Critical Categories (AC#1 Completion)
- [ ] Implement Category 3 assumption detection
  - [ ] Pattern list defined
  - [ ] AskUserQuestion exception rule
  - [ ] Update match_anti_patterns function
  - [ ] Run test_antipattern_matching_assumptions.sh
  - [ ] Verify: 4/4 tests passing

- [ ] Implement Category 4 size violation detection
  - [ ] Pattern thresholds defined
  - [ ] Monolithic skill detection
  - [ ] Update match_anti_patterns function
  - [ ] Run test_antipattern_matching_size_violations.sh
  - [ ] Verify: 4/4 tests passing

**Checkpoint 1 Success:** All AC#1 tests passing (13/13)

### Phase 2: Exception Handling & Edge Cases
- [ ] Enhance legitimate Bash exceptions list
  - [ ] Add npm, git, docker, kubectl patterns
  - [ ] Update exception rules
  - [ ] Run edge case tests E.1-E.2
  - [ ] Verify: 2/2 tests passing

- [ ] Implement case-insensitive matching verification
  - [ ] Confirm normalize_input used consistently
  - [ ] Run edge case test E.4
  - [ ] Verify: 1/1 test passing

- [ ] Verify long input truncation
  - [ ] Test truncation at 10000 chars
  - [ ] Run edge case test E.5
  - [ ] Verify: 1/1 test passing

- [ ] Implement context-aware matching
  - [ ] Add documentation detection
  - [ ] Add code block detection
  - [ ] Run edge case test E.7
  - [ ] Verify: 1/1 test passing

**Checkpoint 2 Success:** All edge cases except special patterns passing (6/10)

### Phase 3: Advanced Patterns
- [ ] Implement multiple violation detection
  - [ ] Verify all 10 categories checked per entry
  - [ ] Run edge case test E.3
  - [ ] Verify: 1/1 test passing

- [ ] Implement Unicode handling
  - [ ] Test with non-ASCII characters
  - [ ] Run edge case test E.6
  - [ ] Verify: 1/1 test passing

- [ ] Implement circular dependency detection
  - [ ] Pattern definitions
  - [ ] Detection logic
  - [ ] Run edge case test E.9
  - [ ] Verify: 1/1 test passing

- [ ] Implement missing frontmatter detection
  - [ ] Pattern definitions
  - [ ] Detection logic
  - [ ] Run edge case test E.10
  - [ ] Verify: 1/1 test passing

**Checkpoint 3 Success:** All edge case tests passing (10/10)

### Final Validation
- [ ] Run full test suite:
  ```bash
  bash tests/STORY-231/run_all_tests.sh
  ```
  - [ ] Expected: 42/42 tests PASSING
  - [ ] No FAIL results
  - [ ] Summary shows 100% pass rate

- [ ] Update story file:
  - [ ] Fix implementation claims (if any were overstated)
  - [ ] Verify status is accurate
  - [ ] Add changelog entry for remediation

- [ ] Commit changes:
  ```bash
  git add .
  git commit -m "fix(STORY-231): Complete anti-pattern mining implementation

  - Implement Category 3 assumption detection
  - Implement Category 4 size violation detection
  - Add comprehensive exception handling
  - Implement all edge case robustness checks

  All 42 tests now passing (100%)"
  ```

---

## Success Criteria

| Item | Target | Current | Status |
|------|--------|---------|--------|
| Total Tests | 42 | 42 | ✓ |
| Passing Tests | 42 | 24 | ✗ Need +18 |
| AC#1 Tests | 13 | 5 | ✗ Need +8 |
| AC#2 Tests | 6 | 6 | ✓ |
| AC#3 Tests | 7 | 7 | ✓ |
| Integration Tests | 6 | 6 | ✓ |
| Edge Case Tests | 10 | 0 | ✗ Need +10 |
| Pass Rate | 100% | 57% | ✗ Need +43% |

---

## Time Estimation

| Phase | Task | Est. Time |
|-------|------|-----------|
| 1 | Implement Category 3 (Assumptions) | 45 minutes |
| 1 | Implement Category 4 (Size Violations) | 45 minutes |
| 2 | Exception handling & basic edge cases | 30 minutes |
| 3 | Advanced pattern detection | 30 minutes |
| Validation | Full test suite + cleanup | 15 minutes |
| **Total** | **All implementation** | **2.5 hours** |

---

## References

- Test file: `/mnt/c/Projects/DevForgeAI2/tests/STORY-231/run_all_tests.sh`
- Implementation file: `/mnt/c/Projects/DevForgeAI2/.claude/agents/session-miner.md` (lines 1007-1834)
- Specification: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/anti-patterns.md`

---

**Next Steps:** Begin Phase 1 implementation immediately to restore test pass rate to 100% and achieve valid Dev Complete status.

