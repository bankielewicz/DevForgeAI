# AC#2 Verification: Per-Phase examples.md Loading in SKILL.md

**Story:** STORY-456
**AC:** AC#2 - Per-phase deferred loading of examples.md in SKILL.md
**Target File:** `src/claude/skills/discovering-requirements/SKILL.md`
**Generated:** 2026-02-19
**TDD Phase:** RED (tests must FAIL against unmodified src/ files)

---

## Background

Current state (RED):
- SKILL.md line 88 contains a single upfront `Read(file_path=".claude/skills/discovering-requirements/references/examples.md")` with no offset/limit
- No per-phase Read() calls with offset/limit parameters exist for examples.md
- SKILL.md is currently 409 lines

Required GREEN state:
- Single upfront load at line 88 replaced with per-phase Read() calls
- Phase 1 section contains Read() with offset/limit targeting lines 1-86 of examples.md
- Phase 2 section contains Read() with offset/limit targeting lines 87-231 of examples.md
- Phase 3 section contains Read() with offset/limit targeting lines 232-321 of examples.md
- SKILL.md remains under 500 lines

---

## Test Specification

### Test 1: Phase 1 section contains Read() with offset referencing examples.md lines ~1-86

**Arrange:**
- File: `src/claude/skills/discovering-requirements/SKILL.md`
- Search context: Phase 1 section (lines between "Phase 1" and "Phase 2" headers)

**Act:**
```bash
# Extract Phase 1 section and check for Read() with offset near line 1 of examples.md
grep -A 50 "### Phase 1:" "$TARGET_FILE" | grep -q "examples.md.*offset"
```

**Assert:** Exit code 0 (per-phase load instruction found in Phase 1)

**Expected RED failure:** No offset-based Read() calls exist for examples.md in SKILL.md.

---

### Test 2: Phase 1 Read() specifies limit targeting ~line 86

**Arrange:**
- File: `src/claude/skills/discovering-requirements/SKILL.md`

**Act:**
```bash
grep -A 50 "### Phase 1:" "$TARGET_FILE" | grep -qE "examples\.md.*limit.*(8[0-9]|9[0-9])"
```

**Assert:** Exit code 0 (limit value around 86 found in Phase 1 context)

**Expected RED failure:** No limit-based Read() calls for examples.md exist.

---

### Test 3: Phase 2 section contains Read() with offset referencing examples.md lines ~87-231

**Arrange:**
- File: `src/claude/skills/discovering-requirements/SKILL.md`
- Search context: Phase 2 section

**Act:**
```bash
grep -A 50 "### Phase 2:" "$TARGET_FILE" | grep -q "examples.md.*offset"
```

**Assert:** Exit code 0 (per-phase load instruction found in Phase 2)

**Expected RED failure:** No offset-based Read() calls exist for examples.md in SKILL.md.

---

### Test 4: Phase 2 Read() offset is ~87

**Arrange:**
- File: `src/claude/skills/discovering-requirements/SKILL.md`

**Act:**
```bash
grep -A 50 "### Phase 2:" "$TARGET_FILE" | grep -qE "examples\.md.*offset.*(8[5-9]|9[0-5])"
```

**Assert:** Exit code 0 (offset value around 87 found in Phase 2 context)

**Expected RED failure:** No offset-based Read() calls for examples.md exist.

---

### Test 5: Phase 3 section contains Read() with offset referencing examples.md lines ~232-321

**Arrange:**
- File: `src/claude/skills/discovering-requirements/SKILL.md`
- Search context: Phase 3 section

**Act:**
```bash
grep -A 50 "### Phase 3:" "$TARGET_FILE" | grep -q "examples.md.*offset"
```

**Assert:** Exit code 0 (per-phase load instruction found in Phase 3)

**Expected RED failure:** No offset-based Read() calls exist for examples.md in SKILL.md.

---

### Test 6: Phase 3 Read() offset is ~232

**Arrange:**
- File: `src/claude/skills/discovering-requirements/SKILL.md`

**Act:**
```bash
grep -A 50 "### Phase 3:" "$TARGET_FILE" | grep -qE "examples\.md.*offset.*(23[0-5])"
```

**Assert:** Exit code 0 (offset value around 232 found in Phase 3 context)

**Expected RED failure:** No offset-based Read() calls for examples.md exist.

---

### Test 7: Single upfront load of examples.md at line 88 is removed

**Arrange:**
- File: `src/claude/skills/discovering-requirements/SKILL.md`

**Act:**
```bash
# The old single upfront load should not exist
# It matched: Read(file_path=".claude/skills/discovering-requirements/references/examples.md")
# without offset/limit parameters
grep -v "offset" "$TARGET_FILE" | grep -v "limit" | grep -qF 'Read(file_path=".claude/skills/discovering-requirements/references/examples.md")'
```

**Assert:** Exit code 1 (unqualified single upfront load is GONE)

**Expected RED failure (inverted):** The old single upfront load currently EXISTS at line 88. This test currently PASSES (exit 0 finds it), but the assertion expects exit 1, so the overall test FAILS.

**Note:** This test uses inverted logic - it FAILS when the old load exists (RED state) and PASSES when it is removed (GREEN state).

---

### Test 8: SKILL.md line count is under 500

**Arrange:**
- File: `src/claude/skills/discovering-requirements/SKILL.md`
- Current baseline: 409 lines

**Act:**
```bash
LINE_COUNT=$(wc -l < "$TARGET_FILE")
[ "$LINE_COUNT" -lt 500 ]
```

**Assert:** Exit code 0 (line count < 500)

**Expected GREEN state:** This test currently passes (409 < 500). It must remain passing after implementation to confirm no excessive content was added.

---

### Test 9: Three separate offset-based Read() calls for examples.md exist in SKILL.md

**Arrange:**
- File: `src/claude/skills/discovering-requirements/SKILL.md`

**Act:**
```bash
COUNT=$(grep -c "examples\.md.*offset" "$TARGET_FILE")
[ "$COUNT" -ge 3 ]
```

**Assert:** Exit code 0 (3 or more offset-based loads found)

**Expected RED failure:** Currently 0 offset-based Read() calls for examples.md exist.

---

## AC#2 GREEN Criteria Summary

All tests pass when:
1. Phase 1 section has `Read(...examples.md...offset=0...limit=86)` (or similar ~lines 1-86)
2. Phase 2 section has `Read(...examples.md...offset=87...limit=145)` (or similar ~lines 87-231)
3. Phase 3 section has `Read(...examples.md...offset=232...limit=90)` (or similar ~lines 232-321)
4. Old single upfront load (no offset) removed from line 88
5. SKILL.md total lines < 500
