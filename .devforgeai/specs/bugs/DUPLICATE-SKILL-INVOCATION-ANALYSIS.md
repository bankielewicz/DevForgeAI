# Duplicate Skill Invocation Bug Analysis

**Date:** 2025-11-14
**Reporter:** User (observed in terminal)
**Symptom:** "devforgeai-development" skill runs twice
**Severity:** MEDIUM (causes duplicate execution, token waste)

---

## Observed Behavior

When running `/dev [STORY-ID]`, the terminal shows:

```
> The "devforgeai-development" skill is running
  ⎿  Model: claude-haiku-4-5-20251001

> The "devforgeai-development" skill is running
  ⎿  Model: claude-haiku-4-5-20251001
```

**Skill runs TWICE instead of ONCE.**

---

## Investigation Results

### Skill Invocation Count in /dev Command
```bash
grep -n "Skill(command=" .claude/commands/dev.md
# Result: 258:Skill(command="devforgeai-development")
```

**Finding:** Only ONE `Skill(command="devforgeai-development")` invocation in the command file.

### No Recursive Invocation in SKILL.md
```bash
grep "Skill(command=" .claude/skills/devforgeai-development/SKILL.md
# Result: No matches
```

**Finding:** SKILL.md does NOT invoke itself recursively.

### No Skill Invocations in Story Files
```bash
grep -l "Skill(command=" .ai_docs/Stories/*.story.md
# Result: No matches
```

**Finding:** Story files do NOT contain Skill() invocations.

---

## Code Block Analysis

### /dev Command Structure

**Step 2.1: Context Markers (Lines 237-249)**
```markdown
**Provide context for skill (Skills extract info from conversation):**

```
Display: ""
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "  DevForgeAI Development Workflow"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: ""
Display: "**Story ID:** ${STORY_ID}"
Display: "**Story File:** {STORY_FILE}"
Display: "**Current Status:** {status}"
Display: ""
Display: "Delegating to devforgeai-development skill..."
Display: ""
```
```

**Step 2.2: Skill Invocation (Lines 257-259)**
```markdown
**Invoke skill and execute its expanded instructions:**

```
Skill(command="devforgeai-development")
```
```

**Observation:** Two separate code blocks in same phase.

---

### /qa Command Structure (For Comparison)

**Phase 1: Single Code Block (Lines 110-118)**
```markdown
Set explicit context markers for skill:

```
**Story ID:** ${STORY_ID}
**Validation Mode:** ${MODE}

Invoke skill:
Skill(command="devforgeai-qa")
```
```

**Observation:** Context markers AND Skill() call in SAME code block.

---

## Hypothesis 1: Code Block Interpretation Issue

### Potential Cause
Claude Code might be interpreting code blocks in slash commands differently:

**Hypothesis A:** Each code block is executed separately
- First execution: Display statements in Step 2.1 code block
- Second execution: Skill() in Step 2.2 code block
- BUT: This wouldn't cause skill to run twice

**Hypothesis B:** Code block with "Invoke skill:" label gets executed twice
- Step 2.2 has label "Invoke skill and execute its expanded instructions:"
- Code block contains: `Skill(command="devforgeai-development")`
- Perhaps label + code block triggers double parsing?

**Hypothesis C:** Display statement referencing skill triggers invocation
- Step 2.1 line 247: `Display: "Delegating to devforgeai-development skill..."`
- Mentioning skill name in Display might trigger auto-invocation?
- Then explicit Skill() in Step 2.2 triggers second invocation?

---

## Hypothesis 2: Model Parameter Mismatch

### Command Frontmatter (Line 4)
```yaml
model: haiku
```

### SKILL.md Frontmatter (Line 21)
```yaml
model: claude-haiku-4-5-20251001
```

### Terminal Output Shows
```
Model: claude-haiku-4-5-20251001
```

**Observation:** Skill is running with haiku model (from SKILL.md), not sonnet (from command).

**Potential cause:**
1. Command invokes skill with sonnet model
2. Skill frontmatter overrides to haiku
3. System creates two invocations (one per model)?

**Counter-evidence:** Terminal shows both invocations use haiku, not one sonnet + one haiku.

---

## Hypothesis 3: SlashCommand Processing Bug

### Potential Internal Processing
When `/dev STORY-001` is executed:

1. SlashCommand tool processes `dev.md`
2. Encounters `@.ai_docs/Stories/$1.story.md` (line 16)
3. Loads story file into context
4. Encounters first code block (Step 2.1) with Display statements
5. Executes Display statements
6. Encounters second code block (Step 2.2) with Skill()
7. **INVOKES Skill() - First invocation**
8. Skill content expands
9. Slash command continues processing
10. Re-encounters Skill() invocation somehow?
11. **INVOKES Skill() again - Second invocation**

**This is speculative** - would need to see Claude Code internal processing.

---

## Hypothesis 4: Code Block vs Plain Text Invocation

### Current /dev Pattern
```markdown
```
Skill(command="devforgeai-development")
```
```

**Code block contains ONLY the Skill() call.**

