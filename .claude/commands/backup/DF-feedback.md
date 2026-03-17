---
description: Manually trigger feedback collection with optional context
argument-hint: [context]
model: opus
allowed-tools: Skill
---

# /feedback - Manual Feedback Trigger

Manually capture feedback with optional context (story ID, operation details).

---

## Command Workflow

### Phase 0: Parse Arguments

**Extract context (optional):**
```
CONTEXT = All arguments joined as string
```

**Validate context:**
- Max length: 500 characters
- Allowed characters: alphanumeric, hyphens, underscores, spaces

---

### Phase 1: Invoke devforgeai-feedback Skill

**Set context markers:**
```
**Feedback Context:** ${CONTEXT}
**Feedback Source:** manual
```

**Invoke skill:**
```
Skill(command="devforgeai-feedback")
```

---

### Phase 2: Display Results

Display results from skill invocation.

---

**BACKUP** - Original command before spec-driven-feedback migration
**Backed up:** 2026-03-16
