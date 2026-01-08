# Test Specification Document: STORY-193

## Story Metadata
- **Story ID:** STORY-193
- **Title:** Consolidate Phase Marker Operations Reference File
- **Type:** Documentation (Markdown files, not executable code)
- **Output:** Test Specification Document (non-executable validation criteria)

---

## Validation Patterns by Acceptance Criteria

### AC-1: Reference File Created
**Validation:**
```bash
Glob(pattern=".claude/skills/devforgeai-qa/references/marker-operations.md")
```
**Pass Criteria:** File exists at specified path

---

### AC-2: Write Pattern Documented
**Validation:**
```bash
Grep(pattern="Write.*file_path.*marker", path=".claude/skills/devforgeai-qa/references/marker-operations.md")
Grep(pattern="## Write New Marker", path=".claude/skills/devforgeai-qa/references/marker-operations.md")
```
**Pass Criteria:** Section header exists; Write tool invocation pattern present

---

### AC-3: Verify Pattern Documented
**Validation:**
```bash
Grep(pattern="Glob.*pattern.*marker", path=".claude/skills/devforgeai-qa/references/marker-operations.md")
Grep(pattern="## Verify Marker", path=".claude/skills/devforgeai-qa/references/marker-operations.md")
```
**Pass Criteria:** Section header exists; Glob verification pattern present

---

### AC-4: Cleanup Pattern Documented
**Validation:**
```bash
Grep(pattern="(rm|Bash.*rm).*marker", path=".claude/skills/devforgeai-qa/references/marker-operations.md")
Grep(pattern="## Cleanup", path=".claude/skills/devforgeai-qa/references/marker-operations.md")
```
**Pass Criteria:** Section header exists; Bash rm cleanup pattern present

---

### AC-5: Write Tool Workaround Documented
**Validation:**
```bash
Grep(pattern="(prior Read|Read.*before|workaround)", path=".claude/skills/devforgeai-qa/references/marker-operations.md", "-i"=true)
```
**Pass Criteria:** Workaround explanation present in document

---

### AC-6: Referenced from SKILL.md
**Validation:**
```bash
Grep(pattern="marker-operations.md", path=".claude/skills/devforgeai-qa/SKILL.md")
```
**Pass Criteria:** Cross-reference to new file exists in SKILL.md

---

## Summary

| AC | Validation Method | Target File |
|----|-------------------|-------------|
| AC-1 | Glob (existence) | `marker-operations.md` |
| AC-2 | Grep (Write pattern) | `marker-operations.md` |
| AC-3 | Grep (Glob pattern) | `marker-operations.md` |
| AC-4 | Grep (rm pattern) | `marker-operations.md` |
| AC-5 | Grep (workaround) | `marker-operations.md` |
| AC-6 | Grep (reference) | `SKILL.md` |

**Test Type:** Structural validation (documentation story)
**Executable Tests:** None (Markdown output requires pattern matching, not unit tests)

---

## RED State Verification (Pre-Implementation)

- [x] AC-1: File does not exist - FAIL (expected)
- [x] AC-2: No Write pattern - FAIL (expected)
- [x] AC-3: No Glob pattern - FAIL (expected)
- [x] AC-4: No Cleanup pattern - FAIL (expected)
- [x] AC-5: No workaround text - FAIL (expected)
- [x] AC-6: No reference in SKILL.md - FAIL (expected)

**RED State Confirmed:** All validations fail as expected before implementation.
