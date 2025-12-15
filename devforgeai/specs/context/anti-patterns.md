# Anti-Patterns - DevForgeAI Framework

**Status**: LOCKED
**Last Updated**: 2025-10-30
**Version**: 1.0

## Framework Anti-Patterns

### Category 1: Tool Usage Violations (SEVERITY: CRITICAL)

❌ **FORBIDDEN: Using Bash for File Operations**

**Wrong**:
```markdown
Bash(command="cat story.md")
Bash(command="echo 'content' > file.md")
Bash(command="find . -name '*.md'")
```

**Correct**:
```markdown
Read(file_path="story.md")
Write(file_path="file.md", content="content")
Glob(pattern="**/*.md")
```

**Rationale**: 40-73% token efficiency gain with native tools.

### Category 2: Monolithic Components (SEVERITY: HIGH)

❌ **FORBIDDEN: All-in-One Skill**

**Wrong**:
```
.claude/skills/devforgeai-everything/
└── SKILL.md (5,000 lines doing ideation + architecture + dev + qa + release)
```

**Correct**:
```
.claude/skills/
├── devforgeai-ideation/
├── devforgeai-architecture/
├── devforgeai-development/
├── devforgeai-qa/
└── devforgeai-release/
```

**Rationale**: Modularity enables independent updates and token efficiency.

### Category 3: Making Assumptions (SEVERITY: CRITICAL)

❌ **FORBIDDEN: Assuming Technology Choices**

**Wrong**:
```markdown
# AI sees "need caching" and adds Redis without asking
Install Redis for caching layer
```

**Correct**:
```markdown
Question: "Spec requires caching. Which technology?"
Header: "Caching"
Options:
  - "Redis (in-memory, distributed)"
  - "Memcached (simple, fast)"
  - "In-memory (no external service)"
multiSelect: false
```

**Rationale**: Assumptions cause technical debt.

### Category 4: Size Violations (SEVERITY: HIGH)

❌ **FORBIDDEN: Exceeding Component Size Limits**

**Wrong**:
```markdown
# SKILL.md with 2,000 lines of inline documentation
```

**Correct**:
```markdown
# SKILL.md with 500 lines + references/ for deep docs
For detailed scoring rubric, see references/complexity-assessment-matrix.md
```

**Rationale**: Character budget constraints (15K for commands).

### Category 5: Language-Specific Framework Code (SEVERITY: CRITICAL)

❌ **FORBIDDEN: Python/C#/JavaScript in Framework**

**Wrong**:
```
.claude/skills/devforgeai-development/
├── SKILL.md
└── scripts/
    └── implement.py    # Python implementation
```

**Correct**:
```
.claude/skills/devforgeai-development/
├── SKILL.md
└── references/
    └── tdd-workflow-guide.md    # Documentation only
```

**Rationale**: Framework must be language-agnostic.

### Category 6: Context File Violations (SEVERITY: CRITICAL)

❌ **FORBIDDEN: Proceeding Without Context Files**

**Wrong**:
```markdown
# Development skill starts implementation without reading context
Implement feature X using EF Core
```

**Correct**:
```markdown
## Phase 1: Context Validation
Read all 6 context files
HALT if missing: "Run /create-context first"
Check tech-stack.md for ORM choice
```

**Rationale**: Context files prevent architectural violations.

### Category 7: Circular Dependencies (SEVERITY: HIGH)

❌ **FORBIDDEN: Skills Calling Each Other in Loops**

**Wrong**:
```
devforgeai-development calls devforgeai-qa
  ↓
devforgeai-qa calls devforgeai-development
  ↓
Infinite loop
```

**Correct**:
```
devforgeai-development calls devforgeai-qa (one-way)
devforgeai-qa returns results
devforgeai-development continues
```

**Rationale**: Prevents infinite loops and context overflow.

### Category 8: Narrative Documentation (SEVERITY: MEDIUM)

❌ **FORBIDDEN: Prose Instead of Instructions**

**Wrong**:
```markdown
The system should first analyze the codebase, and then it might want to consider generating tests...
```

**Correct**:
```markdown
1. Analyze codebase:
   - Grep(pattern="class.*Test", glob="**/*.cs")
2. Generate tests:
   - Use test-automator subagent
```

**Rationale**: Direct instructions are clearer for Claude.

### Category 9: Missing Frontmatter (SEVERITY: HIGH)

❌ **FORBIDDEN: Skills/Subagents/Commands Without Frontmatter**

**Wrong**:
```markdown
# My Skill
Instructions go here...
```

**Correct**:
```markdown
---
name: my-skill
description: Brief description of when to use
tools: Read, Write
---

# My Skill
Instructions go here...
```

**Rationale**: Frontmatter required for discovery.

### Category 10: Hardcoded Paths (SEVERITY: MEDIUM)

❌ **FORBIDDEN: Hardcoded File Paths**

**Wrong**:
```markdown
Read(file_path="/home/user/project/story.md")
```

**Correct**:
```markdown
Read(file_path="devforgeai/specs/Stories/$STORY_ID.md")
```

**Rationale**: Relative paths work across environments.

## Anti-Pattern Detection Protocol

When framework components detect anti-patterns:

1. **HALT immediately**
2. **Report specific violation** with file:line reference
3. **Provide correction example**
4. **Request user confirmation** before proceeding

## Enforcement Checklist

Before committing framework changes:
- [ ] No Bash for file operations (use Read/Write/Edit/Glob/Grep)
- [ ] Components within size limits (skills <1000, commands <500)
- [ ] No language-specific code in framework
- [ ] All ambiguities use AskUserQuestion
- [ ] Context files read before development
- [ ] No circular dependencies
- [ ] Direct instructions, not narrative prose
- [ ] All components have frontmatter
- [ ] No hardcoded absolute paths

---

**REMEMBER**: Projects using DevForgeAI will have their own anti-patterns.md with project-specific forbidden patterns (SQL injection, N+1 queries, God objects, etc.).
