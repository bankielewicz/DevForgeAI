# AC#3 Verification: Phase Boundary Markers in examples.md

**Story:** STORY-456
**AC:** AC#3 - Phase boundary markers and `<example>` tags in examples.md
**Target File:** `src/claude/skills/discovering-requirements/references/examples.md`
**Generated:** 2026-02-19
**TDD Phase:** RED (tests must FAIL against unmodified src/ files)

---

## Background

Current state (RED):
- examples.md is 320 lines
- No `<example>` or `</example>` tags exist (0 occurrences)
- No `---` section separators specifically separating the 3 phase examples

Required GREEN state:
- 3 sections separated by `---` markers
- Each section wrapped in `<example>` and `</example>` tags
- Phase 1 boundary: starts ~line 22, ends ~line 86 (discovery-session-saas example)
- Phase 2 boundary: starts ~line 89, ends ~line 231 (epic-decomposition-saas example)
- Phase 3 boundary: starts ~line 234, ends ~line 321 (complexity-scoring-saas example)

---

## Test Specification

### Test 1: At least 3 `<example>` opening tags exist

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/examples.md`

**Act:**
```bash
COUNT=$(grep -c "<example>" "$TARGET_FILE")
[ "$COUNT" -ge 3 ]
```

**Assert:** Exit code 0 (3 or more `<example>` tags found)

**Expected RED failure:** File currently has 0 `<example>` tags.

---

### Test 2: At least 3 `</example>` closing tags exist

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/examples.md`

**Act:**
```bash
COUNT=$(grep -c "</example>" "$TARGET_FILE")
[ "$COUNT" -ge 3 ]
```

**Assert:** Exit code 0 (3 or more `</example>` closing tags found)

**Expected RED failure:** File currently has 0 `</example>` tags.

---

### Test 3: Opening and closing `<example>` tags are balanced (equal counts)

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/examples.md`

**Act:**
```bash
OPEN=$(grep -c "<example>" "$TARGET_FILE")
CLOSE=$(grep -c "</example>" "$TARGET_FILE")
[ "$OPEN" -eq "$CLOSE" ]
```

**Assert:** Exit code 0 (counts are equal)

**Expected RED failure:** Both counts are 0, so they are technically equal - but Test 1 and 2 will already catch the RED state. This test validates structural integrity in GREEN state.

---

### Test 4: At least 2 `---` section separator markers exist

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/examples.md`

**Act:**
```bash
COUNT=$(grep -cE "^---$" "$TARGET_FILE")
[ "$COUNT" -ge 2 ]
```

**Assert:** Exit code 0 (2 or more `---` separators found)

**Expected RED failure:** File currently lacks the required section separator `---` markers between the 3 example sections.

---

### Test 5: Phase 1 example tag appears before line 90 (discovery-session-saas near line 22)

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/examples.md`

**Act:**
```bash
# Check that an <example> tag appears within first 90 lines
head -90 "$TARGET_FILE" | grep -q "<example>"
```

**Assert:** Exit code 0 (`<example>` found in first 90 lines)

**Expected RED failure:** No `<example>` tags exist in the file.

---

### Test 6: Phase 2 example tag appears between lines 85-235 (epic-decomposition-saas near line 89)

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/examples.md`

**Act:**
```bash
# Extract lines 85-235 and check for <example> tag
sed -n '85,235p' "$TARGET_FILE" | grep -q "<example>"
```

**Assert:** Exit code 0 (`<example>` found in Phase 2 region)

**Expected RED failure:** No `<example>` tags exist in the file.

---

### Test 7: Phase 3 example tag appears after line 230 (complexity-scoring-saas near line 234)

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/examples.md`

**Act:**
```bash
# Extract lines after 230 and check for <example> tag
tail -n +230 "$TARGET_FILE" | grep -q "<example>"
```

**Assert:** Exit code 0 (`<example>` found after line 230)

**Expected RED failure:** No `<example>` tags exist in the file.

---

### Test 8: File contains "discovery-session" keyword (Phase 1 example content marker)

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/examples.md`

**Act:**
```bash
grep -qi "discovery-session" "$TARGET_FILE"
```

**Assert:** Exit code 0 (Phase 1 example content present)

**Expected GREEN state:** This validates the Phase 1 example content exists. May already exist in current file.

---

### Test 9: File contains "epic-decomposition" keyword (Phase 2 example content marker)

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/examples.md`

**Act:**
```bash
grep -qi "epic-decomposition" "$TARGET_FILE"
```

**Assert:** Exit code 0 (Phase 2 example content present)

**Expected GREEN state:** This validates the Phase 2 example content exists. May already exist in current file.

---

### Test 10: File contains "complexity-scoring" keyword (Phase 3 example content marker)

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/examples.md`

**Act:**
```bash
grep -qi "complexity-scoring" "$TARGET_FILE"
```

**Assert:** Exit code 0 (Phase 3 example content present)

**Expected GREEN state:** This validates the Phase 3 example content exists. May already exist in current file.

---

### Test 11: File line count is 320 or more (no deletions)

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/examples.md`
- Baseline: 320 lines

**Act:**
```bash
LINE_COUNT=$(wc -l < "$TARGET_FILE")
[ "$LINE_COUNT" -ge 320 ]
```

**Assert:** Exit code 0 (line count >= 320, additions only)

**Expected GREEN state:** File must retain all 320 original lines plus new `<example>` tags and `---` separators.

---

## AC#3 GREEN Criteria Summary

All tests pass when:
1. Exactly 3 `<example>` opening tags and 3 `</example>` closing tags exist (balanced)
2. At least 2 `---` section separator markers exist between the 3 examples
3. First `<example>` appears within lines 1-90 (Phase 1 / discovery-session example)
4. A `<example>` appears between lines 85-235 (Phase 2 / epic-decomposition example)
5. A `<example>` appears after line 230 (Phase 3 / complexity-scoring example)
6. File line count >= 320 (no deletions)

## Phase Boundary Reference

| Phase | Content | Start Line | End Line |
|-------|---------|-----------|---------|
| Phase 1 | discovery-session-saas | ~22 | ~86 |
| Phase 2 | epic-decomposition-saas | ~89 | ~231 |
| Phase 3 | complexity-scoring-saas | ~234 | ~321 |
