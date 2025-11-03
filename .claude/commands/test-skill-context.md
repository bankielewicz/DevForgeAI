---
description: Test if skills can read conversation context correctly
model: haiku
allowed-tools: Read, Skill
---

# Test: Skill Context Reading

This test validates that skills can extract parameters from conversation context.

## Test Data

Load test data into conversation context:

**Test Story ID:** STORY-001
**Test Validation Mode:** deep
**Test Environment:** staging
**Test Component:** Login form with email and password

## Test Execution

### Test 1: Simple Skill Invocation

Invoke a skill without arguments to verify it can read conversation:

```
Skill(command="devforgeai-architecture")
```

**Expected:** Skill should execute without errors (may ask questions based on project state)

### Test 2: Context Extraction

**Question for Claude:** Did the architecture skill see the test data above (Story ID, Mode, Environment)?

**Validation:**
- Check if skill attempted to extract STORY-001 from conversation
- Check if skill operated normally without parameters

### Test Result

✅ PASS: Skill executed successfully without parameters
❌ FAIL: Skill error or complained about missing parameters

## Notes

This test validates the fundamental assumption that Skills operate on conversation context rather than command-line parameters.

**If test fails:**
- Skills may require parameters (contradicts official documentation)
- Context loading mechanism may be broken
- Skill implementation may have bugs

**If test passes:**
- Confirms Skills read conversation context
- Validates slash command fix approach
- Ready to test actual DevForgeAI commands
