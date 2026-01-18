# Troubleshooting: gaps.json Auto-Detection

This guide helps diagnose and resolve issues with the `/dev` command's automatic gaps.json detection feature (STORY-263).

---

## How Auto-Detection Works

When you run `/dev STORY-XXX`, the command automatically checks for a gaps.json file at:
```
devforgeai/qa/reports/STORY-XXX-gaps.json
```

If found, remediation mode is enabled automatically (same as passing `--fix` flag).

---

## Common Issues

### 1. Auto-Detection Not Triggering

**Symptom:** Running `/dev STORY-XXX` after a failed QA doesn't show the auto-detection banner.

**Possible Causes:**

| Cause | Diagnosis | Solution |
|-------|-----------|----------|
| File not in expected location | Run `Glob(pattern="devforgeai/qa/reports/STORY-XXX-gaps.json")` | Move file to correct location or check STORY_ID |
| Wrong STORY_ID format | Check if ID matches `STORY-NNN` pattern | Use exact ID from QA failure (preserve leading zeros) |
| Explicit `--fix` already passed | Check command invocation | Remove `--fix` flag to see auto-detection banner |
| Versioned file name | File named `STORY-XXX-gaps-v2.json` | Rename to canonical `STORY-XXX-gaps.json` |

**Verification:**
```bash
# Check if gaps file exists
ls devforgeai/qa/reports/STORY-XXX-gaps.json

# Check file content is valid JSON
cat devforgeai/qa/reports/STORY-XXX-gaps.json | jq .
```

---

### 2. Wrong Story Gets Remediation Mode

**Symptom:** Running `/dev STORY-007` triggers remediation for a different story.

**Cause:** STORY_ID mismatch between command and gaps file.

**Solution:**
1. Verify exact STORY_ID: `STORY-007` ≠ `STORY-7`
2. Check gaps file naming: Must be exact match (e.g., `STORY-007-gaps.json`)
3. Ensure only one gaps file exists for the story

---

### 3. Auto-Detection Banner Not Showing

**Symptom:** Remediation mode activates but no "Auto-detected gaps.json" banner appears.

**Cause:** You passed the `--fix` flag explicitly.

**Expected Behavior:**
- With `--fix` flag: Shows "Remediation mode enabled" (from Step 0.1)
- Without `--fix` flag + gaps.json exists: Shows "Auto-detected gaps.json - Remediation mode enabled" (from Step 0.3)

**Solution:** This is expected behavior. Explicit `--fix` takes priority over auto-detection.

---

### 4. Permission Denied Error

**Symptom:** Error accessing gaps.json file.

**Possible Causes:**
- File permissions too restrictive
- File locked by another process
- Antivirus blocking access

**Solution:**
```bash
# Check file permissions
ls -la devforgeai/qa/reports/STORY-XXX-gaps.json

# Fix permissions (if needed)
chmod 644 devforgeai/qa/reports/STORY-XXX-gaps.json
```

---

### 5. File Deleted Between Detection and Loading

**Symptom:** Auto-detection succeeds but Phase 01.9.5 fails to load gaps data.

**Cause:** gaps.json was deleted or moved after Step 0.3 detected it but before the skill loaded it.

**Solution:**
1. Re-run `/qa STORY-XXX` to regenerate the gaps file
2. Re-run `/dev STORY-XXX` immediately after QA completes

---

## Diagnostic Commands

### Check if gaps.json exists for a story
```
Glob(pattern="devforgeai/qa/reports/STORY-XXX-gaps.json")
```

### List all gaps files
```
Glob(pattern="devforgeai/qa/reports/*-gaps.json")
```

### View gaps file content
```
Read(file_path="devforgeai/qa/reports/STORY-XXX-gaps.json")
```

### Force remediation mode (bypass auto-detection)
```
/dev STORY-XXX --fix
```

---

## Expected Behavior Matrix

| Scenario | gaps.json exists? | --fix flag? | REMEDIATION_MODE | Banner |
|----------|-------------------|-------------|------------------|--------|
| Normal TDD | No | No | false | (none) |
| Auto-detect | Yes | No | true | "Auto-detected gaps.json..." |
| Explicit fix | No | Yes | true | "Remediation mode enabled" |
| Explicit fix + gaps | Yes | Yes | true | "Remediation mode enabled" (--fix priority) |

---

## Related Documentation

- `/dev` command: `.claude/commands/dev.md`
- QA gaps generation: `.claude/skills/devforgeai-qa/SKILL.md`
- Remediation workflow: `.claude/skills/devforgeai-development/references/qa-remediation-workflow.md`

---

## Change Log

| Date | Change |
|------|--------|
| 2026-01-17 | Initial creation (STORY-263) |