### /qa Pattern
```markdown
```
**Story ID:** ${STORY_ID}
**Validation Mode:** ${MODE}

Invoke skill:
Skill(command="devforgeai-development")
```
```

**Code block contains context markers AND Skill() call.**

### Hypothesis
- Code blocks in slash commands are processed multiple times?
- First pass: Parse content
- Second pass: Execute tool calls
- Result: Skill() gets invoked twice?

---

## Testing Hypotheses

### Test 1: Consolidate Code Blocks (Match /qa Pattern)

**Change Step 2.1 and 2.2 to single code block:**

```markdown
### Phase 2: Set Context and Invoke Skill

**Set context markers and invoke skill:**

```
**Story ID:** ${STORY_ID}
**Story File:** {STORY_FILE}
**Current Status:** {status}

Delegating to devforgeai-development skill...

Skill(command="devforgeai-development")
```

**After skill invocation:**
...
```

**Expected result:** Skill runs once (if separate code blocks were the issue).

---

### Test 2: Remove Code Block Around Skill()

**Change Step 2.2 to plain text:**

```markdown
#### Step 2.2: Invoke Development Skill

**Invoke skill and execute its expanded instructions:**

Skill(command="devforgeai-development")

**After skill invocation:**
...
```

**Expected result:** Skill runs once (if code block was triggering double execution).

---

### Test 3: Check for Hidden Characters

```bash
# Check for hidden characters or duplicate lines
cat -A .claude/commands/dev.md | grep -n "Skill(command="
```

**Expected result:** Only one line with Skill() invocation visible.

---

### Test 4: Compare with Working Commands

**Commands to check:**
- `/qa` - Does it also run twice?
- `/create-story` - Does it also run twice?
- `/orchestrate` - Does it also run twice?

**If YES:** Pattern issue affects all commands
**If NO:** Issue specific to /dev command structure

---

## Recommended Fix (Pending Test Results)

### Fix Option 1: Consolidate Code Blocks (RECOMMENDED)

**Match /qa pattern by putting context markers and Skill() in same code block:**

```markdown
### Phase 2: Set Context and Invoke Skill

**Set context markers and invoke skill:**

```
**Story ID:** ${STORY_ID}
**Story File:** {STORY_FILE}
**Current Status:** {status}

Skill(command="devforgeai-development")
```

**After skill invocation:**
- Skill's SKILL.md content expands inline in conversation
- **YOU execute the skill's workflow phases** (not waiting for external result)
- Follow the skill's instructions phase by phase
- Produce output as skill instructs
```

**Changes:**
1. Merge Step 2.1 and Step 2.2 into single step
2. Remove Display statements (put context markers directly)
3. Put Skill() in same code block as context markers
4. Match proven /qa pattern

**Lines affected:** ~30 (Step 2.1 and 2.2 merge)

---

### Fix Option 2: Remove Code Block from Skill() Call

**Put Skill() invocation as plain text outside code block:**

```markdown
#### Step 2.2: Invoke Development Skill

**Invoke skill and execute its expanded instructions:**

Skill(command="devforgeai-development")

**After skill invocation:**
...
```

**Changes:**
1. Remove code block backticks around Skill() call
2. Make it plain markdown text

**Lines affected:** 2 (remove backticks on lines 257 and 259)

---

### Fix Option 3: Add "skill:" Prefix (Alternative Syntax)

**Check if SlashCommand expects different syntax:**

```markdown
skill: devforgeai-development
```

**This is the Skill tool's documented parameter format.**

**Changes:**
1. Change from `Skill(command="devforgeai-development")` to `skill: devforgeai-development`

**Lines affected:** 1 (line 258)

---

## Questions for User

Before implementing a fix, need to understand:

1. **Does /qa command also run twice?**
   - Run: `/qa STORY-001 deep`
   - Observe: Does "devforgeai-qa" skill run twice?
   - This determines if issue is pattern-wide or specific to /dev

2. **What terminal version are you using?**
   - Different versions may parse code blocks differently

3. **Can you share the complete terminal output?**
   - See if there are two separate Skill() invocations in Claude's response
   - Or if it's one invocation being displayed twice

---

## Immediate Action (User)

**Please test /qa command to see if it also runs twice:**

```bash
/qa STORY-001 deep
```

**Observe:**
- Does "devforgeai-qa" skill appear once or twice?
- Is the pattern the same as /dev?

**This will help determine:**
- If issue is code block structure specific to /dev
- If issue is pattern-wide affecting all commands
- If issue is terminal display bug (showing once but appearing twice)

---

## Status

**Analysis:** COMPLETE
**Root cause:** UNKNOWN (need more data)
**Hypotheses:** 4 proposed
**Tests:** 4 proposed
**Fix options:** 3 proposed (pending test results)

**Next step:** User testing to narrow down cause.

---

**Note:** This appears to be a Claude Code terminal processing issue, not a SKILL.md issue. The refactoring completed today is unlikely to be the cause since:
1. Only ONE Skill() invocation exists in command
2. SKILL.md doesn't invoke itself recursively
3. Pattern exists in original command too (likely pre-existing bug)
