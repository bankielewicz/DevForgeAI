# STORY-142: Quick Reference Guide
## Replace Bash mkdir with Write/.gitkeep Pattern

**For Developers:** Quick validation and pattern reference

---

## Pattern at a Glance

**Instead of:**
```python
Bash(command="mkdir -p devforgeai/specs/Epics/")
```

**Use:**
```python
Write(file_path="devforgeai/specs/Epics/.gitkeep", content="")
```

---

## Validation Tests

### AC#2: Zero Bash mkdir Pattern

Run this to validate:
```bash
grep -r "Bash.*mkdir" .claude/commands/ideate.md \
  .claude/skills/devforgeai-ideation/SKILL.md \
  .claude/skills/devforgeai-ideation/references/artifact-generation.md \
  .claude/skills/devforgeai-ideation/references/error-handling.md
```

**Expected Result:** No output (zero matches)

---

## Implementation Locations

| File | Phase | Lines | Status |
|------|-------|-------|--------|
| artifact-generation.md | 6.1 Epic Gen | 470 | IMPLEMENTED |
| artifact-generation.md | 6.3 Transition | 599-600 | IMPLEMENTED |
| error-handling.md | Error 6 Rec | 184, 868 | IMPLEMENTED |

---

## Pattern Variants

### Direct Path
```python
Write(file_path="devforgeai/specs/Epics/.gitkeep", content="")
```

### Dynamic Path
```python
Write(file_path=f"{dir}.gitkeep", content="")
```

### Multiple Directories
```python
Write(file_path="devforgeai/specs/Epics/.gitkeep", content="")
Write(file_path="devforgeai/specs/requirements/.gitkeep", content="")
```

---

## Key Points

1. **Content:** Always use empty string `content=""`
2. **Idempotent:** Safe to call multiple times to same path
3. **Git-Friendly:** .gitkeep files enable version control tracking
4. **Constitutional:** Complies with C1 requirement (native tools over Bash)

---

## Related Files

- **Story:** STORY-142-replace-bash-mkdir-with-write-gitkeep.story.md
- **Report:** STORY-142-INTEGRATION-VALIDATION-REPORT.md
- **Tech Stack:** devforgeai/specs/context/tech-stack.md (C1 requirement)

---

## AC Validation Matrix

| AC | Status | Evidence |
|----|---------|---------|
| AC#1 | PASS | 3 Write/.gitkeep patterns in artifact-generation.md |
| AC#2 | PASS | 0 matches for Bash.*mkdir in all files |
| AC#3 | PASS | .gitkeep files with empty content correctly specified |
| AC#4 | PASS | Ready for context-validator C1 compliance check |

---

**For Full Details:** See STORY-142-INTEGRATION-VALIDATION-REPORT.md
