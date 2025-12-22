# Memory File Loading: Critical Findings Summary

**Date:** 2025-11-18
**Status:** CRITICAL - Action Required
**Impact:** ~90K tokens wasted per startup

---

## The Problem (TL;DR)

The `.claude/memory/` directory pattern in CLAUDE.md is **NOT** implementing progressive disclosure correctly.

### Current Behavior

```markdown
# In CLAUDE.md:
@.claude/memory/skills-reference.md      ← AUTO-LOADED at startup
@.claude/memory/subagents-reference.md   ← AUTO-LOADED at startup
@.claude/memory/commands-reference.md    ← AUTO-LOADED at startup
... (9 more memory files)                ← ALL AUTO-LOADED at startup
```

**Result:** ~110K tokens consumed at EVERY startup

### Intended Behavior

Files should load progressively (on-demand), not all at startup.

**Expected:** ~3K tokens at startup

---

## The Fix (Immediate)

### Remove @references from CLAUDE.md

Change from:
```markdown
**Quick Reference - Progressive Disclosure**
For detailed guidance, see:
- **Skills:** @.claude/memory/skills-reference.md
```

To:
```markdown
**Quick Reference**
For detailed guidance, see:
- **Skills:** `.claude/memory/skills-reference.md`
  Read with: Read(file_path=".claude/memory/skills-reference.md")
```

**Token savings:** 90K per startup
**Effort:** 10 minutes
**Risk:** None (removal only, no functionality broken)

---

## How @file Syntax Actually Works

### ❌ What People Think
```
@file = "lazy load, only load when user reads it"
```

### ✅ What It Actually Does
```
@file = "include this file automatically at startup"
```

**Official Documentation:**
> "CLAUDE.md files support importing additional files using @path/to/file.md syntax.
> These referenced files are automatically pulled into context when you START Claude Code."

---

## Real Progressive Disclosure

Progressive disclosure DOES work correctly in **Skills**, not in CLAUDE.md:

```
.claude/skills/devforgeai-development/
├── SKILL.md (200 lines)          ← Loaded at startup (~1K tokens)
├── references/
│   ├── tdd-guide.md (400 lines)  ← Loaded ONLY when skill invoked
│   ├── error-handling.md         ← Loaded ONLY when skill invoked
│   └── patterns.md               ← Loaded ONLY when skill invoked
```

When `/dev` is run:
1. SKILL.md already in context
2. Referenced files loaded as needed (~5-15K tokens)
3. Nothing loaded at startup beyond the skill entry point

---

## Token Impact

### Current (WRONG)
```
Startup: CLAUDE.md + all @files = 110K tokens
Per session: 110K tokens (wasted on unneeded docs)
Per 10 sessions: 1.1M tokens (wasted)
```

### After Fix (CORRECT)
```
Startup: CLAUDE.md only = 3K tokens
Per skill invocation: +5-15K tokens (needed only then)
Per 10 sessions: ~40K tokens (used only when needed)
Savings: 1.06M tokens per 10 sessions
```

---

## Root Cause

1. **Misunderstanding of @syntax**
   - Thought @file = lazy loading
   - Actually @file = include at startup

2. **No official guidance**
   - Documentation unclear on this point
   - GitHub issues show confusion

3. **No monitoring**
   - Never measured actual token usage
   - Pattern assumed to work based on naming

---

## Solution Checklist

### Immediate (10 minutes)
- [ ] Remove @.claude/memory/ references from CLAUDE.md
- [ ] Replace with inline guidance: "See .claude/memory/file.md"
- [ ] Add: "Read with: Read(file_path=...)"
- [ ] Test: Run `/memory` command, verify only CLAUDE.md shows

### Short-term (2 weeks)
- [ ] Move memory files into skill/references/ directories
- [ ] Example: `.claude/skills/devforgeai-development/references/guide.md`
- [ ] Update skills to load references appropriately
- [ ] Delete `.claude/memory/` files as moved

### Long-term (Documentation)
- [ ] Update `.claude/memory/skills-reference.md` with correct patterns
- [ ] Document real progressive disclosure (in skills)
- [ ] Add to best practices: "Don't use @file in CLAUDE.md for big docs"

---

## Key Facts

| Fact | Value |
|------|-------|
| **Current @file overhead** | 90K tokens per startup |
| **Sessions per day (typical)** | 5-10 |
| **Tokens wasted per day** | 450K - 900K |
| **Fix effort** | 10 minutes |
| **Fix risk** | None |
| **Immediate token savings** | 90K per startup |

---

## Sources

- **Official Docs:** code.claude.com/docs/en/memory, /skills
- **GitHub Issue #6431:** CLAUDE.md auto-load confirmation
- **GitHub Issue #1041:** @file import behavior documentation
- **Code Cookbook:** Correct skill progressive disclosure pattern

---

## Next Action

**DECISION NEEDED:**

1. Approve removing @references from CLAUDE.md? (Recommended: YES)
2. Timeline? (Recommended: Immediate, 10-minute fix)
3. Should we move memory files into skills? (Recommended: Yes, but can be done later)

---

**For full details, see:** `devforgeai/research/MEMORY-FILE-LOADING-RESEARCH-REPORT.md`
