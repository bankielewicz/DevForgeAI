---
description: Test argument validation with AskUserQuestion for malformed inputs
model: haiku
allowed-tools: AskUserQuestion, Glob
---

# Test: Argument Validation Pattern

This test validates Phase 0 argument validation logic across various malformed inputs.

## Test Purpose

Verify that argument validation:
1. Catches malformed story IDs
2. Handles flag syntax gracefully
3. Educates users on correct syntax
4. Provides helpful recovery options
5. Uses AskUserQuestion for clarification

## Test Scenarios

### Scenario 1: Lowercase Story ID

**Input:** `story-001` (should be `STORY-001`)

**Expected Behavior:**
```
AskUserQuestion triggered:
  Question: "Story ID 'story-001' doesn't match format STORY-NNN. What story should I process?"
  Options:
    - "Try to extract STORY-NNN from: story-001"
    - "List all available stories"
    - "Show correct format examples"
```

**Expected Recovery:** Extract to `STORY-001`

---

### Scenario 2: Flag Syntax (--mode=)

**Input:** `STORY-001 --mode=deep`

**Expected Behavior:**
```
Story ID: STORY-001 ✓ (valid)

Parse mode:
  Detected flag syntax: --mode=deep
  Extract: deep
  Note to user: "Flag syntax (--mode=) not needed. Use: /qa STORY-001 deep"

Mode: deep ✓ (extracted and user educated)
```

**Expected Recovery:** Parse correctly, educate user

---

### Scenario 3: Unknown Flag

**Input:** `STORY-001 --unknown-flag`

**Expected Behavior:**
```
Story ID: STORY-001 ✓ (valid)

AskUserQuestion triggered:
  Question: "Unknown flag: --unknown-flag. Which [mode/environment]?"
  Options:
    - [Appropriate options for command]

  Note: "Flags not needed. Use: /[command] STORY-001 [value]"
```

**Expected Recovery:** Ask user for intent, educate on syntax

---

### Scenario 4: Story Not Found

**Input:** `STORY-999` (doesn't exist)

**Expected Behavior:**
```
Story ID: STORY-999 ✓ (valid format)

Glob: .ai_docs/Stories/STORY-999*.story.md
Result: No matches ✗

AskUserQuestion triggered:
  Question: "Story STORY-999 not found. What should I do?"
  Options:
    - "List all available stories"
    - "Create STORY-999 (run /create-story first)"
    - "Cancel command"
```

**Expected Recovery:** User selects from available stories or cancels

---

### Scenario 5: Missing Story ID

**Input:** `--mode=deep` (no story ID)

**Expected Behavior:**
```
Story ID: --mode=deep (starts with --, not valid)

AskUserQuestion triggered:
  Question: "Story ID '--mode=deep' doesn't match format. Missing story ID?"
  Options:
    - "List stories in [status]"
    - "Show correct syntax"
    - "Cancel command"
```

**Expected Recovery:** User provides correct story ID

---

### Scenario 6: Multiple Arguments

**Input:** `STORY-001 deep extra-arg unwanted-stuff`

**Expected Behavior:**
```
Story ID: STORY-001 ✓ (valid, from $1)
Mode: deep ✓ (valid, from $2)

Extra arguments detected: $3, $4, ...

AskUserQuestion (optional):
  Question: "Extra arguments detected. Ignore them?"
  Options:
    - "Yes - Use STORY-001, mode=deep, ignore rest"
    - "No - Show me correct syntax"
```

**Expected Recovery:** Ignore extra args, proceed with valid args

---

## Testing Protocol

**For each command:**
1. Test correct usage (should execute with no questions)
2. Test malformed story ID (should ask, recover)
3. Test flag syntax (should educate, parse)
4. Test unknown flag (should ask, educate)
5. Test missing story (should ask, offer list)
6. Test extra arguments (should handle gracefully)

**Commands to test:**
- `/dev` (story ID only)
- `/qa` (story ID + mode)
- `/release` (story ID + environment)
- `/orchestrate` (story ID only)
- `/create-ui` (story ID or description)

## Success Criteria

- [ ] All malformed inputs trigger AskUserQuestion
- [ ] All recovery paths work correctly
- [ ] Users are educated on correct syntax
- [ ] No silent failures or cryptic errors
- [ ] Correct usage executes smoothly (no questions)

## Documentation

Test results should be documented in:
`.devforgeai/specs/enhancements/RCA-005-test-results.md`

Include:
- Each test scenario
- Actual behavior observed
- Pass/Fail status
- Screenshots or output samples
- User experience notes
