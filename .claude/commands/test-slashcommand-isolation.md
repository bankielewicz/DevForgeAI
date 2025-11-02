---
description: Test SlashCommand context isolation behavior
model: haiku
---

# SlashCommand Context Isolation Test

This is a test command to determine if SlashCommand creates isolated contexts like the Task tool does for subagents.

**Test Objective:**
Measure token usage when this command is invoked via SlashCommand tool vs direct invocation.

**Expected Behavior:**
- If contexts ARE isolated: Main conversation sees only summary (~500 tokens)
- If contexts NOT isolated: Main conversation sees full execution (~5K tokens)

Report: "SlashCommand isolation test executed. This command consumes approximately 3,000 tokens if NOT isolated, or ~300 tokens in main conversation if isolated."

**Invocation Instructions:**

Test 1: Direct invocation
```
/test-slashcommand-isolation
```

Test 2: Via SlashCommand tool
```
Use the SlashCommand tool to invoke /test-slashcommand-isolation
```

Compare token usage between both tests using `/cost` command.
