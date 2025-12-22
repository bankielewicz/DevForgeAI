# Skill Execution Troubleshooting Guide

Quick reference for diagnosing and recovering from skill execution errors.

---

## Symptom: I Invoked a Skill But Stopped Working

**Problem:** After `Skill(command="...")`, you stopped and waited instead of executing.

**Root Cause:** Confusion between Skill tool (inline expansion) and Task tool (isolated execution).

---

## Correct Behavior After Skill Invocation

### Step 1: Recognize Skill Content Has Expanded

When you see:
```
<command-message>The "devforgeai-development" skill is running</command-message>
```

**This means:**
- ✅ Skill's SKILL.md file content is now in your conversation
- ✅ You have access to the skill's workflow instructions
- ✅ **You must now execute those instructions**

**This does NOT mean:**
- ❌ Skill is executing elsewhere
- ❌ Wait for skill to return results
- ❌ Skill is running in background

### Step 2: Read the Skill's Phase 0 Instructions

Immediately after skill invocation:
1. The skill's SKILL.md content has been loaded into conversation
2. Locate the skill's Phase 0 section
3. Read the first step of Phase 0

### Step 3: Execute Phase 0

**Action required:** Run the Phase 0 instructions now

Example from devforgeai-development skill:
```
Phase 0: Pre-Flight Validation
Step 1: Validate Git status
  → Invoke git-validator subagent
  → Process subagent result
  → Set CAN_COMMIT flag
```

**You execute this:**
```
Task(
  subagent_type="git-validator",
  description="Check Git availability",
  prompt="Validate Git repository status..."
)
```

### Step 4: Display Phase 0 Results

**Show user what you did:**
```
✓ Git validation complete
✓ Repository status: Clean working tree
✓ CAN_COMMIT: true
```

### Step 5: Continue to Phase 1

**Read Phase 1 instructions from skill**
**Execute Phase 1**
**Display Phase 1 results**

### Step 6: Continue Through All Phases

**Sequential execution:**
- Phase 1 → Execute → Display results
- Phase 2 → Execute → Display results
- Phase 3 → Execute → Display results
- ...
- Final phase → Execute → Display completion report

---

## What to Do If You Catch Yourself Waiting

### If You Notice the Error Immediately

**Recognition:**
- "I just invoked a skill and said 'I'll wait'"
- "I stopped after seeing 'skill is running'"
- "I'm not executing the skill's instructions"

**Correct Course:**
1. **Acknowledge:** "I incorrectly stopped after skill invocation"
2. **Explain:** "Skills expand inline - I need to execute the instructions"
3. **Resume:** "Let me read the skill's Phase 0 now"
4. **Execute:** Begin Phase 0 execution
5. **Continue:** Complete all phases

### If User Points Out the Error

**User says:**
- "Why did you stop?"
- "You should be executing the skill, not waiting"
- "The skill doesn't run in the background"

**Your response:**
1. **Apologize:** "I apologize - I incorrectly treated the skill as a background process"
2. **Correct understanding:** "Skills expand inline and I must execute their instructions"
3. **Resume immediately:** "Let me execute the skill's workflow now, starting from Phase 0"
4. **Complete workflow:** Execute all phases to completion

---

## Quick Check: Am I Executing Correctly?

**Ask yourself after skill invocation:**

- ✅ Am I reading the skill's phase instructions?
- ✅ Am I executing those instructions?
- ✅ Am I displaying results as I work?
- ✅ Am I progressing through phases sequentially?

**If answer is "no" to any:** You've stopped incorrectly. Resume execution.

---

## Mental Model Correction

### ❌ WRONG Mental Model

```
Skill invocation → Wait for result → Display result
```

**This is the Task tool (subagents) pattern, NOT the Skill tool pattern.**

### ✅ CORRECT Mental Model

```
Skill invocation → Load instructions → Execute instructions → Display your work
```

**Skills expand inline. You do the work.**

---

## Comparison: Skills vs Subagents

| When to Wait | Skills (Skill tool) | Subagents (Task tool) |
|--------------|--------------------|-----------------------|
| **After invocation** | ❌ NEVER - You execute | ✅ YES - Agent executes |
| **Who produces output** | You | Agent |
| **Where execution happens** | Current conversation | Isolated context |
| **What you see** | Skill's SKILL.md content | Agent's structured result |

---

## Common Scenarios

### Scenario 1: /dev Command

**Command executes:**
```
Skill(command="devforgeai-development")
```

**System message appears:**
```
<command-message>The "devforgeai-development" skill is running</command-message>
```

**✅ Correct action:**
1. Read devforgeai-development skill's Phase 0
2. Execute Phase 0 Step 1 (git-validator subagent)
3. Execute Phase 0 Step 2 (adapt workflow)
4. Continue through all Phase 0 steps
5. Execute Phase 1 (Red phase)
6. Continue through all phases
7. Display completion report

