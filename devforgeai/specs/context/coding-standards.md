# Coding Standards - DevForgeAI Framework

**Status**: LOCKED
**Last Updated**: 2025-10-30
**Version**: 1.0

## Framework Coding Standards

### Markdown Documentation Style

**All framework components use Markdown with specific patterns**:

✅ **CORRECT Style**:
```markdown
## Phase 1: Context Validation

Read context files in PARALLEL:
- Read(file_path=".devforgeai/context/tech-stack.md")
- Read(file_path=".devforgeai/context/source-tree.md")

HALT if ANY file missing: "Context files incomplete"
```

❌ **FORBIDDEN Style**:
```markdown
## Phase 1: Context Validation

The system should read context files. First it validates...
[Narrative prose instead of direct instructions]
```

**Rationale**: Claude interprets direct instructions better than prose.

### Tool Usage Standards

**LOCKED: Use Native Tools Over Bash**

✅ **CORRECT**:
```markdown
Read(file_path="story.md")
Edit(file_path="config.md", old_string="v1.0", new_string="v1.1")
Glob(pattern="**/*.md")
Grep(pattern="LOCKED", glob="**/*.md")
```

❌ **FORBIDDEN**:
```markdown
Bash(command="cat story.md")
Bash(command="sed -i 's/v1.0/v1.1/' config.md")
Bash(command="find . -name '*.md'")
Bash(command="grep 'LOCKED' **/*.md")
```

**Exception**: Bash required for tests, builds, git, package managers.

### YAML Frontmatter Standards

**All skills, subagents, commands MUST have frontmatter**:

```yaml
---
name: skill-name
description: Brief description of when to use this
tools: Read, Write, Edit, Bash   # Optional, comma-separated
model: inherit                   # Optional: sonnet, haiku, opus, inherit
---
```

### Progressive Disclosure Pattern

✅ **CORRECT**:
```markdown
# SKILL.md (main file - concise)
## Phase 3: Complexity Assessment
Score complexity on 0-60 scale.
For detailed scoring rubric, see references/complexity-assessment-matrix.md

# references/complexity-assessment-matrix.md (deep details)
[1000 lines of detailed scoring criteria]
```

❌ **FORBIDDEN**:
```markdown
# SKILL.md (monolithic - verbose)
## Phase 3: Complexity Assessment
[1000 lines of detailed scoring criteria inline]
```

### AskUserQuestion Pattern

**LOCKED: Use for ALL ambiguities**:

```markdown
Question: "Which [technology/pattern/approach] should be used?"
Header: "[Category]"
Description: "This decision will be locked in [context-file]"
Options:
  - "[Option 1] (recommended for [reason])"
  - "[Option 2] (better for [use-case])"
  - "[Option 3] ([tradeoff])"
multiSelect: false
```

### File Size Standards

**LOCKED Component Size Limits**:
- Skills: Target 500-800 lines, Max 1,000 lines
- Commands: Target 200-400 lines, Max 500 lines
- Subagents: Target 100-300 lines, Max 500 lines
- Context Files: Target 200-400 lines, Max 600 lines

**Enforcement**: Extract to references/ when exceeding target.

### Naming Conventions

**Files**: lowercase-with-hyphens.md
**Skills**: devforgeai-[phase]
**Subagents**: [domain]-[role]
**Commands**: [action] or [action]-[object]

### Documentation Structure Pattern

**Standard Section Order**:
1. YAML frontmatter
2. Purpose statement
3. When to Use
4. Workflow/Process (numbered phases)
5. Reference files
6. Success criteria

---

**REMEMBER**: Projects using DevForgeAI will have their own coding-standards.md with language-specific patterns (C#, Python, JavaScript, etc.).
