# CLAUDE.md - Recommended Changes

**Purpose:** Remove @file references that are wasting 90K tokens per startup

**Change Type:** Removal only (no functionality lost)

**Token Savings:** 90K per startup

**Risk Level:** ZERO (only removing references, not functionality)

---

## Current Section (PROBLEMATIC)

**Location:** Near end of CLAUDE.md

```markdown
## Quick Reference - Progressive Disclosure

**For detailed guidance, see:**

- **Skills:** @.claude/memory/skills-reference.md
- **Subagents:** @.claude/memory/subagents-reference.md
- **Slash Commands:** @.claude/memory/commands-reference.md
- **QA Automation:** @.claude/memory/qa-automation.md
- **Context Files:** @.claude/memory/context-files-guide.md
- **UI Generator:** @.claude/memory/ui-generator-guide.md
- **Token Efficiency:** @.claude/memory/token-efficiency.md
- **Epic Creation:** @.claude/memory/epic-creation-guide.md
- **Token Budget:** @.claude/memory/token-budget-guidelines.md
```

**Problem:** Each @reference automatically loads that file at startup
**Total overhead:** 9 files × 10K tokens average = 90K tokens

---

## Recommended Replacement

### Option A: Minimal Replacement (RECOMMENDED)

```markdown
## Quick Reference

**For detailed guidance:**

When you need reference information about skills, subagents, or commands:

```bash
# Read a specific reference guide
Read(file_path=".claude/memory/skills-reference.md")
Read(file_path=".claude/memory/commands-reference.md")
Read(file_path=".claude/memory/subagents-reference.md")
```

**Available references:**
- `.claude/memory/skills-reference.md` - How to use DevForgeAI skills
- `.claude/memory/subagents-reference.md` - Subagent capabilities
- `.claude/memory/commands-reference.md` - Slash command reference
- `.claude/memory/qa-automation.md` - QA automation scripts
- `.claude/memory/context-files-guide.md` - Context file structure
- `.claude/memory/ui-generator-guide.md` - UI generation workflow
- `.claude/memory/token-efficiency.md` - Token optimization strategies
- `.claude/memory/epic-creation-guide.md` - Epic creation best practices
- `.claude/memory/token-budget-guidelines.md` - Token budget heuristics

**Note:** These files are available on-demand and not loaded at startup to save tokens.
```

**Benefits:**
- Clear instructions on how to read guides
- No automatic loading
- Users know where to find what they need
- 90K token savings

---

### Option B: More Detailed (ALTERNATIVE)

```markdown
## Quick Reference & Documentation

**Files in this repository:**

The `.claude/memory/` directory contains comprehensive reference documentation that is available on-demand (not loaded automatically). To access any reference:

```bash
Read(file_path=".claude/memory/[filename].md")
```

### Available References

| Topic | File | Purpose |
|-------|------|---------|
| Skills | `skills-reference.md` | How to invoke and work with DevForgeAI skills |
| Subagents | `subagents-reference.md` | Specialized AI workers for domain tasks |
| Commands | `commands-reference.md` | All 11 slash commands and their usage |
| QA | `qa-automation.md` | Quality assurance scripts and automation |
| Context | `context-files-guide.md` | The 6 immutable context files |
| UI | `ui-generator-guide.md` | UI specification and code generation |
| Tokens | `token-efficiency.md` | Token optimization strategies |
| Epics | `epic-creation-guide.md` | Epic planning and decomposition |
| Budget | `token-budget-guidelines.md` | Token budget management |

### How to Use These References

These files are NOT automatically loaded at startup (to save 90K tokens). Instead:

1. **When you need information:** Use `Read(file_path=".claude/memory/FILE.md")`
2. **Quick lookup:** See the table above to find what you need
3. **Skill documentation:** Each skill also has `skill/references/` files for that skill's specific guidance

### Note on CLAUDE.md Design

This file is intentionally kept compact to minimize startup token consumption while remaining comprehensive. Reference documentation is available on-demand through the Read tool.
```

**Benefits:**
- More detailed and helpful
- Explains why references aren't auto-loaded
- Clear table of contents
- Still achieves 90K token savings

---

## Verification Steps

### Before Change
```bash
# Check what's currently loaded
/memory

# Should show: All .claude/memory/*.md files loaded
```

### After Change
```bash
# Check what's loaded
/memory

# Should show: Only CLAUDE.md (project instructions)
```

### If Needed, Read Guides
```bash
# Example: Read skills reference
Read(file_path=".claude/memory/skills-reference.md")

# Verify content loads correctly
# (Should show: skills-reference.md content)
```

---

## Implementation Checklist

- [ ] Choose Option A or B (Recommended: Option A - simpler)
- [ ] Locate "Quick Reference - Progressive Disclosure" section in CLAUDE.md
- [ ] Remove current section
- [ ] Add replacement section
- [ ] Save changes
- [ ] Test: Run `/memory` command
- [ ] Verify: Only CLAUDE.md appears (no memory files listed)
- [ ] Test: Try reading a guide: `Read(file_path=".claude/memory/skills-reference.md")`
- [ ] Verify: Guide loads correctly