**❌ Incorrect action:**
```
"The skill is running. I'll wait for it to complete."
[Stops and waits]
```

### Scenario 2: /qa Command

**Command executes:**
```
Skill(command="devforgeai-qa")
```

**✅ Correct action:**
1. Read devforgeai-qa skill's Phase 0
2. Execute validation mode detection
3. Execute story loading
4. Execute context validation
5. Continue through all phases (Light or Deep)
6. Invoke qa-result-interpreter subagent (Phase 5)
7. Display results from subagent

**❌ Incorrect action:**
```
"QA validation is running. I'll monitor progress."
[Stops and waits]
```

### Scenario 3: /orchestrate Command

**Command executes:**
```
Skill(command="devforgeai-orchestration")
```

**✅ Correct action:**
1. Read orchestration skill's Phase 0
2. Execute checkpoint detection
3. Invoke devforgeai-development skill (if needed)
4. Invoke devforgeai-qa skill (if needed)
5. Handle QA retry loop (if QA fails)
6. Invoke devforgeai-release skill (staging, production)
7. Display orchestration completion report

**❌ Incorrect action:**
```
"Orchestration workflow is running. I'll wait for all phases."
[Stops and waits]
```

---

## Emergency Recovery

**If you've already stopped and are reading this:**

### Step 1: Acknowledge the Error
```
"I apologize - I incorrectly stopped after skill invocation. Skills expand inline in the conversation, and I should have immediately begun executing the skill's workflow instructions."
```

### Step 2: Explain the Correct Model
```
"When I invoke a skill, the skill's SKILL.md content becomes part of my context. I am responsible for reading and executing each phase of the skill's workflow, not waiting for an external process to complete."
```

### Step 3: Resume Execution
```
"Let me now execute the skill's workflow, starting from Phase 0."
```

### Step 4: Execute All Phases
- Read Phase 0 instructions
- Execute Phase 0
- Display Phase 0 results
- Continue through all phases sequentially
- Display final completion report

### Step 5: Learn from the Error
```
"I will remember this for future skill invocations: Skills are inline prompt expansions that I execute, not background processes that I wait for."
```

---

## Prevention Checklist

**Before invoking any skill, remind yourself:**
- [ ] Skill invocation loads SKILL.md content into conversation
- [ ] I will read the skill's instructions
- [ ] I will execute those instructions phase by phase
- [ ] I will display results as I work
- [ ] I will NOT wait passively

**After skill invocation message appears:**
- [ ] I see "skill is running" message
- [ ] This means skill content is loaded
- [ ] I now read Phase 0 instructions
- [ ] I execute Phase 0 immediately
- [ ] I continue through all phases

---

## Testing Your Understanding

**Question 1:** After `Skill(command="devforgeai-development")`, what should you do?

**✅ Correct answer:** Read the devforgeai-development skill's Phase 0 instructions and begin executing them immediately.

**❌ Incorrect answer:** Wait for the skill to complete and monitor progress.

---

**Question 2:** What does the system message "The 'devforgeai-qa' skill is running" mean?

**✅ Correct answer:** The skill's SKILL.md content has been loaded into my conversation, and I must now execute its instructions.

**❌ Incorrect answer:** The skill is executing in the background, and I should wait for it to return results.

---

**Question 3:** When should you wait after invoking a skill?

**✅ Correct answer:** NEVER. Skills expand inline, and I execute their instructions immediately.

**❌ Incorrect answer:** Always wait for the skill to complete before continuing.

---

**Question 4:** What's the difference between Skill tool and Task tool?

**✅ Correct answer:**
- Skill tool: Inline expansion, I execute instructions
- Task tool: Isolated context, separate agent executes, I wait for result

**❌ Incorrect answer:** Both tools launch background processes that return results.

---

## Related Documentation

**Core reference:**
- `CLAUDE.md` - Section "CRITICAL: How Skills Work"
- `.claude/memory/skills-reference.md` - Skills overview with execution model

**Skills documentation:**
- `.claude/skills/devforgeai-development/SKILL.md` - Development workflow
- `.claude/skills/devforgeai-qa/SKILL.md` - QA validation workflow
- `.claude/skills/devforgeai-orchestration/SKILL.md` - Orchestration workflow

**Commands documentation:**
- `.claude/commands/dev.md` - /dev command (invokes devforgeai-development skill)
- `.claude/commands/qa.md` - /qa command (invokes devforgeai-qa skill)
- `.claude/commands/orchestrate.md` - /orchestrate command (invokes orchestration skill)

---

## Remember

**Skills are inline prompt expansions.**
- You invoke them
- They load into your conversation
- You execute their instructions
- You produce the output

**You NEVER wait for skills to "complete" or "return results."**

**If you find yourself waiting after skill invocation, STOP and resume execution immediately.**