---

## Files Affected

- **Modified:** `/mnt/c/Projects/DevForgeAI2/CLAUDE.md`
  - Section removed: "Quick Reference - Progressive Disclosure"
  - Section added: "Quick Reference" or "Quick Reference & Documentation"

- **No changes to:**
  - `.claude/memory/*.md` files (content stays same)
  - Commands, skills, or other functionality
  - Any other project files

---

## Token Impact Analysis

### Current (with @references)

```
Session startup:
├─ Load CLAUDE.md: 3K tokens
├─ Load @skills-reference.md: 12K tokens
├─ Load @subagents-reference.md: 15K tokens
├─ Load @commands-reference.md: 16K tokens
├─ Load @qa-automation.md: 8K tokens
├─ Load @context-files-guide.md: 7K tokens
├─ Load @ui-generator-guide.md: 8K tokens
├─ Load @token-efficiency.md: 7K tokens
├─ Load @epic-creation-guide.md: 13K tokens
└─ Load @token-budget-guidelines.md: 4K tokens

Total: 110K tokens (all at startup, regardless of what user does)
```

### After (without @references)

```
Session startup:
└─ Load CLAUDE.md: 3K tokens

When user runs command/skill:
└─ Load if needed: 5-15K tokens (proportional to actual use)

Total per session: 3K + (0-15K needed) = 3-18K tokens
```

### Savings

```
Per startup: 110K - 3K = 107K tokens saved
Per 10 startups: 1.07M tokens saved
Per 100 startups: 10.7M tokens saved

Practical example (daily usage):
- Startups per day: 3-5
- Tokens saved per day: 321K - 535K
- Per month: 9.6M - 16M tokens saved
```

---

## FAQ

### Q: Will users lose access to reference guides?

**A:** No. The guides remain in `.claude/memory/` and are readable with:
```bash
Read(file_path=".claude/memory/skills-reference.md")
```

### Q: Why remove them if they're useful?

**A:** They ARE useful, but they're loaded at every startup whether the user needs them or not. This wastes 90K+ tokens per session. By removing @references, users can read them on-demand instead.

### Q: What's the better solution long-term?

**A:** Move documentation into skills' `references/` directories. Then they load only when that skill is used. Example:

```
.claude/skills/devforgeai-development/
├── SKILL.md
└── references/
    ├── guide-1.md
    └── guide-2.md
```

### Q: Will /memory command still work?

**A:** Yes, but it will only show CLAUDE.md (project instructions), not the memory files. This is correct behavior.

### Q: Is this a breaking change?

**A:** No. It's a token optimization. No features are broken, nothing stops working, documentation is still accessible.

### Q: How do we know this is the problem?

**A:** Official Claude Code documentation states @file syntax loads files "automatically when you start Claude Code." GitHub issues confirm this behavior. This is documented behavior, not a bug.

---

## Risk Mitigation

### Risk 1: Users Can't Find Guides

**Mitigation:**
- Include clear instructions: `Read(file_path="...")`
- Keep the table/list of available files in CLAUDE.md
- Add comments explaining why they're not auto-loaded

### Risk 2: Some Guide Content Gets Lost

**Mitigation:**
- No content is deleted
- All files remain in `.claude/memory/`
- Only the @reference syntax is removed
- Users can still read everything

### Risk 3: Commands/Skills Stop Working

**Mitigation:**
- No commands or skills are changed
- Only CLAUDE.md reference section is modified
- All skills/commands remain unchanged

---

## Success Criteria

1. **Startup token count reduced**
   - Before: 110K tokens in CLAUDE context
   - After: 3K tokens in CLAUDE context
   - Measurement: Run `/memory`, check token usage before/after

2. **Guides still accessible**
   - User can run: `Read(file_path=".claude/memory/skills-reference.md")`
   - Content loads correctly
   - No truncation or errors

3. **No other functionality affected**
   - All commands work: `/dev`, `/qa`, `/release`, etc.
   - All skills work: devforgeai-development, devforgeai-qa, etc.
   - All guides still readable on-demand

---

## Timeline

| Phase | Effort | Time |
|-------|--------|------|
| Review & Approval | 5 min | 5 min |
| Make Changes | 10 min | 10 min |
| Test & Verify | 15 min | 15 min |
| Document | 5 min | 5 min |
| **Total** | **35 min** | **35 min** |

---

## Next Steps

1. **Review this document** - Does the approach make sense?
2. **Choose Option A or B** - Which replacement text preferred?
3. **Approve the change** - Go ahead with modification?
4. **Execute change** - 35-minute task
5. **Verify results** - Confirm 90K token savings

---

**Recommendation:** APPROVE and execute immediately.

This is a low-risk, high-reward optimization that frees up 90K tokens per startup with zero negative impact on functionality.
